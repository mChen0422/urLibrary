from PIL import Image, ImageFont, ImageDraw
import os


def CreateImg(text, max_len):
  fontSize = 100
  liens = text.split()
  # 画布颜色
  im = Image.new("RGB", (474,744), (255, 255, 255))
  dr = ImageDraw.Draw(im)
  # 字体样式
  ft= ImageFont.truetype('./arial.ttf',fontSize)


  # 文字颜色
  dr.text((0, 0), text,font=ft, fill="#000000")
  im.save('ai.jpg')
  im.show()

text = 'this book is asdfasdfasdfasdfas asdfasdfasdf asdfasdfa asdfasdfawdfa'

CreateImg(text,5)
