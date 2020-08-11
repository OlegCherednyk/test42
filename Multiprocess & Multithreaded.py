import multiprocessing
import os
import random
import string
import time
from enum import auto, Enum
from math import ceil
from multiprocessing.pool import ThreadPool
import requests


class timer:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        self.start = time.time()
        return None

    def __exit__(self, type, value, traceback):
        self.elapsed_time = (time.time() - self.start)
        print(self.message.format(self.elapsed_time))


def factorize_naive(n):
    """ A naive factorization method. Take integer 'n', return list of
        factors.
    """
    if n < 2:
        return []
    factors = []
    p = 2

    while True:
        if n == 1:
            return factors

        r = n % p
        if r == 0:
            factors.append(p)
            n = n / p
        elif p * p >= n:
            factors.append(n)
            return factors
        elif p > 2:
            # Advance in steps of 2 over odd numbers
            p += 2
        else:
            # If p == 2, get to 3
            p += 1
    assert False, "unreachable"


### Single-threaded version
result = {}
data = [n for n in range(100000)]

#with timer('Elapsed: {}s'):
#    for n in data:
#        result[n] = factorize_naive(n)

### Multiprocess version

workers = os.cpu_count()


def parting(xs, parts):
    part_len = ceil(len(xs)/parts)
    return [xs[part_len*k:part_len*(k+1)] for k in range(parts)]


def total_factorize_naive(d):
    for n in d:
        result[n] = factorize_naive(n)


def fetch_pic(num_pic):
    url = 'https://picsum.photos/400/600'
    path = '/home/oleg/PycharmProjects/test42/pics'
    for _ in range(num_pic):
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'{path}/{random_name}.jpg', 'wb') as f:
                f.write(response.content)
                print(f"Fetched pic [{os.getpid()}]: {f.name}")
        else:
            print(f"Error {response.status_code}")


class SpeedupType(Enum):
    MULTITHREADING = auto
    MULTIPROCESSING = auto


def check_multi(func, type_multi, data):

    workers = 1
    while True:

        start = time.time()

        if type_multi == SpeedupType.MULTIPROCESSING:
            if func == factorize_naive:
                with multiprocessing.Pool(workers) as pool:
                    results = pool.map(func, data)
                    for n, k in enumerate(results):
                        result[n] = k

            if func == fetch_pic:
                with multiprocessing.Pool(workers) as pool:
                    input_data = [data // workers for _ in range(workers)]
                    pool.map(fetch_pic, input_data)

        if type_multi == SpeedupType.MULTITHREADING:
            if func == total_factorize_naive:
                with ThreadPool(workers) as pool:
                    results = pool.map(func, data)
                    for n, k in enumerate(results):
                        result[n] = k

            if func == fetch_pic:
                with ThreadPool(workers) as pool:
                    input_data = [data // workers for _ in range(workers)]
                    pool.map(fetch_pic, input_data)

        elapsed_time = (time.time() - start)

        if workers == 1:
            pre_elapsed_time = elapsed_time

        if pre_elapsed_time < elapsed_time:
            print(f'{func} \noptimal number workers : {workers-1} \ntime : {pre_elapsed_time}')
            break

        pre_elapsed_time = elapsed_time
        workers += 1


check_multi(factorize_naive, SpeedupType.MULTIPROCESSING, data)
check_multi(factorize_naive, SpeedupType.MULTITHREADING, data)

# check_multi(fetch_pic, SpeedupType.MULTIPROCESSING, 20)
# check_multi(fetch_pic, SpeedupType.MULTITHREADING, 20)






