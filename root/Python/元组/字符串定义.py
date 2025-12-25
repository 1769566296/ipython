nae = "quads"
print(nae[0])
print(nae[-1])


print("元素的替换")
nae = "阿玉"
nap = nae.replace("阿玉", "阿杨")
print(f"字符串{nae}完成替换后变成{nap}")


print("字符串去指定内容：  字符串.strip（内容），无内容删前后空格")
abc = " 你 00 好"
print(abc)
print(abc.strip())
print(abc.strip("00"))
png = "你好你好你好你好你好我是啊啊亚砸吧"
print(f"统计某内容在字符串出现的次数：{png.count('你好')}")




