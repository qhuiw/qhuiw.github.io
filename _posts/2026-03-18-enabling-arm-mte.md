---
title: "Enabling ARM MTE: Surveying Current Software Support"
author: qianhui
date: 2026-03-18 00:00:00 +0000
categories: [Research]
tags: [ARM, MTE, Software Support]
---


## Introduction

ARM memory tagging extension (MTE) is a hardware security feature that provides memory safety by tagging both pointers and memory regions to detect invalid memory accesses at runtime. This feature is particularly useful for detecting common memory safety vulnerabilities such as buffer overflows and use-after-free errors.

In this post, I will survey the current state of software support for ARM MTE, including how mainstream operating systems, C/C++ runtime libraries and compiler toolchains have implemented support for this feature and how to use it in practice.

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










