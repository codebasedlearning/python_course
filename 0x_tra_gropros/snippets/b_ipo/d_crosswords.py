# (C) 2026 Alexander Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Solve the crossword task using the IPO structure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Self, Sequence, Iterator
import random

from gropro import Producer, Processor, Consumer, IPOProblem


"""
Problem-specific data classes for the crossword task.

We keep the three IPO concerns strictly separated:
  - InputData   : what the producer parses out of a text block
  - ProcessData : the working state for the backtracking solver
  - OutputData  : what a consumer needs in order to render a result
"""

@dataclass
class InputData:
    """ everything a producer extracts from one input block """
    source: str          # logical name of the source (e.g. 'example_1')
    comment: str         # the '# ...' comment line (kept verbatim)
    words: list[str]     # the parsed, uppercased word list

    @classmethod
    def of(cls, source: str, textblock: str) -> Self:
        """ parse a textblock in the canonical 'one comment + comma list' format """
        comment, words = "", []
        for line in textblock.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith('#'):
                if not comment:
                    comment = stripped
            else:
                words = [w.strip().upper() for w in stripped.split(',') if w.strip()]
                break
        return cls(source=source, comment=comment, words=words)

# A placement records 'where and how' a single word ended up on the grid:
# (word_idx, row, col, vertical?). The word_idx refers into ProcessData.words /
# OutputData.words — using an index keeps inner-loop comparisons cheap and
# makes lookup of the precomputed char_dist/keys O(1).
Placement = tuple[int, int, int, bool]

@dataclass
class ProcessData:
    """ working state of the backtracking solver """
    words: list[str]

    # precomputed per-word indexes (filled by the solver's apply()):
    #   char_dist[i][c] = list of indices in words[i] where character c appears
    #   keys[i]         = set of distinct characters in words[i]
    # These are exactly the WordData fields from the reference solution; we
    # keep them on ProcessData so the solver can use them without smuggling
    # state outside of the IPO data flow.
    char_dist: list[dict[str, list[int]]] = field(default_factory=list)
    keys: list[set[str]] = field(default_factory=list)

    # current attempt (mutated during backtracking)
    grid: dict[tuple[int, int], str] = field(default_factory=dict)
    # cells covered specifically by horizontal / vertical placements; the
    # flanking-cell embedding check needs to know the direction of an
    # already-occupied cell (a horizontal word can sit right next to a
    # perpendicular vertical word without 'extending' it).
    h_cells: set[tuple[int, int]] = field(default_factory=set)
    v_cells: set[tuple[int, int]] = field(default_factory=set)
    placements: list[Placement] = field(default_factory=list)
    used: set[int] = field(default_factory=set)
    # parallel stack: which cells were *newly added* by each placement,
    # so that an unplace step touches only those cells (O(len(word))
    # rather than rebuilding the whole grid).
    owned_stack: list[list[tuple[int, int]]] = field(default_factory=list)
    # parallel stack of all cells (newly added or crossed) belonging to each
    # placement; used to undo h_cells/v_cells on backtrack.
    all_cells_stack: list[list[tuple[int, int]]] = field(default_factory=list)
    # current bounding box, kept O(1)-fresh via a stack
    # (min_y, max_y, min_x, max_x); empty when no word placed yet.
    bounds_stack: list[tuple[int, int, int, int]] = field(default_factory=list)

    # best result so far
    best_size: int = 0
    best_grid: dict[tuple[int, int], str] = field(default_factory=dict)
    best_bounds: tuple[int, int, int, int] = (0, 0, 0, 0)  # min_y, max_y, min_x, max_x
    best_placements: list[Placement] = field(default_factory=list)

    @classmethod
    def of(cls, input_data: InputData) -> Self:
        return cls(words=list(input_data.words))


@dataclass
class OutputData:
    """ snapshot of the final result, ready to be rendered by a consumer """
    source: str
    comment: str
    words: list[str]
    best_size: int
    best_grid: dict[tuple[int, int], str]
    best_bounds: tuple[int, int, int, int]
    best_placements: list[Placement]

    @classmethod
    def of(cls, input_data: InputData, process_data: ProcessData) -> Self:
        return cls(
            source=input_data.source,
            comment=input_data.comment,
            words=input_data.words,
            best_size=process_data.best_size,
            best_grid=dict(process_data.best_grid),
            best_bounds=process_data.best_bounds,
            best_placements=list(process_data.best_placements),
        )

"""
Producers
  - ConstantProducer : one input from a single string constant
  - StreamProducer   : a sequence of (source, textblock) pairs

Consumers
  - ConsoleConsumer  : pretty-print the result table to stdout
"""

class StreamProducer(Producer[InputData]):
    """ many (source, textblock) pairs, fed sequentially """

    def __init__(self, items: Sequence[tuple[str, str]]) -> None:
        self.items = items

    def read(self) -> Iterator[InputData]:
        for source, textblock in self.items:
            yield InputData.of(source=source, textblock=textblock)


def _render_grid(grid: dict[tuple[int, int], str],
                 bounds: tuple[int, int, int, int],
                 fill: str = " ") -> str:
    """ render the grid in the task's '|---' table style; `fill` for empty cells """
    min_y, max_y, min_x, max_x = bounds
    width = max_x - min_x + 1
    sep = "|".join(["---"] * width)

    rows: list[str] = []
    for y in range(min_y, max_y + 1):
        cells = [f" {grid.get((y, x), fill)} " for x in range(min_x, max_x + 1)]
        rows.append("|".join(cells))
        if y != max_y:
            rows.append(sep)
    return "\n".join(rows)


def _filled_grid(grid: dict[tuple[int, int], str],
                 bounds: tuple[int, int, int, int],
                 rng: random.Random) -> dict[tuple[int, int], str]:
    """ copy of grid where all blank cells are stuffed with random letters """
    min_y, max_y, min_x, max_x = bounds
    out = dict(grid)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (y, x) not in out:
                out[(y, x)] = chr(ord('A') + rng.randint(0, 25))
    return out


class ConsoleConsumer(Consumer[OutputData]):
    """ print result, optionally with the 'Buchstabensalat' filler """

    def __init__(self, *, with_filled: bool = True, seed: int | None = 42) -> None:
        self.with_filled = with_filled
        self.seed = seed

    def write(self, output_data: OutputData) -> None:
        d = output_data
        print(d.comment)
        print(f"Wörter: {', '.join(d.words)}")
        print()

        if d.best_size == 0:
            print("Lösung: keine gefunden (keine gemeinsamen Buchstaben?).")
            return

        print("Lösung:")
        print()
        print(_render_grid(d.best_grid, d.best_bounds))

        if self.with_filled:
            rng = random.Random(self.seed)
            print()
            print("Aufgefüllt:")
            print()
            print(_render_grid(_filled_grid(d.best_grid, d.best_bounds, rng),
                               d.best_bounds))

        print()
        print(f"Diese Lösung nimmt {d.best_size} Felder ein.")

"""
Strategy:
  - Place the longest word first (heuristic: tends to anchor the grid well).
  - Backtrack: at each step, pick a not-yet-placed word and try every
    perpendicular crossing on every already-placed word.
  - Two layers of pruning:
      a) Candidate-time: estimate the new bounding box *before* placing;
         skip if the estimate already meets/exceeds the current best.
      b) Post-place: re-check the actual bbox area before recursing.

Performance notes:
  - For each word we precompute `char_dist[c] -> list[int]` and `keys`
    (the set of distinct characters). 
  - We also maintain a `bounds_stack` so that the current bbox is always
    available in O(1), instead of scanning the whole grid each time.

Validity rules per placement:
  - Crossing cells must agree on the shared character.
  - The cell directly before/after the word in its own direction must be
    empty (otherwise the word would silently extend an existing one,
    which is the 'embedding' case forbidden by the task description).
  - Parallel adjacency in the perpendicular direction is allowed — see
    the second example arrangement in the task spec, where NETT, ESSEN
    and HUNGER sit in three consecutive rows.

The algorithm is strictly perpendicular: every newly placed word crosses
at least one previously placed word, so the result is always connected
through crossings.
"""

class CrosswordSolver(Processor[ProcessData]):
    """ backtracking solver minimising the bounding-box area """

    def apply(self, pd: ProcessData) -> ProcessData:
        if not pd.words:
            return pd

        # one-time precomputation: char_dist + keys per word
        pd.char_dist = [self._char_distribution(w) for w in pd.words]
        pd.keys = [set(d.keys()) for d in pd.char_dist]

        # anchor: longest word at (0,0). Try BOTH orientations — placing the
        # longest word horizontally locks the bbox width to len(word) for the
        # rest of the search, so any optimum where the longest word is
        # vertical (e.g. example 3 → 5×17) would otherwise be unreachable.
        first_idx = max(range(len(pd.words)), key=lambda i: len(pd.words[i]))
        first = pd.words[first_idx]

        for vertical in (False, True):
            owned, all_cells = self._place(pd, first, 0, 0, vertical=vertical)
            pd.owned_stack.append(owned)
            pd.all_cells_stack.append(all_cells)
            pd.placements.append((first_idx, 0, 0, vertical))
            if vertical:
                pd.bounds_stack.append((0, len(first) - 1, 0, 0))
            else:
                pd.bounds_stack.append((0, 0, 0, len(first) - 1))
            pd.used.add(first_idx)

            self._solve(pd)

            pd.used.remove(first_idx)
            pd.bounds_stack.pop()
            pd.placements.pop()
            for cell in pd.owned_stack.pop():
                del pd.grid[cell]
            cells_set = pd.v_cells if vertical else pd.h_cells
            for cell in pd.all_cells_stack.pop():
                cells_set.discard(cell)
        return pd

    # backtracking core

    def _solve(self, pd: ProcessData) -> None:
        if len(pd.used) == len(pd.words):
            self._record_if_better(pd)
            return

        cur_bounds = pd.bounds_stack[-1]

        for i, word in enumerate(pd.words):
            if i in pd.used:
                continue
            for (y, x, vertical) in self._candidates(pd, i):
                # (a) early prune: would the bbox be too large already?
                est = self._extend_bounds(cur_bounds, len(word), y, x, vertical)
                est_size = (est[1] - est[0] + 1) * (est[3] - est[2] + 1)
                if pd.best_size > 0 and est_size >= pd.best_size:
                    continue
                # (b) legality check
                if not self._fits(pd, word, y, x, vertical):
                    continue

                owned, all_cells = self._place(pd, word, y, x, vertical)
                pd.owned_stack.append(owned)
                pd.all_cells_stack.append(all_cells)
                pd.placements.append((i, y, x, vertical))
                pd.bounds_stack.append(est)
                pd.used.add(i)

                self._solve(pd)

                pd.used.remove(i)
                pd.bounds_stack.pop()
                pd.placements.pop()
                for cell in pd.owned_stack.pop():
                    del pd.grid[cell]
                cells_set = pd.v_cells if vertical else pd.h_cells
                for cell in pd.all_cells_stack.pop():
                    cells_set.discard(cell)

    def _candidates(self,
                    pd: ProcessData,
                    word_idx: int) -> Iterator[tuple[int, int, bool]]:
        """ yield (y, x, vertical) for every perpendicular cross with a placed word """
        word_keys = pd.keys[word_idx]
        word_dist = pd.char_dist[word_idx]

        seen: set[tuple[int, int, bool]] = set()
        for (placed_idx, py, px, p_vertical) in pd.placements:
            common = word_keys & pd.keys[placed_idx]
            if not common:
                continue
            placed_dist = pd.char_dist[placed_idx]
            for c in common:
                placed_indices = placed_dist[c]
                new_indices = word_dist[c]
                for j in placed_indices:
                    for i in new_indices:
                        if p_vertical:
                            # placed runs vertically; new word runs horizontally
                            ny, nx, nv = py + j, px - i, False
                        else:
                            # placed runs horizontally; new word runs vertically
                            ny, nx, nv = py - i, px + j, True
                        pos = (ny, nx, nv)
                        if pos in seen:
                            continue
                        seen.add(pos)
                        yield pos

    def _fits(self,
              pd: ProcessData,
              word: str,
              y: int,
              x: int,
              vertical: bool) -> bool:
        # the cells flanking the word in its own direction must not be part
        # of another word in the *same* direction — otherwise we would
        # silently extend / be extended by an existing word ('embedding').
        # A flanking cell that belongs only to a perpendicular word is fine,
        # because that's just a neighbour, not a continuation.
        if vertical:
            before, after = (y - 1, x), (y + len(word), x)
            same_dir_cells = pd.v_cells
        else:
            before, after = (y, x - 1), (y, x + len(word))
            same_dir_cells = pd.h_cells
        if before in same_dir_cells or after in same_dir_cells:
            return False

        for (cy, cx), ch in self._cells(word, y, x, vertical):
            existing = pd.grid.get((cy, cx))
            if existing is not None and existing != ch:
                return False
            # else: cell empty, or matches existing letter (valid crossing)
        return True

    @staticmethod
    def _cells(word: str,
               y: int,
               x: int,
               vertical: bool) -> list[tuple[tuple[int, int], str]]:
        if vertical:
            return [((y + i, x), ch) for i, ch in enumerate(word)]
        return [((y, x + i), ch) for i, ch in enumerate(word)]

    def _place(self,
               pd: ProcessData,
               word: str,
               y: int,
               x: int,
               vertical: bool) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        """ write newly added grid cells AND record direction-typed cells.

        Returns (owned_grid_cells, all_cells_for_this_placement) so unplace
        can revert both pd.grid and pd.h_cells / pd.v_cells precisely.
        """
        owned: list[tuple[int, int]] = []
        all_cells: list[tuple[int, int]] = []
        cells_set = pd.v_cells if vertical else pd.h_cells
        for (cy, cx), ch in self._cells(word, y, x, vertical):
            if (cy, cx) not in pd.grid:
                pd.grid[(cy, cx)] = ch
                owned.append((cy, cx))
            cells_set.add((cy, cx))
            all_cells.append((cy, cx))
        return owned, all_cells

    # helpers

    @staticmethod
    def _char_distribution(word: str) -> dict[str, list[int]]:
        out: dict[str, list[int]] = {}
        for i, c in enumerate(word):
            out.setdefault(c, []).append(i)
        return out

    @staticmethod
    def _extend_bounds(cur: tuple[int, int, int, int],
                       word_len: int,
                       y: int,
                       x: int,
                       vertical: bool) -> tuple[int, int, int, int]:
        """ extend (min_y, max_y, min_x, max_x) by a hypothetical placement """
        min_y, max_y, min_x, max_x = cur
        if vertical:
            new_min_y = y if y < min_y else min_y
            end_y = y + word_len - 1
            new_max_y = end_y if end_y > max_y else max_y
            return (new_min_y, new_max_y, min_x, max_x)
        else:
            new_min_x = x if x < min_x else min_x
            end_x = x + word_len - 1
            new_max_x = end_x if end_x > max_x else max_x
            return (min_y, max_y, new_min_x, new_max_x)

    @staticmethod
    def _record_if_better(pd: ProcessData) -> None:
        min_y, max_y, min_x, max_x = pd.bounds_stack[-1]
        size = (max_y - min_y + 1) * (max_x - min_x + 1)
        if pd.best_size == 0 or size < pd.best_size:
            pd.best_size = size
            pd.best_grid = dict(pd.grid)
            pd.best_bounds = (min_y, max_y, min_x, max_x)
            pd.best_placements = list(pd.placements)


class CrosswordsProblem(IPOProblem[InputData, ProcessData, OutputData]):
    """ binds Input/Process/Output classes to the generic IPO solver """

"""
Inline copies of the data/example_N.txt files
"""

EXAMPLE_1 = """\
# Beispiel 1, Platz<=28
MATSE, NETT, ESSEN, HUNGER
"""

EXAMPLE_2 = """\
# Beispiel 2, Platz<=36
AUTO, LADUNG, UNGARN, MILCH
"""

EXAMPLE_3 = """\
# Beispiel 3, Platz<=85
AUTO, LADUNG, UNGARN, MILCH, ESSEN, VERSUCH, MATHEMATIK, INFORMATIK, PROGRAMMIERUNG
"""

EXAMPLE_4 = """\
# Beispiel 4, Platz<=98
PRUEFUNG, AUFGABE, MATHEMATIK, INFORMATIK, PROGRAMMIERUNG, ZEIT
"""

EXAMPLE_5 = """\
# Beispiel 5, Platz<=98
PROGRAMMIERUNG, ZEIT, KONZENTRATION, RECHNEN, ERGEBNIS, INTEGRAL, STOCHASTIK, STATISTIK
"""

def solve_all_examples(with_filled: bool = False) -> None:
    examples: list[tuple[str, str]] = [
        ("example_1", EXAMPLE_1),
        ("example_2", EXAMPLE_2),
        ("example_3", EXAMPLE_3),
        ("example_4", EXAMPLE_4),
        ("example_5", EXAMPLE_5),
    ]
    CrosswordsProblem.of(
        input=StreamProducer(examples),
        process=CrosswordSolver(),
        output=ConsoleConsumer(with_filled=with_filled),
    ).solve()


if __name__ == "__main__":
    solve_all_examples()
