# マルチプロセス  

* [参考動画](https://www.udemy.com/course/python-beginner/)  

***  

* [Process](#section1)
* [Pool](#section2)
* [プロセス間通信について](#section3)
* [Pipe](#section4)
* [Value, Array](#section5)
* [Manager](#section6)
* [BaseManager](#section7)
* [高水準のインターフェイス](#section8)

# <a id="section1" href="#section1">Process</a>   

```python
import logging
import time
import multiprocessing


logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')

def worker1(i):
    logging.debug('start')
    logging.debug(i)
    logging.debug('end')

def worker2(i):
    logging.debug('start')
    logging.debug(i)
    logging.debug('end')

# スレッドやマルチプロセスを使うときは↓を使う
if __name__ == '__main__':
    i = 3
    # targetに並列化したい処理を指定
    t1 = multiprocessing.Process(target=worker1, args=(i,))
    t2 = multiprocessing.Process(
        name='renamed worker2', target=worker2, args=(i,))
    t1.start()
    t2.start()
```  

実行結果  

```python
Process-1: start
renamed worker2: start
Process-1: 3
renamed worker2: 3
Process-1: end
renamed worker2: end
```  


# <a id="section2" href="#section2">Pool</a>    
Pool()の引数にプロセス数を指定できる  

```python
import logging
import time
import multiprocessing


logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')

def worker1(i):
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')
    return i

# スレッドやマルチプロセスを使うときは↓を使う
if __name__ == '__main__':
    # Pool()の引数はプロセスの数を指定できる。
    with multiprocessing.Pool(5) as p:
        # apply_asyncで非同期で並列化
        p1 = p.apply_async(worker1, (100, ))
        p2 = p.apply_async(worker1, (100, ))
        logging.debug('executed')
        logging.debug(p1.get())
        logging.debug(p2.get())
```  

実行結果  

```python
MainProcess: executed
SpawnPoolWorker-1: start
SpawnPoolWorker-2: start
SpawnPoolWorker-1: end
MainProcess: 100
SpawnPoolWorker-2: end
MainProcess: 100
```  

multiprocessing.Pool(1)のように、Pool()の引数を1にして上記のコードを実行すると次のようになる。  

```python
MainProcess: executed
SpawnPoolWorker-1: start
SpawnPoolWorker-1: end
SpawnPoolWorker-1: start
MainProcess: 100
SpawnPoolWorker-1: end
MainProcess: 100
```  

同じプロセスが2回動いているのがわかる。  
  
また、get()の引数にtimeoutを指定すると、時間内に処理が戻ってこないと、エラーを返す。

```python
import logging
import time
import multiprocessing


logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')

def worker1(i):
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')
    return i

# スレッドやマルチプロセスを使うときは↓を使う
if __name__ == '__main__':
    # Pool()の引数はプロセスの数を指定できる。
    with multiprocessing.Pool(5) as p:
        p1 = p.apply_async(worker1, (100, ))
        p2 = p.apply_async(worker1, (100, ))
        logging.debug('executed')
        # timeoutで1秒待っても処理が戻ってこない場合は、エラーを返す
        logging.debug(p1.get(timeout=1))
        logging.debug(p2.get())

```  

1秒以内に戻ってこないため、TimeoutErrorが出ているのがわかる。  

```python
MainProcess: executed
SpawnPoolWorker-1: start
SpawnPoolWorker-2: start
Traceback (most recent call last):
  File ".\sample.py", line 22, in <module>
    logging.debug(p1.get(timeout=1))
  File "C:\Users\yanag\AppData\Local\Programs\Python\Python36\lib\multiprocessing\pool.py", line 640, in get
    raise TimeoutError
multiprocessing.context.TimeoutError
```  

次に、apply()を使うとブロックすることができる。

```python
import logging
import time
import multiprocessing


logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')

def worker1(i):
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')
    return i

# スレッドやマルチプロセスを使うときは↓を使う
if __name__ == '__main__':
    # Pool()の引数はプロセスの数を指定できる。
    with multiprocessing.Pool(5) as p:
        # apply()は、並列化ではなくブロックするから、worker1がおわってから「executed apply」が出力する。
        logging.debug(p.apply(worker1, (200, )))
        logging.debug('executed apply')
        p1 = p.apply_async(worker1, (100, ))
        p2 = p.apply_async(worker1, (100, ))
        logging.debug('executed')
        # timeoutで1秒待っても処理が戻ってこない場合は、エラーを返す
        logging.debug(p1.get())
        logging.debug(p2.get())
```  

worker1がおわってから「executed apply」が出力していることがわかる。  
一番初めに、ブロックしたいときに使える。

```python
SpawnPoolWorker-1: start
SpawnPoolWorker-1: end
MainProcess: 200
MainProcess: executed apply
MainProcess: executed
SpawnPoolWorker-2: start
SpawnPoolWorker-3: start
SpawnPoolWorker-2: end
MainProcess: 100
SpawnPoolWorker-3: end
MainProcess: 100
```  

上記では、apply_asyncをわざわざ二行書いていたが、map()を使えば、一行になる。  

```python
import logging
import time
import multiprocessing


logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')

def worker1(i):
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')
    return i * 2

# スレッドやマルチプロセスを使うときは↓を使う
if __name__ == '__main__':
    # Pool()の引数はプロセスの数を指定できる。
    with multiprocessing.Pool(5) as p:
        # mapの引数に、リストで渡す。
        r = p.map(worker1, [100, 200])
        logging.debug('executed')
        logging.debug(r)
        # p1 = p.apply_async(worker1, (100, ))
        # p2 = p.apply_async(worker1, (100, ))
        # logging.debug(p1.get())
        # logging.debug(p2.get())
```  

map()でブロックするので、プロセス処理が終了してからexecutedのメッセージが出力されているのがわかる。  

```python
SpawnPoolWorker-1: start
SpawnPoolWorker-2: start
SpawnPoolWorker-2: end
SpawnPoolWorker-1: end
MainProcess: executed
MainProcess: [200, 400]
```  

map()でプロセス処理をが終了するのを待たずに、次の行にいく方法もある。  

```python
import logging
import time
import multiprocessing


logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')

def worker1(i):
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')
    return i * 2

# スレッドやマルチプロセスを使うときは↓を使う
if __name__ == '__main__':
    # Pool()の引数はプロセスの数を指定できる。
    with multiprocessing.Pool(5) as p:
        # map_asyncで処理を待たずに、次の行へ
        r = p.map_async(worker1, [100, 200])
        logging.debug('executed')
        logging.debug(r.get())
```  

プロセス処理を待たないので、一番初めにexecutedメッセージが出力されてるのがわかる。  

```python
MainProcess: executed
SpawnPoolWorker-1: start
SpawnPoolWorker-2: start
SpawnPoolWorker-2: end
SpawnPoolWorker-1: end
MainProcess: [200, 400]
```  

map()をimap()にすることで、イテレーターにすることもできる。その場合は、ループで回さないと、プロセスが実行されない。  


# <a id="section3" href="#section3">プロセス間通信について</a>    

マルチスレッドは共有メモリで、マルチプロセスは共有メモリではなく、それぞれ独自であるため、挙動が異なる。  
  
まずは、マルチスレッドの使った場合を見てみる。

```python
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1(d, lock):
    with lock:
        i = d['x']
        d['x'] = i + 1
        logging.debug(d)

def worker2(d, lock):
    with lock:
        i = d['x']
        d['x'] = i + 1
        logging.debug(d)


if __name__ == '__main__':
    d = {'x': 0}
    lock = threading.Lock()
    t1 = threading.Thread(target=worker1, args=(d, lock))
    t2 = threading.Thread(target=worker2, args=(d, lock))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    logging.debug(d)
```  

共有メモリであるため、同じ辞書を参照しているのがわかる。

```python
Thread-1: {'x': 1}
Thread-2: {'x': 2}
MainThread: {'x': 2}
```  

では、マルチプロセスで書くとどうなるか。  

```python
import logging
import multiprocessing
import time

logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')


def worker1(d, lock):
    with lock:
        i = d['x']
        d['x'] = i + 1
        logging.debug(d)

def worker2(d, lock):
    with lock:
        i = d['x']
        d['x'] = i + 1
        logging.debug(d)


if __name__ == '__main__':
    d = {'x': 0}
    lock = multiprocessing.Lock()
    t1 = multiprocessing.Process(target=worker1, args=(d, lock))
    t2 = multiprocessing.Process(target=worker2, args=(d, lock))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    logging.debug(d)
```  

マルチプロセスは、共有メモリではなく、独自でもっているため辞書が共有されていないことがわかる。  

```python
Process-1: {'x': 1}
Process-2: {'x': 1}
MainProcess: {'x': 0}
```  


# <a id="section4" href="#section4">Pipe</a>    

マルチプロセスで共有メモリとして扱える方法としてPipeがある。

```python
import logging
import multiprocessing
import time

logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')


def f(conn):
    # sendで文字列などを渡してやる
    conn.send(['test'])
    time.sleep(5)
    # 処理が終了
    conn.close()


if __name__ == '__main__':
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=f, args=(parent_conn, ))
    p.start()
    # parent_connプロセスから、sendで値を受け取る
    logging.debug(child_conn.recv())
```

parent_connとchild_connの異なるプロセスで、値を共有(受けっとっている)ことがわかる。  

```python
MainProcess: ['test']
```  

# <a id="section5" href="#section5">Value, Array</a>    

マルチプロセスで共有メモリとして扱える方法として、ほかにはValueとArrayがある。

```python
import logging
import multiprocessing
import time

logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')


def f(num, arr):
    logging.debug(num)
    # Valueは、valueで中身の値にアクセス
    num.value += 1.0
    logging.debug(arr)
    # Arrayは、indexを指定して値をアクセス
    for i in range(len(arr)):
        arr[i] *= 2


if __name__ == '__main__':
    num = multiprocessing.Value('f', 0.0)
    arr = multiprocessing.Array('i', [1, 2, 3, 4, 5])

    p1 = multiprocessing.Process(target=f, args=(num, arr))
    p2 = multiprocessing.Process(target=f, args=(num, arr))
    p1.start()
    p2.start()
    # プロセスが終了するまでjoin()で待つ
    p1.join()
    p2.join()
    logging.debug(num.value)
    logging.debug(arr[:])
```  

実行結果

```python
Process-1: <Synchronized wrapper for c_float(0.0)>
Process-1: <SynchronizedArray wrapper for <multiprocessing.sharedctypes.c_long_Array_5 object at 0x0000025AF1B802C8>>
Process-2: <Synchronized wrapper for c_float(1.0)>
Process-2: <SynchronizedArray wrapper for <multiprocessing.sharedctypes.c_long_Array_5 object at 0x0000012E406702C8>>
MainProcess: 2.0
MainProcess: [4, 8, 12, 16, 20]
```  

# <a id="section6" href="#section6">Manager</a>     

Managerもマルチプロセスで共有メモリとして扱えるが、速度が若干遅い。  

```python:mult
import logging
import multiprocessing
import time

logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')


def worker1(l, d, n):
    l.reverse()
    d['x'] += 1
    n.y += 1


if __name__ == '__main__':
    # Managerはサーバープロセスを管理するもの。
    with multiprocessing.Manager() as manager:
        l = manager.list()
        d = manager.dict()
        n = manager.Namespace()

        l.append(1)
        l.append(2)
        l.append(3)
        d['x'] = 0
        n.y = 0

        p1 = multiprocessing.Process(target=worker1, args=(l, d, n))
        p2 = multiprocessing.Process(target=worker1, args=(l, d, n))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

        logging.debug(l)
        logging.debug(d)
        logging.debug(n)
```  

実行結果 (リストのところは、プロセスでreverseを2回行っているため、もとに戻っている。)

```python
MainProcess: [1, 2, 3]
MainProcess: {'x': 2}
MainProcess: Namespace(y=2)
```  



# <a id="section7" href="#section7">BaseManager</a>    


# <a id="section8" href="#section8">高水準のインターフェイス</a>    


  





