---
title: "Enabling ARM MTE: Surveying Current Userspace Support"
author: qianhui
date: 2026-03-18 00:00:00 +0000
categories: [Research]
tags: [ARM, MTE, Userspace, Support]
---


## Introduction

ARM memory tagging extension (MTE) is a hardware security feature that provides memory safety by tagging pointers and memory regions to detect invalid memory accesses at runtime. This feature is particularly useful for preventing common memory-related vulnerabilities such as buffer overflows and use-after-free errors.

In this post, I will survey the current state of userspace support for ARM MTE, including how mainstream operating systems, C/C++ runtimes and compilers have implemented support for this feature and how to use it in practice.

## Hardware Requirements
- AArch64 hardware with MTE support (e.g., Armv8.5-A/Armv9-A), or
- Emulation environment that supports MTE (e.g., QEMU with MTE support).

## Linux & <code>glibc</code>
<!-- Linux has been actively working on integrating ARM MTE support into the kernel and userspace. The Linux kernel has added support for MTE in recent versions, allowing applications to take advantage of this feature.  -->
Linux kernel 5.10+
a Linux kernel compiled with memory tagging support (CONFIG_ARM64_MTE).

Glibc (GNU C Library) version 2.33 and later supports ARM MTE on AArch64 Linux. 

- check if linux kernel supports MTE:
  ```shell
  $ grep MTE /boot/config-$(uname -r)
  CONFIG_ARM64_MTE=y
  CONFIG_ARM64_AS_HAS_MTE=y
  $ 
  ```


```shell
# Glibc tunables: Bit 0 enabled (tagged memory), Bit 1 NOT set
export GLIBC_TUNABLES=glibc.malloc.mte=1

# Glibc tunables: Bit 1 enables precise faulting
export GLIBC_TUNABLES=glibc.malloc.mte=3
```


## LLVM/Clang
LLVM/Clang has supported MTE stack tagging since version 12 via `-fsanitize=memtag-stack`.




