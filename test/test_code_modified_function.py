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
            (["static"], "void", "code_private_static_function"),
            (["private"], "void", "code_private_function"),
            (["private", "static"], "void", "code_private_static_function"),
            (["protected"], "void", "code_protected_function"),
            (["protected", "static"], "void", "code_protected_static_function"),
            (["public"], "void", "code_public_function"),
            (["public", "static"], "void", "code_public_static_function"),
        ]

        for modifiers, return_type, target_action in examples:
            mock = MagicMock()
            actions.register_test_action("user", target_action, mock)

            talon.actions.user.code_modified_function(
                modifiers, return_type, "test func"
            )

            mock.assert_called_once()

        # code_default_function remains outside the for loop since it does not take in a return_type
        mock = MagicMock()
        actions.register_test_action("user", "code_default_function", mock)

        talon.actions.user.code_modified_function(0, return_type, "test func")

        mock.assert_called_once()
