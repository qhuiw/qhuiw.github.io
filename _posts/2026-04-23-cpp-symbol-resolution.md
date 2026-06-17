---
title: "VSCode C/C++ Symbol Resolution with clangd"
author: qianhui
date: 2026-04-08 00:00:00 +0000
description: >-
  C/C++ symbol resolution in Visual Studio Code (VSCode)
categories: [Configuration]
tags: [vscode, clangd]
render_with_liquid: false
---


## Using clangd
`clangd` is a language server that provides code completion, navigation, and other features for C/C++ development. It can be used with Visual Studio Code (VSCode) to enhance the coding experience.


1. Generate `compile_commands.json` for your C/C++ project, which is a compilation database that `clangd` uses to understand how to compile your code. Clangd is essentially running the compiler mentally on each file to understand it. 

You can generate by either fully building the project, or just configure using CMake with `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`:
```shell
cmake -S llvm -B build \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;lld;lldb" \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```
This creates `build/compile_commands.json`. Adjust `-DLLVM_ENABLE_PROJECTS` to include whichever subprojects you care about.

You can optionally symlink `compile_commands.json` to the repo root for easier access as this is where clangd looks for it by default:
```shell
ln -s build/compile_commands.json compile_commands.json
```


2. `.clangd` at repo root
```
CompileFlags:
  CompilationDatabase: <path_to_compile_commands.json>

Index:
  Background: Build

Diagnostics:
  UnusedIncludes: None
  MissingIncludes: None
```

3. `.vscode/settings.json` at repo root
```json
{
  "clangd.arguments": [
    "--compile-commands-dir=<path_to_compile_commands.json>",
    "--background-index",
    "--header-insertion=never",
    "--completion-style=detailed",
    "-j=8"
  ]
}
```

4. Restart Clangd server in VSCode command palette (Ctrl+Shift+P) by searching "clangd: Restart clangd server".