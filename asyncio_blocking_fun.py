# Example that converts a blocking function into an async coroutine that can be run with other coroutines

import time
import asyncio
import functools

def run_in_executor(f):
    # a decorator that turns a blocking function into an asynchronous function
    # from https://stackoverflow.com/questions/41063331/how-to-use-asyncio-with-existing-blocking-library
    @functools.wraps(f)
    def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, lambda: f(*args, **kwargs))

    return inner

@run_in_executor
def blocking():
    # time.sleep is a "blocking" synchronous function
    time.sleep(0.5)
    return "asd"

async def async_blocking():
    return await blocking()


async def nonblocking():
    # asyncio.sleep is a "nonblocking" asynchronous coroutine
    await asyncio.sleep(0.5)
    return "fgh"



# main and main2 produce identical results
async def main():
    tasks = [
        asyncio.create_task(async_blocking()), 
        asyncio.create_task(async_blocking()), 
        asyncio.create_task(nonblocking())
        ]
    [print(await _) for _ in asyncio.as_completed(tasks)]

async def main2():
    results = await asyncio.gather(
        async_blocking(),
        async_blocking(),
        nonblocking()
    )
    [print(_) for _ in results]


if __name__ == "__main__":
    asyncio.run(main2())
