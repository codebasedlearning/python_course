# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Drowsy Pudina' """

from contextlib import contextmanager, closing


@contextmanager
def readable_file(file_path):
    file = open(file_path, mode="r")
    try:
        yield file
    finally:
        file.close()


def read_file(filename):
    try:
        print(f" 1| try to open '{filename}'")
        with readable_file(filename) as reader:
            text = reader.readlines()
            print(f"    lines: {text}")
        print(f"    reader closed? {reader.closed}")
    except OSError as e:
        print(f"    -> IO error: {e}")
    print()


def main():
    filename_r = "../snippets/c_language/ihk_exam_sample.txt"
    read_file(filename_r)


if __name__ == "__main__":
    main()
