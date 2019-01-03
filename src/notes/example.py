import time
from threading import Thread
import asyncio

# from unsync import unsync  # must comment out if using just asyncio
import trio


def timed_sleep(sec):
    time.sleep(sec)


async def async_sleep(sec):
    await asyncio.sleep(sec)


async def trio_sleep(sec):
    await trio.sleep(sec)


# @unsync()
# async def unsync_sleep(sec):
#     await asyncio.sleep(sec)
#
#
# @unsync()
# def unsync_sleep2(sec):
#     time.sleep(sec)


def sync():
    # Make http request #1
    timed_sleep(8)
    # Process http response #1
    timed_sleep(5)
    # Make http request #2
    timed_sleep(8)
    # Process http response #2
    timed_sleep(2)
    return 'COMPLETE'


def threaded():
    threads = [
        # Make http request #1
        Thread(target=timed_sleep, args=(8,), daemon=True),
        # Process http response #1
        Thread(target=timed_sleep, args=(5,), daemon=True),
        # Make http request #2
        Thread(target=timed_sleep, args=(8,), daemon=True),
        # Process http response #2
        Thread(target=timed_sleep, args=(2,), daemon=True),
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]
    return 'COMPLETE'


def asynced():
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(async_sleep(8)),
        loop.create_task(async_sleep(5)),
        loop.create_task(async_sleep(8)),
        loop.create_task(async_sleep(2)),
    ]
    final_task = asyncio.gather(*tasks)
    loop.run_until_complete(final_task)
    return 'COMPLETE'


# def unsynced():
#     tasks = [
#         unsync_sleep(8),
#         unsync_sleep(5),
#         unsync_sleep2(8),
#         unsync_sleep2(2),
#     ]
#     [t.result() for t in tasks]
#     return 'COMPLETE'


async def trioed():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(trio_sleep, 8, name='Http request 1')
        nursery.start_soon(trio_sleep, 5, name='Http process response 1')
        nursery.start_soon(trio_sleep, 8, name='Http request 2')
        nursery.start_soon(trio_sleep, 2, name='Http process response 2')
    return 'COMPLETE'


if __name__ == '__main__':
    start = time.time()

    # result = sync()            # 23 sec
    # result = threaded()        # 8 sec
    result = asynced()         # 8 sec
    # result = unsynced()        # 8 sec
    # result = trio.run(trioed)  # 8 sec

    print(result)
    print('Time taken in seconds -', time.time() - start)
