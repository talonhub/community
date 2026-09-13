# Draft editor

The draft editor plugin lets you use a Talon-enabled text editor to compose or
revise text from almost any application. It is most useful in applications with
limited support for text editing and/or Talon.

To start a draft, the draft editor records the current window, opens a temporary
tab in the text editor and optionally copies selected text into the tab. When
you say `draft submit`, the draft editor closes the temporary tab, returns
keyboard focus to the original window, and pastes the (revised) text. If text
was selected in the original window, the pasted text replaces it.

## Requirements

- The text editor must be running before you start a draft.
- By default, the plugin recognizes Visual Studio Code, VSCodium, Codium, and
  code-oss as text editors.
- The source application and text editor must support standard Talon editing and
  tab actions defined by community.

Commands for starting a draft are available only when a recognized text editor
is running and is not the focused application.

## Commands

| Command         | Action                                                                                            |
| --------------- | ------------------------------------------------------------------------------------------------- |
| `draft this`    | Open a temporary text editor tab for use as a draft. If text is selected, copy it into the draft. |
| `draft all`     | Select all text in the focused text field (document) and copy it into a new draft.                |
| `draft line`    | Select and copy the current line into a new draft.                                                |
| `draft top`     | Select and copy from the insertion point to the start of the document into a new draft.           |
| `draft bottom`  | Select and copy from the insertion point to the end of the document into a new draft.             |
| `draft submit`  | While editing a draft, close its tab, focus the original window, and paste the drafted text.      |
| `draft discard` | Close the draft without saving your changes and focus the original window.                        |

## Example workflow

1. Start Visual Studio Code or another configured text editor.
2. Focus the application in which you want to compose or revise text.
3. Say `draft this` to start with an empty draft, or select some text and say
   `draft this` to revise it.
4. Edit the text in the draft's tab.
5. Say `draft submit` to paste the result into the original window, or
   `draft discard` to discard your changes and focus the original window.

The most recently submitted draft is kept in memory. While a recognized text
editor is running but not focused, saying `draft submit` pastes the drafted
text. This can be used to recover from a failed window switch or to insert the
drafted text somewhere else. The submitted draft is not preserved when Talon
restarts.

## Configure a different text editor

Set `user.draft_editor` to the application name Talon reports for your text
editor (`app.name` in `help scope`, or use `talon copy name` to copy it to the
Clipboard). For example, add the following to a `.talon` file to use Sublime
Text:

```talon
settings():
    user.draft_editor = "Sublime Text"
```

To recognize multiple application names, separate them with a comma and a space:

```talon
settings():
    user.draft_editor = "Sublime Text, Notepad++"
```

Setting this value replaces the default editor list; it does not add to it.

After changing this setting, either quit and restart Talon or your configured
text editor so the draft editor recognizes it is running.

## Demo

[Watch the draft editor demo on YouTube](https://www.youtube.com/watch?v=U6Q9qjSIVQg).
