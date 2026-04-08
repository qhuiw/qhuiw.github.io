---
title: "Useful Web Commands"
author: qianhui
date: 2026-04-06 00:00:00 +0000
description: >-
  A practical note for commonly used web commands.
categories: [Configuration]
tags: [web]
render_with_liquid: false
---

#### Download a file from the web using `curl` (client URL)
```shell
user@host % curl -L -O <file_url>
```
- `-L` means "follow redirects", which is useful when the URL provided is a shortened link or when the server redirects to another URL, e.g., if the URL returns `301/302/307/308`, curl will request the new Location URL automatically.
- `-O` option saves the file with its original name as specified in the URL.
- `-o <output_file_name>` option allows you to specify a custom name for the downloaded file instead of using the original name from the URL.

#### Download a file from the web using `wget` (web get)
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