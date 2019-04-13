import asyncio
import time


async def sleep(tics=1):
    for i in range(tics):
        await asyncio.sleep(0)


async def blink(symbol='*'):
    while True:
        print(symbol + '1')
        await sleep(60)

        print(symbol + '2')
        await sleep(30)

        print(symbol + '3')
        await sleep(30)

        print(symbol + '4')
        await sleep(60)


def initialize_coroutines():
    star_symbols = ['+', '*', '.', ':']

    coroutines = [
        blink(star) for star in star_symbols]

    return coroutines


def main():
    coroutines = initialize_coroutines()

    while coroutines:
        try:
            for coroutine in coroutines:
                coroutine.send(None)

            time.sleep(0.1)

        except StopIteration:
            coroutines.remove(coroutine)


if __name__ == '__main__':
    main()
