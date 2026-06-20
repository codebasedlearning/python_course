# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about tasks and async processes.

Teaching focus
  - task groups
  - exceptions
  - async, await

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.

Ref. to
    https://docs.python.org/3/library/asyncio-task.html
    https://docs.python.org/3/library/asyncio-future.html
    https://www.integralist.co.uk/posts/python-generators/

asyncio.TaskGroup (3.11+) is essentially the structured-concurrency successor to
gather. The advantages over asyncio.gather:

  - Proper error propagation via ExceptionGroup. When multiple tasks fail,
    TaskGroup collects all exceptions into an ExceptionGroup.
    For that we have a new exception handling: except*

  - Automatic cancellation of siblings on failure. If one task in a TaskGroup
    raises, the remaining tasks are automatically cancelled.

  - Structured concurrency — no orphaned/leaked tasks. The async with block
    is a hard boundary: control doesn't leave it until every child task is done.

  - Dynamic task addition. You can tg.create_task inside the block, including
    from within already-running child tasks, and they're all still awaited.

  - Cancellation safety. If the surrounding code is cancelled, TaskGroup
    cleanly tears down its children.

Rule of thumb:
  - default to TaskGroup for correctness
  - reach for gather only when you want the compact result-list ergonomics
    and the failure semantics genuinely don't matter
"""

import asyncio

from utils import print_function_header, reset_timing, set_current_task_name, ttprint


async def query_database(table):
    """ suspendable function: wait for an external event such as database query results """
    ttprint(f" a| - select count(*) from '{table}'...")
    await asyncio.sleep(0.1)
    ttprint(f" b| - '{table}' results available")
    return 1 if table=="people" else 2


@reset_timing
@print_function_header
async def using_a_task_group():
    """ use task groups to manage multiple tasks at once """

    ttprint(" 1| create tasks in taskgroup")

    # note:
    # - once a TaskGroup exits, it no longer holds references to its tasks
    # - implicitly awaits all
    async with asyncio.TaskGroup() as tg:
        task_people = tg.create_task(query_database("people"))
        task_projects = tg.create_task(query_database("projects"))

    ttprint(" 2| task group awaited")

    # results are available due to the implicit await
    people = task_people.result()
    projects = task_projects.result()
    ttprint(f" 3| all done: {people=}, {projects=}")


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

async def boom(table, delay):
    try:
        ttprint(f" a| - boom in query 'select * from {table}' in {delay}s")
        await asyncio.sleep(delay)
        ttprint(f" b| - raise ValueError in '{table}'")
        raise ValueError(f"query for '{table}' blew up!")
    except asyncio.CancelledError:
        ttprint(f" c|  - '{table}' got cancelled")
        raise

@reset_timing
@print_function_header
async def exceptions_and_task_cancellation():
    """ show how to handle exceptions and task cancellation """

    ttprint(" 1| create tasks in taskgroup and crash them")
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(boom("people", 0.1))     # boom in 0.1
            tg.create_task(boom("projects", 0.1))   # boom in 0.1
            tg.create_task(boom("orders", 0.3))     # still running at boom, will be canceled
    except* ValueError as eg:                       # exception group, keyword 'except*' (since 3.11)
        ttprint(f" 2| Caught ValueError group with {len(eg.exceptions)} exceptions:")
        for e in eg.exceptions:
            ttprint(" 3| - Error:", e)

    ttprint(" 4| all done")


async def main():
    set_current_task_name("run")

    await using_a_task_group()
    await exceptions_and_task_cancellation()

if __name__ == "__main__":
    asyncio.run(main())
