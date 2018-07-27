---
title: 在vscode jupyter模式下工作
date: 2018-07-26 18:53:19
tags: 
- vscode 
- jupyter
category: 
- 工具
---

## 概述
使用jupyter notebook工作时候不习惯，自己还是喜欢在vscode纯vim的工作模式。于是下载了vscode jupyter的插件，但是这是来写pyd代码的。我的目的最终是生成md文档，记录我学习的过程。于是我下载了一个py2md.py的工具。做了些修改，用于把py生成md文件。

```python
#! /usr/bin/env python
import sys
import itertools

for markdown, lines in itertools.groupby(open(sys.argv[1]).readlines(), key=lambda line: line.startswith('# ')):
    if markdown:
        print(''.join(line[2:] for line in lines))
    else:
        print('\n```python')
        print(''.join(lines).strip())
        print('```\n')
```

写的python文档如下：
![py文档](lxf-python-py.png)

生成的markdown文档如下：

![md文档](lxf-python-md.png)

写的过程中需要注意的几点:
- **文档直接用＃　隔开，并且不要留有空格**
- **python文档的代码用＃％％是表示执行cell的**

更新
vscode 下安装的插件
- open in github
- github
