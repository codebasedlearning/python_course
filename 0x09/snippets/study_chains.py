# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about chaining async processes.

Teaching focus
  - async, await
  - callback-hell
  - what are the benefits of async?

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.

Most content stems from:
    https://realpython.com/async-io-python/

The async example is not faster (results depend on one another),
and it is not about saving time but about being clear in flow.
"""

import asyncio
import time

from utils import print_function_header, reset_timing, set_current_task_name, ttprint


@reset_timing
@print_function_header
def callback_hell():
    """ call me """

    def check_connection(cont_with):
        """ check net connection and continue with the 'cont' function """
        ttprint(" a| - check connection")
        time.sleep(0.1)
        is_fast = True
        ttprint(f" b| - {is_fast=}")
        return cont_with(is_fast)           # <- call cont-function with a result

    def determine_speed(is_fast, cont_with):
        """ determine speed and continue with the 'cont' function """
        ttprint(" c| - determine speed")
        time.sleep(0.1)
        speed = 2 if is_fast else 1
        ttprint(f" d| - {speed=}")
        return cont_with(is_fast, speed)    # <- call cont-function

    def load_data(is_fast, speed):
        """ load data with fast- and speed info and return result """
        ttprint(" e| - load data")
        time.sleep(0.1)
        bulk = (3 if is_fast else 1)*speed
        ttprint(f" f| - {bulk=}")
        return bulk

    ttprint(" 1| start chain")
    # 1. check_connection => is_fast
    # 2.   => determine_speed(is_fast) => speed
    # 3.     => load_data(is_fast,speed)
    result = check_connection(
        cont_with=lambda is_fast: determine_speed(is_fast,
            cont_with=lambda is_fast, speed: load_data(is_fast, speed)
        )
    )
    ttprint(f" 2| {result=}")


@reset_timing
@print_function_header
async def call_me_when_done():
    """ it is not about saving time but about being clear """

    async def check_connection():
        ttprint(" a| - check connection")
        # explicitly calling some blocking function
        await asyncio.create_task(asyncio.to_thread(lambda: time.sleep(0.1)))
        is_fast = True
        ttprint(f" b| - {is_fast=}")
        return is_fast

    async def determine_speed(is_fast):
        ttprint(" c| - determine speed")
        await asyncio.create_task(asyncio.to_thread(lambda: time.sleep(0.1)))
        speed = 2 if is_fast else 1
        ttprint(f" d| - {speed=}")
        return speed

    async def load_data(is_fast, speed):
        ttprint(" e| - load data")
        await asyncio.create_task(asyncio.to_thread(lambda: time.sleep(0.1)))
        bulk = (3 if is_fast else 1)*speed
        ttprint(f" f| - {bulk=}")
        return bulk

    ttprint(" 1| start chain")
    is_fast = await check_connection()      # this is the basic idea! here it is not about
    speed = await determine_speed(is_fast)  # being faster but having a straight forward logic
    result = await load_data(is_fast, speed)
    ttprint(f" 2| {result=}")


async def main():
    set_current_task_name("run")
    await call_me_when_done()

if __name__ == "__main__":
    callback_hell()
    asyncio.run(main())
