import random


nk = input("请输入是否开始，y/n")

# 游戏结束是否继续判断
def go():
    print("是否开始下一局")
    go = input("y/n")
    if go == 'y':
        print("开始游戏")
        yes()
    elif go == 'n':
        print("游戏退出")


# 游戏数字及次数判断
def yup():
    global df
    jack = None
    dp = 0
    while jack != 1:
        # print(f"输入的随机数{jack}，源随机数{yuo}")
        if dp != pp:
            df = int(input("请输入你拆测的数字"))
            dp += 1
            if df == yuo:
             print(f"当前数字{df}，对了")
             jack = 1
             go()
            elif df > yuo:
                if dp == pp:
                    print(f"---当前次数以用完---")
                    print(f"本局以用{pp}次，随机数是{yuo}")
                    jack = 1
                    go()
                else:
                    print(f"当前数字{df}，大了")
            elif df < yuo:
                print(f"当前数字{df}，小了")
                if dp == pp:
                    print(f"---当前次数以用完---")
                    print(f"本局以用{pp}次，随机数是{yuo}")
                    jack = 1
                    go()
                else:
                    print(f"当前数字{df}，小了")

        elif dp == pp:
            print(f"---当前次数以用完---")
            print(f"本局以用{pp}次，随机数是{yuo}")
            jack = 1
            go()





        # df = int(input("请输入你拆测的输入"))
        # if df == yuo:
        #     print(f"当前数字{df}，对了")
        #     jack = 1
        #     go()
        # elif df > yuo:
        #     print(f"当前数字{df}，大了")
        # elif df < yuo:
        #     print(f"当前数字{df}，小了")


# 游戏初始化
def yes():
    global yuo
    global pp
    yy = int(input("请输入拆数字的最大随机数"))
    yuo = random.randint(1, yy)
    pp = int(input("请输入拆的次数"))
    yup()


if nk == 'y':
    print("游戏开始")
    yes()
elif nk == 'n':
    print("游戏退出")