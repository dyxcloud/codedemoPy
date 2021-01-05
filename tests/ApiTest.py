from PIL import Image
from PIL import ImageFilter

img = Image.open(r'D:\file\pic\TIM截图20200219150107.png')
threshold = 50
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
img = img.convert("L").point(table, '1')
img.show()
