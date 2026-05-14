This documents preferred practices and offers advice on contributing to Community. Contributors are not expected to read this entire document. This primarily exists to preserve knowledge if maintainers leave, let maintainers save time in code review by linking relevant sections, and help onboard frequent contributors.

This will not repeat information in [CONTRIBUTING.md](CONTRIBUTING.md).

# Breaking Changes
Consider discussing if breaking changes are acceptable with maintainers before following these instructions.

In general, breaking changes to the project should be documented in [BREAKING_CHANGES.txt](BREAKING_CHANGES.txt) including a description of what replaced the prior functionality. 

When we decide to remove existing functionality, deprecate it if possible using [deprecations.py](core/deprecations.py) instead of removing it immediately. See the documentation string at the top of that file for instructions on deprecations. Deprecated behavior should remain unchanged in community for 6 months if possible.

# Remove Useless/Unused Code
We do not leave useless code in Community. This includes commented out code, code that cannot be executed, code that is not used anywhere, and Talon abstractions defined on a context that will never activate. 

Defining actions on a tag we do not activate is fine if we advertise to the user that activating that tag will enable some optional functionality.

# Consider Using Snippets for Complex Text Insertion
See [the snippets read me for details on snippets](core/snippets/README.md). A snippet inserts text with placeholders so the user can use a command to go to the next placeholder. Consider using a snippet in the following situations:
  - You need to make sure the cursor ends up in a specific location in the text and user.insert_between is inadequate
  - The user is likely to want to put the cursor in another location shortly after using the command/action
  - You are currently depending on editor specific behavior to put the cursor in the right place or do things like close delimiters
  - Similar functionality is already implemented with snippets and keeping the `snip` prefix consistent makes it easier for the user to remember the command
  - You are implementing functionality for a programming language where the same functionality is implemented for other languages using snippets

Note that you can use the `insert_snippet_by_name` action to programmatically insert snippets. The first argument is the name of the snippet and the second is an optional dictionary containing substitutions. The substitution dictionary maps snippet stops (placeholders) to text to put there, such as the following to put `return False` at the stop `$0`: 

```python
action.user.insert_snippet_by_name("ifStatement", {"0": "return False"})
```

