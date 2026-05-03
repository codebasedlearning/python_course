# (C) A.Voss, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet discusses ...

Teaching focus
  -
"""

from utils import print_function_header


"""
Topic: Singleton pattern
"""


class DatabaseConnector:                    # problems?
    """ a class meant to be a singleton """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Call only the first time
        return cls._instance

    def __init__(self, connection_string):
        self.connection_string = connection_string


class ServiceDetector:
    """ a class meant to be a singleton - improved """
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, url):
        if not self._initialized:
            self.url = url
            self._initialized = True


@print_function_header
def define_a_singleton():
    """ define a singleton """

    db_connector = DatabaseConnector(connection_string="aws.com")
    database_access = DatabaseConnector(connection_string="azure.com")
    print(f" 1|    {id(db_connector)=}, connected to: '{db_connector.connection_string}'")
    print(f"    {id(database_access)=}, connected to: '{database_access.connection_string}'")

    main_service = ServiceDetector(url="//server")
    docker_service = ServiceDetector(url="//docker")
    print(f" 2|   {id(main_service)=}, ask here: '{main_service.url=}'")
    print(f"    {id(docker_service)=}, ask here: '{docker_service.url=}'")


"""
Topic: Factory methods
"""


class Color:
    """ color class with multiple factory methods """
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def from_hex(cls, hex_str: str) -> Self:
        """ create Color from hex string like '#FF8800' """
        hex_str = hex_str.lstrip('#')
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return cls(r, g, b)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """ create Color from a dictionary """
        return cls(r=data['r'], g=data['g'], b=data['b'])

    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b})"


@print_function_header
def show_factory_methods():
    """ multiple ways to create instances """

    c1 = Color(255, 136, 0)
    c2 = Color.from_hex("#FF8800")
    c3 = Color.from_dict({'r': 255, 'g': 136, 'b': 0})

    print(f" 1| direct:    {c1=}")
    print(f" 2| from_hex:  {c2=}")
    print(f" 3| from_dict: {c3=}")
    print(f" 4| {(c1.r == c2.r == c3.r)=}")

if __name__ == "__main__":
    define_a_singleton()
    show_factory_methods()
