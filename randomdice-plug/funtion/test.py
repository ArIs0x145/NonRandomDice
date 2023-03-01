from multiprocessing import set_start_method, Queue, Process
import time


def count(q_a):
    a = 0
    print('啟動')
    while True:
        if q_a.empty():
            if q_a.get() is True:
                print('sssss')
            time.sleep(2)
            if q_a.get() is False:
                print('aaaa')


def count_n(q_a):
    while True:
        time.sleep(0.5)
        q_a.put(False)


def combine():
    c = []
    a = "1"
    b = [0, 1, 2, 3]
    c.append(int(a))
    c.append(b)
    print(c[1][0])
    print(c[1][1])
    # print(type(c))


if __name__ == "__main__":
    q_a = Queue()
    p_d = Process(target=count, args=(q_a,))
    p_d.start()
    p_b = Process(target=count_n, args=(q_a,))
    p_b.start()
