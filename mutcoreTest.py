# Method to test multicore using Pool object

from multiprocessing import Pool,Process,Queue
import requests


import os

def func(x,q):
    arr=[x]
    tillNow=0
    for i in range(100000):
        tillNow=i
        q.put(i)
        pass
    return arr


def funcWrite(q):
    i=0
    while(i<100000):
        res=requests.get("https://www.w3schools.com/python/ref_func_input.asp")
        print(res.headers.get('Date'))
        print(q.get())
        i+=1
    return res.headers


if __name__=="__main__":
    print("parent PID", os.getppid())
    
    # a message queue is used to communicate between processes, we can also use pipes   
    messageQueue=Queue()        # create a message queue

    # spawn a process using the process object
    proc1=Process(target=func, args=(10,messageQueue,))
    proc2=Process(target=funcWrite,args=(messageQueue,))
    proc1.start() # start the child process
    proc2.start()
    proc1.join() # wait until the process terminates
    proc2.join()
    

# creates a pool with os.cpu_list() workers. Where work will be distributed across nodes
def poolProcess():
    with Pool(5) as p:
        # The map function in python reutrns an iterator that applies the func to every
        # variable inside the second argument(an iterable object)
        # starmap does the same except that the function it takes has 
        # variable number of parameters
        results=p.map(func,[10,20,30,40,50,60,70,80])
        for res in results:
            print(res)
