# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about tasks and async processes.

Teaching focus
  - tasks
  - async, await
  - what is really async?
  - supervised vs. unsupervised async cooking
  - a second example to discuss async

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import time
import asyncio

from thread_helper import dt


def heat_soup():
    """ heat soup """
    print(f"{dt()}  a| - Heat soup [sync] (needs 0.3s)...")
    time.sleep(0.3)
    print(f"{dt()}  b| - Soup is hot.")

def fry_onions():
    """ fry onions """
    print(f"{dt()}  c| - Frying onions [sync] (needs 0.2s)...")
    time.sleep(0.2)
    print(f"{dt()}  d| - Onions are ready.")

def synchronous_cooking():
    """ synchronous cooking """
    print("\nsynchronous_cooking\n===================")
    dt(reset=True)

    print(f"{dt()}  1| start cooking")
    heat_soup()
    fry_onions()
    print(f"{dt()}  2| done")


async def heat_soup_async():
    """ heat soup and leave it alone """
    print(f"{dt()}  a| - Heat soup [async] (needs 0.3s)...")
    await asyncio.sleep(0.3)
    print(f"{dt()}  b| - Soup is hot.")

async def fry_onions_async():
    """ fry onions and leave it alone """
    print(f"{dt()}  c| - Frying onions [async] (needs 0.2s)...")
    await asyncio.sleep(0.2)
    print(f"{dt()}  d| - Onions are ready.    <- !!!")  # ready before soup

async def asynchronous_cooking():
    """ asynchronous cooking """
    print("\nasynchronous_cooking\n====================")
    dt(reset=True)

    task1 = asyncio.create_task(heat_soup_async())
    task2 = asyncio.create_task(fry_onions_async())

    print(f"{dt()}  1| start cooking")
    await task1
    await task2
    print(f"{dt()}  2| done")


async def heat_soup_with_stirring_async():
    """ de facto same as heat_soup but async """
    print(f"{dt()}  a| - Heat soup with stirring [async] (needs 0.3s)...")
    time.sleep(0.3)                         # do real stuff like stirring
    print(f"{dt()}  b| - Soup is hot.")

async def fry_onions_with_turning_async():
    """ de facto same as fry_onions but async """
    print(f"{dt()}  c| - Frying onions with turning [async] (needs 0.2s)...")
    time.sleep(0.2)                         # do real stuff like turning
    print(f"{dt()}  d| - Onions are ready.")

async def asynchronous_cooking_supervised():
    """ asynchronous cooking but supervised """
    print("\nasynchronous_cooking_supervised\n===============================")
    dt(reset=True)

    task1 = asyncio.create_task(heat_soup_with_stirring_async())
    task2 = asyncio.create_task(fry_onions_with_turning_async())

    print(f"{dt()}  1| start cooking")
    await task1
    await task2
    print(f"{dt()}  2| done")


async def asynchronous_cooking_with_helping_hands():
    """ asynchronous cooking with helping hands """
    print("\nasynchronous_cooking_with_helping_hands\n=======================================")
    dt(reset=True)

    task1 = asyncio.create_task(asyncio.to_thread(heat_soup))
    task2 = asyncio.create_task(asyncio.to_thread(fry_onions))

    print(f"{dt()}  1| start cooking")
    await task1
    await task2
    print(f"{dt()}  2| done")


if __name__ == "__main__":
    synchronous_cooking()
    asyncio.run(asynchronous_cooking())
    asyncio.run(asynchronous_cooking_supervised())
    asyncio.run(asynchronous_cooking_with_helping_hands())
