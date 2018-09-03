import threading
import time

sem = threading.Semaphore(4)


def gothread():
    with  sem:
        for i in range(8):
            print(threading.current_thread().name, i)
            time.sleep(1)


for i in range(5):
    threading.Thread(target=gothread).start()
