import _thread,time

def test(x,y):
    for i in range(x,y):
        print(i)
        time.sleep(1)
        


_thread.start_new_thread(test, (1, 10))
#_thread.start_new_thread(test, (11, 20))