# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about tasks and async processes.

Teaching focus
  - task groups
  - exceptions
  - async, await

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.
"""

import asyncio
from thread_helper import dt


async def query_database(delay, table):
    """ suspendable function: wait for an external event such as database query results """
    print(f"{dt()}  a|  - select count(*) from '{table}' (needs {delay}s) ...")

    await asyncio.sleep(delay)              # suspension point, suspends until the task completes

    print(f"{dt()}  b|  - '{table}' results available")
    return int(delay*10)                    # simulate counts


async def using_a_task_group():
    """ use task groups to manage multiple tasks at once """
    print("\nusing_a_task_group\n==================")
    dt(reset=True)

    print(f"{dt()}  1| create tasks in taskgroup")

    # note:
    # - once a TaskGroup exits, it no longer holds references to its tasks
    # - implicitly awaits all
    async with asyncio.TaskGroup() as tg:
        task_people = tg.create_task(query_database(0.2, 'people'))
        task_projects = tg.create_task(query_database(0.1, 'projects'))

    print(f"{dt()}  2| task group awaited")

    # results are available due to the implicit await
    people = task_people.result()
    projects = task_projects.result()
    print(f"{dt()}  3| all done: {people=}, {projects=}")

"""
  - Tasks can easily and safely be cancelled. When a task is cancelled, 
    asyncio.CancelledError will be raised in the task at the next opportunity.
  - The first time any of the tasks belonging to the group fails with 
    an exception other than asyncio.CancelledError, the remaining tasks in 
    the group are canceled.
  - It is recommended that coroutines use try/finally blocks to robustly 
    perform clean-up logic. In case asyncio.CancelledError is explicitly 
    caught, it should generally be propagated when clean-up is complete.
"""

async def boom(name, delay):
    try:
        print(f"{dt()}  a|  - boom of '{name}' in {delay}")
        await asyncio.sleep(delay)
        print(f"{dt()}  c|  - raise ValueError in '{name}'")
        raise ValueError(f"'{name}' blew up! -> clean up!")
    except asyncio.CancelledError:
        print(f"{dt()}  b|  - '{name}' got cancelled")
        raise

async def exceptions_and_task_cancellation():
    """ deal with task cancellation and exceptions in a task group """
    print("\nexceptions_and_task_cancellation\n================================")
    dt(reset=True)

    print(f"{dt()}  1| create tasks in taskgroup and crash them")
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(boom("A", 0.01))
            tg.create_task(boom("B", 0.01)) # 0.01 creates two exceptions, 0.02 only one
            tg.create_task(boom("C", 0.03))
    except* ValueError as eg:               # exception group, keyword 'except*' (since 3.11)
        print(f"{dt()}  2| Caught ValueError group with {len(eg.exceptions)} exceptions:")
        for e in eg.exceptions:
            print(f"{dt()}  3| - Error:", e)

    print(f"{dt()}  4| all done")

if __name__ == "__main__":
    asyncio.run(using_a_task_group())
    asyncio.run(exceptions_and_task_cancellation())

"""
Ref. to
    https://docs.python.org/3/library/asyncio-task.html
    https://docs.python.org/3/library/asyncio-future.html
    https://www.integralist.co.uk/posts/python-generators/
"""
