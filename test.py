import time,threading
from Queue import Queue

class TaskThread(threading.Thread):
    def __init__(self,name,que):
        threading.Thread.__init__(self,name=name)
        self.que = que
    def run(self):
        print('thread %s is running...' % self.getName())

        while not self.que.empty():
            print('thread %s >>> %d' % (self.getName(), self.que.get()))
            # time.sleep(1)
 
        print('thread %s finished.' % self.getName())

queue = Queue(maxsize=0)
for i in range(20):
    queue.put(i)

taskthread = TaskThread('TaskThread1', queue)
taskthread2 = TaskThread('TaskThread2', queue)
taskthread.start()
taskthread2.start()
taskthread.join()
taskthread2.join()