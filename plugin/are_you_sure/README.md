# Are You Sure Dialog

This lets you require confirmation before executing an action, which can be useful for potentially destructive commands like shutting down your computer or exiting talon.

To require confirmation for an action, you use the user.are_you_sure_set_on_confirmation_action function that receives a message to display for the dialogue and the action to perform on confirmation. An optional action to perform on cancelling the action can be provided as the third argument. As this is intended to work with particularly destructive actions, this only supports executing a single action at a time and does not work with chaining.

You confirm an action by saying "yes I am sure" and cancel it by saying "cancel".

## Example

```python
from talon import actions, Module, app

mod = Module()
@mod.action_class
class Actions:
    def test_are_you_sure():
        '''A simple test for the are you sure dialog'''
        def on_confirm():
            app.notify('Confirmed')
        def on_cancel():
            app.notify('Cancelled')
        actions.user.are_you_sure_set_on_confirmation_action('Would you like to receive the on confirm message?', on_confirm, on_cancel)
```

```talon
test are you sure: user.test_are_you_sure()
```
