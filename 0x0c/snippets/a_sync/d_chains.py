# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about chaining async processes.

Teaching focus
  - async, await
  - callback-hell
  - what are the benefits of async?

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import time
import asyncio
from thread_helper import dt


def callback_hell():
    """ call me """
    print("\ncallback_hell\n=============")
    dt(reset=True)

    def check_connection(cont_with):
        """ check net connection and continue with the 'cont' function """
        print(f"{dt()}  1| check connection: ", end='')
        time.sleep(0.1)
        is_fast = True
        print(f"{is_fast=}")
        return cont_with(is_fast)           # <- call cont-function with a result

    def determine_speed(is_fast, cont_with):
        """ determine speed and continue with the 'cont' function """
        print(f"{dt()}  2| determine speed: ", end='')
        time.sleep(0.1)
        speed = 2 if is_fast else 1
        print(f"{speed=}")
        return cont_with(is_fast, speed)    # <- call cont-function

    def load_data(is_fast, speed):
        """ load data with fast- and speed info and return result """
        print(f"{dt()}  3| load data: ", end='')
        time.sleep(0.1)
        bulk = (3 if is_fast else 1)*speed
        print(f"{bulk=}")
        return bulk

    # 1. check_connection => is_fast
    # 2.   => determine_speed(is_fast) => speed
    # 3.     => load_data(is_fast,speed)
    bulk = check_connection(
        cont_with=lambda is_fast: determine_speed(is_fast,
            cont_with=lambda is_fast, speed: load_data(is_fast, speed)
        )
    )
    print(f"{dt()}  4| result: {bulk=}\n")


async def call_me_when_done():
    """ it is not about saving time but about being clear """
    print("\ncall_me_when_done\n=================")
    dt(reset=True)

    async def check_connection():
        print(f"{dt()}  1| check connection: ", end='')
        # explicitly calling some blocking function
        await asyncio.create_task(asyncio.to_thread(lambda: time.sleep(0.1)))
        is_fast = True
        print(f"{is_fast=}")
        return is_fast

    async def determine_speed(is_fast):
        print(f"{dt()}  2| determine speed: ", end='')
        await asyncio.create_task(asyncio.to_thread(lambda: time.sleep(0.1)))
        speed = 2 if is_fast else 1
        print(f"{speed=}")
        return speed

    async def load_data(is_fast, speed):
        print(f"{dt()}  3| load data: ", end='')
        await asyncio.create_task(asyncio.to_thread(lambda: time.sleep(0.1)))
        bulk = (3 if is_fast else 1)*speed
        print(f"{bulk=}")
        return bulk

    is_fast = await check_connection()      # this is the basic idea! here it is not about
    speed = await determine_speed(is_fast)  # being faster but having a straight forward logic
    bulk = await load_data(is_fast, speed)
    print(f"{dt()}  4| result: {bulk=}")


if __name__ == "__main__":
    callback_hell()
    asyncio.run(call_me_when_done())


"""
Most content stems from:
    https://realpython.com/async-io-python/
"""
