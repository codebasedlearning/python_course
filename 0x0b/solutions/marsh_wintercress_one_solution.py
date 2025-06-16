# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Marsh Wintercress' """

import concurrent.futures
import threading
import time
import collections

import sys
sys.path.append("../snippets/a_threads")
from thread_helper import dt


class MessageQueue:
    neutral_message = 0
    poison_pill = -1

    def __init__(self):
        self.message_list = collections.deque()  # or []
        self.signal = threading.Condition()
        print(f"{dt()}  a|   - init, {self._status()}")

    @property
    def message(self):
        with self.signal:
            while not self.message_list:
                self.signal.wait()
            message = self.message_list.popleft()  # pop(0)
            print(f"{dt()}  b|   - red slot from {id(threading.current_thread())}, {self._status()}")
            return message

    @message.setter
    def message(self, message):
        with self.signal:
            self.message_list.append(message)
            print(f"{dt()}  c|   - wrote slot from {id(threading.current_thread())}, {self._status()}")
            self.signal.notify()

    def _status(self):
        slot = f"{self.message_list}" if self.message_list else "-"
        return f"slot:{slot}"


def producer(pipeline):
    for index in range(1, 5):
        message = index
        print(f"{dt()}  1|   write message: {message}")
        pipeline.message = message
        time.sleep(0.1)

    print(f"{dt()}  3|   write poison pill")
    pipeline.message = MessageQueue.poison_pill
    print(f"{dt()}  4|   producer done")


def consumer(pipeline):
    message = MessageQueue.neutral_message
    while message != MessageQueue.poison_pill:
        message = pipeline.message
        print(f"{dt()}  5|   got message: {message}")
        time.sleep(0.5)
    pipeline.message = MessageQueue.poison_pill
    print(f"{dt()}  6|   consumer done")


def run_messages():
    pipeline = MessageQueue()
    print(f"{dt()}  1|   start threads")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)
        executor.submit(consumer, pipeline)

    print(f"{dt()}  7| main done")


if __name__ == "__main__":
    run_messages()
