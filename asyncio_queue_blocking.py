import time
import asyncio

# Write a program that runs
# - task1 synchronously (a task1 running blocks other task1s)
# - task2 asynchronously
# but task1 doesn't block task2

start_time = time.time()

# task1
async def task1(q):
    await q.put("running")
    await asyncio.sleep(0.5)
    await q.get()
    q.task_done()
    return f"task1 finished after {time.time() - start_time:.2g}s"


# task2
async def task2():
    # asyncio.sleep is a "nonblocking" asynchronous function
    await asyncio.sleep(0.75)
    return f"task2 finished after {time.time() - start_time:.2g}s"


async def main():
    # Setting queue max size to 1 blocks other task1s from running while a task1 is running
    q = asyncio.Queue(maxsize=1)

    queued_tasks = [
        asyncio.create_task(task1(q)),
        asyncio.create_task(task1(q)),
        asyncio.create_task(task1(q)),
    ]
    nonqueued_tasks = [
        asyncio.create_task(task2()),
        asyncio.create_task(task2()),
        asyncio.create_task(task2()),
    ]

    [print(await _) for _ in asyncio.as_completed(queued_tasks + nonqueued_tasks)]

    await q.join()


if __name__ == "__main__":
    asyncio.run(main())