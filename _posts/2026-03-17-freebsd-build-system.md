---
title: "Reflections on the FreeBSD build system"
description: "Reflections on the FreeBSD build system, including tips for building FreeBSD release images, managing source code and build artifacts, and useful make targets and flags for efficient builds."
author: qianhui
date: 2026-03-17 00:00:00 +0000
categories: [Research]
tags: [make, build, kernel, world]
render_with_liquid: false
---

## Building a FreeBSD release VM image
FreeBSD provides a standard `release.sh` script for building release images under `release/` in the source tree. It is a top-level automation tool that orchestrates the build pipeline, including bootstrapping the build environment, building and installing the kernel and world for the target architecture, creating the image, and packaging it for distribution. This script is easily customisable to fit specific needs.

- Phase 1: Prepare a clean build environment (Host Phase)
  - create a clean mini-FreeBSD inside the chroot so all later build tools run in a controlled environment.

Below is a working configuration that builds a FreeBSD 16.0-RELEASE image that implements very early stage support for ARM64 Memory Tagging Extension (MTE). To build a FreeBSD image, one has to be inside a FreeBSD environment -- for my experiment, I built inside a FreeBSD 14.0-RELEASE VM on QEMU.


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


## On kernel builds
#### Hosting source code for kernel development
It is very common to have various development branches for an operating system source code. How to keep the source code clean and tidy is always the first question to ask. Normal git workflow is to have a single location for the source code, and `git checkout` to the branch you want to work on. There are also the option of `git worktree` to have multiple branches checked out at different locations for source code isolation.

Personally, I might lean towards using the `worktree` approach, since switching branches could add to the number of times where you have to deal with massive kernel rebuilds. This is especially the case for OS development, where a single overwrite by git [on switch] is likely happened to a core kernel file sitting on the upper end of the import chain for many other indirectly dependent files. 

Even though git is smart enough to refresh the timestamps only for files that are actually different across branches, the build system would still cause headaches because of the cascades of includes. Under this light, maintaining multiple worktrees is a good option to reduce unnecessary rebuilds for working across multiple development features.

There is another option for workaround -- to use the Meta Mode with `make`. This feature does hash comparison of the file contents to determine actual file changes, as opposed to relying on timestamps that could be false indicators. However, this option is not perfect and what we desire is completely independent source code locations to avoid unnecessary rebuilds.

#### Time that cannot be saved
In a linear commit history, normal edits to the kernel files could still incur expensive rebuilds, because the cascading nature of imports triggers necessary rebuilds. This parts of overhead could not be easily avoided, not least from what I have currently known of. 

#### Hosting build and install artifacts
The build artifacts are usually hosted in a separate location from the source code, for example, under `/usr/obj` for FreeBSD. For kernel development, it is common to have separate build directories for different branches or features to avoid conflicts and to allow for parallel development. This is especially important when working on features that require significant changes to the kernel, as it can lead to large rebuilds that would affect other branches if they share the same build directory.

For example, for FreeBSD, it is common to have separate build directories for different branches or features under `/usr/obj`, such as `/usr/obj/arm64/mte` for the MTE development branch. This allows for parallel development and avoids conflicts between different branches. It also allows for easier cleanup of build artifacts when a branch is no longer needed, as you can simply remove the corresponding build directory without affecting other branches.

To change the build directory for a specific build, you can use the `MAKEOBJDIRPREFIX` variable when invoking `make`. For example, set a custom directory for a specific kernel build with a custom `GENERIC-MTE` configuration:
```shell
  env MAKEOBJDIRPREFIX=/usr/obj/mte_new make -j8 buildkernel KERNCONF=GENERIC-MTE [NO_MODULES=yes]
```

If you are only working on the core kernel and do not require the modules, you can optionally pass the `NO_MODULES=yes` flag to save time. This would only tell the build system to produce static kernel binary and skip hours of compilation for ZFS and drivers.

It is also common to have separate install directories. For example, one can use `KODIR` or `DESTDIR` to specify the target location for installing the built kernel, and `INSTKERNNAME` to specify the name of the installed kernel binary. This allows for testing different kernel builds without affecting the existing installed kernel, and also allows for easy cleanup of installed kernels when they are no longer needed.
```shell
  env MAKEOBJDIRPREFIX=/usr/obj/mte_new make -j8 installkernel KERNCONF=GENERIC-MTE
  { [ KODIR | DESTDIR =/boot/testkernel ] | INSTKERNNAME=kernel.GENERIC-MTE } 
  [NO_MODULES=yes]
```

Note that for the build and install steps, it is important to ensure that the configuration variables (e.g., `MAKEOBJDIRPREFIX`, `KERNCONF`, `NO_MODULES`) are set consistently for a single target. Otherwise, the build system might get confused and produce unexpected results.


```shell
  cd /usr/src
  env MAKEOBJDIRPREFIX=/usr/obj/mte_new make -j8 _worldtmp _legacy _bootstrap-tools
  env MAKEOBJDIRPREFIX=/usr/obj/mte_new make installincludes
```


## More on `make`

#### Common `make` targets
- `make buildkernel`: build the kernel only, without building the world (userland).
- `make buildworld`: build the world (userland) only, without building the kernel. This is useful when you only need to update the userland libraries and tools without changing the kernel. It can save a lot of time if you are only working on userland features or applications.
- `make installkernel`: install the built kernel to the target location (e.g., `/boot/kernel`).
- `make installworld`: install the built world (userland) to the target location (e.g., `/usr/local`).
- `make distribution`: install the distribution files (e.g., documentation, man pages) to the target location.
- `make install`: a convenient target that combines `installkernel`, `installworld`, and `distribution` to install everything in one step. This is useful for quickly deploying the built system after a successful build.
- `make clean`: clean up the build artifacts. This is useful when you want to start a fresh build or when you encounter build issues that might be caused by stale artifacts. However, it can be time-consuming, so use it judiciously.
- `make cleandir`: clean up the build artifacts and also remove the configuration files. This is even more thorough than `make clean` and is typically used when you want to completely reset the build environment. Again, it can be very time-consuming, so use it only when necessary.


#### Useful `make` flags to save build time
- `-jN`: this option tells the build system to use N parallel jobs for building. This can significantly speed up the build process, especially on multi-core machines. 
- `-DWITHOUT_CLEAN`: this option tells the build system to skip the cleaning step before building. It is particularly useful when there are little changes in the source code and to avoid time-consuming full rebuilds. Common usage is `make buildkernel -DWITHOUT_CLEAN` or `make buildworld -DWITHOUT_CLEAN`.
- `-DWITHOUT_CLEANDIR`: this option tells the build system to skip the cleaning step and also to keep the configuration files. This can save even more time than `WITHOUT_CLEAN` if the configuration files are not changed and do not need to be regenerated.
- `-DWITHOUT_DEPENDENCIES`: this option tells the build system to skip the dependency checking step. This can save time when you are confident that the dependencies are up to date and do not need to be checked. 
- `-DNO_CLEAN -DNO_CLEANDIR -DNO_DEPEND`: the old version of the above three options, which are still supported for backward compatibility. Always use the skip clean options with caution, as they can lead to build issues if there are actually changes that are not detected in the source code, configuration, or dependencies. It is always recommended to do a clean build when there are significant changes in the source code or when you encounter build issues that might be caused by stale artifacts.
- `-DWITHOUT_MODULES`: this option tells the build system to skip building kernel modules. This can save time if you are only working on the core kernel and do not need to build the modules. However, if you are working on features that require changes to the modules, it is recommended to build with modules to ensure that everything is built correctly.
- `-DWITH_META_MODE`: this option enables the Meta Mode, which allows for more efficient builds by only rebuilding the parts of the kernel or world that have changed. This can significantly reduce build times, especially for large codebases. 




