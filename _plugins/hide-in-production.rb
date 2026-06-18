# frozen_string_literal: true

# Drop any post flagged `hidden_in_prod: true` from the PRODUCTION build only.
#
# They still render in local previews (JEKYLL_ENV=development, the default for
# `jekyll serve`), so the bundled Chirpy demo posts can stay as a writing /
# structure reference while you draft — but never appear on the deployed site
# (home, archives, categories, tags, feed, or their own pages).
#
# See README-local.md.
Jekyll::Hooks.register :site, :post_read do |site|
  next unless Jekyll.env == 'production'

  site.posts.docs.reject! { |doc| doc.data['hidden_in_prod'] == true }
end
