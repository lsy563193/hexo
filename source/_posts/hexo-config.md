---
title: hexo主题配置
date: 2018-07-24 13:23:04
tags: hexo
categories: Testing
---

## hexo设置网站的图标Favicon

具体方法实现

ico图标 32*32 
去别的网站下载或者制作，并将图标名称改为 
favicon.ico，然后把图标放在/themes/next/source/images里，并且修改主题配置文件：

# 隐藏网页底部powered By Hexo / 强力驱动

打开themes/next/layout/_partials/footer.swig,使用”<!-- -->”隐藏之间的 "power by" "theme-info"代码即可，或者直接删除。