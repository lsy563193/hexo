---
title: youtube-dl pri
date: 2018-07-25 16:28:07
tags: 
- youtube-dl 
category: 环境搭建
---
### 概述
这是一个可以下载youtube视频和字幕的神奇工具，我主要用于下载youtube视频和字幕.使用这个的前提是你得翻墙。
aria2c可以使youtube-dl多线程下载，但是不支持socks5,所以终端使用privoxy代理socker
<!-- more -->

systemctl start privoxy.service


```bash
youtube-dl --proxy https://127.0.0.1:8118  --playlist-start  285   -o "%(playlist_index)s-%(title)s.%(ext)s" "https://www.youtube.com/watch?v=G7qwhdnE7RA&index=2&list=PLAwxTw4SYaPlqMkzr4xyuD6cXTIgPuzgn&t=0s" --external-downloader aria2c --external-downloader-args "--https-proxy='https://127.0.0.1:8118'  -x 16 -k 1M"
```
命令解析:
youtube:
--proxy https://127.0.0.1:8118
j
8118是privoxy代理socks5协议的https端口.

同理，aria2c也需要配置代理

--https-proxy='https://127.0.0.1:8118

-x 16 -k 1M

-x 是最大线程数，1M每个线程最大下载速度

### 常用命令

youtube-dl有很多参数，我就不一一介绍。运行`youtube -h`可以查看所有命令,这里列出我用到的一些命令:

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