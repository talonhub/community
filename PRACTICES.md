# Community Practices

This file documents preferred practices and offers advice on contributing to Community. Contributors are not expected to read this entire document. This primarily exists to preserve knowledge when maintainers leave, let maintainers save time in code review by linking relevant sections, and help onboard frequent contributors.

This does not make [the contributing guidelines file](./CONTRIBUTING.md) obsolete.

## Table of Contents

- [Breaking Changes](#breaking-changes)
- [Useless/Unused Code](#uselessunused-code)
- [When to Use Snippets](#when-to-use-snippets)
- [Code Simplicity](#code-simplicity)
- [Supporting Multiple Operating Systems](#supporting-multiple-operating-systems)
- [Generalizing Commands](#generalizing-commands)
- [Spoken Form Considerations](#spoken-form-considerations-and-practices)
- [Sleep Practices](#sleep-practices)
- [GUI Practices](#gui-practices)

## Breaking Changes

Consider discussing whether breaking changes are acceptable with maintainers before following these instructions.

In general, document breaking changes in [BREAKING_CHANGES.txt](./BREAKING_CHANGES.txt) including a description of what replaced the prior functionality.

When we decide to remove existing functionality, deprecate it if possible using [our deprecations support](./core/deprecations.py) instead of removing it immediately. See the documentation string at the top of that file for instructions on deprecations. We should leave deprecated behavior unchanged in Community for 6 months if possible.

## Useless/Unused Code

We do not leave useless code in Community. This includes commented out code, code that cannot be executed, code that is not used anywhere, and Talon abstractions defined on a context that will never activate.

Defining actions on a tag we do not activate is fine if we advertise to the user that activating that tag will enable some optional functionality.

## When to Use Snippets

A snippet inserts text with placeholders so the user can use a command to go to the next placeholder. Consider using a snippet in the following situations:

- You need to make sure the cursor ends up in a specific location in the text and `user.insert_between` is inadequate.
- The user is likely to want to put the cursor in another location shortly after using the command/action.
- You are currently depending on editor-specific behavior to put the cursor in the right place or do things like close delimiters.
- Similar functionality is already implemented with snippets and keeping the `snip` prefix consistent makes it easier for the user to remember the command.
- You are implementing functionality for a programming language where the same functionality is implemented for other languages using snippets.

Use the `user.insert_snippet_by_name` action to programmatically insert snippets. The first argument is the name of the snippet and the second is an optional dictionary containing substitutions. The substitution dictionary maps snippet stops (placeholders) to replacement text, such as the following to insert `return False` at stop `$0`:

```python
action.user.insert_snippet_by_name("ifStatement", {"0": "return False"})
```

See the [snippets README](./core/snippets/README.md) for details on snippets.

## Code Simplicity

Simplify your code when possible; consider leaving a comment describing unavoidably complicated code. In general, use the simplest Talon abstraction that does what you want.

When you want to limit some behavior to a specific context:

- If the behavior is only relevant to an application, just match it directly and provide an [app definition](https://talon.wiki/Customization/Talon%20Framework/apps) if needed.
- If the behavior is general enough to be used by multiple applications or contexts and should not be manually turned on and off by the user, consider putting it behind a [tag](https://talon.wiki/Customization/Talon%20Framework/tags).
- If behavior needs to be activated/deactivated by the user:
  - Putting it behind a tag is simplest.
  - Consider using a [mode](https://talon.wiki/Customization/Talon%20Framework/modes) if only specific commands should be available in the context.
- A [scope](https://talon.wiki/Customization/Talon%20Framework/scopes) can be used for complex context matching if nothing else is adequate.

When you want to define spoken forms:

- Defining a single command directly is simplest.
- Avoid adding multiple spoken forms for a single command without a good reason.
- Consider using a [list](https://talon.wiki/Customization/Talon%20Framework/lists) to give users a set of options
  - Implementing a list in a [.talon-list file](https://talon.wiki/Customization/talon_lists/) is preferred unless you have a good reason to do so in Python.
- Consider using a [capture](https://talon.wiki/Customization/Talon%20Framework/captures) for complex spoken forms.

In general, implementing functionality in .talon files is simpler than doing so in Python. However, in Community, prefer implementing behavior in a Python [action](https://talon.wiki/Customization/Talon%20Framework/actions) for reusability and to facilitate contextual overrides despite the added complexity.

## Supporting Multiple Operating Systems

Some functionality needs to support multiple operating systems, such as using the correct keyboard shortcut based on the current operating system (OS). While new contributions do not have to support every OS, implement functionality needing OS specific behavior using Talon abstractions to make overriding easier.

### Recommended File Structure

- 1. Put actions that work universally in a base Python file.
- 2. Create empty action definitions for actions needing OS specific implementations in the base file.
- 3. Define separate files for different implementations. Implementations that are the same for multiple OSs can go in the same implementation file.
- 4. The implementation files' names should be the base file name followed by the suffix(es) for the implemented OS(es), i.e. `base_name_win_linux.py` for a file providing Windows and Linux implementations.

| OS      | Suffix  |
| ------- | ------- |
| Windows | \_win   |
| MacOS   | \_mac   |
| Linux   | \_linux |

Consider looking at the [Firefox implementation](./apps/firefox) for an example.

## Generalizing Commands

If you write commands for a specific context that would be useful in other contexts, consider doing the following:

- 1. Define a subdirectory for your commands in the [tags/](./tags/) directory.
- 2. Provide empty action definitions in your subdirectory.
- 3. Define a tag for the commands.
- 4. Put the commands in your subdirectory.
- 5. Make the commands available when the tag is active.
- 6. Update [the tags README](./tags/README.md) describing your new commands.
- 7. Provide implementations for the actions in the original context you wrote them for.
- 8. Activate the tag in the original context.

You can see examples of the kinds of things we put in the general command grammar in the [tags/](./tags/) directory.

This approach allows reusing the same commands in multiple contexts and helps prevent inconsistencies.

## Spoken Form Considerations and Practices

- Our convention is to capitalize single letters to slightly improve readability.
- Talon currently only handles alphabetic characters in spoken forms. Spell out numbers, symbols, etc.
- Anchor commands only when needed to prevent misrecognitions or ambiguities. For example, a trailing anchor `$` after a command ending with the `user.prose` capture ensures the remainder of the utterance is consumed by the capture. Anchoring at both the start (`^`) and end (`$`) is useful for commands that users would want to avoid triggering accidentally and would not use often.
- Consider using a prefix word for a group of commands, such as window commands being prefixed with the word `window`. Making the commands longer reduces the probability of misrecognitions, and adding a prefix helps prevent conflicts.
- Hesitate when adding short commands — especially when always available — because they can be easily misrecognized.
- Consider testing that your spoken forms recognize with multiple Conformer speech engines.

### Clip Versus Paste

Our voice commands using the clipboard usually have `paste` or `clip` in their spoken forms. Going forward, use `paste` for commands directly performing a kind of paste operation, such as pasting without formatting. Use `clip` for commands using the clipboard contents for anything else. This includes performing a paste as a step towards achieving a bigger objective, such as searching for the current clipboard contents in a file.

## Sleep Practices

- Use the `sleep` action instead of the Python `time.sleep` function.
- Avoid sleeping inside a `cron` callback because public Talon runs all such callbacks in a single thread.
- Avoid command or action implementations that sleep for more than a total of ~200 ms. Talon is unresponsive to commands while sleeping; long delays also trigger watchdog warnings in the Talon log. Consider using `cron` to schedule actions requiring a longer delay.
- Sleep duration settings should be a `float`-typed number of seconds to sleep unless you have a good reason to do otherwise. Note that the `sleep` action interprets a `float` argument as seconds.

## GUI Practices

- Please add a screenshot showing GUI changes to the PR description to make review easier.
- Manually activate a `tag` if you want a context to match whether a GUI element is visible.

### imgui Practices

- Keep operations in an imgui drawing function (decorated by `imgui.open`) efficient and limited because the imgui framework will frequently and repeatedly call the function. For example, cache displayed information in a global variable.
- Create a button and voice command for closing each imgui window.
- For each option in a list of options, provide a button and voice command. Either make the buttons show the exact spoken forms for selecting the corresponding options or explain the spoken forms elsewhere in the UI.
- Keep the "new user message" description consistent with new UI. Update the description if you have a good reason to not follow the patterns it documents.
- If your imgui window is too tall for some screens, consider using pagination buttons like the help system.
- Try to avoid having multiple spoken forms for the same button. If you must, show alternatives using TalonScript syntax (e.g. `(foo | bar) [baz]`).
