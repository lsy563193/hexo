
# ## python基础
# ### 使用list和tuple
# #### list
# list是一种有序的集合，可以随时添加和删除其中的元素。
# %% 
classmates = ["aaa", "bbb", "ccc"]
classmates
# %%
classmates = ('Michael', 1, 'Tracy')
classmates
# %%
if 1:
    print("hello")
else:
    print("aaaa")

# ##* 循环
# for x in ...循环就是把每个元素代入变量x，然后执行缩进块的语句。
# %%
sum = 0
for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    sum = sum + x
print(sum)

# 如果要计算1-100的整数之和，从1写到100有点困难，幸好Python提供一个range()函数，可以生成一个整数序列，再通过list()函数可以转换为list。比如range(5)生成的序列是从0开始小于5的整数：
# %%
list(range(5))

# ### dist和set 
# %%
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
d.items
d.popitem('Michael')
d.items
###
# %%
s = set([1, 2, 3])
s
# %%
a = 'abc'
a.replace('a', 'A')
# 'Abc'
a
# 'abc'

# ## 函数
# ### 调用
# - **数据类型转换:** int() str() bool()

# %%
int('123')
a = int(12.34)
a
float('12.34')
str(1.23)
str(100)
bool(1)
bool('')

# ### 定义
# # 略

# ### 参数
# > - **注意**:
# > -默认参数不按顺序提供部分默认参数时，需要把参数名写上


# %%
def add_end(L=[]):
    L.append('END')
    return L

# ## 当你正常调用时，结果似乎不错：


add_end([1, 2, 3])

# %%
add_end(['x', 'y', 'z'])

# 当你使用默认参数调用时，一开始结果也是对的：

# %%
add_end()

# %%
# 但是，再次调用add_end()时，结果就不对了：

# %%
add_end()
# ['END', 'END']
# %%
add_end()
# ['END', 'END', 'END']

# 原因解释如下：
# Python函数在定义的时候，默认参数L的值就被计算出来了，即[]，因为默认参数L也是一个变量，它指向对象[]，每次调用该函数，如果改变了L的内容，则下次调用时，默认参数的内容就变了，不再是函数定义时的[]了。
# -**注意**: **定义默认参数要牢记一点：默认参数必须指向不变对象！**jo

# 要修改上面的例子，我们可以用None这个不变对象来实现：

# %%
add_end()
add_end()

# ### 可变参数
# - **使用列表
# - **定义前面加个*号**,参数numbers接收到的是一个tuple
# - **参数前面加个*号**已经有一个list或者tuple

# ### 关键字参数