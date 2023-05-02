import base64
import os
import subprocess
import sys
import time
from io import BytesIO
from PIL import Image
from flask import Flask, send_file, make_response
from flask import jsonify, request
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import mongoengine as me
from wordcloud import WordCloud
import openai
from PIL import Image, ImageFont, ImageDraw

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
  "db": "bookdata",
  "host": 'localhost',
  'port': 27017,
  'connect': True
}
app.config["DEBUG"] = False

db = MongoEngine(app)
CORS(app)


class books(me.Document):
  ISBN = me.StringField(primary_key=True)
  Book_Title = me.StringField(required=True)
  Book_Author = me.StringField(required=True)
  Year_Of_Publication = me.StringField(required=True)
  Publisher = me.StringField(required=True)
  Image_URL_S = me.StringField(required=True)
  Image_URL_M = me.StringField(required=True)
  Image_URL_L = me.StringField(required=True)
  rating = me.FloatField(required=True)
  score = me.IntField(required=True)
  count = me.IntField(required=True)


# routes

# get data from mongo
@app.route('/', methods=['GET'])
def heroes():
  return jsonify(books.objects())


# get specific  hero
@app.route('/detail/<id>', methods=['GET'])
def detail(id):
  print('start fetch')
  for x in books.objects():
    if str(x['ISBN']) == str(id):
      return jsonify(x)

  return 'record not found', 400


# update specific hero
@app.route('/update', methods=['POST'])
def update():
  #   print('start update')
  data = request.json
  #   print(data)
  if books.objects(ISBN=data['_id']):
    findHero = books.objects(ISBN=data['_id'])
    findHero.update(rating=data['rating'])
    return 'updated', 200
  return 'non match', 300


# add hero
@app.route('/add', methods=['POST'])
def add_hero():
  data = request.json
  print(data)
  checkNames = books.objects()
  for x in checkNames:
    if x['ISBN'] == data['ISBN']:
      return 'existed name'

  books(ISBN=data['ISBN'], Book_Title=data['Book_Title'], Book_Author=data['Book_Author'],
        Year_Of_Publication=data['Year_Of_Publication'], Publisher=data['Publisher'], Image_URL_S=data['Image_URL_S'],
        Image_URL_M=data['Image_URL_M'], Image_URL_L=data['Image_URL_L'], rating=data['rating'], score=data['score'],
        count=data['count']).save()
  return 'ok', 200


# update specific hero
@app.route('/delbook/<ids>', methods=['GET'])
def delbook(ids):
  print('del book')
  if books.objects(ISBN=ids):
    findbook = books.objects(ISBN=ids)
    findbook.delete()
    print('delete success')
    return 'deleted', 200
  return 'non match', 300


@app.route('/rating', methods=['GET'])
def rating():
  print('rating')
  ratinglist = books.objects.order_by('-rating')
  #   res = rating[:10]
  #   if len(res) >5:
  #     return res
  #   return 'rating wrong',300
  return jsonify(ratinglist)


@app.route('/upsearch', methods=['POST'])
def upsearch():
  file = request.files['file']
  # 处理文件
  image_bytes = file.read()
  # 将二进制数据转换为 base64 编码字符串
  image_base64 = base64.b64encode(image_bytes).decode('utf-8')
  # print(image_base64)
  img_data = base64.b64decode(image_base64)
  with open('../DBnet+crNN/DBNet/datasets/icdar/pred_img/test.jpg', 'wb') as f:
    f.write(img_data)
  print('-' * 25)
  print('成功保存前端上传图片，保存位置在dbnet/datasets/icdar/pred_img,开始dbnet文字位置检测')
  subprocess.run([sys.executable, '../DBnet+crNN/DBNet/pred.py'], capture_output=False)
  print('-' * 25)
  print('dbnet处理结束，文件中转在dbnet+crnn/dbnet/outputs_pred/img_result')
  print(os.getcwd())
  image = Image.open('../DBnet+crNN/DBNet/outputs_pred/img_result/test.jpg')
  img_bytes = BytesIO()
  image.save(img_bytes, format='JPEG')
  img_bytes = img_bytes.getvalue()
  response = make_response(img_bytes)
  response.headers.set('Content-Type', 'image/jpeg')
  response.headers.set('Access-Control-Allow-Origin', '*')
  return response


@app.route('/getcrnn', methods=['GET'])
def getcrnn():
  print('-' * 25)
  print('开始切分dbnet 处理结果')

  subprocess.run([sys.executable, '../DBnet+crNN/Tools/cropper.py'], capture_output=False)
  print('ok')
  time.sleep(5)
  # print(os.getcwd())
  print('-' * 25)
  print('开始crnn识别')
  # subprocess.run([sys.executable, '../DBnet+crNN/CRNNet/demo.py'], capture_output=False)
  p = subprocess.Popen([sys.executable, '../DBnet+crNN/CRNNet/demo.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  (stdoutput, erroutput) = p.communicate()
  print(stdoutput)
  id = str(stdoutput).index(']')
  # print(id,len(str(stdoutput)))
  reslist = eval(str(stdoutput)[2:(id - len(str(stdoutput)) + 1)])
  # # print(type(reslist))
  res_list = list(reversed(reslist))
  file = open('list.txt', 'w+')
  file.write(str(res_list))
  words = str(stdoutput)[3:-6]
  print(words)
  wordcloud = WordCloud(background_color="white", width=474, height=744, margin=2).generate(words)
  # print(result)
  wordcloud.to_file('test.jpg')
  time.sleep(3)
  image = Image.open('test.jpg')
  img_bytes = BytesIO()
  image.save(img_bytes, format='JPEG')
  img_bytes = img_bytes.getvalue()
  response = make_response(img_bytes)
  response.headers.set('Content-Type', 'image/jpeg')
  response.headers.set('Access-Control-Allow-Origin', '*')
  return response
  # return 200,'ok'


@app.route('/checkdb', methods=['GET'])
def checkdb():
  print('-' * 25)
  print('开始查询数据库')
  file = open('./list.txt')
  st = file.readline()
  book = books.objects(Book_Title__icontains=st[0]).first()
  if book:
    res = [str(book.Book_Title), str(book.ISBN), str(book.Book_Author)]
  else:
    res = ['get', 'no', 'result', 'from', 'database']
  words = str(res)[1:-1]
  wordcloud = WordCloud(background_color="white", width=474, height=744, margin=2).generate(words)
  # print(result)
  wordcloud.to_file('db.jpg')
  time.sleep(3)
  image = Image.open('db.jpg')
  img_bytes = BytesIO()
  image.save(img_bytes, format='JPEG')
  img_bytes = img_bytes.getvalue()
  response = make_response(img_bytes)
  response.headers.set('Content-Type', 'image/jpeg')
  response.headers.set('Access-Control-Allow-Origin', '*')
  return response


@app.route('/openai', methods=['GET'])
def aii():
  print('-' * 25)
  print('开始查询openai')
  file = open('./list.txt')
  st = file.readline()
  # print(st)
  prompt = 'guess a book with these words ' + st + ' and ignore the misspelling or incomplete words, and simply discribe this book in 30 words'
  openai.api_key = ""
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": prompt}
    ]
  )
  text = completion.choices[0].message["content"]
  res = {'code':200,'text':text}
  return jsonify(res)


app.run()
