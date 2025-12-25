# if就近与else配对

a =int(input("请输入年龄"))
if a >= 12:
    print("青少年，正是风华正茂的年纪")
elif not 12 < a:
    print("你还是个孩子，多快乐啊")
else:
    print("你以成年了")