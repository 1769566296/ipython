def ko(ok):
    """ 求两数相加的和
    根据价格返回折扣后价格：
    满 100 减 20，不满 100 不打折
    :return:"""
    if ok >= 100:
        ok -= 20
        print(f"当前以满100可减20")
    else:
        print(f"当前未满100不参与减免")
        return ok


ko(int(input("请输入金额")))