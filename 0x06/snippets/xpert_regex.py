# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about regular expressions with the re module.

Teaching focus
  - re.search, re.match, re.findall, re.sub
  - groups and named groups
  - re.compile for repeated patterns
  - re.VERBOSE for readable patterns
  - common practical patterns

You know regex. Python's 're' module follows the PCRE tradition
with a few Python-specific additions (named groups, VERBOSE mode).

See also
  https://docs.python.org/3/library/re.html
  https://docs.python.org/3/howto/regex.html
"""

import re

from utils import print_function_header


"""
Topic: Basic matching
"""


@print_function_header
def basic_matching():
    """ search, match, and findall """

    text = "The quick brown fox jumps over 2 lazy dogs at 3pm."

    # re.search: find the FIRST match anywhere in the string
    m = re.search(r"\d+", text)
    print(f" 1| search found: '{m.group()}' at position {m.start()}")

    # re.match: match only at the BEGINNING of the string
    m = re.match(r"The", text)
    print(f" 2| match at start: '{m.group()}'" if m else " 2| no match")

    m = re.match(r"quick", text)            # does NOT search inside
    print(f" 3| match 'quick': {m}")        # None

    # re.findall: return ALL non-overlapping matches as a list
    numbers = re.findall(r"\d+", text)
    print(f" 4| all numbers: {numbers}")

    words = re.findall(r"\b\w{4,}\b", text)         # words with 4+ characters
    print(f" 5| long words: {words}")

    # re.fullmatch: the ENTIRE string must match the pattern
    print(f" 6| fullmatch 'abc': {re.fullmatch(r'[a-z]+', 'abc')}")
    print(f" 7| fullmatch 'ab3': {re.fullmatch(r'[a-z]+', 'ab3')}")


"""
Topic: Groups and named groups
"""


@print_function_header
def groups_and_named_groups():
    """ extract structured data with groups """

    # parentheses create capturing groups
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", "Today is 2025-01-15, a Wednesday.")
    if m:
        print(f" 1| full match: '{m.group()}'")
        print(f" 2| year={m.group(1)}, month={m.group(2)}, day={m.group(3)}")

    # named groups: (?P<name>pattern)
    pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
    m = re.search(pattern, "deadline: 2025-06-30")
    if m:
        print(f" 3| named: year={m.group('year')}, month={m.group('month')}")
        print(f" 4| as dict: {m.groupdict()}")

    # findall with groups returns tuples
    log = "ERROR 10:15 disk full, WARN 10:16 low memory, ERROR 10:17 timeout"
    entries = re.findall(r"(ERROR|WARN)\s(\d{2}:\d{2})\s(.+?)(?:,|$)", log)
    print(f" 5| log entries: {entries}")


"""
Topic: Substitution
"""


@print_function_header
def substitution():
    """ re.sub for search-and-replace """

    # simple replacement
    text = "Hello World, Hello Python"
    result = re.sub(r"Hello", "Hi", text)
    print(f" 1| simple: '{result}'")

    # replacement with backreference
    text = "John Smith, Jane Doe"
    swapped = re.sub(r"(\w+) (\w+)", r"\2, \1", text)          # swap first/last
    print(f" 2| swapped: '{swapped}'")

    # replacement with a function
    def censor(match):
        word = match.group()
        return word[0] + "*" * (len(word) - 1)

    text = "The password is secret and the code is hidden"
    censored = re.sub(r"\b(secret|hidden)\b", censor, text)
    print(f" 3| censored: '{censored}'")

    # re.subn returns (result, count)
    result, count = re.subn(r"\d", "#", "abc123def456")
    print(f" 4| subn: '{result}' ({count} replacements)")


"""
Topic: Compiled patterns and VERBOSE mode
"""


@print_function_header
def compiled_and_verbose():
    """ re.compile and re.VERBOSE for maintainable regex """

    # re.compile: pre-compile for repeated use (efficiency + clarity)
    email_pattern = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")

    emails = [
        "alice@example.com",
        "not-an-email",
        "bob.smith+tag@company.co.uk",
        "also@not@valid",
    ]

    valid = [e for e in emails if email_pattern.fullmatch(e)]
    print(f" 1| valid emails: {valid}")

    # re.VERBOSE: ignore whitespace and allow comments in the pattern
    url_pattern = re.compile(r"""
        (?P<scheme>https?)://           # http or https
        (?P<host>[\w.-]+)              # hostname
        (?::(?P<port>\d+))?            # optional port
        (?P<path>/[\w/.-]*)?           # optional path
    """, re.VERBOSE)

    urls = [
        "https://example.com/path/to/page",
        "http://localhost:8080/api/v1",
    ]

    for url in urls:
        m = url_pattern.search(url)
        if m:
            print(f" 2| {m.group('scheme')}://{m.group('host')}"
                  f" port={m.group('port')} path={m.group('path')}")


"""
Topic: Practical patterns
"""


@print_function_header
def practical_patterns():
    """ common real-world regex tasks """

    # split on multiple delimiters
    data = "one,two;three four\tfive"
    parts = re.split(r"[,;\s]+", data)
    print(f" 1| split: {parts}")

    # extract key-value pairs from a config-like string
    config = "host=localhost port=5432 db=mydb timeout=30"
    pairs = dict(re.findall(r"(\w+)=(\S+)", config))
    print(f" 2| config: {pairs}")

    # validate and extract from structured text
    version_str = "Python 3.12.1 (main, Dec 2024)"
    m = re.search(r"Python (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)", version_str)
    if m:
        print(f" 3| version: {m.group('major')}.{m.group('minor')}.{m.group('patch')}")

    # non-greedy vs greedy
    html = "<b>bold</b> and <i>italic</i>"
    greedy = re.findall(r"<.+>", html)      # matches as MUCH as possible
    non_greedy = re.findall(r"<.+?>", html)           # matches as LITTLE as possible
    print(f" 4| greedy:     {greedy}")
    print(f" 5| non-greedy: {non_greedy}")

    # lookahead and lookbehind
    text = "100px 200em 300px 50%"
    px_values = re.findall(r"\d+(?=px)", text)        # digits followed by 'px'
    print(f" 6| px values: {px_values}")

    after_dollar = re.findall(r"(?<=\$)\d+", "price $42 discount $10")
    print(f" 7| after $: {after_dollar}")


if __name__ == "__main__":
    basic_matching()
    groups_and_named_groups()
    substitution()
    compiled_and_verbose()
    practical_patterns()
