# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet collects async building blocks that the other snippets use but
do not explain, plus a few everyday asyncio patterns.

Teaching focus
  - async context managers   (__aenter__/__aexit__, 'async with')
  - async iterators          (__aiter__/__anext__, 'async for')
  - async generators         ('async def' + 'yield', async comprehensions)
  - timeouts                 (asyncio.timeout, asyncio.wait_for)
  - cancellation             (task.cancel, CancelledError, cleanup)
  - bounded concurrency      (asyncio.Semaphore)
  - producer/consumer        (asyncio.Queue)
  - completion order         (asyncio.as_completed vs gather)

The protocols here are the async siblings of things you already know:
    __await__   ~  awaitable        (see study_awaitable.py)
    __aenter__  ~  context manager  ('with'  -> 'async with')
    __anext__   ~  iterator         ('for'   -> 'async for')

Also note 'README.md' for terms and references.

Ref. to
    https://docs.python.org/3/reference/datamodel.html#asynchronous-context-managers
    https://docs.python.org/3/reference/datamodel.html#asynchronous-iterators
    https://docs.python.org/3/library/asyncio-task.html
    https://docs.python.org/3/library/asyncio-queue.html
    https://docs.python.org/3/library/asyncio-sync.html
"""

import asyncio
from contextlib import asynccontextmanager

from utils import print_function_header, reset_timing, set_current_task_name, ttprint

#
# awaitable protocol
#

class WaitableMessage:
    def __init__(self, delay, message):
        self.delay = delay
        self.message = message

    def __await__(self):                    # this makes the object awaitable
        yield from asyncio.sleep(self.delay).__await__()
        return self.message


@reset_timing
@print_function_header
async def use_awaitable():
    """ use awaitable objects in an async function """

    ttprint(" 1| waiting for the message")
    msg = await WaitableMessage(0.2, "Hello after 0.2 seconds!")
    ttprint(f" 2| message: '{msg}'")


#
# async context managers: __aenter__ / __aexit__ and 'async with'
#

class DatabaseSession:
    """ an async context manager: __aenter__ and __aexit__ are coroutines """

    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        ttprint(f" a| - open session {self.name!r} (async setup)")
        await asyncio.sleep(0.1)            # e.g. open a connection -> may suspend
        return self                         # this is what 'as' binds

    async def __aexit__(self, exc_type, exc, tb):
        ttprint(f" d| - close session {self.name!r} (async teardown)")
        await asyncio.sleep(0.1)            # e.g. flush + close -> may suspend
        return False                        # False: do not suppress exceptions

    async def query(self, sql):
        ttprint(f" b| -   query {sql!r}")
        await asyncio.sleep(0.1)
        return 42


@asynccontextmanager
async def database_session(name):
    """ same protocol, written as a single async generator """
    ttprint(f" a| - open session {name!r} (via contextlib)")
    await asyncio.sleep(0.1)
    try:
        yield name                          # everything before 'yield' == __aenter__
    finally:
        ttprint(f" d| - close session {name!r}")   # everything after == __aexit__
        await asyncio.sleep(0.1)


@reset_timing
@print_function_header
async def use_async_context_manager():
    """ 'async with' drives __aenter__/__aexit__, both awaitable """

    ttprint(" 1| enter 'async with' (class based)")
    async with DatabaseSession("employees") as db:
        ttprint(" 2| inside the block")
        count = await db.query("select count(*)")
        ttprint(f" 3| {count=}")
    ttprint(" 4| left the block (session closed)")

    ttprint(" 5| same thing via contextlib.asynccontextmanager")
    async with database_session("freelancers") as name:
        ttprint(f" 6| inside session {name!r}")
    ttprint(" 7| left the block")

    """
      - 'async with' is to 'with' what 'await' is to a call: __aenter__ and
        __aexit__ are coroutines, so setup/teardown may themselves suspend
        (open a socket, flush a buffer, ...)
      - you have already used this: 'asyncio.TaskGroup()' and
        'httpx.AsyncClient()' are async context managers
      - contextlib.asynccontextmanager turns one async generator into the
        same protocol: code before 'yield' is the enter, code after is the exit
    """


#
# async iterators and async generators: __anext__ and 'async for'
#

class CountdownAiter:
    """ a hand-written async iterator """

    def __init__(self, start):
        self.current = start

    def __aiter__(self):                     # note: NOT async, just returns the iterator
        return self

    async def __anext__(self):               # awaited by 'async for' on every step
        if self.current == 0:
            raise StopAsyncIteration         # the async cousin of StopIteration
        await asyncio.sleep(0.1)             # e.g. wait for the next chunk to arrive
        self.current -= 1
        return self.current + 1


async def ticker(n, delay=0.1):
    """ an async generator: 'async def' + 'yield' -> consume with 'async for' """
    for i in range(n):
        await asyncio.sleep(delay)           # suspension point between items
        yield i                              # hand one item to the consumer


@reset_timing
@print_function_header
async def use_async_iteration():
    """ 'async for' over an async iterator and over an async generator """

    ttprint(" 1| async for over a hand-written __anext__")
    async for n in CountdownAiter(3):
        ttprint(f" a| -   countdown {n}")

    ttprint(" 2| async for over an async generator (async def + yield)")
    async for tick in ticker(3):
        ttprint(f" b| -   tick {tick}")

    ttprint(" 3| async comprehension (only valid inside a coroutine)")
    squares = [t * t async for t in ticker(3)]
    ttprint(f" 4| {squares=}")

    """
      - recall 'countdown321' (the generator in a_async_basics): same idea,
        but every step may suspend, so the consumer must use 'async for'
            generator : yield / for      ~   async generator : yield / async for
            __next__ / StopIteration     ~   __anext__ / StopAsyncIteration
      - an async generator is the natural way to *stream* results as they
        arrive (rows from a cursor, lines from a socket, events, ...)
    """


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


#
# completion order: asyncio.as_completed vs gather
#

@reset_timing
@print_function_header
async def use_as_completed():
    """ react to results in the order they FINISH, not the order submitted """

    ttprint(" 1| three jobs with different delays")
    coros = [slow_task("slow", 0.3), slow_task("mid", 0.2), slow_task("fast", 0.1)]

    ttprint(" 2| handle each as soon as it is ready")
    for finished in asyncio.as_completed(coros):
        result = await finished
        ttprint(f" b| - first-ready: {result!r}")

    """
      - asyncio.gather returns ALL results together, in submission order, and
        only after the slowest one finishes
      - asyncio.as_completed yields each awaitable AS it finishes, so the fast
        one is handled first (fast, mid, slow here)
      - use gather when you need the whole batch at once; use as_completed when
        you want to start processing whichever finishes first
    """


async def main():
    set_current_task_name("run")

    await use_awaitable()
    await use_async_context_manager()
    await use_async_iteration()
    await use_timeouts()
    await use_cancellation()
    await use_semaphore()
    await use_queue()
    await use_as_completed()


if __name__ == "__main__":
    asyncio.run(main())
