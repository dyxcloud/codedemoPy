import re

str1 = "123@qq.comaaa@163.combbb@126.comasdf111@asdfcom"
print(re.findall(r'\w+@(?:qq|163|126)\.com',str1))
print(re.match(r'\w+@(?:qq|163|126)\.com',str1).groups())