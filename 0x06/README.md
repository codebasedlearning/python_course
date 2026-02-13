[© A.Voß, FH Aachen, codebasedlearning.dev](mailto:info@codebasedlearning.dev)

# Unit `0x06` – Scopes and language features


## Topics covered

- scopes and LEGB rule
- lambdas
- file io
- context managers
- match


## Tasks

---

### 👉 Task 'Ancestor Clove' 

- Think about how you could design a 'Timer' class implementing the 'ContextManager' protocol to measure time. Test it.
- What would a function 'timer' look like that uses '@contextmanager.' Also test it.

In both cases you can use the `fib(n)` function as a workload.
```
def fib(n):
    return fib(n-1)+fib(n-2) if n >= 3 else 1 if n >= 1 else 0
```

---

### 👉 Task 'Barren Grass' 

- Implement a context manager `Note` so that you get output indented by level. Example:

``` 
def show_loops():
    items = [2, 3, 5, 7, 11]
    number = 24
    with Note() as note:
        note(" 1| start loops")
        with note:
            for i in items:
                if number % i == 0:
                    note(f"{i} | {number}")
                    with note:
                        if i == 3:
                            note("found 3!")
                note.print(f"{i} checked")
        note.print(" 2| end")
```

Output:
```
 1| start loops
    2 | 24
    2 checked
    3 | 24
        found 3!
    3 checked
    5 checked
    7 checked
    11 checked
 2| end
```

---

### 👉 Task 'Moon Ragweed' 

- Write your own `my_closing` class and/or function so that this code works:
```
def close_a_context_manager():
    class Resource:
        def close(self):
            print(" a|   clean me")

    print(f" 1| use Resource with closing ver 1")
    with my_closing1(Resource()) as res:
        print(f"    type res: {type(res)}")
    print(f" 2| after using Resource")

    print(f" 3| use Resource with closing ver 2")
    with my_closing2(Resource()) as res:
        print(f"    type res: {type(res)}")
    print(f" 4| after using Resource")
```

---

### 👉 Task 'Drowsy Pudina'

- Create a context manager `readable_file` so that this code both opens and closes the file.

```
    with readable_file(filename) as reader:
        text = reader.readlines()
```

### 👉 Task 'Eastern Rye'

The `match` snippet contains the `from_chat` function, which decides which 
formatter to create based on the arguments passed.
- Change the function implementation to use only the `match` command for selection.

Hint: The arguments can be part of the match condition.

---

### 👉 Task 'Self-Study'

- Review all snippets from the lecture. Ask if there are any outstanding questions.

---

### 👉 Task 'Recap'

- Review any outstanding tasks from previous units. Is there any task that you should definitely do or have questions about?

---

### 👉 Task 'Couch Potato' - Recurring homework

- If you did not finish the essential tasks in the exercise, finish them at home.

---

### 👉 Comprehension Check – Talk with your Neighbor

General
- What is the main reason behind a 'context manager'?
- What is a 'scope,' and what kind of scopes do you know?
- What happens exactly when you import something?

---

### 👉 Lecture Check - Online Questionare

- Please participate in the survey: [Slido](https://wall.sli.do)

---

End of `Unit 0x08`
