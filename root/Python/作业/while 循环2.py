# 99乘法表
i = 1
ass = 1
while i <= 9:
    ass = 1
    while ass <= i:
        print(f"{i}*{ass}={i*ass}", end='\t')
        ass += 1
    i += 1
print()