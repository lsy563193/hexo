---
title: Hello World
tags:
  - Testing
  - Another Tag
categories: Testing
---
Welcome to [Hexo](https://hexo.io/)! This is your very first post. Check [documentation](https://hexo.io/docs/) for more info. If you get any problems when using Hexo, you can find the answer in [troubleshooting](https://hexo.io/docs/troubleshooting.html) or you can ask me on [GitHub](https://github.com/hexojs/hexo/issues).

## Quick Start


### Create a new post

``` bash
$ hexo new "My New Post"
```

More info: [Writing](https://hexo.io/docs/writing.html)

### Run server

``` bash
$ hexo server
```

More info: [Server](https://hexo.io/docs/server.html)

### Generate static files

``` bash
$ hexo generate
```

More info: [Generating](https://hexo.io/docs/generating.html)

### Deploy to remote sites

``` bash
$ hexo deploy
```

More info: [Deployment](https://hexo.io/docs/deployment.html)

## 内置标签

### 文本居中的引用
使用方式
```
    {% cq %} 文本居中的引用 {% endcq %}
```
效果示例:
{% cq %} 文本居中的引用 {% endcq %}

### 突破容器宽度限制的图片
使用方式
```
    {% fi /image-url, alt, title %}
```
效果示例:
{% fi /image-url, alt, title %}

### Bootstrap Callout
这些样式出现在 [Bootstrap的官方文档](http://getbootstrap.com/)中。

使用方式
{% note class_name %} Content (md partial supported) {% endnote %}
其中，class_name 可以是以下列表中的一个值：

* default
* primary
* success
* info
* warning
* danger

效果示例:
{% note class_name %} Content (md partial supported) {% endnote %}