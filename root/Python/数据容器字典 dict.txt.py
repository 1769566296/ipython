'''
为什么用字典？
    生活中      [字]:[含义]
    Python中  key : value   通过key 找 value
    姓名     成绩
    TJJ     77
    ZJL     88
    LJJ     99  现需要将此表录入到Python程序中
'''
# 数据容器字典 dict  字典用{}括起来，元素是：一个个 键值对
my_dict = {'陶者': 86, '周结论': 96, '林骏捷': 100}
print(f"字典my_dict的内容是：{my_dict}\n字典my_dict的数据类型是：{type(my_dict)}")

# 定义空字典
my_dict1 = {}
print(f"空字典my_dict1的内容是：{my_dict1}\n空字典my_dict1的数据类型是：{type(my_dict1)}")
my_set = set()
print(f"空集合my_set的内容是：{my_set}")

# 字典数据的获取   通过key 获取的是value 的值   key 不可重复,不可以是list/set  value可以是任何数据
stu_score = {'周伯通': 86, '黄药师': 96, '欧阳锋': 100}
print(stu_score['周伯通'])

# 字典的嵌套
stu_score = {'周伯通': {'语文':86, '数学': 76, '英语': 60},
             '黄药师': {'语文':96, '数学': 95, '英语': 97},
             '欧阳锋': {'语文':100, '数学': 83, '英语': 99}
             }
print(stu_score)
# 从嵌套字典中获取数据
print(f"周伯通所有科目成绩是：{stu_score['周伯通']}")
print(f"周伯通英语成绩是：{stu_score['周伯通']['英语']}")

# 字典的常用操作  新增元素
stu_score = {'周伯通': 86,
             '黄药师': 96,
             '欧阳锋': 100
             }
stu_score['洪七公'] = 101
print(f"stu_score的内容是：{stu_score}")
# 字典的常用操作  更新元素
stu_score['周伯通'] = 102
print(f"stu_score的内容是：{stu_score}")

# 删除元素
stu_score = {'王重阳': 106,'黄药师': 96, '欧阳锋': 100 ,'洪七公': 101}
del stu_score['王重阳']
print(f"删除王重阳后的内容是：{stu_score}")
value = stu_score.pop('黄药师')
print(f"删除王重阳后的内容是：{stu_score}")
print(f"被pop方法取出的内容是key对应的value值：{value}")

# 清空字典
stu_score.clear()
print(f"被clear()方法清空后字典的内容是：{stu_score}")

# 获取全部的key
stu_score = {'王重阳': 106,'黄药师': 96, '欧阳锋': 100 ,'洪七公': 101}
keys = stu_score.keys()
print(f"通过.keys()方法获得全部key的值是：{keys}\n他的数据类型是：{type(keys)}")

# 将   数据类型是：<class 'dict_keys'>的变量   keys 转化成list列表
dict_keys_list = list(keys)
print(dict_keys_list)

# 字典的循环遍历
stu_score = {'王重阳': 106,'黄药师': 96, '欧阳锋': 100 ,'洪七公': 101}
# 字典的遍历 每一次循环得到的都是key   
for i in stu_score:
    print(i)