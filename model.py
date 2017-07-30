from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.flickr
collection = db.photoInfo
urls = db.photoUrl

def getPepples():# 返回长度为50未被访问过的用户队列，广度优先搜索用
    return collection.find({'$exists': {'used': False}}).limit(50)['nsid']

def savePhotoInfo(data):
    if data is None:
        pass
    photo = data['photo']
    collection.insert_one({
        "id": photo['id'],
        "tags": photo['tags'],
        "owner": photo["owner"],
        "people": photo['people']
    })

def savePhotoUrl(photo):
    if photo is None:
        pass
    image_url = "https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_q.jpg".format(
        farm=photo['farm'],
        server=photo['server'],
        id=photo['id'],
        secret=photo['secret']
    )
    urls.insert_one({
        "id": photo['id'],
        "url": image_url
    })