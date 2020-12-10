# マルチスレッド  

* [スレッド](#section1)
* [スレッドに渡す引数](#section2)
* [デーモンスレッド](#section3)
* [スレッドの一覧](#section4)
* [タイマー](#section5)
* [スレッドのロック](#section6)
* [セマフォ](#section7)
* [キュー](#section8)
* [イベント](#section9)
* [コンディション](#section10)
* [バリア](#section11)

# <a id="section1" href="#section1">スレッド</a>   
```python
import logging
import threading
import time

# thread の名前を取得
logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

def worker1():
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')

def worker2():
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')

# スレッドやマルチプロセスを使うときは↓を使う
if __name__ == '__main__':
    t1 = threading.Thread(target=worker1)
    t2 = threading.Thread(target=worker2)
    # スレッドスタート。並列で動かす。
    t1.start()
    t2.start()
    print('started')
```

実行結果  

```python  
Thread-1: start
Thread-2: start
started
Thread-1: end
Thread-2: end  
```  

# <a id="section2" href="#section2">スレッドに渡す引数</a>    

スレッドは引数を渡して処理を実行できる

```python  
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1():
    # thread の名前を取得
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')


def worker2(x, y=1):
    logging.debug('start')
    logging.debug(x)
    logging.debug(y)
    time.sleep(5)
    logging.debug('end')

if __name__ == '__main__':
    # nameでスレッド名を変えれる
    t1 = threading.Thread(name='rename worker1', target=worker1)
    # argsとkwargsは*を使うことができない
    t2 = threading.Thread(target=worker2, args=(100, ), kwargs={'y': 200})
    # スレッドスタート
    t1.start()
    t2.start()
    print('started')  
```

実行結果  

```python
rename worker1: start
Thread-1: start
started
Thread-1: 100
Thread-1: 200
rename worker1: end
Thread-1: end  
```  

# <a id="section3" href="#section3">デーモンスレッド</a>  

setDaemon関数で、デーモン化することができる。

```python
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

def worker1():
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')


def worker2():
    logging.debug('start')
    time.sleep(2)
    logging.debug('end')

if __name__ == '__main__':
    t1 = threading.Thread(target=worker1)
    # スレッドをデーモン化する
    t1.setDaemon(True)
    t2 = threading.Thread(target=worker2)
    t1.start()
    t2.start()
    print('started')
```  
実行結果を見ると、worker1をデーモン化したことで、worker2がsleep(2)ですぐ終わり、worker1を待たずにプログラムが強制終了する。  

```python
Thread-1: start
Thread-2: start
started
Thread-2: end
```  

デーモン化したスレッドの処理を待って、プログラムを終了させる場合は、join()を使う 

```python
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1():
    # thread の名前を取得
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')


def worker2():
    logging.debug('start')
    time.sleep(2)
    logging.debug('end')

if __name__ == '__main__':
    t1 = threading.Thread(target=worker1)
    # t1 スレッドをデーモン化する
    t1.setDaemon(True)
    t2 = threading.Thread(target=worker2)
    t1.start()
    t2.start()
    print('started')
    # t1 スレッドの完了を待つ
    t1.join()
    # デーモン化されていない場合は、書かなくてもよい
    t2.join()
```  

実行結果  

```
Thread-1: start
Thread-2: start
started
Thread-2: end
Thread-1: end
```  

# <a id="section4" href="#section4">スレッドの一覧</a>  

# <a id="section5" href="#section5">タイマー</a>  

Timer()で、スレッドを一定期間おいて実行できる  

```python
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1(x, y=1):
    # thread の名前を取得
    logging.debug('start')
    logging.debug(x)
    logging.debug(y)
    time.sleep(5)
    logging.debug('end')

if __name__ == '__main__':
    # スレッドを 3 秒後にスタート
    t = threading.Timer(3, worker1, args=(100,), kwargs={'y': 200})
    t.start()
```  

実行結果  

```python
Thread-1: start
Thread-1: 100
Thread-1: 200
Thread-1: end
```  

# <a id="section6" href="#section6">ロック</a>   

スレッドが同時に走ると不具合が生じるので、Lock()を使ってロックをする。  

```python  
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1(d):
    logging.debug('start')
    i = d['x']
    d['x'] = i + 1
    logging.debug(d)
    logging.debug('end')


def worker2(d):
    logging.debug('start')
    i = d['x']
    d['x'] = i + 1
    logging.debug(d)
    logging.debug('end')

if __name__ == '__main__':
    d = {'x': 0}
    t1 = threading.Thread(target=worker1, args=(d,))
    t2 = threading.Thread(target=worker2, args=(d,))
    t1.start()
    t2.start()
```  

問題なくxのカウントができている。  

```
Thread-1: start
Thread-1: {'x': 1}
Thread-1: end
Thread-2: start
Thread-2: {'x': 2}
Thread-2: end
```  

だが、スレッド内のカウントする処理の前に、何らかの処理が入る場合、正常にカウントされない  

```python
logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1(d):
    logging.debug('start')
    i = d['x']
    time.sleep(5)
    d['x'] = i + 1
    logging.debug(d)
    logging.debug('end')


def worker2(d):
    logging.debug('start')
    i = d['x']
    d['x'] = i + 1
    logging.debug(d)
    logging.debug('end')

if __name__ == '__main__':
    d = {'x': 0}
    t1 = threading.Thread(target=worker1, args=(d,))
    t2 = threading.Thread(target=worker2, args=(d,))
    t1.start()
    t2.start()
```  

正常にカウントされていないことがわかる  

```python
Thread-1: start
Thread-2: start
Thread-2: {'x': 1}
Thread-2: end
Thread-1: {'x': 1} # xがカウントされない
Thread-1: end
```  

d[x] は、スレッド間で共有されているが、スレッド1が「x = 1」の値を保持した状態で  
5 秒間停止してしまうので、その間にスレッド2が 「x = 1」の値を d[x] に格納する。  
その後、スレッド1によって「x = 1」 の値で上書きしてしまうので、カウントされない。  

これを防ぐためにロックをかける。  

```python
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1(d, lock):
    logging.debug('start')
    # ②ロック実行
    lock.acquire()
    i = d['x']
    time.sleep(5)
    d['x'] = i + 1
    logging.debug(d)
    # ③アンロック
    lock.release()
    logging.debug('end')


def worker2(d, lock):
    # withでも書ける
    with lock:
        logging.debug('start')
        # ②ロック実行(worker1の実行が完了するまで、処理を待つ)
        lock.acquire()
        i = d['x']
        d['x'] = i + 1
        logging.debug(d)
        # ③アンロック
        lock.release()
        logging.debug('end')

if __name__ == '__main__':
    d = {'x': 0}
    # ①ロックを作成
    lock = threading.Lock()
    t1 = threading.Thread(target=worker1, args=(d, lock))
    t2 = threading.Thread(target=worker2, args=(d, lock))
    t1.start()
    t2.start()
```

実行結果

```python
Thread-1: start
Thread-2: start
Thread-1: {'x': 1}
Thread-1: end
Thread-2: {'x': 2} # xがカウントされている
Thread-2: end
```

[RLock](https://docs.python.org/ja/3/library/threading.html#rlock-objects)というのもある  

# <a id="section7" href="#section7">セマフォ</a>  

Semaphore()を使うと、ロックをかけるスレッド数をコントロールできる。  

まずは、Lockを使った場合  

```python
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1(lock):
    with lock:
        logging.debug('start')
        time.sleep(5)
        logging.debug('end')

def worker2(lock):
    with lock:
        logging.debug('start')
        time.sleep(5)
        logging.debug('end')

def worker3(lock):
    with lock:
        logging.debug('start')
        time.sleep(5)
        logging.debug('end')


if __name__ == '__main__':
    lock = threading.RLock()
    t1 = threading.Thread(target=worker1, args=(lock,))
    t2 = threading.Thread(target=worker2, args=(lock,))
    t3 = threading.Thread(target=worker3, args=(lock,))
    t1.start()
    t2.start()
    t3.start()
```

スレッドが5秒間隔で実行されている。  

```python
Thread-1: start
Thread-1: end
Thread-2: start
Thread-2: end
Thread-3: start
Thread-3: end
```

セマフォを使った場合  

```python
import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(5)
        logging.debug('end')

def worker2(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(5)
        logging.debug('end')

def worker3(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(5)
        logging.debug('end')


if __name__ == '__main__':
    # セマフォを使用(引数にはスレッド数を指定)
    semaphore = threading.Semaphore(2)
    t1 = threading.Thread(target=worker1, args=(semaphore,))
    t2 = threading.Thread(target=worker2, args=(semaphore,))
    t3 = threading.Thread(target=worker3, args=(semaphore,))
    t1.start()
    t2.start()
    t3.start()
```  

セマフォを使った場合は、スレッド1とスレッド2が最初に実行されて、最後にスレッド3が走っていることが確認できる。  

```python
Thread-1: start
Thread-2: start
Thread-1: end
Thread-2: end
Thread-3: start
Thread-3: end
```

# <a id="section8" href="#section8">キュー</a>  



# <a id="section9" href="#section9">イベント</a>   

スレッドでイベントを発生させ、イベントをトリガーにしてほかのスレッドを実行させる。

以下は、スレッド3の処理が終わったら、スレッド1,2が実行される。

```python
import logging
import threading
import time
import queue

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1(event):
    # event.set が実行されるまで待機
    event.wait()
    logging.debug('start')
    time.sleep(3)
    logging.debug('end')

def worker2(event):
    # event.set が実行されるまで待機
    event.wait()
    logging.debug('start')
    time.sleep(3)
    logging.debug('end')

def worker3(event):
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')
    # event.waitにしたスレッドを実行
    event.set()

if __name__ == '__main__':
    # イベントを作成
    event = threading.Event()
    t1 = threading.Thread(target=worker1, args=(event,))
    t2 = threading.Thread(target=worker2, args=(event,))
    t3 = threading.Thread(target=worker3, args=(event,))
    t1.start()
    t2.start()
    t3.start()
```  

スレッド3の実行が完了後、スレッド1～2が実行されていることがわかる。  

```python
Thread-3: start
Thread-3: end
Thread-1: start
Thread-2: start
Thread-2: end
Thread-1: end
```

# <a id="section10" href="#section10">コンディション</a>  

スレッド3実行後、例えばスレッド1とスレッド2で、同時に同じファイルを書き込む場合など、一斉に動作させることが望ましくない場合は、  
コンディションを使う。  

コンディションはイベントと似たような機能だが、スレッドにロックがかけられる。  
  
以下は、スレッド3の実行が完了後、スレッド1を先にロックし、最後にスレッド2を動作させる。


```python
import logging
import threading
import time
import queue

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1(condition):
    # condition.notifyAll が実行されるまで待機
    # ロックを取得
    with condition:
        condition.wait()
        logging.debug('start')
        time.sleep(3)
        logging.debug('end')

def worker2(condition):
    # condition.notifyAll が実行されるまで待機
    # ロックを取得
    with condition:
        condition.wait()
        logging.debug('start')
        time.sleep(3)
        logging.debug('end')

def worker3(condition):
    with condition:
        logging.debug('start')
        time.sleep(5)
        logging.debug('end')
        # condition.waitにしたスレッドを実行
        condition.notifyAll()

if __name__ == '__main__':
    # コンディションを作成
    condition = threading.Condition()
    t1 = threading.Thread(target=worker1, args=(condition,))
    t2 = threading.Thread(target=worker2, args=(condition,))
    t3 = threading.Thread(target=worker3, args=(condition,))
    t1.start()
    t2.start()
    t3.start()
```

スレッド3→スレッド1→スレッド2の順番に処理が実行されている。  

```python
Thread-3: start
Thread-3: end
Thread-1: start
Thread-1: end
Thread-2: start
Thread-2: end
```  

# <a id="section11" href="#section11">バリア</a>  

指定した数のスレッドが立ち上がるまで、処理を待機させておくことができる。

```python
import logging
import threading
import time
import queue

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1(barrier):
    r = barrier.wait()
    logging.debug('num={}'.format(r))
    while True:
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')

def worker2(barrier):
    r = barrier.wait()
    logging.debug('num={}'.format(r))
    while True:
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')


if __name__ == '__main__':
    # バリアを作成(2個のスレッドが立ち上がるまで、処理を待機)
    barrier = threading.Barrier(2)
    t1 = threading.Thread(target=worker1, args=(barrier,))
    t2 = threading.Thread(target=worker2, args=(barrier,))
    t1.start()
    t2.start()

```  

スレッドが 2 個立ち上がった後、while ループが回り始めたことが確認できる。  

```python
Thread-2: num=1
Thread-2: start
Thread-1: num=0
Thread-1: start
Thread-1: end
Thread-1: start
Thread-2: end
Thread-2: start
Thread-2: end
```  

例えば、worker1がサーバー、worker2がクライアントで、両方が立ち上がっていないと、サービスを開始できないときなどに、実装する