---
title: 一些神奇的工具使用笔记
date: 2018-07-25 16:28:07
tags: 
- youtube-dl 
- proxychains 
- notedown
category: 环境搭建
---

## youtube-dl

### 概述
这是一个可以下载youtube视频和字幕的神奇工具，我主要用于下载字幕.使用这个的前提是你得翻墙。

### 安装
```bash
pip install --upgrade youtube-dl
```

### 常用命令

youtube-dl有很多参数，我就不一一介绍。运行`youtube -h`可以查看所有命令,这里列出我用到的一些命令:

> **注意**:
> 由于众所周知的原因，使用之前需要下载proxychains,
```
sudo apt-get install proxychains
```
> 安装proxychains,需要修改`/etc/proxychains`配置最后一行
```
# socks4    127.0.0.1 9050
socks5  127.0.0.1 1080
```
> 1080是你翻墙的端口

```bash
proxychains youtube-dl --write-sub --sub-lang en --skip-download -o "%(playlist_index)s-%(title)s.%(ext)s" "https://www.youtube.com/playlist?list=PLAwxTw4SYaPkCSYXw6-a_aAoXVKLDwnHK"
 ```
 youtube-dl --list-subs --no-playlist "https://youtu.be/nLEbJZFm5-E?list=PLAwxTw4SYaPkCSYXw6-a_aAoXVKLDwnHK "
选项的解释
* **--write-sub**: 写到字幕文件
* **--sub-lang**: 下载语言
* **--skip-download**: 不下载视频
* **-o "%(playlist_index)s-%(title)s.%(ext)s" **: 使用编号加标题

## notedown
notedown主要是用来实现md to ipynb，这样我就可以直接一边写博客一边调试代码。
使用方法如下:

- **安装**:
```
pip install https://github.com/aaren/notedown/tarball/master
```
- **打开文件**:
```
sudo gedit ~/.jupyter/jupyter_notebook_config.py
```
` **增加以下内容，存盘**

> c.NotebookApp.contents_manager_class = ‘notedown.NotedownContentsManager’

- **重启jupyter notebook 服务 **