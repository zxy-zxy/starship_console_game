import itertools
import asyncio
import sys

loop = asyncio.get_event_loop()


def clear_line():
    sys.stdout.write('\r')
    sys.stdout.write('\033[K')


async def spin(msg):
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        sys.stdout.write(status)
        await asyncio.sleep(0.3)
        clear_line()


async def slow_function():
    await asyncio.sleep(10)
    return 42


async def supervisor():
    spinner = spin('thihking')
    loop.create_task(spinner)
    result = await slow_function()
    clear_line()
    return result


def main():
    result = loop.run_until_complete(supervisor())
    print(result, flush=True)


if __name__ == '__main__':
    main()
