---
title: "Enabling ARM MTE: Surveying Current Software Support"
author: qianhui
date: 2026-03-18 00:00:00 +0000
categories: [Research]
tags: [ARM, MTE, Software Support]
---


## Introduction

ARM memory tagging extension (MTE) is a hardware security feature that provides memory safety by tagging both pointers and memory regions to detect invalid memory accesses at runtime. This feature is particularly useful for detecting common memory safety vulnerabilities such as buffer overflows and use-after-free errors.

In this post, I will survey the current landscape of software support for ARM MTE, including how mainstream operating systems, C/C++ runtime libraries and compiler toolchains have implemented support for this feature and how to use it in practice.

## Hardware Requirements
To enable ARM MTE, you need either:
- an AArch64 hardware with MTE capability (e.g., minimum implementing Armv8.5-A), or
- an emulation environment that exports MTE capability (e.g., QEMU that enables MTE feature, or Hypervisors that allow host MTE pass-through).

## Linux & <code>glibc</code>
<!-- Linux has been actively working on integrating ARM MTE support into the kernel and userspace. The Linux kernel has added support for MTE in recent versions, allowing applications to take advantage of this feature.  -->
Linux kernel 5.10+
a Linux kernel compiled with memory tagging support (CONFIG_ARM64_MTE).

- On Linux system, check if the CPU supports MTE by checking the system's CPU features:
  ```shell
  $ cat /proc/cpuinfo | grep mte
  Features : ... mte ...
  ```
- check if the linux kernel is compiled with MTE support enabled:
  ```shell
  $ grep MTE /boot/config-$(uname -r)
  CONFIG_ARM64_MTE=y
  CONFIG_ARM64_AS_HAS_MTE=y
  ```

Glibc (GNU C Library) version 2.33 and later supports ARM MTE on AArch64 Linux. 
- check if your glibc version supports MTE:
  ```shell
  $ ldd --version
  ldd (Ubuntu GLIBC 2.42-0ubuntu3.1) 2.42
  ```




```shell
# Glibc tunables: Bit 0 enabled (tagged memory), Bit 1 NOT set
export GLIBC_TUNABLES=glibc.malloc.mte=1

# Glibc tunables: Bit 1 enables precise faulting
export GLIBC_TUNABLES=glibc.malloc.mte=3
```




## XNU & LLVM/Clang
Mac OS X 26.0+ [Darwin 25/XNU 12377.81.4] on Apple Silicon (A19/M5 chip) supports ARM MTEv4, also known as EMTE as part of Apple's Memory Integrity Enforcement(MIE).


LLVM/Clang has supported MTE stack tagging since version 12 via `-fsanitize=memtag-stack`.










## Debugging tools
#### GNU Debugger (GDB)

GDB first introduced support for ARM MTE debugging in [release 11.1][GDB-11-1], September 2021. This version added the core infrastructure for AArch64 memory tagging, including the `memory-tag` command prefix and various subcommands to inspect and manipulate tags, a new `/m` format for the `x` (examine) command to display memory content along with its allocation tags, as well as a `-memory-tag-violations` option for the `print` command to warn about tag violations when the printed expression value is a pointer.
<!-- 
If the underlying architecture supports memory tagging, like AArch64 MTE or SPARC ADI do, GDB can make use of it to validate pointers against memory allocation tags. -->

GDB 13.1 and later significantly improved how MTE tags are handled in core dumps, allowing inspection of tags in post-mortem debugging even if the crash happened on a different machine.

```shell
(gdb) help memory-tag
Generic command for printing and manipulating memory tag properties.

List of memory-tag subcommands:

memory-tag check -- Validate a pointer\'s logical tag against the allocation tag.
memory-tag print-allocation-tag -- Print the allocation tag for ADDRESS.
memory-tag print-logical-tag -- Print the logical tag from POINTER.
memory-tag set-allocation-tag -- Set the allocation tag(s) for a memory range.
memory-tag with-logical-tag -- Print a POINTER with a specific logical TAG.

(gdb) help print
print, inspect, p
Print value of expression EXP.
Usage: print [[OPTION]... --] [/FMT] [EXP]

  ...
  -memory-tag-violations [on|off]
    Set printing of memory tag violations for pointers.
    Issue a warning when the printed value is a pointer
    whose logical tag doesn\'t match the allocation tag of the memory
    location it points to.
  ...
```

For example, in a program that contains an Out-of-Bounds access bug, GDB can catch the memory tag violation and report as follows:
```shell
(gdb) set env GLIBC_TUNABLES=glibc.mem.tagging=3
(gdb) run

Program received signal SIGSEGV, Segmentation fault
Memory tag violation while accessing address 0x0100fffff7cb0740
Allocation tag 0x0
Logical tag 0x1.

# buf_a is a pointer to a 16-byte buffer allocated with malloc.

(gdb) memory-tag check &buf_a[16]
Logical tag (0xe) does not match the allocation tag (0x0) for address 0xe00fffff7cb0740.
(gdb) memory-tag print-allocation-tag &buf_a[16]
$9 = 0x0
(gdb) memory-tag print-logical-tag &buf_a[16]
$10 = 0xe

(gdb) x/m 0x0100fffff7cb0740
<Allocation Tag 0x0 for range [0x100fffff7cb0740,0x100fffff7cb0750)>
0x100fffff7cb0740:	0 # memory content at address 0xfffff7cb0740 is 0.

(gdb) print -memory-tag-violations on -- &buf_a[16]
Logical tag (0xe) does not match the allocation tag (0x0).
$4 = 0xe00fffff7cb0740 ""
(gdb) print buf_a+16
Logical tag (0xe) does not match the allocation tag (0x0).
$8 = 0xe00fffff7cb0740 ""
```




#### LLVM Debugger (LLDB)

built-in annotations in the register view `register read` command -- When MTE is active, standard register reads will show the logical tag in the top bits of pointers stored in registers. 

```shell
(lldb) memory tag 
Commands for manipulating memory tags

Syntax: memory tag <sub-command> [<sub-command-options>]

The following subcommands are supported:

      read  -- Read memory tags for the given range of memory. Mismatched tags will be marked.
      write -- Write memory tags starting from the granule that contains the given address.

(lldb) help memory read
Read from the memory of the current target process.
    
      ...
      --show-tags
          Include memory tags in output (does not apply to binary output).

```


```shell
(lldb) env GLIBC_TUNABLES=glibc.mem.tagging=3
(lldb) run
...
Process 36250 stopped
* thread #1, name = 'oob_malloc', stop reason = signal SIGSEGV: sync tag check fault (fault address=0x800fffff7cb0740 logical tag=0x8 allocation tag=0x0)

(lldb) memory tag read buf_a
Logical tag: 0x8
Allocation tags:
[0xfffff7cb0730, 0xfffff7cb0740): 0x8
(lldb) memory tag read &buf_a[16]
Logical tag: 0x8
Allocation tags:
[0xfffff7cb0740, 0xfffff7cb0750): 0x0 (mismatch)

(lldb) register read x0
      x0 = 0x0800fffff7cb0740
```






[GDB-11-1]: https://www.phoronix.com/news/GDB-11.1-Released