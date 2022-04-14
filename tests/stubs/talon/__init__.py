from typing import Callable


class DictAccessor:
    def __init__(self, dict):
        self.dict = dict

    def __getattr__(self, name):
        return self.dict[name]


class Actions:
    """
    Implements something like talon.actions. You can use the register
    function to add in an action definition from your test (e.g. a mock).
    """

    def __init__(self):
        self.reset_actions()

    def reset_actions(self):
        self.registered_actions = {"user": {}, "edit": {}}
        self.edit = self._build_namespace_accessor("edit")
        self.user = self._build_namespace_accessor("user")

    def register_test_action(self, name: str, func: Callable):
        """
        Registers the given action, use like:

            actions.register("user.my_action", lambda: None)
        """

        namespace, action_name = name.split(".")
        self.registered_actions[namespace][action_name] = func

    def key(self, key):
        """
        Stub out actions.key
        """

        pass

    def _build_namespace_accessor(self, key):
        return DictAccessor(self.registered_actions[key])


class Module:
    """
    Implements something like the Module class built in to Talon
    """

    def list(self, *args, **kwargs):
        pass

    def setting(self, *args, **kwargs):
        pass

    def capture(self, rule=None):
        def __funcwrapper(func):
            def __inner(*args, **kwargs):
                return func(*args, **kwargs)

            return __inner

        return __funcwrapper

    def action_class(self, target_class):
        # TODO: Register all the actions on the action class with Actions.register
        return target_class


class Context:
    """
    Implements something like the Context class built in to Talon
    """

    lists = {}

    def action_class(self, path=None):
        def __funcwrapper(clazz):
            return clazz
        return __funcwrapper


class ImgUI:
    """
    Stub out ImgUI so we don't get crashes
    """

    GUI = None

    def open(self):
        def __funcwrapper(func):
            def __inner(*args, **kwargs):
                return func(*args, **kwargs)

            return __inner

        return __funcwrapper

class UI:
    """
    Stub out UI so we don't get crashes
    """

    def register(*args, **kwargs):
        pass

actions = Actions()
app = None
clip = None
imgui = ImgUI()
ui = UI()

# Indicate to test files that they should load
test_mode = True
