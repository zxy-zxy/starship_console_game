import asyncio

loop = asyncio.get_event_loop()


async def countdown_minutes_till_one_left(minutes):
    for minutes_left in range(minutes, 1, -1):
        print('{} minutes left'.format(minutes_left))
        await asyncio.sleep(60)
    print('one minute left')


async def countdown_seconds(secs):
    print('timer started')
    for secs_left in range(secs, 0, -1):
        print('{} seconds left'.format(secs_left))
        await asyncio.sleep(1)


async def run_five_minutes_timer():
    # await countdown_minutes_till_one_left(5)
    await countdown_seconds(5)

    print('Finish')


async def run_first_function():
    await run_five_minutes_timer()
    await run_five_minutes_timer()
    await run_five_minutes_timer()


async def run_second_function():
    loop.create_task(run_five_minutes_timer())
    loop.create_task(run_five_minutes_timer())
    loop.create_task(run_five_minutes_timer())


if __name__ == '__main__':
    # first function:
    # loop.create_task(run_first_function())
    # loop.run_forever()

    # second function:
    loop.create_task(run_second_function())
    loop.run_forever()
