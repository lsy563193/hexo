---
title: 打造Hexo个人博客中遇到的坑
date: 2018-07-25 09:46:24
tags: hexo
category: 工具
---

经历了几天的努力，终于解决了几个重大问题，打造出自己理想的博客个人网站。主要是参照[大黄菌的个人博客](http://kyonhuang.top/),但是她没有公布使用如何使用hexo跳转到docsify的步骤。现在把我这几天填过的坑记下来。

首先说下我的需求:

* hexo作博客,next作主题.
* 可以自动跳转到docsify文档的界面.
* 使用个人域名

## hexo作博客,next作主题

### hexo作博客
使用`hexo`构建博客主要是参照[hexo的官方文档](https://hexo.io/zh-cn/index.html).以下是构建的步骤:

#### 开始使用

* 1. **概述**: 
  * **安装**: post_asset_folder: true
  > **注意**:
  >  npm 必须使用sudo

* **建站**:
 * **npm install**这条指令有什么用
 * **package.json**　的文档内容现在有不明白有什么用
 * **scaffolds**: 默认post,draft是草稿模板，page是页面模板，当你使用tag,category的时候用到，后面会讲到
 * **source**: _文件隐藏，Markdown,html解析，其他拷贝过去。如拷贝CNAME
 * **themes**:主题，next就是拷贝到这里的

*  **配置**:
 
 * **网站**: title ,就是浏览器标签栏的名字，subtitle 网页显示的Hexo首页的地方. 
 > 注意：必须hexo serve重启才能生效

 * **网址**: 网站存放在子目录,目前不用
 * **目录**: 目前不用
 * **文章**: titlecase指的是将每个单词首字母转换成大写,post_asset_folder: true
 * **分类 & 标签**: 不用到
 * **日期 / 时间格式**: 不用到
 * **分页 不用到**:
 * **扩展**:
  * **theme**: ,现在不用，但是后面改为next要回来改
  * **deploy** 最好现在就布置，自动发布到github,之前没有看到这个选项，手动发布.
> **注意**: 这是我的设置
> type: git
> repo: git@github.com:lsy563193/lsy563193.github.io.git
> branch: master

* **指令**: init, new, generate, deploy, publish ,server
> **注意**:
> hexo g -d, hexo d -g　通常用,一样的
> hexo serve　也是可以简写为hexo s的，不用加路径，常用

* 迁移

#### 基本操作
* 写作
* Front-matter
开启了 comments 评论功能
* 预先定义的参数
* 分类和标签
> **注意**:
> categories:
> - Diary
> - Life
> 会使分类Life成为Diary的子分类

* 标签插件
在markdown 中添加太多的hexo 标签，其实会在以后用其他编辑器预览，查看，迁移时留下诸多不变，毕竟，私有的语法意味着不兼容
* 资源文件夹
资源（Asset）代表 source 文件夹中除了文章以外的所有文件，例如图片、CSS、JS 文件等。
* 数据文件
* 服务器
* 生成器
* 部署
#### 自定义
* 永久链接

## 可以自动跳转到docsify文档的界面


实现的方式是使用域名覆盖。以链接到[吴恩达《深度学习》系列课程笔记][1],为例,网址为http://lsy563193/github.io/Andrew-Ng-Deep-Learning-notes/ ,我们只要让page的网址也为这个，这样在点击的时候就自动替换为 Andrew-Ng-Deep-Learning-notes的内容
实现的步骤如下: 
* **克隆**:克隆Andrew-Ng-Deep-Learning-notes到你的github目录，
* **设置为github.io的doc目录**: 把这个项目设置为你博客下的目录
{% asset_img github-spages-docs.png This is an example image %}
* **把hexo生成的地址也设置为这个**: 首先创建Andrew-Ng-Deep-Learning-notes的博文
```
    hexo new Andrew-Ng-Deep-Learning-notes
```
 * 设置category,比如为深度学习笔记,效果如下
{% asset_img Andrew-Ng-Deep-Learning-notes.png This is an example image %}
 * **设置_config.yml的permalink: :title/**: 这样两者的地址就一样的

## Hexo-Next-主题优化
[参考](https://www.jianshu.com/p/4ef35521fee9)
1. 浏览页面的时候显示当前浏览进度
_config.yml scrollpercent
  
[1]: http://kyonhuang.top/Andrew-Ng-Deep-Learning-notes/

2. 开启版权声明
主题配置文件下,搜索关键字post_copyright,enable改为true

主题