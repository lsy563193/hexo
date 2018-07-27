---
title: python函数式编程
date: 2018-07-26 19:35:47
tags: python
category: python
---

### 高阶函数
#### 概念
一个函数接收另一个函数作为参数，这种函数就称之为高阶函数。


```python
#%%
def add(x, y, f):
    return f(x) + f(y)


x = -5
y = 6
f = abs

add(x, y, f)
```

return 11

#### map/reduce
map(function, iterable):**注意**,其实就是线性变换


```python
#%%
def f(x):
    return x*x

L = map(f, [1,2,3,4,5,6])
```

一开始以为这样就可以调用，但是实际输出的是什么时候开始调用 <mat at ******>,函数指针，只是构建一个map实例


```python
#%%
list(L)
```

lisk 可以用set实例实例化
map()作为高阶函数，事实上它把运算规则抽象了，因此，我们不但可以计算简单的f(x)=x2，还可以计算任意复杂的函数，比如，把这个list所有数字转为字符串：


```python
#%%
list(map(str, [1,2,3,4,5,6]))
```

#### reduce
reduce(function, iterable)把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算，其效果就是：
**就是降维，就是卷积**


```python
#%%
from functools import reduce
def f(x,y):
    return x*10 +y

reduce(f, [1,2,3,4,5,6])
```

#### filter


```python
#%%
list(filter(lambda x:x%2==1, [1,2,3,4,5,6]))
```

把一个序列中的空字符串删掉，可以这么写：


```python
#%%
```

list(filter(lambda s:s and s.strip(), ['A    ', '    B    ', s and s.strip()'      C','  D    D   ']))


```python
list(filter(lambda s:s and s.strip() , ['A', '', 'B', None, 'C', '  ']))
```

#### sort
对数列进行排序


```python
#%%
```

sorted([2,4,-5,1,6,-10,3,5])
sorted([2,4,-5,1,6,-10,3,5],key=abs)


```python
sorted([2,4,-5,1,6,-10,3,5],reverse=True)
```

