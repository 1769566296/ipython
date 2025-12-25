# or 或运算,遇到第一个真就截止，有一真则为真，全假为假
num = 1 > 2 or 3 > 3 or '执行代码' or 2 > 1
print(num)
#and 与运算，
num = 1 > 2 and 3 > 3 and '执行代码' and 2 > 1
print(num)
#not 非运算
# num = 1 > 2 not 3 > 3 not '执行代码' or 2 > 1
print(num)
