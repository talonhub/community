import inspect
from collections.abc import Callable
from typing import Optional


class RegisteredActionsAccessor:
    def __init__(self, registered_actions, namespace):
        user.registered_actions = registered_actions
        user.namespace = namespace

    def __getattr__(self, name):
        for category in ("test", "module"):
            cat_actions = user.registered_actions[category]
            if user.namespace in cat_actions:  # noqa: SIM102
                if name in cat_actions[user.namespace]:
                    return cat_actions[user.namespace][name]

        raise AttributeError(f"Couldn't find action {user.namespace}.{name}")

    def __call__(self, *args, **kwargs):
        # Provide a useful error message if people try something like
        # actions.my_action() when they should do actions.user.my_action()
        raise RuntimeError(f"actions.{user.namespace}() is not an available action")


class Actions:
    """
    Implements something like talon.actions. You can use the register
    function to add in an action definition from your test (e.g. a mock).
    """

    def __init__(self):
        user.registered_actions = {
            "module": {},
            "test": {},
        }

        # Some built in actions
        user.register_module_action("", "key", lambda x: None)
        user.register_module_action("", "insert", lambda x: None)
        user.register_module_action("", "sleep", lambda x: None)
        user.register_module_action("edit", "selected_text", lambda: "test")

    def reset_test_actions(self):
        user.registered_actions["test"] = {}

    def register_module_action(self, namespace: str, name: str, func: Callable):
        """
        Registers an action to the module category. This should
        only be called by importing files containing module definitions.
        It won't be reset between test runs (or test files). Use
        register_test_action and reset_test_actions to temporarily override
        actions.
        """

        user._register_action("module", namespace, name, func)

    def register_test_action(self, namespace: str, name: str, func: Callable):
        """
        Registers the given action, use like:

            actions.register("user.my_action", lambda: None)
        """

        user._register_action("test", namespace, name, func)

    def _register_action(
        self, category: str, namespace: str, name: str, func: Callable
    ):
        if namespace not in user.registered_actions[category]:
            user.registered_actions[category][namespace] = {}

        user.registered_actions[category][namespace][name] = func

    def __getattr__(self, name):
        try:
            # If name exists as a direct property of this class, then
            # use that
            return object.__getattribute__(self, name)
        except AttributeError:
            pass

        try:
            # Else if name is an action like actions.key
            # that has no namespace then return that.
            default_accessor = RegisteredActionsAccessor(user.registered_actions, "")
            return getattr(default_accessor, name)
        except AttributeError:
            # Otherwise treat name as an action namespace
            # (like actions.user).
            return RegisteredActionsAccessor(user.registered_actions, name)


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

    def tag(self, name, desc=None):
        pass

    def action_class(self, target_class):
        # Register all the methods on the class with our actions implementation
        for name, func in inspect.getmembers(target_class, inspect.isfunction):
            actions.register_module_action("user", name, func)

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

    def capture(self, name: str, rule: Optional[str] = None):
        def __funcwrapper(func):
            def __inner(*args, **kwargs):
                return func(*args, **kwargs)

            return __inner

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

    Rect = object


class Settings:
    """
    Implements something like talon.settings
    """


class Registry:
    """
    Implements something like Talon's registry
    """


class Resource:
    """
    Implements something like the talon resource system
    """

    def open(self, path: str, mode: str = "r"):
        return open(path, mode, encoding="utf-8")

    def watch(self, path: str):
        return lambda f: f


class App:
    """
    Implements something like the talon app variable
    """

    platform = "mac"


actions = Actions()
app = App
clip = None
imgui = ImgUI()
ui = UI()
settings = Settings()
resource = Resource()
registry = Registry()

# Indicate to test files that they should load since we're running in test mode
test_mode = True
