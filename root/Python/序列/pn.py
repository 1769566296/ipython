s = "Python is a powerful programming language"
# .lower() 方法 大写转小写
s1 = s.lower()
a = 0
for ok in s:
    if s1 == 'p':
        a += 1

# .split('') 方法： 字符串分割
#     wo



# 练习2
sum1 = (1, 2, 3, 4, 5)
sum2 = list(sum1)
index = 0
while index < len(sun2):
    if sum1[index] % 2 == 0:
        sum2[index] =int(sum2[index] / 2)
    index += 1
