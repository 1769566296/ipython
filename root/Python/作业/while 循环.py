# while循环猜数字游戏

import random
mo = random.randint(1, 10)
count = 0
flag = True
mk = 0
while flag:
    cp = int(input("请输入你猜的数字"))
    count += 1
    mk += 1
    print(f"你总共猜了{count}次")
    if cp == mo:
        flag = False
        print("猜对了")
    else:
        if cp > mo:
            print("猜大了")
        else:
            print("猜小了")
    if mk == 5:
        print("请下一位")
        mk = 0
print(f"总共猜了{count}次")


