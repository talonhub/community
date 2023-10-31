# Snippets

Custom formats to represent snippets.

## Features

-   Custom file ending `.snippet`.
-   VSCode syntax highlights.
-   VSCode document formatter.
-   Support for insertion and wrapper snippets.
-   Support for phrase formatters.

## Format

-   A `.snippet` file can contain multiple snippet documents separated by `---`.
-   Each snippet document has a context and body separated by `-`.
-   Optionally a file can have a single context at the top with no body. This is not a snippet in itself, but default values to be inherited by the other snippet documents in the same file.
-   Some context keys supports multiple values. These values are separated by `|`.

### Context fields

| Key            | Required | Multiple values | Example                        |
| -------------- | -------- | --------------- | ------------------------------ |
| name           | Yes      | No              | `name: ifStatement`            |
| language       | No       | Yes             | `language: javascript \| java` |
| phrase         | No       | Yes             | `phrase: if \| if state`       |
| insertionScope | No       | Yes             | `insertionScope: statement`    |

### Variables

Tab stops(`$0`) and variables(`$try`) can be used to wrap with using the following fields.

| Key                | Required | Multiple values | Example                             |
| ------------------ | -------- | --------------- | ----------------------------------- |
| insertionFormatter | No       | Yes             | `$0.insertionFormatter: SNAKE_CASE` |
| wrapperPhrase      | No       | Yes             | `$0.wrapperPhrase: try \| trying`   |
| wrapperScope       | No       | No              | `$0.wrapperScope: statement`        |

## Images

### Single snippet definition

![snippets1](./images/snippets1.png)

### Multiple snippet definitions in single file

![snippets2](./images/snippets2.png)

### Default context and multiple values

![snippets3](./images/snippets3.png)
