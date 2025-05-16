# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Moon Ragweed' """

from contextlib import contextmanager


class my_closing1:
    def __init__(self, obj):
        self.obj = obj

    def __enter__(self):
        return self.obj

    def __exit__(self, *args):
        self.obj.close()


@contextmanager
def my_closing2(obj):
    try:
        yield obj
    finally:
        obj.close()


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


if __name__ == "__main__":
    close_a_context_manager()
