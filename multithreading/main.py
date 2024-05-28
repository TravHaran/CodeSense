import threading
import time

'''
multithreading python demo
'''

def multithreading_demo():
    def worker(text):
        counter = 0
        while True:
            time.sleep(1)
            counter += 1
            print(f"{text}: {counter}\n")
    # deamon if something else is running keep thread live, else terminate it
    t1 = threading.Thread(target=worker, daemon=True, args=("ABC", ))
    t2 = threading.Thread(target=worker, daemon=False, args=("XYZ", ))

    t1.start()
    t2.start()


    t1.join()
    t2.join()


'''
queue demo
'''

from queue import Queue

def queue_demo():
    def do_stuff(q):
        while not q.empty():
            print(q.get())
            q.task_done()

    q = Queue(maxsize=0)

    for x in range(20):
        q.put(x)

    do_stuff(q)


'''
multithreading & queue (Batch Processing) demo
'''

def multithreading_queue_demo():
    def do_stuff(q):
        while True:
            print(q.get())
            q.task_done()
    
    # set 10 worker threads running
    q = Queue(maxsize=0)
    num_threads = 10
    
    for i in range(num_threads):
        worker = threading.Thread(target=do_stuff, daemon=True, args=(q, ))
        worker.start()
    
    for y in range(10):
        for x in range(100):
            q.put(x)
        q.join() 
        print("Batch " + str(y) + "Done")
        
    
    # waits until the queue is empty and all threads are done working
    # which it knows because task_done() was called on every element of the queue
    # this way if we're running a program in batches, you would use q.join()
    # to wait for the batch to finish and then write the resutls to a file, 
    # and then throw more tasks into the queue

multithreading_queue_demo()
    