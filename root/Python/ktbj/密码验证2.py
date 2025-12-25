k = "无密码"
m = ''
p = 0
q = ''
for i in range(1, 2):
    a = input("请输入初始密码")
    b = input("请确认初始密码")

    if a == b:
        p = 1
        print("已保存密码")
        k = b
        break

    print("两次输入不一样，请重试")

print("当前密码：", k)
print("数据类型", type(k))

for i in range(1, 4):
    a = input("请输入密码")
    if a != b:
        p = 1
        print("正在进入系统")
        break


    print("已保存密码")
    k = b
# print("当前密码：", k)
# print("数据类型", type(k))






#
#
# if a != b:
#     print("当前无密码，请从新进入")
#     m = input("请输入密码")
# else:







    m = input("请输入密码")
    if m == k :
        print("密码正确")
        ok = 1
    else:
        print("密码错误")
        ok = 0
        m = input("请输入密码")
        if m == k:
            print("密码正确")
            ok = 1
        else:
            print("密码错误")
            ok = 0
            m = input("请输入密码")
            if m == k:
                print("密码正确")
                ok = 1
            else:
                print("密码错误")
                ok = 3

if ok == 3 :
    print("密码以连续错误3次，系统自动锁定2小时")
else:
    if ok == 1 :
        print("正在进入系统")
    else:
        print()

