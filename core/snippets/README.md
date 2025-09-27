# Snippets

Custom format to represent snippets.

## Features

- Custom file ending `.snippet`.
- Supports syntax highlighting in VSCode via an [extension](https://marketplace.visualstudio.com/items?itemName=AndreasArvidsson.andreas-talon)
- Supports auto-formatting in VSCode via an [extension](https://marketplace.visualstudio.com/items?itemName=AndreasArvidsson.andreas-talon)
- Support for insertion and wrapper snippets. Note that while the snippet file syntax here supports wrapper snippets, you will need to install [Cursorless](https://www.cursorless.org) for wrapper snippets to work.
- Support for phrase formatters.

## Format

- A `.snippet` file can contain multiple snippet documents separated by `---`.
- If you want a snippet to insert `---`, use `\---` to escape it.
- Each snippet document has a context and body separated by `-`.
- Optionally a file can have a single context at the top with no body. This is not a snippet in itself, but default values to be inherited by the other snippet documents in the same file.
- Some context keys supports multiple values. These values are separated by `|`.
  - For most keys like `language` or `phrase` multiple values means _or_. You can use phrase _1_ or phrase _2_. The snippet is active in language _A_ or language _B_.
  - For `insertionFormatter` multiple values means that the formatters will be applied in sequence.

### Context fields

| Key            | Required | Multiple values | Example                        |
| -------------- | -------- | --------------- | ------------------------------ |
| name           | Yes      | No              | `name: ifStatement`            |
| description    | No       | No              | `description: My snippet`      |
| language       | No       | Yes             | `language: javascript \| java` |
| phrase         | No       | Yes             | `phrase: if \| if state`       |
| insertionScope | No       | Yes             | `insertionScope: statement`    |

- `name`: Unique name identifying the snippets. Can be referenced in Python to use the snippet programmatically.
- `description`: A description of the snippet.
- `language`: Language identifier indicating which language the snippet is available for. If omitted the snippet is enabled globally.
- `phrase`: The spoken phrase used to insert the snippet. eg `"snip if"`.
- `insertionScope`: Used by [Cursorless](https://www.cursorless.org) to infer scope when inserting the snippet. eg `"snip if after air"` gets inferred as `"snip if after state air"`.

### Variables

It's also possible to set configuration that applies to a specific tab stop (`$0`) or variable (`$try`):

| Key                | Required | Multiple values | Example                             |
| ------------------ | -------- | --------------- | ----------------------------------- |
| insertionFormatter | No       | Yes             | `$0.insertionFormatter: SNAKE_CASE` |
| wrapperPhrase      | No       | Yes             | `$0.wrapperPhrase: try \| trying`   |
| wrapperScope       | No       | No              | `$0.wrapperScope: statement`        |

- `insertionFormatter`: Formatter to apply to the phrase when inserting the snippet. eg `"snip funk get value"`. If omitted no trailing phrase is available for the snippet. Supports fetching formatters from settings variables, e.g. `setting(user.code_private_variable_formatter)`.
- `wrapperPhrase`: Used by [Cursorless](https://www.cursorless.org) as the spoken form for wrapping with the snippet. eg `"if wrap air"`. Without Cursorless this spoken form is ignored by Talon.
- `wrapperScope`: Used by [Cursorless](https://www.cursorless.org) to infer scope when wrapping with the snippet. eg `"if wrap air"` gets inferred as `"if wrap state air"`.

## Formatting and syntax highlighting

To get formatting, code completion and syntax highlighting for `.snippet` files: install [andreas-talon](https://marketplace.visualstudio.com/items?itemName=AndreasArvidsson.andreas-talon)

## Examples

### Single snippet definition

![snippets1](./images/snippets1.png)

### Multiple snippet definitions in single file

![snippets2](./images/snippets2.png)

### Default context and multiple values

![snippets3](./images/snippets3.png)
