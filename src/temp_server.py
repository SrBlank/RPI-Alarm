import multiprocessing
import time
 
def func():
    while True:
        print("World")
 
# list of all processes, so that they can be killed afterwards
def trueLoop():
    while True:
        print("Hello")


process = multiprocessing.Process(target=func)
process2 = multiprocessing.Process(target=trueLoop)

process2.start()
process.start()
 
# kill all processes after 0.03s
time.sleep(2)

process.kill()
process2.terminate()
process.is_alive()
process.start()
#process.close()
#process = multiprocessing.Process(target=func)
#process.start()

print("stop")
