# 要素 条件 循环

mn = 'learn'
cn = 0
# while i != 1:
#     m += 1
#     i = int(input("输入数字"))
#     print(f"输入了{m}次")
#     print(i)


# for x in mn:
#     if x != "":
#         cn += 1
# print(cn)
i = 9
m = 1
for i in range(1,10):
    for m in range(1,10-i+1):
        print(f"{10-i}*{m}={(10-i)*m}\t", end='')
        print(m)
        print(i)



    print()  # 控制外层循环

# range() 语句 生成一个数字序列
# 语法1：
# range(num)
# 获取一个重零开始到nam结束的数字序列（不包含aum本身）
# range(5)           <0,1,2,3