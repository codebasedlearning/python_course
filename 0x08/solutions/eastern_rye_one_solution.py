# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Eastern Rye' """


import unittest


class Formatter:
    ...


class JsonFormatter(Formatter):
    ...


class XmlFormatter(Formatter):
    ...


def from_chat(text: str | None = None, force_json: bool = False, force_xml: bool = False) -> Formatter | None:
    # classical
    # if force_json or "json" in text:
    #     return JsonFormatter()
    # elif force_xml or "xml" in text:
    #     return XmlFormatter()
    # else:
    #     return None  # raise RuntimeError("not enough information to choose a formatter")

    # maybe ok, pro/con?
    match [force_json, force_xml, text]:
        case [True, False, _]:
            return JsonFormatter()
        case [_, False, str()] if "json" in text:
            return JsonFormatter()
        case[False, True, _]:
            return XmlFormatter()
        case[False, _, str()] if "xml" in text:
            return XmlFormatter()
        case _:
            return None

    # ugly?
    # match [force_json or "json" in text, force_xml or "xml" in text]:
    #     case [True, False]:
    #         return JsonFormatter()
    #     case [False, True]:
    #         return XmlFormatter()
    #     case _:
    #         return None


class TestFactory(unittest.TestCase):
    def test_from_chat(self):
        self.assertIsNone(from_chat('Lorem Ipsum'))
        self.assertIsInstance(from_chat('Lorem json Ipsum'), JsonFormatter)
        self.assertIsInstance(from_chat('Lorem Ipsum', force_json=True), JsonFormatter)
        self.assertIsNone(from_chat('Lorem json', force_json=True, force_xml=True))
        self.assertIsInstance(from_chat('Lorem xml Ipsum'), XmlFormatter)
        self.assertIsInstance(from_chat('Lorem Ipsum', force_xml=True), XmlFormatter)
        self.assertIsNone(from_chat('Lorem xml', force_json=True, force_xml=True))


if __name__ == "__main__":
    unittest.main()
