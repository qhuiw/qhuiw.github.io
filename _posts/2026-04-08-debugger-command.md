---
title: "Useful GDB/LLDB Commands"
author: qianhui
date: 2026-04-08 00:00:00 +0000
description: >-
  A practical note for commonly used debugger commands.
categories: [Configuration]
tags: [gdb, lldb]
render_with_liquid: false
---



```shell
This GDB supports auto-downloading debuginfo from the following URLs:
  <https://debuginfod.ubuntu.com>
Enable debuginfod for this session? (y or [n]) y
Debuginfod has been enabled.
To make this setting permanent, add 'set debuginfod enabled on' to .gdbinit.
Downloading separate debug info for system-supplied DSO at 0xfffff7ffa000
[Thread debugging using libthread_db enabled]      
```


## Debugging cross-compiled FreeBSD/CheriBSD QEMU guest on a native host
To debug FreeBSD/CheriBSD, the debugger (e.g., GDB) should be either built for the target OS/ABI (e.g.,  FreeBSD/CheriBSD on AArch64/Morello) and then run on the target system, or be built as a cross-debugger that runs on the host system but can understand the target OS/ABI (e.g., aarch64-linux-gnu-gdb running on x86_64 Linux host to debug AArch64 FreeBSD/CheriBSD guest).

For example, if `file` reports `gdb` as an AArch64 FreeBSD ELF binary, then it has to be run on the FreeBSD/CheriBSD system. 
For `gdb-native` is a cross-debugger that can run on a Mac OS X/Darwin host but can understand AArch64 FreeBSD/CheriBSD ELF objects.

```shell
$ gdb /
(gdb) set architecture aarch64
(gdb) target remote <ip_address>:<port> # Connect to a remote target (e.g., a QEMU VM) for debugging. The target must be running a GDB server that listens on the specified IP address and port.

```