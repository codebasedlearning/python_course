# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Yellow Hemp' """

from pathlib import Path
import concurrent.futures
import functools
import time


""" code to write data files
def write_test_files_to_data(samples: int):
    import random
    try:
        sample_len = 3
        sample_bound = 9
        print(f"-a| write {samples=} to 'data'")
        for n in range(1, samples+1):
            filename = Path(f"../../data/test{n:03}.txt")
            with open(filename, 'w') as writer:
                print(f"{n:03} ", end='')
                numbers = [random.randint(1, sample_bound) for _ in range(sample_len)]
                sum_numbers = sum(numbers)
                writer.write(f"# data {n:03}\n"
                             f"{str(numbers)[1:-1]}\n"
                             f"{sum_numbers}\n")
        print(f"\n-b| done")
    except OSError as e:
        print(f"    -> IO error: {e}")
"""


def read_file(filename: Path):
    with open(filename, "r") as reader:
        return reader.readlines()


def check_content(lines: list[str]):
    # it is not about the error, so returning False is sufficient
    return len(lines) == 3 and int(lines[2]) == sum([int(s.strip()) for s in lines[1].split(',')])
    # if len(lines) != 3:
    #     return False
    # numbers = [int(s.strip()) for s in lines[1].split(',')]
    # sum1 = int(lines[2])
    # sum2 = sum(numbers)
    # return sum1 == sum2


def check_sample(n: int):
    return check_content(read_file(Path(f"../data/test{n:03}.txt")))
    # filename = Path(f"../../data/test{n:03}.txt")
    # return check_content(read_file(filename))


def check_range(n0: int, n1: int):
    return [n for n in range(n0, n1) if not check_sample(n)]
    # ec = []
    # for n in range(n0, n1):
    #     if not check_sample(n):
    #         ec.append(n)
    # return ec


def check_all_files_serial(samples):
    print(f" 1| check {samples=} files serial")
    t0 = time.process_time()
    result = f"no errors" if not (ec := check_range(1, samples+1)) else f"errors in samples {ec}"
    dt = time.process_time() - t0
    print(f" 2| {result}, {dt=}\n")


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


if __name__ == "__main__":
    samples = 120
    check_all_files_serial(samples)
    check_all_files_parallel(samples, 12)

"""
  - https://www.twilio.com/blog/working-with-files-asynchronously-in-python-using-aiofiles-and-asyncio
  - https://stackoverflow.com/questions/34699948/does-asyncio-supports-asynchronous-i-o-for-file-operations
"""
