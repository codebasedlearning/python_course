# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet collects async building blocks that the other snippets use but
do not explain, plus a few everyday asyncio patterns.

Teaching focus
  - async context managers   (__aenter__/__aexit__, 'async with')
  - async iterators          (__aiter__/__anext__, 'async for')
  - async generators         ('async def' + 'yield', async comprehensions)

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


async def main():
    set_current_task_name("run")

    await use_awaitable()
    await use_async_context_manager()
    await use_async_iteration()


if __name__ == "__main__":
    asyncio.run(main())
