import threading, Queue
import requests
import os
from pymongo import MongoClient
from time import time,sleep
import socket
socket.setdefaulttimeout(30)

client = MongoClient('localhost', 27017)
db = client.flickr
urls = db.photoUrl
t0 = time()
count = 0
max_retry = 10

class download(threading.Thread):  
    def __init__(self,que,name):  
        threading.Thread.__init__(self,name=name)  
        self.que=que  
    def run(self):
        print('%s is running...' % self.getName())
        while not self.que.empty():  
            item = que.get()
            savePhotoFile(item['url'], item['id'])
        print('%s finished.' % self.getName())

def savePhotoFile(url, id):
    try:
        savePath = os.path.normcase("D:\\flickrImages\\" + id + ".jpg")
        rs = requests.get(url)
        with open(savePath, "wb") as img:
            img.write(rs.content)
    except IOError as err:
        print("IO Error")
        print(err)
    except Exception as unexpected:
        print unexpected
    else:
        global count
        count+=1
        urls.find_one_and_update({"id": id}, {'$set':{'saved': 1}})
        print('%d photos saved to disk, %ds used...' % (count, time()-t0))

while True:
    photos = urls.find({"saved": {"$exists": False}}).limit(400)
    if not photos:
        print('no more photos to save!')
        if max_retry>0:
            max_retry-=1
            sleep(10)
            continue
        else:
            break
    max_retry = 10
    que = Queue.Queue(maxsize = 0)
    max_thread = 10
    threads = []
    for photo in photos:
        que.put(photo)
    for i in range(max_thread):
        thread = download(que, 'Thread'+str(i))
        threads.append(thread)
    for i in range(max_thread):
        threads[i].start()
    for i in range(max_thread):    
        threads[i].join()
    sleep(2)