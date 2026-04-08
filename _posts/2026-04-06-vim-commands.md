---
title: "Useful Vim Commands"
author: qianhui
date: 2026-04-06 00:00:00 +0000
description: >-
  A practical note for commonly used vim commands.
categories: [Configuration]
tags: [web]
render_with_liquid: false
---

### Common file opening and navigation commands 
- `:e <file_path>`: Open a file in the current window.
- `:tabnew <file_path>`: Open a file in a new tab.
- `:vnew <file_path>`: Open a file in a new vertical split.
- `:new <file_path>`: Open a file in a new horizontal split.
- `vim <file_path>`: Open a file directly from the command line.
- `:Ex` or `:Explore`: Open the file explorer to navigate and open files.
- `gf`: Open the file under the cursor (useful for opening files linked in code, e.g., header files in C/C++).
- `:find <file_name>`: Search for a file in the current path and open it if found.
- `:tabfind <file_name>`: Search for a file in the current path and open it in a new tab if found.
- `:vsplit <file_name>`: Search for a file in the current path and open it in a vertical split if found.
- `:split <file_name>`: Search for a file in the current path and open it in a horizontal split if found.
- `<C-]>`: Jump to the definition of the tag under the cursor (requires ctags to be set up).
- `:b <buffer_number>`: Switch to a specific buffer by its number.
- `:ls` or `:buffers`: List all open buffers and their numbers for easy navigation.
- `:tabnext` or `:tabn`: Move to the next tab.
- `:tabprev` or `:tabp`: Move to the previous tab.
- `:tabfirst`: Move to the first tab.
- `:tablast`: Move to the last tab.
- `:w <file_path>`: Save the current file with a new name or path.
- `:wa`: Save all open files.
- `:q`: Quit the current window.
- `:qa`: Quit all windows and exit Vim.
- `:wq`: Save the current file and quit.
- `:x`: Save the current file and quit (same as `:wq`).
- `:wqa`: Save all open files and quit.
- `:tabclose`: Close the current tab.
- `:tabonly`: Close all tabs except the current one.
- `:bd`: Close the current buffer (useful for closing files without closing the window).
- `:bwipeout`: Close the current buffer and remove it from the buffer list.



### reading and loading external configuration file from `.vimrc`
- `source <full_file_path>`: Load and execute Vim commands from an external file. This requires the file to be in Vim script format. 
- `so <file_path>`: This is a shorthand for `source`.
- `runtime <file_name>`: Load a file from Vim's runtime path, which is useful for loading plugins or configuration files that are placed in standard locations (e.g., `~/.vim/` or `/usr/share/vim/`).
- automatic loading at startup if the file is placed in the `~/.vim/plugin/` directory. Do not need a `source` command in your `vimrc`.