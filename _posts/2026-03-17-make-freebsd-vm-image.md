---
title: "Caveats of using *make* for creating FreeBSD VM images"
author: qianhui
date: 2026-03-17 00:00:00 +0000
categories: [Research]
tags: [make, build, kernel, world]
render_with_liquid: false
---

## Hosting the source code for OS development
It is very common to have various development branches for an operating system source cod. How to keep the source code clean and tidy is always the first question to ask. Normal git workflow is to have a single location for the source code, and ``git checkout`` to the branch you want to work on. There are also the option of ``git worktree`` to have multiple branches checked out at different locations for source code isolation.

Personally, I might lean towards the worktree approach, since switching branches could add to the times of having massive kernel rebuilds. This is especially the case for OS development, where a single overwrite by git is likely made to a core kernel file which is in turn on the upper end of the chain of imports for thousands of indirectly related files. 

So, even though git is smart enough to only refresh the timestamps for files that are actually different across branches, the build system is the one that still causes headaches because of the cascades of includes. In this sense, maintaining multiple worktrees is a good option to reduce unnecessary rebuilds for working across multiple development features.

There is another option for workaround -- to use the Meta Mode with make. This feature does hash comparison of the file contents to determine actual file changes, as opposed to relying on timestamps that could be false indicators. 

## Time that cannot be saved
In a linear commit history, normal edits to the kernel files could still incur expensive rebuilds, because of the cascading nature of imports in the source code. This part could not be easily avoided, not least that I have currently known of. 

## Useful make options
- ``-DWITHOUT_CLEAN``: this option tells the build system to skip the cleaning step before building. It is particularly useful when there are little changes in the source code and we want to avoid time-consuming full rebuilds. Most useful in ``make buildkernel -DWITHOUT_CLEAN`` or ``make buildworld -DWITHOUT_CLEAN``.


- ``-DWITH_META_MODE``: this option enables the Meta Mode, which allows for more efficient builds by only rebuilding the parts of the kernel or world that have changed. This can significantly reduce build times, especially for large codebases. 


## A working config for release build
<div file="MTE.conf" class="language-sh highlighter-rouge">
  <div class="code-header">
    <span data-label-text="MTE.conf"><i class="far fa-file-code fa-fw"></i></span>
    <button aria-label="copy" data-title-succeed="Copied!"><i class="far fa-clipboard"></i></button>
  </div>
  <div class="highlight">
    <pre><code><span class="rouge-code" id="mte-conf-code">Loading /assets/code/MTE.conf ...</span></code></pre>
  </div>
</div>

<script>
  (function() {
    var codeEl = document.getElementById('mte-conf-code');
    if (!codeEl) return;

    function escapeHtml(text) {
      return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    }

    function highlightShell(text) {
      var html = escapeHtml(text);
      var tokens = [];

      function mark(regex, cls) {
        html = html.replace(regex, function(match) {
          var id = tokens.length;
          tokens.push('<span class="' + cls + '">' + match + '</span>');
          return '\u0000' + id + '\u0000';
        });
      }

      mark(/#.*$/gm, 'c1');
      mark(/"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'/g, 's2');
      mark(/\$\{?[A-Za-z_][A-Za-z0-9_]*\}?/g, 'nv');
      mark(/\b(if|then|fi|for|do|done|case|esac|while|in|function)\b/g, 'k');
      mark(/\b(sudo|make|cd|export|set|echo|cat|cp|mv|rm|ln|chmod|chown|grep|awk|sed|find|xargs|tar|uname|sysctl)\b/g, 'nb');

      return html.replace(/\u0000(\d+)\u0000/g, function(_, i) {
        return tokens[Number(i)];
      });
    }

    fetch('/assets/code/MTE.conf')
      .then(function(res) {
        if (!res.ok) {
          throw new Error('HTTP ' + res.status);
        }
        return res.text();
      })
      .then(function(text) {
        codeEl.innerHTML = highlightShell(text);
      })
      .catch(function(err) {
        codeEl.textContent = 'Failed to load /assets/code/MTE.conf: ' + err.message;
      });
  })();
</script>

