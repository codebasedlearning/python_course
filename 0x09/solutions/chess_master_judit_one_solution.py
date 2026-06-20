# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Judit' """

import time
import asyncio

#from thread_helper import dt
from utils import print_function_header, reset_timing, set_current_task_name, ttprint

MOVES_PER_GAME = 30
NUM_GAMES = 24
JUDIT_MOVE_TIME_SEC = 5
OPPONENT_MOVE_TIME_SEC = 55

"""
sync
    24 * 30 * (5+55)s = 24 * 30 * 1min = 12h
async
    30 * 24 * 5s = 30 * 2min = 1h (+remaining last opponents)

-> scale 1h->1s => /60/60
"""

JUDIT_MOVE_TIME = JUDIT_MOVE_TIME_SEC/60.0/60.0
OPPONENT_MOVE_TIME = OPPONENT_MOVE_TIME_SEC/60.0/60.0


@reset_timing
@print_function_header
def synchronous_exhibition():
    """ play the synchronized exhibition """
    #print("\nsynchronous_exhibition\n======================")
    #dt(reset=True)

    ttprint(f" 1| expected: {NUM_GAMES*MOVES_PER_GAME*(JUDIT_MOVE_TIME+OPPONENT_MOVE_TIME)}s")
    start = time.monotonic()
    ttprint(" 2| games")
    for game_id in range(NUM_GAMES):
        ttprint(f" a| - {game_id + 1}")
        for move in range(MOVES_PER_GAME):
            time.sleep(JUDIT_MOVE_TIME)     # Judit thinks
            time.sleep(OPPONENT_MOVE_TIME)  # Opponent thinks
    end = time.monotonic()
    ttprint(f" 3| synchronous exhibition took {(end - start):.2f} seconds")


@reset_timing
@print_function_header
async def asynchronous_exhibition():
    """ play the asynchronized exhibition """
    #print("\nasynchronous_exhibition\n=======================")
    #dt(reset=True)

    def blocking_think():
        time.sleep(OPPONENT_MOVE_TIME)      # blocking!

    async def opponent_think(game_id):      # 'converted' to async
        await asyncio.to_thread(blocking_think)

    ttprint(f" 1| expected: min. {MOVES_PER_GAME*NUM_GAMES*JUDIT_MOVE_TIME+(OPPONENT_MOVE_TIME-JUDIT_MOVE_TIME)}s")
    start = asyncio.get_running_loop().time()
    ttprint(" 2| moves")
    tasks = []
    for move in range(MOVES_PER_GAME):
        ttprint(f" a| - {move + 1}")
        for game_id in range(NUM_GAMES):
            await asyncio.sleep(JUDIT_MOVE_TIME)                        # Judit plays move
            tasks.append(asyncio.create_task(opponent_think(game_id)))  # Opponent starts thinking
    await asyncio.gather(*tasks)
    end = asyncio.get_running_loop().time()
    ttprint(f" 3| asynchronous exhibition took {(end - start):.2f} seconds")


async def main():
    set_current_task_name("run")
    await asynchronous_exhibition()

if __name__ == "__main__":
    synchronous_exhibition()
    asyncio.run(main())
