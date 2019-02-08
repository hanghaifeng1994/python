from concurrent.futures import ThreadPoolExecutor
import time

def to():
    p = 0
    for i in [1,2,3,4,5,6]:
        p += i
    return p

executor = ThreadPoolExecutor(max_workers=2)



for j in range(2):
    task = executor.submit(to)

print(task.result())
