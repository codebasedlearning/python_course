# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about meta-classes.

Teaching focus
  - metaclass
"""


class RequiresRunMeta(type):
    def __new__(cls, name, bases, class_dict):
        if 'run' not in class_dict:
            raise TypeError(f"Class '{name}' must define a 'run' method.")
        return super().__new__(cls, name, bases, class_dict)

# -> Task = RequiresRunMeta('Task', (object,), class_dict)
class Task(metaclass=RequiresRunMeta):
    def run(self):
        print("Running task...")

def require_class_structure():
    """ example for RequiresRunMeta """
    print("\nrequire_class_structure\n=======================")

    # class BrokenTask(metaclass=RequiresRunMeta): pass


plugin_registry = {}

class PluginMeta(type):
    def __new__(cls, name, bases, class_dict):
        new_class = super().__new__(cls, name, bases, class_dict)
        if not name.startswith("Base"):
            plugin_registry[name] = new_class
        return new_class

class BasePlugin(metaclass=PluginMeta):
    pass

class MyPlugin(BasePlugin):
    def run(self):
        print("I am a plugin.")

class AnotherPlugin(BasePlugin):
    def run(self):
        print("Another plugin.")

def register_all_classes():
    """ example for registering classes """
    print("\nregister_all_classes\n====================")

    print(plugin_registry)

if __name__ == "__main__":
    require_class_structure()
    register_all_classes()
