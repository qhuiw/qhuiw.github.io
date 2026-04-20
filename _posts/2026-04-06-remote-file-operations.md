---
title: "Useful Remote File Operations"
author: qianhui
date: 2026-04-06 00:00:00 +0000
description: >-
  A practical note for commonly used remote commands.
categories: [Configuration]
tags: [web]
render_with_liquid: false
---

## Downloading files from the web
#### Using `curl` (client URL)
```shell
user@host % curl -L -O <file_url>
```
- `-L` means "follow redirects", which is useful when the URL provided is a shortened link or when the server redirects to another URL, e.g., if the URL returns `301/302/307/308`, curl will request the new Location URL automatically.
- `-O` option saves the file with its original name as specified in the URL.
- `-o <output_file_name>` option allows you to specify a custom name for the downloaded file instead of using the original name from the URL.

#### Using `wget` (web get)
```shell
user@host % wget <file_url>
```
- `wget` will save the file with its original name as specified in the URL by default, so you don't need to specify an option for that. However, if you want to save the file with a different name, you can use the `-O` option followed by the desired output file name:
```shell
user@host % wget -O <output_file_name> <file_url>
```

##### Note
To download a file from GitHub using `curl` or `wget`, you must use the **RAW** URL of the file. For example, if you want to download a file from a GitHub repository, you can navigate to the file in the repository, click on the "Raw" button to get the raw URL, and then use that URL with `curl` or `wget` to download the file.
```shell
user@host % curl -L -O https://raw.githubusercontent.com/username/repository/branch/path/to/file
```

## Remote file operations
#### `rsync` for repeated syncs of trees
`rsync` is a powerful tool for synchronizing files and directories between two locations over SSH. It supports incremental transfers, which means it only transfers the parts of files that have changed, making it efficient for syncing large codebases.
N.B. `rsync` needs to be installed on both ends of the transfer.

For QEMU that assigns local port `x` to the SSH server on a VM guest, use `-e "ssh -p x"` if `x` is not the default SSH port `22`.

A standard template to sync files from the local host to the VM guest or vice versa by swapping source and destination paths:
```bash
rsync -av --delete -e "ssh -p x" /path/to/local/dir/ user@vm-guest:/path/to/remote/dir/
```
- `-a` means "archive mode", which preserves symbolic links, permissions, timestamps, and other file attributes.
- `-v` means "verbose", which provides detailed output of the syncing process.
- `-z` means "compress file data during the transfer", which can speed up the transfer if the files are large and compressible.
- `-P` is a combination of `--progress` and `--partial`, which shows progress during transfer and allows resuming interrupted transfers.
- `-e "ssh -p x"` specifies the remote shell to use, in this case, SSH with a custom port `x`.
- `--delete` option can be added if you want to delete files in the destination that are not present in the source, ensuring that the destination is an exact mirror of the source.
- `/path/to/local/dir/` is the source directory on the local machine. The trailing slash means "sync the contents of this directory".
- `user@vm-guest:/path/to/remote/dir/` is the destination on the remote machine, where `user` is the username, `vm-guest` is the hostname or IP address of the VM, and `/path/to/remote/dir/` is the target directory on the VM where the files will be synced to. The trailing slash means "sync into this directory".

N.B. make sure to include the trailing slash in the source path to sync the contents of the directory rather than the directory itself. Otherwise, it will create a new directory `remote/dir/dir` on the destination instead of syncing the contents directly into `remote/dir/`.

An example command might look like this:
```bash
rsync -av --delete -e "ssh -p 19507" ./sys/ root@127.0.0.1:/usr/src/sys/
```
This command will sync the local `./sys/` directory to `/usr/src/sys/` on the VM guest, using SSH on port `19507`.

#### `scp` for quick file copy
`scp`(secure copy) is a simpler tool for copying files between hosts over SSH. It uses the old SCP/RCP protocol (now SFTP protocol on modern OpenSSH due to security concerns). The client opens an SSH session and runs a remote `scp` in a special mode, then streams files over. It's simple, fast for bulk transfers.

Downsides: it does not have directory listing, no resume, no rename, no remove like the full `sftp` tool. It also does not support incremental transfers like `rsync` tool.

E.g., to copy a single file from the local host to the VM guest:
```bash
scp -P 19507 \
  sys/conf/Makefile.arm64 \
  root@127.0.0.1:/usr/src/sys/conf/Makefile.arm64
```
- `-P 19507` specifies the SSH port to use (note that `scp` uses uppercase `-P` for port, while `ssh` uses lowercase `-p`).

#### `sftp` for interactive file transfer
`sftp` (SSH File Transfer Protocol) is an interactive command-line tool for transferring files over SSH. SFTP is a proper file-transfer protocol that runs as a subsystem over SSH. It supports listing directories, stat'ing files, partial reads/writes, resuming, renaming, removing, setting permissions — basically a real remote filesystem API. 

It provides a simple interface for navigating the remote file system and transferring files. The `sftp` command gives you an interactive FTP-like shell (`ls`, `cd`, `put`, `get`, `mput`), but you can also script it with `-b` batchfile or just use `sftp` user@host:/path/file localfile for one-shots. It's what GUI tools like FileZilla, Cyberduck, and VS Code's Remote-SSH use. 


#### Practical guidance today:
- For one-off "copy this file/dir from A to B," `scp` is still the most ergonomic and is fine — and on modern OpenSSH it's secretly sftp anyway.
- For scripting, browsing, or anything that needs resume/rename/listing, use `sftp`.
- For repeated syncs of trees, use `rsync` (which itself rides on ssh) — neither `scp` nor `sftp` do incremental transfers.