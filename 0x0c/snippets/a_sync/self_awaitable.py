# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about awaitables.

Teaching focus
  - awaitables
  - __await__

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import time
import asyncio
import threading

from thread_helper import dt

"""
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

class WaitableMessage:
    def __init__(self, delay, message):
        self.delay = delay
        self.message = message

    def __await__(self):                    # This makes the object awaitable
        yield from asyncio.sleep(self.delay).__await__()
        return self.message


async def use_awaitable():
    """ use awaitable objects in an async function """
    print("\nuse_awaitable\n=============")
    dt(reset=True)

    print(f"{dt()}  1| Waiting for the message...")
    msg = await WaitableMessage(0.2, "Hello after 0.2 seconds!")
    print(f"{dt()}  2| message: '{msg}'")


if __name__ == "__main__":
    asyncio.run(use_awaitable())

