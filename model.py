#coding=utf-8
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.flickr
collection = db.userInfo
urls = db.photoUrl

import json

def getQueue():# 返回作为文件存储的用户队列，广度优先搜索用
    with open('./queue.json', 'rb') as f:
        return json.load(f)

def dumpQueue(queue):# 将队列存至本地，异常时可恢复
    with open('./queue.json', 'wt') as f:
        json.dump(queue, f)

def saveUserInfo(data):
    if data is None:
        pass
    try:
        collection.insert_one(data)
    except Exception as err:
        print err

# def savePhotoInfo(data):
#     if data is None:
#         pass
#     photo = data['photo']
#     collection.insert_one({
#         "id": photo['id'],
#         "tags": photo['tags'],
#         "owner": photo["owner"],
#         "people": photo['people']
#     })

def savePhotoUrl(photos):# 查重交给文件写入来做，减少开销
    if not photos:
        return
    photos = map(lambda photo: {
        "id": photo['id'], 
        'image_url':"https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_q.jpg".format(
            farm=photo['farm'],
            server=photo['server'],
            id=photo['id'],
            secret=photo['secret']
        )
    }, photos)
    urls.insert_many(photos)