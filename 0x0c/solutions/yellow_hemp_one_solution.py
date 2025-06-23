# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Yellow Hemp' - see also the solution in Unit 0x0b """

from pathlib import Path
import concurrent.futures
import functools
import time
import asyncio

# as before
def read_file(filename: Path):
    with open(filename, "r") as reader:
        return reader.readlines()


# as before
def check_content(lines: list[str]):
    # it is not about the error, so returning False is enough
    return len(lines) == 3 and int(lines[2]) == sum([int(s.strip()) for s in lines[1].split(',')])


# as before
def check_sample(n: int):
    return check_content(read_file(Path(f"../../0x0b/data/test{n:03}.txt")))


# as before
def check_range(n0: int, n1: int):
    return [n for n in range(n0, n1) if not check_sample(n)]


# as before
def check_all_files_serial(samples):
    print(f" 1| check {samples=} files serial")
    t0 = time.process_time()
    result = f"no errors" if not (ec := check_range(1, samples+1)) else f"errors in samples {ec}"
    dt = time.process_time() - t0
    print(f" 2| {result}, {dt=}\n")


# as before
def check_all_files_parallel(samples: int, workers: int):
    print(f" 1| check {samples=} files parallel (pool) with {workers=}")
    dn = samples // workers
    t0 = time.process_time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        results = [executor.submit(check_range, n0=k * dn+1, n1=(k + 1) * dn+1) for k in range(workers)]
        ec = functools.reduce(lambda x, w: x + w.result(), results, [])  # assuming all tasks need nearly same time
    result = f"no errors" if not ec else f"errors in samples {ec}"
    dt = time.process_time() - t0
    print(f" 2| {result}, {dt=}\n")


# new
async def check_range_async(n0: int, n1: int):
    return await asyncio.to_thread(check_range, n0, n1)


# new
async def check_all_files_async(samples: int, workers: int):
    print(f" 1| check {samples=} files async with {workers=}")
    dn = samples // workers
    t0 = time.monotonic()
    # tasks = [asyncio.create_task(asyncio.to_thread(check_range, n0=k * dn + 1, n1=(k + 1) * dn + 1)) for k in range(workers)]
    tasks = [asyncio.create_task(check_range_async(n0=k * dn + 1, n1=(k + 1) * dn + 1)) for k in range(workers)]
    results = await asyncio.gather(*tasks)
    ec = functools.reduce(lambda x, w: x + w, results, [])
    result = f"no errors" if not ec else f"errors in samples {ec}"
    dt = time.monotonic() - t0
    print(f" 2| {result}, {dt=}\n")


if __name__ == "__main__":
    samples = 120
    check_all_files_serial(samples)
    check_all_files_parallel(samples, 12)
    asyncio.run(check_all_files_async(samples, 12))

"""
  - https://www.twilio.com/blog/working-with-files-asynchronously-in-python-using-aiofiles-and-asyncio
  - https://stackoverflow.com/questions/34699948/does-asyncio-supports-asynchronous-i-o-for-file-operations
"""
