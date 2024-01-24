import talon

if hasattr(talon, "test_mode"):
    from unittest.mock import MagicMock

    from talon import actions

    def setup_function():
        # Load our code under test (register code_* actions)
        import lang.tags.functions  # isort:skip

        actions.reset_test_actions()

    def test_calls_expected_function():
        """
        Test that the given combination of modifiers ends up delegating to the
        correct function
        """

        examples = [
            (0, "code_default_function"),
            (["static"], "code_private_static_function"),
            (["private"], "code_private_function"),
            (["private", "static"], "code_private_static_function"),
            (["protected"], "code_protected_function"),
            (["protected", "static"], "code_protected_static_function"),
            (["public"], "code_public_function"),
            (["public", "static"], "code_public_static_function"),
        ]
        for modifiers, target_action in examples:
            mock = MagicMock()
            actions.register_test_action("user", target_action, mock)

            talon.actions.user.code_modified_function(modifiers, "test func")

            mock.assert_called_once()
