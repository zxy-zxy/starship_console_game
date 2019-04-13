import asyncio
import time


async def say_after(delay, what):
    current_time = time.strftime('%X')
    print(f'current time {current_time}')
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))
    current_time = time.strftime('%X')
    print(f'started at {current_time}')
    await task1
    await task2
    current_time = time.strftime('%X')
    print(f'finished at {current_time}')


asyncio.run(main())
