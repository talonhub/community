# Snippets

Custom format to represent snippets.

## Features

- Custom file ending `.snippet`.
- Supports syntax highlighting in VSCode via an [extension](https://marketplace.visualstudio.com/items?itemName=AndreasArvidsson.andreas-talon)
- Supports auto-formatting in VSCode via an [extension](https://marketplace.visualstudio.com/items?itemName=AndreasArvidsson.andreas-talon)
- Support for insertion and wrapper snippets.
- Support for phrase formatters.

## Format

- A `.snippet` file can contain multiple snippet documents separated by `---`.
- Each snippet document has a context and body separated by `-`.
- Optionally a file can have a single context at the top with no body. This is not a snippet in itself, but default values to be inherited by the other snippet documents in the same file.
- Some context keys supports multiple values. These values are separated by `|`.

### Context fields

| Key            | Required | Multiple values | Example                        |
| -------------- | -------- | --------------- | ------------------------------ |
| name           | Yes      | No              | `name: ifStatement`            |
| language       | No       | Yes             | `language: javascript \| java` |
| phrase         | No       | Yes             | `phrase: if \| if state`       |
| insertionScope | No       | Yes             | `insertionScope: statement`    |

### Variables

It's also possible to set configuration that applies to a specific tab stop (`$0`) or variable (`$try`):

| Key                | Required | Multiple values | Example                             |
| ------------------ | -------- | --------------- | ----------------------------------- |
| insertionFormatter | No       | Yes             | `$0.insertionFormatter: SNAKE_CASE` |
| wrapperPhrase      | No       | Yes             | `$0.wrapperPhrase: try \| trying`   |
| wrapperScope       | No       | No              | `$0.wrapperScope: statement`        |

## Formatting and syntax highlighting

To get formatting and syntax highlighting for `.snippet` files install [andreas-talon](https://marketplace.visualstudio.com/items?itemName=AndreasArvidsson.andreas-talon)

## Images

### Single snippet definition

![snippets1](./images/snippets1.png)

### Multiple snippet definitions in single file

![snippets2](./images/snippets2.png)

### Default context and multiple values

![snippets3](./images/snippets3.png)
