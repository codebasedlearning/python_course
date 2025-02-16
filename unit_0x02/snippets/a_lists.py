# (C) 2024 A.Voß, a.voss@fh-aachen.de, python@codebasedlearning.dev

"""
Lists
  - todo

Refs
  - https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
  - https://www.w3schools.com/python/python_lists_methods.asp
"""


def using_lists():
    print("\nusing_lists\n===========")

    data = [2, 3, 5, "seven"]                                       # lists, mutable, objects of different type
    # data: list[int | str] = [2, 3, 5, "seven"]                    # with type hint
    print(f" 1| {data=}, {len(data)=}, {type(data)=}")

    single = [1, ]                                                  # =[1] both lists, cf. tuple
    print(f" 2| [1,]={single}")


def non_modifying_list_ops():
    print("\nnon_modifying_list_ops\n======================")

    data = [2, 3, 5, "seven"]
    print(f" 1| {data=}")
    print(f" 2| {data[1]=}")                                        # index access, 0-based, read
    print(f" 3| {data.index(3)=}")                                  # find or exception
    print(f" 4| {(5 in data)=} {(6 in data)=}")                     # contains
    print(f" 5| {(11 not in data)=}")                               # contains not

    print(f" 6| traverse: ", end='')
    for n in data:                                                  # traverse
        print(f"{n=} ", end='')
    print()

    print(f" 7| slicing: {data[-2:]=}")                             # start=length-2, end=length(ecl.)


def modifying_list_ops():
    print("\nmodifying_list_ops\n==================")

    data = [2, 3, 5]
    print(f" 1| {data=}")

    data[0] = 1
    print(f" 2| set [0]=1: {data}")                                 # write

    data.append(7)
    print(f" 3| append 7: {data}")

    data.extend([11, 13, 17])
    print(f" 4| extend [11, 13, 17]: {data}")

    data.remove(13)                                                 # remove object
    print(f" 5| remove of 13: {data}")

    item = data.pop(2)                                              # remove at index
    print(f" 6| pop at 2: {data}, item={item}")

    data.reverse()
    print(f" 7| reverse: {data}")

    data.sort()
    print(f" 8| sort: {data}")

    data.clear()
    print(f" 9| clear: {data}")

    data = [1, 3, 5] + [2, 4]
    print(f"10| +={data}")

    del data[1:4:2]                                                 # index 1, 3
    print(f"11| del [1:4:2]: {data}")

    del data[:]                                                     # all indices, i.e. clear
    print(f"12| del [:]: {data}")


def shallow_and_deep():
    print("\nshallow_and_deep\n================")

    data = [2, 3, 5]                                                # working on one object
    data_ref = data
    print(f" 1| same object: {data=}, {data_ref=}, {(data == data_ref)=}")
    print(f"      {id(data)=}, {id(data_ref)=}, {(data is data_ref)=}")
    data[2] = 7                                                     # modifying only 'data'
    print(f"      set [2]=7: {data=}, {data_ref=}")                 # same for both

    data_copy = list(data)                                          # creates copy
    print(f" 2| two objects: {data=}, {data_copy=}, {(data == data_copy)=}")
    print(f"      {id(data)=}, {id(data_copy)=}, {(data is data_copy)=}")
    data[2] = 11                                                    # modifying only 'data'
    print(f"      set [2]=11: {data=}, {data_copy=}, {(data == data_copy)=}")

    list1 = ['X']
    item = [23]
    list1.append(item)
    list2 = list(list1)                                             # no deep copy
    print(f" 3| {list1=}, {list2=}, {(list1 == list2)=}")

    item[0] = 42                                                    # same item affected in list1 and list2
    print(f"      set item[0]=42: {list1=}, {list2=}, {(list1 == list2)=}")


if __name__ == "__main__":
    using_lists()
    non_modifying_list_ops()
    modifying_list_ops()
    shallow_and_deep()
