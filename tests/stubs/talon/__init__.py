import inspect
from typing import Callable


class RegisteredActionsAccessor:
    def __init__(self, registered_actions, namespace):
        self.registered_actions = registered_actions
        self.namespace = namespace

    def __getattr__(self, name):
        for category in ("test", "module"):
            cat_actions = self.registered_actions[category]["namespaced"]
            if self.namespace in cat_actions:
                if name in cat_actions[self.namespace]:
                    return cat_actions[self.namespace][name]

        print(self.registered_actions)
        raise AttributeError(f"Couldn't find action {self.namespace}.{name}")


class Actions:
    """
    Implements something like talon.actions. You can use the register
    function to add in an action definition from your test (e.g. a mock).
    """

    def __init__(self):
        self.registered_actions = {
            "module": {"non_namespaced": {}, "namespaced": {}},
            "test": {"non_namespaced": {}, "namespaced": {}},
            # "contexts": []
        }

        # Some built in actions
        self.register_module_action("", "key", lambda x: None)
        self.register_module_action("", "insert", lambda x: None)
        self.register_module_action("", "sleep", lambda x: None)
        self.register_module_action("edit", "selected_text", lambda: "test")

    def reset_test_actions(self):
        self.registered_actions["test"] = {"non_namespaced": {}, "namespaced": {}}

    def register_module_action(self, namespace: str, name: str, func: Callable):
        """
        Registers an action to the module category. This should
        only be called by importing files containing module definitions.
        It won't be reset between test runs (or test files). Use
        register_test_action and reset_test_actions to temporarily override
        actions.
        """

        self._register_action("module", namespace, name, func)

    def register_test_action(self, namespace: str, name: str, func: Callable):
        """
        Registers the given action, use like:

            actions.register("user.my_action", lambda: None)
        """

        self._register_action("test", namespace, name, func)

    def _register_action(
        self, category: str, namespace: str, name: str, func: Callable
    ):
        if namespace == "":
            self.registered_actions[category]["non_namespaced"][name] = func
        else:
            if namespace not in self.registered_actions[category]["namespaced"]:
                self.registered_actions[category]["namespaced"][namespace] = {}

            self.registered_actions[category]["namespaced"][namespace][name] = func

    def __getattr__(self, name):
        callable = None
        try:
            callable = object.__getattribute__(self, name)
        except AttributeError:
            pass

        if callable:
            return callable

        found_namespace = False
        for category in ("test", "module"):
            # Prefer test to module to allow overriding in tests
            cat_actions = self.registered_actions[category]
            if name in cat_actions["non_namespaced"]:
                return cat_actions["non_namespaced"][name]
            elif name in cat_actions["namespaced"]:
                found_namespace = True

        if not found_namespace:
            raise RuntimeError(
                f"{name} action namespace not found, have you imported"
                " your code under test?"
            )

        return RegisteredActionsAccessor(self.registered_actions, name)


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


class Settings:
    """
    Implements something like talon.settings
    """


actions = Actions()
app = None
clip = None
imgui = ImgUI()
ui = UI()
settings = Settings()

# Indicate to test files that they should load since we're running in test mode
test_mode = True
