# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about tasks and async processes.

Teaching focus
  - tasks
  - async, await

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import time
import asyncio
import threading
from thread_helper import dt
from inspect import isgeneratorfunction, isgenerator, iscoroutinefunction, iscoroutine


"""
Async/await terminology:
- Suspendable function  A function that can be paused and resumed, i.e., 
                        an Async function.
- Async function        A function defined with 'async def', which returns 
                        a coroutine when called.
- Suspension point      A point in a coroutine where it yields control to the 
                        event loop (e.g. await something).
- Coroutine             An object created when you call an Async function
                        — it can be suspended and resumed.
- Awaitable             Any object you can await — typically a coroutine.

'Using' an Async function:
- query_database        A reference to the async function.
- query_database()      Returns a coroutine object.
- await query_database() Runs the coroutine to the next await or completion.

'cooperative multitasking':
- A coroutine can be scheduled to run concurrently with other coroutines.
- The event loop is responsible for scheduling coroutines.

History:
- Windows 3.x (1990–1993) used cooperative multitasking, i.e. each running program 
  had to voluntarily yield control back to the system - "be polite or be a problem".
- Windows NT (1993+) has full preemptive multitasking.
- Intel 80386 (1985-) is the first CPU that made true preemptive multitasking
  (interrupt a running process to give another one CPU time) feasible and efficient.
"""



async def query_database(delay, table):
    """ suspendable function: wait for an external event such as database query results """
    print(f"{dt()}  a|  - select count(*) from '{table}' (needs {delay}s) ...")

    await asyncio.sleep(delay)              # suspension point, suspends until the task completes

    print(f"{dt()}  b|  - '{table}' results available")
    return int(delay*10)                    # simulate counts


async def basic_idea_of_a_suspendable_function():
    """ suspendable function """
    print("\nbasic_idea_of_a_suspendable_function\n====================================")
    dt(reset=True)

    print(f"{dt()}  1| create tasks")

    # this schedules the coroutine to run, and it returns a Task object
    # (which is also a Future);
    # no execution until the event loop proceeds
    task_people = asyncio.create_task(query_database(0.2, 'people'))

    # comment this in and see that the event loop runs 'task_people'
    # await asyncio.sleep(0)
    task_projects = asyncio.create_task(query_database(0.1, 'projects'))

    # await asyncio.sleep(0)
    print(f"{dt()}  2| tasks created")

    # 'await' suspends until the task completes (and returns the coroutine’s result)
    people = await task_people
    projects = await task_projects

    print(f"{dt()}  3| all done: {people=}, {projects=}")
    print(f"{dt()}  4| or: {task_people.result()=}, {task_projects.result()=}")


async def just_call_it():
    """ call a coroutine directly, no await -> RuntimeWarning """
    print("\njust_call_it\n============")
    dt(reset=True)

    print(f"{dt()}  1| call tasks")

    people = query_database(0.2, 'people')
    projects = query_database(0.1, 'projects')

    time.sleep(0.5)                         # is there anything running?
    print(f"{dt()}  2| all done: {people=}, {projects=}")
    # RuntimeWarning at the end: coroutine 'query_database' was never awaited


async def sometimes_it_keeps_serial():
    """ awaiting alone keeps serial execution order """
    print("\nsometimes_it_keeps_serial\n=========================")
    dt(reset=True)

    print(f"{dt()}  1| create tasks")

    # this does not (implicitly) create a task, it simply suspends the execution;
    # we come to this situation in 'chains' again
    people = await query_database(0.2, 'people')
    projects = await query_database(0.1, 'projects')

    print(f"{dt()}  2| all done: {people=}, {projects=}")


async def make_it_parallel():
    """ parallel calling """
    print("\nmake_it_parallel\n================")
    dt(reset=True)

    people, projects = await asyncio.gather(
        query_database(0.2, 'people'),
        query_database(0.1, 'projects')
    )
    print(f"{dt()}  3| all done: {people=}, {projects=}")


async def characterizations():
    """ check for the types """
    print("\ncharacterizations\n=====================")
    dt(reset=True)

    print(f"{dt()}  1| ...")

    # remember
    def gen_function(n):                    # isgeneratorfunction(gen_function)
        yield n
    gen = gen_function(1)                   # isgenerator(gen)
    print(f"{dt()}  2| {isgeneratorfunction(gen_function)=}, {isgenerator(gen)=}")

    # nested
    async def coro_function():              # iscoroutinefunction: an async def function
        print(f"{dt()}] -c|   return from 'nested', thread {threading.current_thread().name!r}")
        return 42
    coro = coro_function()                  # iscoroutine
    print(f"{dt()}  3| {iscoroutinefunction(coro_function)=}, {iscoroutine(coro)=}")
    # RuntimeWarning at the end: coroutine 'characterizations' was never awaited


if __name__ == "__main__":
    # 'asyncio.run' we need a runner for async stuff
    asyncio.run(basic_idea_of_a_suspendable_function())
    # asyncio.run(just_call_it())
    asyncio.run(sometimes_it_keeps_serial())
    asyncio.run(make_it_parallel())
    # asyncio.run(characterizations())


"""
Ref. to
    https://docs.python.org/3/library/asyncio-task.html
    https://docs.python.org/3/library/asyncio-future.html
    https://www.integralist.co.uk/posts/python-generators/
"""
