[© 2025, Alexander Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x04` – Puzzle-Driven Programming Challenges 


> Python is well known for its ability to quickly write scripts and proof of concepts. Today we are going to practise both, by building a quick solution to a problem (puzzle) and then doing a proper refactoring of it.

> As well as the fun part, there is also a very practical side. Many companies use coding challenges as part of the application process for software developers; you are given a limited amount of time to find and present a solution to a specific problem. We also have such a situation at the well-known "Grosse Prog".


## Inspiration

### Advent of Code

The first puzzles presented are inspired by those from [Advent of Code](https://adventofcode.com) For scientific purposes, I have used only the basic concept and included 
self-generated data specific to the task to avoid any legal issues.

For more information and to enjoy the engaging story, please visit the website and register for next Christmas! Finally, I would like to thank Eric Wastl, who invented and organized 'Advent of Code.'

### LeetCode

LeetCode is an online platform for improving coding skills, preparing for technical interviews, and solving algorithm and data structure problems. A sample list of questions can be found here [Top Interview 150](https://leetcode.com/studyplan/top-interview-150).


## Puzzle Structure

Each original puzzle consists of two parts. The first part can usually be completed fast with a straightforward approach, prioritizing speed over beauty — also known as a 'hack'.
The second part often involves a significant increase in complexity as the problem or solution space explodes. In many cases, it is essential to improve your solution concept, for example, by developing or using a clever approach to reduce the order or number of algorithmic iterations.

Here we add refactoring as the third part, so we have:
- Complete Part 1 as quickly as possible.
- Same for Part 2. It is explicitly allowed to simply 'hack' your solution.
- Then, in Part 3, refactor your solution to be as Pythonic and object-oriented as possible. This means using or creating appropriate (data) classes and hierarchies, aiming for efficiency in your algorithms and solutions, and considering best practices. 




## Input Data

Parts 1 and 2 typically introduce the problem and provide sample data before addressing the actual input data.
All data is provided in the form of text files in `data/`, e.g. 
```
- tinted_coast_example1.txt
- tinted_coast_example2.txt
- tinted_coast_input.txt
```

If the format of a line is given, you can rely on it. For example, if the explanation states that a line has this form 
```
10: 23, 46
```
starting with an identifier (10), followed by a colon and then a list of integer numbers (23, 46) separated with commas, then there is no need to check syntax or semantics. Note, however, the text file may end with a line break.

> As a rule, you cannot assume that the data you receive from an external source is in the correct format, even if someone claims that it is. In general, it is important to handle corrupt or malicious data.

> Here, we want to improve our problem-solving skills and focus on the algorithmic side. So, all files are formatted as promised.

## Overview

- 'Tinted Coast' – find numbers in strings
- 'Lonely Seafront' – analyze game values
- 'Stonenet Sands' – 2D grid symbol search
- 'Tortoise Cove' – simulate winning scratchcards
- 'AoC Originals' – hand-picked examples

## Puzzles

---

### 👉 Puzzle 'Tinted Coast' (Calibration Values)

You are given a list of strings. Each line contains a mix of letters and digits. Your task is to extract digits from each line in a specific way and compute the sum of the results.

#### Part 1

From each line extract the first digit and the last digit that appears (ignore all letters) and combine them to form a two-digit number. For example:

- "a1b2c3" → first digit is 1, last digit is 3 → number is 13.
- "x8x" → 88.
- "abc" → no digits → 0.

Sum all the resulting two-digit numbers, this is the puzzle solution.

#### Example 1

```
1hhex0xrcsn
q0g0argw
8osi6w
6egyk5
ordmc6ltizb1jutl
```

The puzzle solution is `10+0+86+65+61=222`.

#### Part 2

The twist: digits can be written as words, and those count too! So you must also consider:
- "one" → 1, "two" → 2, …, "nine" → 9

But here’s the catch:
- The digit words may overlap or be embedded within other letters.
- You still extract the first and last digit, now allowing digit words as valid digits too.

What is now the sum of all values?

#### Example 2

``` 
zeroioufourflthreegv
uwonevtwoyythree6b
uoe1eh9xsfivesml7e
ra0twoyusixdjsixfoa7qy
eoneyffoureightpa
```

The puzzle solution (part 2) is `3+16+17+7+18=61`.

#### Part 3

- Refactor your solution to be as Pythonic and object-oriented as possible.
- Use `pylint` to detect issues.
- Feed an AI agent (ChatGPT etc.) with your solution.

You will find the original task [here](https://adventofcode.com/2023/day/1)

#### Solutions

|           |   Part 1 | Part 2 |
|:---------:|---------:|-------:|
| Example 1 |      222 |        |
| Example 2 |       90 |     61 |
|   Input   |    44161 |  51119 |

---

### 👉 Puzzle 'Lonely Seafront' (Cube Games)

You are given a list of 'games'. Each game consists of multiple rounds, and in each round, a number of colored cubes (red, green, blue) is shown.

Each game is described like this:

```
Game 4: 5 red; 17 red, 15 blue; 12 red, 7 blue, 11 green
```

This means:
- Game 4 has three rounds:
- Round 1: 5 red
- Round 2: 17 red, 15 blue
- Round 3: 12 red, 7 blue, 11 green

#### Part 1

You’re told that the maximum number of cubes available per color is:
12 red, 13 green, 14 blue.

Parse each game and check if any round exceeds the allowed cube limits. If the game is possible (i.e. all rounds stay within the cube limits), then it’s valid.

Determine the sum of the IDs of all valid games.

#### Example 1

```
Game 1: 5 red, 2 green
Game 2: 8 blue; 2 red, 5 blue, 8 green
Game 3: 19 green, 3 blue, 4 red; 11 green; 11 red; 7 green, 7 red; 2 blue, 6 red
Game 4: 5 red; 17 red, 15 blue; 12 red, 7 blue, 11 green
Game 5: 11 red, 10 green; 16 blue, 11 green
```

Here only games 1 and 2 are valid, so the solution is `1+2=3`.

#### Part 2

For each game, determine the minimum number of cubes required to make all the rounds possible.
- For each color, find the maximum count used in any round.
- Multiply these three maximums to get the game’s 'power'.
- Return the sum of all games’ powers.

Example Game:
```
Game 4: 5 red; 17 red, 15 blue; 12 red, 7 blue, 11 green
```
Max red = 17, max green = 11, max blue = 15, so the 'power' is `17 × 11 × 15 = 2805`.

Do this for every game and sum all powers.

#### Example 1

The sum of all powers in the example is `0+128+627+2805+1936=5496`.

#### Part 3

- Refactor your solution to be as Pythonic and object-oriented as possible.
- Use `pylint` to detect issues.
- Feed an AI agent (ChatGPT etc.) with your solution.

You will find the original task [here](https://adventofcode.com/2023/day/2)

#### Solutions

|           | Part 1 |  Part 2 |
|:---------:|-------:|--------:|
| Example 1 |      3 |    5496 |
|   Input   |    542 |  206969 |

---

### 👉 Puzzle 'Stonenet Sands' (Symbols)

You are given a 2D grid where each cell contains one of:
- A digit (0-9)
- A period (.), which represents empty space
- A symbol (any non-digit, non-period character), like *, #, +, etc.

#### Part 1

Find all numbers in the grid that are adjacent to a symbol. A number is a sequence of digits (123, 8, etc.) and it is considered adjacent to a symbol if any of its digits are directly next to a symbol in the 8 neighboring positions (up, down, left, right, and the 4 diagonals).

Your task is to add up all these adjacent numbers.

#### Example 1

```
...$......
51..123...
..*.#...15
...23...24
.......*..
.....11.12
```
Explanation:
- 51 is adjacent to *
- 123 is adjacent to $ and #
- 23 is adjacent to * and #
- 24,11,12 are adjacent to *
- 15 is not placed next to any of the symbols

The sum is `51+123+23+24+11+12=244`.

#### Example 2

```
...$..1...
..305*+...
+..121....
.407#..80.
.#6..*....
....397..*
.#..*....*
..544.....
.428.....+
..184..339
```

The sum here is `2120`.

#### Part 2

Extra Rule: A gear is defined as a * symbol that is adjacent to exactly two numbers.

For each gear, find the two adjacent numbers, and calculate their product (called the gear ratio).
Sum all such gear ratios.

#### Examples

In the first grid the only gear ratio is `51*23=1173`. In the second example there is also only one, namely `397*544=215968`. In the final input data, there will be more than one of them.

#### Part 3

- Refactor your solution to be as Pythonic and object-oriented as possible.
- Use `pylint` to detect issues.
- Feed an AI agent (ChatGPT etc.) with your solution.

You will find the original task [here](https://adventofcode.com/2023/day/3)

#### Solutions

|           |    Part 1 |         Part 2 |
|:---------:|----------:|---------------:|
| Example 1 |       244 |           1173 |
| Example 2 |      2120 |         215968 |
|   Input   |    290027 |       15524298 |

---

### 👉 Puzzle 'Tortoise Cove' (Scratchcards)

Each line in your data represents a scratchcard. The format is:
```
Card No: winning_numbers | your_numbers
```
e.g.
```
Card 1: 17 43 71 97 | 8 33 37 56 71 73 96 97
```
where
- No is the card number.
- `winning_numbers` is a list of integers.
- `your_numbers` is another list of integers.

#### Part 1

For each card:
- Count how many numbers from `your_numbers` are in `winning_numbers`.
- If you have at least one match:
  - The first match gives you 1 point. 
  - Each additional match doubles the points, i.e. 1 match = 1 point, 2 matches = 2 points, 3 matches = 4 points, 4 matches = 8 points, etc.

What is the total score of all scratchcards?

#### Example 1

```
Card 1: 17 43 71 97 |  8 33 37 56 71 73 96 97
Card 2: 36 68 84 97 |  2 13 36 47 68 75 84 97
Card 3:  2 13 64 93 |  3  4  7 31 44 64 87 94
Card 4: 11 21 42 44 | 10 12 22 38 47 62 74 87
Card 5: 17 57 70 94 |  5 34 50 51 57 70 80 100
```

Explanation:
- Card 1 has 2 matching numbers ⇒ 2^1 = 2 points.
- Card 2 has 4 matches ⇒ 2^3 = 8 points.
- Card 3 has 1 match ⇒ 1 point.
- Card 4 has no match ⇒ 0 point.
- Card 5 has 2 match ⇒ 2^1 = 2 point.

The total score is `2+8+1+0+2=13`.

#### Part 2

This time, scratchcards can generate copies of other (following) scratchcards.
- Start with 1 of each card.
- If a card has k matching numbers, you win 1 copy of each of the next k cards.
- These extra cards can themselves generate further copies recursively.

Simulate this until all the cascading copies are resolved. How many total scratchcards do you end up with?

Important notes:
- You don’t 'play' beyond the last card — i.e., if you’re on Card 99 and win 3, you can only copy up to Card 100.
- Cards don’t generate more copies of themselves — only of following cards.

#### Example 1

Card 1 has 2 matches, and you have 1 copy of Card 1:
- You gain 1 copy each of Card 2 and Card 3.
- Then, those new cards also add more cards based on their own matches!

In this example you end up with 
`(1)+(1+1)+(1+1+2)+(1+2+4)+(1+2)=17`.

#### Part 3

- Refactor your solution to be as Pythonic and object-oriented as possible.
- Use `pylint` to detect issues.
- Feed an AI agent (ChatGPT etc.) with your solution.

You will find the original task [here](https://adventofcode.com/2023/day/4)

#### Solutions

|           | Part 1 |          Part 2 |
|:---------:|-------:|----------------:|
| Example 1 |     13 |              17 |
|   Input   |    503 | 203450115848628 |

---

### 👉 Puzzles 'AoC Originals' 

The examples selected in AoC are partly handmade and therefore not easy to simulate with own data, so I prefer to refer to the original task. Please note that you have to register to get the data.

There are a lot of 2D puzzles, so having a good and reusable class structure to deal with them might help.

My favourites are 'Cosmic Expansion' (warm-up), 'Step Counter', 'Claw Contraption' and 'Sand Slabs'.

### Level-1-Puzzle

- [2023 - Day 11 - Cosmic Expansion](https://adventofcode.com/2023/day/11)
- [2023 - Day 13 - Point of Incidence](https://adventofcode.com/2023/day/13)
- [2024 - Day 04 - Ceres Search](https://adventofcode.com/2024/day/4)
- [2024 - Day 25 - Code Chronicle - Part 1](https://adventofcode.com/2024/day/25)

### Level-1+-Puzzle

- [2023 - Day 21 - Step Counter - Part 1](https://adventofcode.com/2023/day/21)
- [2024 - Day 13 - Claw Contraption - Part 1](https://adventofcode.com/2024/day/13)
- [2024 - Day 17 - Chronospatial Computer - Part 1](https://adventofcode.com/2024/day/17)

### Level-2-Puzzle

- [2023 - Day 19 - Aplenty](https://adventofcode.com/2023/day/19)
- [2023 - Day 22 - Sand Slabs](https://adventofcode.com/2023/day/22)
- [2023 - Day 23 - A Long Walk](https://adventofcode.com/2023/day/23)

---

# Have fun!
