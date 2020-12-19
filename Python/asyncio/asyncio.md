# asyncio(非同期)  

# asyncio.Lock  

```python
import asyncio

# loopのオブジェクト作成
loop = asyncio.get_event_loop()


async def worker1(lock):
    print('worker1 start')
    with await lock:
        print('worker1 got lock')
        await asyncio.sleep(3)
    print('worker1 end')


# asyncioの古い書き方
@asyncio.coroutine
def worker2(lock):
    print('worker2 start')
    with (yield from lock):
        print('worker2 got lock')
        yield from asyncio.sleep(3)
    print('worker2 end')


lock = asyncio.Lock()
loop.run_until_complete(asyncio.wait([
    worker1(lock), worker2(lock)
]))
loop.close()
```

worker1とworker2が同時にスタートして、worker2が先にロックしたので、worker2が終わった後に、worker1がロックしていることがわかる。

```python
worker2 start
worker2 got lock
worker1 start
worker2 end
worker1 got lock
worker1 end
```  

# asyncio.Event  

```python
import asyncio

# loopのオブジェクト作成
loop = asyncio.get_event_loop()


async def worker1(event):
    print('worker1 start')
    await event.wait():
    print('worker1 got event')
    await asyncio.sleep(3)
    print('worker1 end')


async def worker2(event):
    print('worker2 start')
    await event.wait():
    print('worker2 got event')
    await asyncio.sleep(3)
    print('worker2 end')


async def worker3(event):
    print('worker3 start')
    await asyncio.sleep(3)
    print('worker3 end')
    event.set()


event = asyncio.Event()
loop.run_until_complete(asyncio.wait([
    worker1(event), worker2(event), worker3(event)
]))
loop.close()

```  

worker3が終了した後に、worker2とworker1がイベントで動いているのがわかる。  

```python
worker2 start
worker3 start
worker1 start
worker3 end
worker2 got event
worker1 got event
worker2 end
worker1 end
```  


# Condition  

```python
import asyncio
loop = asyncio.get_event_loop()
 
async def worker1(condition):
    async with condition:
        await condition.wait()
        print('asyncio native start1')
        await asyncio.sleep(3)
        print('asyncio native stop1')
 
async def worker2(condition):
    async with condition:
        await condition.wait()
        print('asyncio native start2')
        await asyncio.sleep(3)
        print('asyncio native stop2')
 
async def worker3(condition):
    await asyncio.sleep(1)
    async with condition:
        print('asyncio native start3')
        await asyncio.sleep(3)
        print('asyncio native stop3')
        condition.notify_all()
 
 
if __name__ == '__main__':
    condition = asyncio.Condition()
    loop.run_until_complete(asyncio.wait([
        worker1(condition), worker2(condition), worker3(condition)
    ]))
    loop.close()

```

実行結果

```python
asyncio native start3
asyncio native stop3
asyncio native start1
asyncio native stop1
asyncio native start2
asyncio native stop2
```  


# asyncio.Semaphore  

```python
import asyncio

# loopのオブジェクト作成
loop = asyncio.get_event_loop()


async def worker1(semaphore):
    with await semaphore:
        print('worker1 start')
        await asyncio.sleep(3)
        print('worker1 end')


async def worker2(semaphore):
    with await semaphore:
        print('worker2 start')
        await asyncio.sleep(3)
        print('worker2 end')


# Semaphore()の引数により、いくつのタスクが実行できるかが変わる
semaphore = asyncio.Semaphore(2)
loop.run_until_complete(asyncio.wait([
    worker1(semaphore), worker2(semaphore)
]))
loop.close()

```

実行結果  

```python
worker2 start
worker1 start
worker2 end
worker1 end
```


# asyncio.Queue  

別々のタスクでデータを共有  

```python
import asyncio

# loopのオブジェクト作成
loop = asyncio.get_event_loop()


async def worker1(queue):
    print('worker1 start')
    await queue.put(100)
    print('worker1 end')


async def worker2(queue):
    print('worker2 start')
    x = await queue.get()
    print(x)
    print('worker2 end')


queue = asyncio.Queue(2)
loop.run_until_complete(asyncio.wait([
    worker1(queue), worker2(queue)
]))
loop.close()
```  

worker1でputした値がworker2でgetできているのがわかる  

```python
worker2 start
worker1 start
worker1 end
100
worker2 end
```


# asyncio.Future

