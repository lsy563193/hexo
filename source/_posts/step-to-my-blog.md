---
title: 打造个人博客中遇到的坑
date: 2018-07-25 09:46:24
tags: hexo
category: 工具
---

经历了几天的努力，终于解决了几个重大问题，打造出自己理想的博客个人网站。主要是参照[大黄菌的个人博客](http://kyonhuang.top/),但是她没有公布使用如何使用hexo跳转到docsify的步骤。现在把我这几天填过的坑记下来。

首先说下我的需求:

* hexo作博客,next作主题.
* 可以自动跳转到docsify文档的界面.

## hexo作博客,next作主题

### hexo作博客
使用`hexo`构建博客主要是参照[hexo的官方文档](https://hexo.io/zh-cn/index.html).以下是构建的步骤:

1. **安装**: 首先要安装node.js, 再用 npm install -g hexo-cli
> 注意: 
>
> npm 必须使用sudo

2. **建站** 

> 注意：
> 到现在我都不知道npm install这条指令有什么用
> package.json　的文档内容现在有不明白有什么用
> scaffolds: 默认post,draft是草稿模板，page是页面模板，当你使用tag,category的时候用到，后面会讲到
> source: _文件隐藏，Markdown,html解析，其他拷贝过去。如拷贝CNAME
> themes:主题，next就是拷贝到这里的

3 **配置** 

> **网站**: title ,subtitle  必须hexo serve重启才能生效
> **网址**: 网站存放在子目录,目前不用
> **目录**: 目前不用
> **文章**: titlecase指的是将每个单词首字母转换成大写,post_asset_folder: true
