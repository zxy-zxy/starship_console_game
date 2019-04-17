import asyncio


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


async def sleep(tics=1):
    for i in range(tics):
        await asyncio.sleep(0)


def read_animation_from_file(file_path):
    with open(file_path, 'r') as f:
        animation = f.read()
        return animation
