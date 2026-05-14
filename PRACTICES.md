This file documents preferred practices and offers advice on contributing to Community. Contributors are not expected to read this entire document. This primarily exists to preserve knowledge when maintainers leave, let maintainers save time in code review by linking relevant sections, and help onboard frequent contributors.

This will not repeat information in [CONTRIBUTING.md](CONTRIBUTING.md).

# Breaking Changes
Consider discussing wether breaking changes are acceptable with maintainers before following these instructions.

In general, breaking changes to the project should be documented in [BREAKING_CHANGES.txt](BREAKING_CHANGES.txt) including a description of what replaced the prior functionality. 

When we decide to remove existing functionality, deprecate it if possible using [deprecations.py](core/deprecations.py) instead of removing it immediately. See the documentation string at the top of that file for instructions on deprecations. Deprecated behavior should remain unchanged in Community for 6 months if possible.

# Remove Useless/Unused Code
We do not leave useless code in Community. This includes commented out code, code that cannot be executed, code that is not used anywhere, and Talon abstractions defined on a context that will never activate. 

Defining actions on a tag we do not activate is fine if we advertise to the user that activating that tag will enable some optional functionality.

# Consider Using Snippets for Complex Text Insertion
See [the snippets README for details on snippets](core/snippets/README.md). A snippet inserts text with placeholders so the user can use a command to go to the next placeholder. Consider using a snippet in the following situations:
  - You need to make sure the cursor ends up in a specific location in the text and user.insert_between is inadequate.
  - The user is likely to want to put the cursor in another location shortly after using the command/action.
  - You are currently depending on editor-specific behavior to put the cursor in the right place or do things like close delimiters.
  - Similar functionality is already implemented with snippets and keeping the `snip` prefix consistent makes it easier for the user to remember the command.
  - You are implementing functionality for a programming language where the same functionality is implemented for other languages using snippets.

Note that you can use the `insert_snippet_by_name` action to programmatically insert snippets. The first argument is the name of the snippet and the second is an optional dictionary containing substitutions. The substitution dictionary maps snippet stops (placeholders) to text to put there, such as the following to put `return False` at the stop `$0`: 

```python
action.user.insert_snippet_by_name("ifStatement", {"0": "return False"})
```

# Avoid Unnecessarily Complex Code
Simplify your code when possible and consider leaving a comment describing complicated code. Try to avoid using an unnecessarily complex Talon abstraction for what you are trying to do. 

When you want to limit some behavior to a specific context:
  - If the behavior is only relevant to an application, just match it directly and provide an [app definition](https://talon.wiki/Customization/Talon%20Framework/apps) if needed.
  - If the behavior is general enough to be used by multiple applications or contexts and should not be manually turned on and off by the user, consider putting it behind a [tag](https://talon.wiki/Customization/Talon%20Framework/tags).
  - If behavior needs to be activated/deactivated by the user
    - Putting it behind a tag is simplest.
    - Consider using a [mode](https://talon.wiki/Customization/Talon%20Framework/modes) if only specific commands should be available in the context.
  - A [scope](https://talon.wiki/Customization/Talon%20Framework/scopes) can be used for complex context matching if nothing else is adequate.

When you want to define spoken forms:
  - Defining a single command directly is simplest. Defining a list with a single item is not recommended.
  - Avoid adding multiple spoken forms for a single command without a good reason.
  - Consider using a [list](https://talon.wiki/Customization/Talon%20Framework/lists) to give users a static set of options
    - Implementing a list in a [.talon-list](https://talon.wiki/Customization/talon_lists/) is preferred unless you have a good reason to do so in Python.
  - Consider using a [capture](https://talon.wiki/Customization/Talon%20Framework/captures) for complex spoken forms.

In general, implementing functionality in .talon files is simpler than doing so in .py files. It is nonetheless usually preferred to implement behavior in an [action](https://talon.wiki/Customization/Talon%20Framework/actions) in Python to allow reusability and context-specific overriding despite the added complexity.

# Supporting Multiple Operating Systems
Some functionality needs to support multiple operating systems, such as using the correct keyboard shortcut based on the current operating system. It is not always necessary for new features to support every operating system, but it is recommended to put functionality that needs to work across operating systems in Talon abstractions so that they can be overridden based on the active operating systems.

The common approach in Community is to provide the Windows implementation in the base files and put the Mac implementation in variants with the `_mac` postfix and the Linux implementation (if different from the Windows implementation) in variants with the `_linux` postfix. Consider looking at the [slack implementation](apps/slack) for an example. 

# Generalizing Commands
If you write commands for a specific context that would be useful in other contexts, consider doing the following:
  - Define a subdirectory for your commands in the [tags/](tags/) directory.
  - Provide empty action definitions in your subdirectory.
  - Define a tag for the commands.
  - Put the commands in your subdirectory.
  - Make the commands available when the tag is active.
  - Update [the tags README](tags/README.md) describing your new commands.
  - Provide implementations for the actions in the original context you wrote them for.
  - Activate the tags in the original context.

You can see examples of the kinds of things we put in the general command grammar in the [tags/](tags/) directory. 

This approach allows reusing the same commands in multiple contexts and helps prevent inconsistencies.
