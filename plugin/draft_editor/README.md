# Draft editor

The draft editor lets you revise text in a full text editor before inserting it
back into the application where you started. It is useful for composing longer
messages in applications whose text fields have limited editing or voice-control
support.

The plugin uses an already-running editor application. It opens a new tab in
that editor, optionally copies selected text into it, and remembers the original
window. When you submit the draft, the plugin closes the temporary tab, returns
to the original window, and pastes the revised text. If text was selected in the
original window, the paste replaces that selection.

## Requirements

- The editor application must be running before you start a draft.
- By default, the plugin recognizes Visual Studio Code, VSCodium, Codium, and
  code-oss.
- The source application and editor must support the standard Talon editing and
  tab actions used by the community command set.

The commands for starting a draft are available only when a recognized editor
is running and is not the focused application.

## Commands

| Command         | Action                                                                                           |
| --------------- | ------------------------------------------------------------------------------------------------ |
| `draft this`    | Open a new editor tab. If text is selected, copy it into the draft.                              |
| `draft all`     | Select all text in the current field or document and open it as a draft.                         |
| `draft line`    | Select the current line and open it as a draft.                                                  |
| `draft top`     | Select from the cursor to the start of the document and open it as a draft.                      |
| `draft bottom`  | Select from the cursor to the end of the document and open it as a draft.                        |
| `draft submit`  | While editing a draft, close its tab, return to the original window, and paste the revised text. |
| `draft discard` | Close the draft without pasting it and return to the original window.                            |

## Example workflow

1. Start Visual Studio Code or another configured editor.
2. Focus the application in which you want to compose or revise text.
3. Say `draft this` to start with an empty draft, or select some text and say
   `draft this` to revise it.
4. Edit the text in the newly opened editor tab.
5. Say `draft submit` to send the result back, or `draft discard` to cancel.

The most recently submitted draft is kept in memory. When the editor is running
but not focused, saying `draft submit` pastes that text again. This can be used
to recover from a failed window switch or to insert the last draft in another
location. The saved draft is cleared when Talon restarts.

## Configure a different editor

Set `user.draft_editor` to the application name Talon reports for your editor.
For example, add the following to a `.talon` file to use Sublime Text:

```talon
settings():
    user.draft_editor = "Sublime Text"
```

To recognize multiple application names, separate them with a comma and a
space:

```talon
settings():
    user.draft_editor = "Sublime Text, Notepad++"
```

Setting this value replaces the default editor list; it does not add to it.

## Demo

[Watch the draft editor demo on YouTube](https://www.youtube.com/watch?v=U6Q9qjSIVQg).
