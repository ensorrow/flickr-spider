import service,model,utils
from time import time,sleep
import flickrapi
import threading

count = 0
t0 = time()
tlock = threading.Lock()

class saveUser(threading.Thread):
    def __init__(self, queue, name):
        threading.Thread.__init__(self,name=name)  
        self.queue = queue
    def run(self):
        print('%s is running...' % self.getName())
        while not utils.isEmpty(self.queue):
            tlock.acquire()
            userId = utils.dequeue(self.queue)
            tlock.release()
            handleUser(userId)
            # sleep(1)            
        print('%s is finished...' % self.getName())

def handleUser(userId):
    contactors = service.getContactInfo(userId)
    pubContactors= service.getPublicContactInfo(userId)
    if pubContactors is not None:
        for item in pubContactors:
            if item['nsid'] not in contactors:
                contactors.append(item)
    if contactors is not None:
        tlock.acquire()
        for contact in contactors:
            if contact['nsid'] not in queue:
                queue.append(contact['nsid'])
        tlock.release()
    contactors = utils.handleContact(contactors)
    groups = service.getUserGroup(userId)
    tags = service.getUserTagInfo(userId)
    photos = service.getFaviPhotos(userId)
    model.savePhotoUrl(photos)
    photos = map(lambda photo: photo['id'], photos)
    # print('saving photos to the database, %ds have passed...' % (time() - t0))
    document = {
        "nsid": userId,
        "groups": groups,
        "tags": tags,
        "photos": photos,
        "contactors": contactors
    }
    model.saveUserInfo(document)
    global count
    tlock.acquire()    
    count+=1
    tlock.release()
    print('saving the %dth user to the database, %ds have passed...' % (count, time() - t0))

if __name__ == '__main__':
    service.auth()
    print('get queue from the json file...')
    queue = model.getQueue()
    print('queue init successfully!')
    max_threads = 10
    for attempt in range(10):
        try:
            if not utils.isEmpty(queue):
                threads= []
                for i in range(max_threads):
                    thread = saveUser(queue, 'Thread'+str(i))
                    threads.append(thread)
                for i in range(max_threads):
                    threads[i].start()
                for i in range(max_threads):    
                    threads[i].join()
        except flickrapi.FlickrError as ferr:
            print(ferr)
            model.dumpQueue(queue)
            sleep(10)
            service.auth()
        except Exception as err:
            print(err)
            model.dumpQueue(queue)
            sleep(10)
        else:
            model.dumpQueue(queue)