# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet collects async building blocks that the other snippets use but
do not explain, plus a few everyday asyncio patterns.

Teaching focus
  - timeouts                 (asyncio.timeout, asyncio.wait_for)
  - cancellation             (task.cancel, CancelledError, cleanup)
  - bounded concurrency      (asyncio.Semaphore)
  - producer/consumer        (asyncio.Queue)
  - completion order         (asyncio.as_completed vs gather)

Also note 'README.md' for terms and references.

Ref. to
    https://docs.python.org/3/reference/datamodel.html#asynchronous-context-managers
    https://docs.python.org/3/reference/datamodel.html#asynchronous-iterators
    https://docs.python.org/3/library/asyncio-task.html
    https://docs.python.org/3/library/asyncio-queue.html
    https://docs.python.org/3/library/asyncio-sync.html
"""

import asyncio

from utils import print_function_header, reset_timing, set_current_task_name, ttprint

#
# timeouts: asyncio.timeout (3.11+) and asyncio.wait_for
#

async def slow_task(name, delay):
    """ a job that takes 'delay' seconds """
    ttprint(f" a| -   {name}: working for {delay}s")
    await asyncio.sleep(delay)
    ttprint(f" c| -   {name}: done")
    return f"{name}-result"


@reset_timing
@print_function_header
async def use_timeouts():
    """ bound how long we are willing to wait """

    ttprint(" 1| asyncio.timeout block, generous budget")
    try:
        async with asyncio.timeout(0.3):
            result = await slow_task("fast", 0.1)
        ttprint(f" 2| got {result!r}")
    except TimeoutError:
        ttprint(" 2| timed out (unexpected here)")

    ttprint(" 3| asyncio.timeout block, too tight")
    try:
        async with asyncio.timeout(0.1):
            await slow_task("slow", 0.5)     # gets cancelled at 0.1s
    except TimeoutError:
        ttprint(" 4| timed out -> the inner task was cancelled")

    ttprint(" 5| asyncio.wait_for, the single-coroutine form")
    try:
        await asyncio.wait_for(slow_task("slow", 0.5), timeout=0.1)
    except TimeoutError:
        ttprint(" 6| wait_for timed out")

    """
      - a timeout works by CANCELLING the wrapped operation when the deadline
        passes -> the same cancellation as in c_task_group, but triggered by
        the clock instead of a sibling's exception
      - asyncio.timeout(delay) wraps a whole block; asyncio.wait_for(coro,
        timeout) wraps exactly one awaitable
      - on expiry both raise TimeoutError (a builtin since 3.11)
    """


#
# cancellation from the outside: task.cancel() and CancelledError
#

async def cancellable_worker(name):
    """ a worker that cleans up properly when cancelled """
    try:
        ttprint(f" a| -   {name}: start, would run 'forever'")
        while True:
            await asyncio.sleep(0.1)         # cancellation can only hit at an await
            ttprint(f" .| -   {name}: still working")
    except asyncio.CancelledError:
        ttprint(f" b| -   {name}: cancelled -> cleaning up")
        raise                                # re-raise after cleanup (the contract)
    finally:
        ttprint(f" c| -   {name}: finally (runs on success, error and cancel)")


@reset_timing
@print_function_header
async def use_cancellation():
    """ cancel a running task from the outside and observe the effect """

    ttprint(" 1| create a task and let it run a bit")
    task = asyncio.create_task(cancellable_worker("W"))
    await asyncio.sleep(0.25)

    ttprint(" 2| request cancellation")
    task.cancel()                            # arranges CancelledError inside the task

    try:
        await task                           # await the now-cancelled task
    except asyncio.CancelledError:
        ttprint(" 3| confirmed: task ended via CancelledError")
    ttprint(f" 4| {task.cancelled()=}")

    """
      - task.cancel() raises CancelledError inside the coroutine at its next
        suspension point (await) - cooperative, never preemptive
      - c_task_group showed the loop cancelling siblings; here YOU cancel
      - catch CancelledError only to clean up, then re-raise it; swallowing it
        silently breaks the cancellation contract
      - 'finally' is the robust place for cleanup
      - asyncio.shield(coro) can protect a critical section from being
        cancelled - use sparingly
    """


#
# bounded concurrency: asyncio.Semaphore
#

async def fetch_with_limit(sem, name, delay):
    """ only N of these may be inside the 'async with sem' block at once """
    async with sem:
        ttprint(f" a| -   {name}: acquired a slot, fetching ({delay}s)")
        await asyncio.sleep(delay)
        ttprint(f" b| -   {name}: done, releasing the slot")
        return name


@reset_timing
@print_function_header
async def use_semaphore():
    """ limit how many coroutines run a section concurrently """

    ttprint(" 1| 6 jobs, but at most 2 may run at the same time")
    sem = asyncio.Semaphore(2)
    names = [f"job{i}" for i in range(6)]
    results = await asyncio.gather(
        *(fetch_with_limit(sem, name, 0.1) for name in names)
    )
    ttprint(f" 2| {results=}")

    """
      - the async answer to 'the thread pool is small' (b_async_blocking):
        a Semaphore caps concurrency without any threads
      - typical use: do not hammer an API/DB with 1000 simultaneous requests;
        allow N in flight and queue the rest
      - 6 jobs * 0.1s with limit 2 -> ~0.3s (three waves), not 0.1s
      - asyncio.Lock is essentially a Semaphore(1); asyncio.Event signals a
        one-shot 'go' to many waiters
    """


#
# producer / consumer: asyncio.Queue
#

async def producer(queue, n):
    """ produce n items, then a sentinel to signal 'no more' """
    for i in range(n):
        await asyncio.sleep(0.1)             # producing takes some time
        await queue.put(i)
        ttprint(f" a| - produced {i}")
    await queue.put(None)                    # sentinel
    ttprint(" b| - producer done (sent sentinel)")


async def consumer(queue):
    """ consume items until the sentinel arrives """
    while True:
        item = await queue.get()
        if item is None:                     # sentinel -> stop
            queue.task_done()
            break
        ttprint(f" c| -   consumed {item}")
        queue.task_done()
    ttprint(" d| - consumer done")


@reset_timing
@print_function_header
async def use_queue():
    """ decouple producer and consumer with an asyncio.Queue """

    ttprint(" 1| start producer + consumer in a task group")
    queue = asyncio.Queue()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer(queue, 3))
        tg.create_task(consumer(queue))
    ttprint(" 2| both finished")

    """
      - asyncio.Queue is the async sibling of queue.Queue from the threading
        units - but you 'await put/get' instead of blocking a thread
      - it decouples rates: producer and consumer each run at their own pace,
        the queue buffers between them
      - the 'None' sentinel is a simple shutdown signal; queue.join() together
        with task_done() is the alternative for 'wait until all processed'
    """


async def main():
    set_current_task_name("run")

    await use_timeouts()
    await use_cancellation()
    await use_semaphore()
    await use_queue()


if __name__ == "__main__":
    asyncio.run(main())
