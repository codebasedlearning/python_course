# (C) 2023 A.Voß, a.voss@fh-aachen.de, python@codebasedlearning.dev

""" This snippet demonstrates some functions from the data model.  """


class LoggingDict:
    def __init__(self):
        self.log_dict = {}

    def __getitem__(self, key):                                     # (A) data model
        print(f"0a| getitem, key={key}")
        return self.log_dict[key]

    def __setitem__(self, key, value):      # also __delitem__
        print(f"0b| setitem, key={key}, value={value}")
        self.log_dict[key] = value
        #return super().__setitem__(key, value)

    def __len__(self):
        print(f"0c| len")
        return self.log_dict.__len__()

    def __iter__(self):
        return iter(self.log_dict)

    # in
    #def __contains__(self, name):
    #    return name.lower() in self._spells


    def items(self):                # same for keys(), values()
        return self.log_dict.items()


def using_logging_dicts():
    ld = LoggingDict()
    ld[1] = "one"
    ld["two"] = 2
    print(f"01| ld={ld}, len={len(ld)}")

    for item in ld.log_dict:                                   # keys .keys()

        print(f"02|   item={item}")

    for i, item in ld.log_dict.items():                                   # keys
        print(f"02|   i={i}, item={item}")

    for item in ld:                           # keys, values
        print(f"03|   item={item}")

    for item in ld.items():                           # keys, values
        print(f"03|   item={item}")

    #for i, item in enumerate(ld.items()):                           # keys, values
    #    print(f"03|   i={i}, item={item}")

    #ints = filter(lambda it: isinstance(it[1][0], int), enumerate(ld.items()))
    #print(f"04| ints={ints}, *ints={[*ints]}\n")



def main():
    using_logging_dicts()


if __name__ == "__main__":
    main()


"""
(A) data model
    see https://docs.python.org/3.6/reference/datamodel.html
"""
