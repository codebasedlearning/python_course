# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about tasks and async processes.

Teaching focus
  - tasks
  - async, await
  - the trap: 'await a; await b' is sequential, not concurrent
  - how to actually overlap work (gather / create_task)
  - completion order

Note (compare with unit 0x08)
  - In 0x08 the 'tprint' prefix showed different thread names (T-1, T-2),
    because work ran on several OS threads.
  - Here every line says 'main': async concurrency happens on ONE thread.
    The event loop interleaves coroutines at each 'await' (suspension point).
    Concurrency without threads, no locks needed for the shared state.

Also note 'README.md' for terms and references, and
'thread_helper.py' for relative time durations.

Ref. to
    https://docs.python.org/3/library/asyncio-task.html
    https://docs.python.org/3/library/asyncio-future.html
    https://www.integralist.co.uk/posts/python-generators/
"""

import asyncio
import concurrent
import concurrent.futures
import time

from utils import print_function_header, reset_timing, set_current_task_name, tprint, ttprint

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
- fetch_user            A reference to the async function.
- fetch_user(42)        Returns a coroutine object (nothing runs yet!).
- await fetch_user(42)  Runs the coroutine to the next await or completion.

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

#
# first: traditional ways to cook
#

def heat_soup():
    """ heat soup, return temperature (°C) """
    tprint(" a| - heat soup (needs 0.3s) [fcn]")
    time.sleep(0.3)
    tprint(" b| - soup is hot")
    return 60.0

def fry_onions():
    """ fry onions, return number of onions """
    tprint(" c| - frying onions (needs 0.2s) [fcn]")
    time.sleep(0.2)
    tprint(" d| - onions are ready")
    return 5

@reset_timing
@print_function_header
def synchronous_cooking():
    """ synchronous cooking, one ingredient at a time """

    tprint(" 1| soup first")
    soup_temp = heat_soup()

    tprint(" 2| onions next")
    num_onions = fry_onions()

    tprint(f" 3| no wait, done; soup:{soup_temp}°C, #onions:{num_onions}")


@reset_timing
@print_function_header
def concurrent_cooking_with_threads():
    """ concurrent cooking in separate threads """

    """
      - we use futures to get the results
      - this also cooks concurrently, but 'join' provides no result
            soup = threading.Thread(target=heat_soup, name="soup")
            soup.start()
            soup.join()
    """

    tprint(" 1| soup and onions")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        soup_future = executor.submit(heat_soup)
        onions_future = executor.submit(fry_onions)
        tprint(" 2| wait")
    
    soup_temp = soup_future.result()
    num_onions = onions_future.result()
    tprint(f" 3| done; soup:{soup_temp}°C, #onions:{num_onions}")


#
# recap: yield and suspending
#

def countdown321():
    """ a generator: 'yield' suspends and resumes """
    tprint(" a| - countdown starts")
    yield 3                                 # suspend here, value goes to caller
    tprint(" b| - resumed after 3")
    yield 2                                 # suspend here, value goes to caller
    tprint(" c| - resumed after 2")
    yield 1                                 # suspend here, value goes to caller
    tprint(" d| - resumed after 1, generator returns")

    """
      - 'yield' is the suspension point: the function freezes its local
        state, hands a value back to the caller, and later resumes exactly 
        where it left off
      - this is the same idea for coroutines
    """
    

@reset_timing
@print_function_header
def the_idea_of_suspending():
    """ a generator pauses at 'yield' and resumes """

    tprint( " 1| call generator")
    gen = countdown321()                    # no code runs!
    tprint(f" 2| the body has not run yet, {gen=}")

    tprint( " 3| start loop")
    for n in gen:                           # the generator starts at first next()
        tprint(f" 4| - got {n=}")           # (inside 'for') and runs up to the first 'yield'
    tprint(" 5| done")


#
# recap: suspending functions
#

async def signin_async(name:str):
    """ simulate a sign-in call and return an identifier """
    ttprint(f" a| - sign in of {name!r} starts")

    await asyncio.sleep(0.1)                # instead of time.sleep, discussed later
    user_id = 23 if name=="Alice" else 42 if name=="Bob" else 99

    ttprint(f" b| - {name!r} signed in, coro returns with {user_id=}")
    return user_id

@reset_timing
@print_function_header
async def the_idea_of_coros_focus_starting():
    """ coroutines, focus on the timing """

    ttprint( " 1| call coro")
    coro_alice = signin_async("Alice")      # no code runs, similar to the generator function
    ttprint(f" 2| the body has not run yet, {coro_alice=}")

    await asyncio.sleep(0.05)               # we wait a little bit, nothing runs

    ttprint( " 3| start sign-in ")
    id_alice = await coro_alice             # now it runs
    ttprint(f" 4| got {id_alice=}\n")

    """
      - a coroutine can 'await' another coroutine and use its result, just like 
        a function calls another function and uses its return value
      - 'await f()' means: run f to completion and substitute its result
      - a coroutine, a task and a future are all 'awaitables' - awaiting
        any of them unwraps the value it produces
      - coroutines let you write asynchronous, concurrent control flow as 
        straight-line, top-to-bottom code — no callbacks or hand-written 
        state machines — while the await points stay explicitly visible as 
        the only places execution can suspend and interleave
      - against threads, the advantage is cheapness of tasks -> see below
      - the similarities to 'yield' are
          - generator : yield                ~   coroutine : async and await
          - next(gen) drives the generator   ~   the event loop drives the coroutine
          - calling it -> generator          ~   calling it -> coroutine (nothing runs)
    """

@reset_timing
@print_function_header
async def the_idea_of_coros_focus_mainthread():
    """ coroutines, focus on the running (main)thread """

    ttprint( " 1| call coros")
    coro_bob = signin_async("Bob")
    coro_charly = signin_async("Charly")
    ttprint(f" 2| got only coros, {coro_bob=}, {coro_charly=}")

    await asyncio.sleep(0.05)               # we wait a little bit, nothing runs

    ttprint( " 3| start both sign-in")       # 'start' is precised below
    task_alice = asyncio.create_task(coro_bob)
    task_charly = asyncio.create_task(coro_charly)

    await asyncio.sleep(0.05)

    ttprint( " 4| wait for user ids")
    id_bob = await task_alice
    id_charly = await task_charly
    ttprint(f" 5| got {id_bob=} {id_charly=}")

    """
        both sign-in need 0.1s and run on main-thread, and
        need in total 0.1s -> how can this be?
    """

@reset_timing
@print_function_header
async def the_idea_of_coros_event_loop():
    """ coroutines, focus on the underlying loop """

    """
    Event loop — a single-threaded scheduler that runs in a loop: 
      - it runs all ready callbacks (stepping each coroutine from one 
        await to the next), then waits on the OS for the next timer 
        or IO event, then repeats
      - it drives tasks cooperatively — it only ever switches at 
        a coroutine's await (suspension point), never by preemption
      - the kernel does the actual waiting, so one thread can juggle 
        thousands of suspended coroutines
      - 'asyncio.run(coro)' also wraps the coro in a task and schedules 
        it on the loop
    A metaphor is a single waiter in a restaurant. 
      - take an order (start a coroutine), and instead of standing at 
        the table while the kitchen cooks (await), they go serve other tables
      - they never cook or wait idly — they just keep moving between tables 
        whose food is ready; one waiter, many tables
      - the kitchen (the OS/kernel) does the slow work
      - the waiter only gets stuck if one customer monologues without pausing
        a 'blocking' call
    """
    
    ttprint(f" 1| check loop: {len(asyncio.all_tasks())}")       # one task from 'asyncio.run(coro)'
    
    coro_alice = signin_async("Alice")                          # no task created
    ttprint(f" 2| tasks on loop: {len(asyncio.all_tasks())}")
    
    id_alice = await coro_alice                                 # run coro to completion
    ttprint(f" 3| {id_alice=}, tasks on loop: {len(asyncio.all_tasks())}")

    """
      - 'await f' is like a subroutine call that's allowed to suspend;
        the awaited coroutine shares the current task's execution,
        it's not a separate unit the loop knows about and therefore
        does not appear in asyncio.all_tasks()
    """

    task_alice = asyncio.create_task(signin_async("Bob"))       # create tasks with the coros
    task_charly = asyncio.create_task(signin_async("Charly"))

    ttprint(f" 4| tasks on loop: {len(asyncio.all_tasks())}")
    # await asyncio.sleep(0)

    """
      - technically, they are not started, but they are scheduled
        in the event loop => 3 tasks including the one from 'asyncio.run(coro)'
      - 'await asyncio.sleep(0)' is special-cased in CPython: it doesn't arm 
        a timer, it just suspends the current coroutine and lets the loop run 
        one round of everything currently ready 
    """

    id_bob = await task_alice
    id_charly = await task_charly
    ttprint(f" 5| {id_bob=}, {id_charly=}, tasks on loop: {len(asyncio.all_tasks())}")


#
# focus: suspension points
#

async def fetch_stats(table:str, default:int):
    """ fetch some statistical data from a database table """

    ttprint(f" .|   - fetch stats from {table!r}")
    await asyncio.sleep(0.1)
    ttprint(f" :|   - {table!r} processed, result: {default}")
    return default

async def collect_data(schema:str):
    """ collect data from different tables; process them when available """

    ttprint(f" a| - collect from {schema!r}")
    salary = await fetch_stats(table=f"{schema}.salary", default=1)
    ttprint(f" b| - got {salary=} from {schema!r}")
    bonus = await fetch_stats(table=f"{schema}.bonus", default=2)
    ttprint(f" c| - got {bonus=} from {schema!r}")
    return salary+bonus

@reset_timing
@print_function_header
async def all_coros_in_main():
    """ concurrently collect data from different schemes """

    ttprint( " 1| start employee and freelancer coro")

    # instead of creating two tasks we delegate this to 'asyncio.gather'
    #   employee_task = asyncio.create_task(collect_data(schema="employee"))
    #   freelancer_task = asyncio.create_task(collect_data(schema="freelancer"))
    #   employee_costs = await employee_task
    #   freelancer_costs = await freelancer_task

    employee_costs, freelancer_costs = await asyncio.gather(
        collect_data(schema="employee"),
        collect_data(schema="freelancer")
    )

    ttprint(f" 2| done, {employee_costs=}, {freelancer_costs=}")


#
# close the story: cooking with tasks
#   btw: the suffix '_async' is no official convention; here it separates
#   the coros from the functions
#

async def heat_soup_async():
    """ heat soup, return temperature (°C) """
    ttprint(" a| - heat soup (needs 0.3s) [coro]")
    await asyncio.sleep(0.3)
    ttprint(" b| - soup is hot")
    return 60.0

async def fry_onions_async():
    """ fry onions, return number of onions """
    ttprint(" c| - frying onions (needs 0.2s) [coro]")
    await asyncio.sleep(0.2)
    ttprint(" d| - onions are ready")
    return 5

@reset_timing
@print_function_header
async def cooking_to_gather():
    """ cooking with tasks """
    ttprint(" 1| soup and onions")

    # multiple create_tasks here, no worker limit
    soup_temp, num_onions = await asyncio.gather(
        heat_soup_async(),
        fry_onions_async()
    )
    ttprint(f" 2| wait, done; soup:{soup_temp}°C, #onions:{num_onions}")


@reset_timing
@print_function_header
async def cooking_as_completed():
    """ react to results in the order they finish, not the order submitted """

    ttprint(" 1| soup and onions")

    """
      - 'for' pulls the next item synchronously via __next__ (the iterable 
        must have it ready immediately), while 'async for' awaits the next 
        item via __anext__, letting the coroutine suspend at each step until 
        the value is ready
      - 'async for' available for 3.13+
      
      - asyncio.gather returns all results together, in submission order, and
        only after the slowest one finishes
      - asyncio.as_completed yields each awaitable as it finishes, so the fast
        one is handled first (fast, mid, slow here)
      - use gather when you need the whole batch at once; use as_completed when
        you want to start processing whichever finishes first
    """

    # handle each as soon as it is ready
    async for finished in asyncio.as_completed([
            heat_soup_async(),
            fry_onions_async()
    ]):
        result = await finished
        # finished._coro not always defined for a future, but it is for the coroutine
        ttprint(f" e| - first-ready: {result!r} from {finished._coro.__name__!r}")  # ty:ignore[unresolved-attribute]


async def main():
    set_current_task_name("run")

    await the_idea_of_coros_focus_starting()
    await the_idea_of_coros_focus_mainthread()
    await the_idea_of_coros_event_loop()

    await all_coros_in_main()
    await cooking_to_gather()
    await cooking_as_completed()


if __name__ == "__main__":
    synchronous_cooking()
    concurrent_cooking_with_threads()

    the_idea_of_suspending()

    asyncio.run(main())
