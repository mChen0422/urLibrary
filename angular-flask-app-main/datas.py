import csv
import mongoengine as me
import time


def get_book_data():
  book_dict = {}
  isbn_list = []
  with open('books.csv') as f:
    files = csv.reader(f)
  #   print(next(files))
    keys = next(files)
    key_list_raw = [x for x in keys if x !='']
    temp = key_list_raw[0]
    keys = list(temp.split(';'))
    data_len = len(keys)
    print(keys,data_len)

    for row in files:
      try:
    #     time.sleep(10)
        row_data = [x for x in row if x !='']
        if len(row_data) ==1:
          datas=list(str(row_data[0]).split(';'))
        else:
          temp = ''
          for j in row_data:
            temp += j
          datas = list(str(temp).split(';'))
    #     print(datas[2])
    #     time.sleep(5)
        temp_dict = {}
        temp_dict['ISBN'] = datas[0]
        isbn_list.append(datas[0])
        temp_dict['Book_Title'] = datas[1].replace('"','')
        temp_dict['Book_Author'] = datas[2].replace('"','')
        temp_dict['Year_Of_Publication'] = datas[3].replace('"','')
        temp_dict['Publisher'] = datas[4].replace('"','')
        temp_dict['Image_URL_S'] = datas[5].replace('"','')
        temp_dict['Image_URL_M'] = datas[6].replace('"','')
        temp_dict['Image_URL_L'] = datas[7].replace('"','')
        temp_dict['rating'] = 0
        temp_dict['count'] = 0
        temp_dict['score'] = 0
        book_dict['%s'%datas[0]] = temp_dict
      except:
        print('!!!!!!!!!!!!')
        print(row)
        time.sleep(20)

#   print(book_dict)
  return book_dict,isbn_list

# get_book_data()

def get_book_rating():
  with open('ratings2.csv', encoding='utf-8', errors='ignore') as f:
    files = csv.reader(f)
    #   print(next(files))
    keys = next(files)
    key_list_raw = [x for x in keys if x !='']
    temp = key_list_raw[0]
    keys = list(temp.split(';'))
    data_len = len(keys)
    print(keys,data_len)
    book_dict,isbn_list = get_book_data()
    for row in files:
      datas=list(str(row[0]).split(';'))
      try:
        isbns = datas[1].replace('"','')
      except:
        isbns = 0
      try:
        ratings = int(str(datas[2])[1])
      except:
        ratings = 0
#       print(isbns)
      if isbns in isbn_list:
#          print(type(isbns))
         book_dict['%s'%isbns]['count']+=1
         book_dict['%s'%isbns]['score']+=ratings
#          print(isbns,book_dict['%s'%isbns]['count'],book_dict['%s'%isbns]['score'])

    return book_dict


def count_rating():
  book_dict = get_book_rating()
  for i in book_dict:
      count = book_dict[i]['count']
      score = book_dict[i]['score']
      book_dict[i]['rating'] = round(score/count,1)
#       print(book_dict[i])
#       time.sleep(5)
  return book_dict

final_book_data = count_rating()
me.connect(
       db="bookdata",
       host='localhost',
       port=27017
   )

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

book_data = [ final_book_data[i]for i in final_book_data ]

data = [books(**data) for data in book_data]
# print(data)
books.objects.insert(data,load_bulk=False)
