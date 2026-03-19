#!/usr/bin/env ruby

require 'digest'
require 'fileutils'
require 'json'
require 'open3'
require 'pathname'
require 'tmpdir'

AUDIO_EXTS = %w[.mp3 .m4a .wav .flac .ogg .aac].freeze

def compact_segments(segments)
  Array(segments).filter_map do |seg|
    text = seg['text'].to_s.strip
    next if text.empty?

    {
      'start' => seg.fetch('start', 0).to_i,
      'text' => text
    }
  end
end

def run_whisper_json(whisper_bin:, audio_path:, model:, task:, language: nil)
  Dir.mktmpdir('whisper-jekyll-') do |tmp_dir|
    cmd = [
      whisper_bin,
      audio_path,
      '--model', model,
      '--output_format', 'json',
      '--output_dir', tmp_dir,
      '--task', task
    ]
    cmd.concat(['--language', language]) if language

    stdout, stderr, status = Open3.capture3(*cmd)
    unless status.success?
      raise "whisper failed: #{stderr.strip.empty? ? stdout.strip : stderr.strip}"
    end

    json_file = Dir.glob(File.join(tmp_dir, '*.json')).max_by { |f| File.mtime(f) }
    raise 'whisper did not produce json output' unless json_file

    JSON.parse(File.read(json_file))
  end
end

def transcript_payload(whisper_bin:, audio_path:, model:)
  zh_raw = run_whisper_json(
    whisper_bin: whisper_bin,
    audio_path: audio_path,
    model: model,
    task: 'transcribe',
    language: 'zh'
  )
  en_raw = run_whisper_json(
    whisper_bin: whisper_bin,
    audio_path: audio_path,
    model: model,
    task: 'translate'
  )

  {
    'track' => File.basename(audio_path, '.*'),
    'source' => "/#{audio_path}",
    'zh' => compact_segments(zh_raw['segments']),
    'en' => compact_segments(en_raw['segments'])
  }
end

Jekyll::Hooks.register :site, :pre_render do |site|
  cfg = site.config['audio_transcripts'] || {}
  enabled = cfg.key?('enabled') ? cfg['enabled'] : true
  next unless enabled

  source_dir_rel = cfg['source_dir'] || 'assets/audio'
  output_dir_rel = cfg['output_dir'] || 'assets/transcripts'
  source_dir = File.join(site.source, source_dir_rel)
  output_dir = File.join(site.source, output_dir_rel)
  whisper_bin = cfg['whisper_bin'] || 'whisper'
  model = cfg['model'] || 'small'
  force = cfg['force'] == true
  mapping = cfg['mapping'] || {}

  unless system('command', '-v', whisper_bin, out: File::NULL, err: File::NULL)
    Jekyll.logger.warn('audio_transcripts:', "whisper binary not found: #{whisper_bin}")
    next
  end

  unless Dir.exist?(source_dir)
    Jekyll.logger.info('audio_transcripts:', "source directory not found: #{source_dir_rel}")
    next
  end

  audio_files = Dir.glob(File.join(source_dir, '**', '*')).select do |path|
    AUDIO_EXTS.include?(File.extname(path).downcase)
  end

  if audio_files.empty?
    Jekyll.logger.info('audio_transcripts:', 'no audio files found')
    next
  end

  FileUtils.mkdir_p(output_dir)

  updated = 0
  skipped = 0

  audio_files.sort.each do |audio_path|
    rel_audio = Pathname.new(audio_path).relative_path_from(Pathname.new(source_dir)).to_s
    basename = File.basename(audio_path)
    out_name = mapping[rel_audio] || mapping[basename]

    if out_name.nil?
      stem = Jekyll::Utils.slugify(File.basename(audio_path, '.*'), mode: 'pretty', cased: false)
      stem = "track-#{Digest::SHA1.hexdigest(rel_audio)[0, 8]}" if stem.nil? || stem.empty?
      out_name = "#{stem}.json"
    end

    out_name = "#{out_name}.json" unless out_name.end_with?('.json')
    out_path = File.join(output_dir, out_name)

    stale = !File.exist?(out_path) || File.mtime(audio_path) > File.mtime(out_path)
    unless force || stale
      skipped += 1
      next
    end

    begin
      payload = transcript_payload(whisper_bin: whisper_bin, audio_path: audio_path, model: model)
      File.write(out_path, JSON.pretty_generate(payload))
      updated += 1
      Jekyll.logger.info('audio_transcripts:', "saved #{Pathname.new(out_path).relative_path_from(Pathname.new(site.source))}")
    rescue StandardError => e
      Jekyll.logger.warn('audio_transcripts:', "failed for #{rel_audio}")
      Jekyll.logger.warn('audio_transcripts:', e.message)
    end
  end

  Jekyll.logger.info('audio_transcripts:', "updated #{updated}, skipped #{skipped}")
end