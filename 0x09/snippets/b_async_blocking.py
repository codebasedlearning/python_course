# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about blocking and async processes.

Teaching focus
  - async, await

Situation: I have a blocking call, and I'm in an async context:

  - never call the blocking function directly in the coroutine
    'async def' does not make blocking code non-blocking!

  - replace it with a native-async client — best when one exists

  - use 'asyncio.to_thread' — the default fix when no async client exists
      - it offloads the blocking call to the default ThreadPoolExecutor,
        and because blocking IO releases the GIL while parked in the syscall,
        multiple offloaded calls genuinely overlap; the loop thread stays free
      - this is your go-to for a legacy-blocking library, IO-bound
      - problems:
        - the default pool is small, too many threads will queue;
          fine for moderate fan-out, a bottleneck for massive fan-out
        - no control over pool size or naming
        - cancellation doesn't reach the thread; if you await and that task
          gets cancelled (timeout, TaskGroup sibling failed), the coroutine
          stops awaiting, but the thread keeps running

  - use 'loop.run_in_executor' — when you need control
      - tune max_workers
      - reuse one long-lived pool instead of spawning per call
      - to_thread is literally a thin wrapper over this with the default executor

  - switch to a ProcessPoolExecutor for CPU-bound blocking work
"""

import asyncio
import concurrent
import concurrent.futures
import re
import time

import httpx

from utils import print_function_header, reset_timing, reset_timing_now, set_current_task_name, ttprint

#
# benchmark first
#

async def busy_loop_async(budget:float, step:float=0.1) -> None:
    """ prints a heartbeat every steps so you can see whether the loop is still being serviced """
    for _ in range(round(budget/step)):
        ttprint(f" .| - busy async, {budget=:4.2f}")
        budget -= step
        await asyncio.sleep(step)

@reset_timing
@print_function_header
async def show_busy_loops():
    """ demonstrate async busy loops """

    ttprint(" 1| two busy loops - run alternately")
    await asyncio.gather(
        busy_loop_async(0.3),
        busy_loop_async(0.3)
    )

#
# blocking vs. async
#

def extract_first_tag(text:str, tag:str) -> str | None:
    """ extract the first occurrence of a tag in a string """
    if m := re.search(f"<{tag}>(.*?)</{tag}>", text, re.IGNORECASE | re.DOTALL):
        return m.group(1)
    return None

def read_first_tag_blocking(url:str, tag:str, default="Dummy Text") -> str:
    """ real request, blocking """
    try:
        ttprint( " a| - get...")
        response = httpx.get(url,timeout=1.0)
        ttprint(f" b| - got response [status={response.status_code}]")
        if text:=extract_first_tag(response.text, tag):
            return text
    except httpx.RequestError as e:
        ttprint(f" -| - RequestError {e}")
    return default

async def read_first_tag_blocking_async(url:str, tag:str, default="Dummy Text") -> str:
    """ real request, blocking """

    """
        note: async def, but httpx.get is blocking and there is no await, this
        freezes the whole event loop while the request runs (see busy_loop stall)
    """
    return read_first_tag_blocking(url, tag, default)

async def read_first_tag_async(url:str, tag:str, default="Dummy Text") -> str:
    """ real request, async """

    """
      - a native async network driver (asyncpg, aiohttp) does not use a
        hidden thread pool; it issues non-blocking socket syscalls and lets 
        the kernel signal readiness the OS and the network card do the waiting
      - a thread pool only appears when we wrap a blocking call with 
        to_thread / run_in_executor
    """

    try:
        async with httpx.AsyncClient() as client:
            ttprint( " a| - get...")
            response = await client.get(url,timeout=1.0)
            ttprint(f" b| - got response [status={response.status_code}]")
            if text := extract_first_tag(response.text, tag):
                return text
    except httpx.RequestError as e:
        ttprint(f" -| - RequestError {e}")
    return default

@reset_timing
@print_function_header
async def blocking_vs_async():
    """ demonstrate real IO blocking """

    url = "https://example.com"

    ttprint(f" 1| read from {url} (blocking) + busy loop")
    title, _ = await asyncio.gather(
        read_first_tag_blocking_async(url, "title"),
        busy_loop_async(0.3)
    )
    ttprint(f" 2| title {title!r}\n")

    reset_timing_now()

    ttprint(f" 3| read from {url} (async) + busy loop")
    title, _ = await asyncio.gather(
        read_first_tag_async(url, "title"),
        busy_loop_async(0.3)
    )
    ttprint(f" 4| title {title!r}")


#
# blocking to_thread
#

async def read_first_tag_in_thread(url:str, tag:str, default="Dummy Text") -> str:
    """ real request, blocking """

    """
      - to_thread runs the blocking httpx.get on a pool thread 
        (which blocks, GIL released)
      - meanwhile the event loop stays free; when the call 
        finishes, the result comes back and the coroutine resumes 
        on the loop thread
    """

    try:
        ttprint( " a| - get...")
        response = await asyncio.to_thread(httpx.get, url,timeout=1.0)
        ttprint(f" b| - got response [status={response.status_code}]")
        if text:=extract_first_tag(response.text, tag):
            return text
    except httpx.RequestError as e:
        ttprint(f" -| - RequestError {e}")
    return default

@reset_timing
@print_function_header
async def blocking_in_thread():
    """ demonstrate real IO blocking in a thread """

    url = "https://example.com"

    ttprint(f" 1| read from {url} (blocking in thread) + busy loop")
    title, _ = await asyncio.gather(
        read_first_tag_in_thread(url, "title"),
        busy_loop_async(0.3)
    )
    ttprint(f" 2| title {title!r}\n")


#
# blocking in pool
#

def busy_loop_blocking(budget:float, step:float=0.1) -> None:
    """ prints a heartbeat every steps so you can see whether the loop is still being serviced """
    for _ in range(round(budget/step)):
        ttprint(f" :| - busy blocking, {budget=:4.2f}")
        budget -= step
        time.sleep(step)                    # blocks

@reset_timing
@print_function_header
async def blocking_in_pool():
    """ demonstrate real IO blocking in a pool """

    url = "https://example.com"

    """
    run_in_executor submits the call to the executor and bridges the worker's 
    thread-Future to an asyncio-Future, so that when the thread finishes 
    it wakes the loop and the await resumes with the result.
    to_thread is literally run_in_executor(None, functools.partial(fn, *args, **kwargs)) 
    — same bridge, default executor.
    """

    loop = asyncio.get_running_loop()       # the event loop
    with concurrent.futures.ThreadPoolExecutor(max_workers=4,
                                               thread_name_prefix="db") as pool:
        ttprint(f" 1| read from {url} (blocking in thread) + busy loop")
        title, _ = await asyncio.gather(
            loop.run_in_executor(pool, read_first_tag_blocking, url, "title"),
            loop.run_in_executor(pool, busy_loop_blocking, 0.3)
        )
        ttprint(f" 2| title {title!r}\n")


async def main():
    set_current_task_name("run")

    await show_busy_loops()
    await blocking_vs_async()
    await blocking_in_thread()
    await blocking_in_pool()

if __name__ == "__main__":
    asyncio.run(main())
