# 集合     去重、无序
# 定义字面量
# {1, 2.2, 'wed', True, 1, 2}

# 定义字集合变量
qss = {1, 2.2, 'wed', True, 1, 2}
print(f"集合的内容是{qss}\n数据类型是：{type(qss)}")
# 集合的内容是{1, 2, 2.2, 'wed'}
# 数据类型是：<class 'set'>

qss = {1, 5, 3, 4, 6, 'w', 's', 2}
print(f"集合的内容是{qss}\n数据类型是：{type(qss)}")
# 集合的内容是{1, 's', 3, 4, 5, 6, 2, 'w'}
# 数据类型是：<class 'set'>

asd = {}
print(asd, type(asd))
# {} <class 'dict'>

# 集合常用操作
# 添加新元素   集合.add(元素)        （element元素）
wde = {'sk', 'ds', 'dc', 'fdd'}
wde.add('集合是无序的')
print(f"添加新元素{wde}")
# 移除元素  .remove()
wde.remove('ds')
print(f"移除元素 {wde}")

# 随机取出元素 集合 .pop()
qsw = {1, 'zs', '老年机', 4}
x = qsw.pop()
print(f'集合的内容是：{qsw}')
print(f'集合中取出的数是：{x}')


# 清空集合   集合.clear()
qaz = {'qw', 'ws', 'ed', 'rf'}
qaz.clear()
print(f'集合清空后：{qaz}')


# 取出两个集合的差集
set1 = {1, 2, 3, 4}
set2 = {5, 6, 7, 8}
# 取出两个集合（set1，set2）的差集
# (集合1中有集合2中没有的元素 )
# 集合1改变,集合2不变
set1


# len()   长度/元素个数

# 遍历集合
set3 = {1, 2, 3, 4}
for bnl in set3:
    print(f'集合set3中的元素有：{bnl}')
