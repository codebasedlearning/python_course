# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about awaitables.

Teaching focus
  - awaitables
  - __await__

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.

Awaitables
From https://docs.python.org/3/library/asyncio-task.html
- We say that an object is an awaitable object if it can be used in an await
  expression. Many asyncio APIs are designed to accept awaitables.
- There are three main types of awaitable objects: coroutines, Tasks, and Futures

Futures
- A Future is a special low-level awaitable object that represents an eventual
  result of an asynchronous operation. [...]
- Future objects in asyncio are needed to allow callback-based code to be used
  with async/await.
- Normally there is no need to create Future objects at the application level code.
"""

import asyncio

from utils import print_function_header, reset_timing, set_current_task_name, ttprint


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


async def main():
    set_current_task_name("run")
    await use_awaitable()

if __name__ == "__main__":
    asyncio.run(main())
