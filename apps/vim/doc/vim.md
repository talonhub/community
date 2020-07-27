<!-- vim-markdown-toc GFM -->

* [Using VIM under Talon](#using-vim-under-talon)
* [Initial Setup Walkthrough](#initial-setup-walkthrough)
    * [Talon Change - The word `yank`](#talon-change---the-word-yank)
    * [Talon Change - The key `end`](#talon-change---the-key-end)
    * [Talon Change - The command `word`](#talon-change---the-command-word)
    * [The `generic_editor.talon` commands](#the-generic_editortalon-commands)
    * [Detecting VIM running inside terminals from Talon](#detecting-vim-running-inside-terminals-from-talon)
    * [Detecting the code language of edited files](#detecting-the-code-language-of-edited-files)
    * [Detecting current vim mode](#detecting-current-vim-mode)
    * [Automatically switching neovim using RPC](#automatically-switching-neovim-using-rpc)
    * [Using VIM as your terminal](#using-vim-as-your-terminal)
        * [Neovim Terminal Quirks](#neovim-terminal-quirks)
        * [Working directory](#working-directory)
        * [Installing neovim python package inside talon](#installing-neovim-python-package-inside-talon)
* [Supported command overview](#supported-command-overview)
    * [Commands](#commands)
    * [Motions](#motions)
    * [Text object selection](#text-object-selection)
* [VIM Plugins](#vim-plugins)
    * [fugitive.vim](#fugitivevim)
    * [vim-plug.vim](#vim-plugvim)
    * [fzf.vim](#fzfvim)
    * [nerdtree.vim](#nerdtreevim)
    * [cscope.vim](#cscopevim)
    * [ale.vim](#alevim)
    * [surround.vim](#surroundvim)
* [VIM Examples and Tutorial](#vim-examples-and-tutorial)
    * [Simple motions and edits](#simple-motions-and-edits)
        * [Intermediate Usage](#intermediate-usage)
        * [Advanced Usage](#advanced-usage)
* [Frequently Asked Questions](#frequently-asked-questions)
    * [Why not just use raw vim keyboard commands](#why-not-just-use-raw-vim-keyboard-commands)
    * [What are some advantages of using talon vim vs raw vim?](#what-are-some-advantages-of-using-talon-vim-vs-raw-vim)
    * [What are some disadvantages of using talon vim v man mode?](#what-are-some-disadvantages-of-using-talon-vim-v-man-mode)

<!-- vim-markdown-toc -->

# Using VIM under Talon

This document serves as an instruction manual and quick tutorial for people
wanting to set up running vim under talon. Henceforth it will be referred to as
"talon vim". The original inspiration for creating talon vim was vimspeak,
however it has evolved far beyond what vimspeak was able to do.

Most of the testing has been done on Linux, but if you do test this on other
systems and you have positive or negative results you can provide feedback on
the slack channel.

Please note that if you want to have the full vim experience you will have to
make modifications to both the vim config and talon.

Currently supported VIM features:

* motions
* registers
* macros
* folds
* tabs
* splits
* [plugins](plugins) (see list below)
* settings
* automatic mode switching (including terminal)

You can contact `fidget` on the Talon slack for questions/support.

# Initial Setup Walkthrough

## Talon Change - The word `yank`

The default Talon alphabet uses `yank` for the letter `y`. This conflicts with
the natural VIM verb, so it is recommended you change the `y` word in
`code/keys.py`. For example you could instead use: `yell`

## Talon Change - The key `end`

The `code/vim.py` script include support for a motion verb called `end`. To the
problem is that talon also supports the ability to simply say the word `end` and
it will trigger pressing the keyboard key `end`.

You currently have two options to deal with this:

1) You can disable the `end` key in talon, however this will negatively impact
other scenarios where you would normally like to be able to press key directly.

2) Use the alternate vim motion verb `end word`. There aren't too many
downside to this approach aside from it being somewhat cumbersome.

## Talon Change - The command `word`

By default talon will use the command `word` as a command for saying a single
word. See `misc/formatters.talon`. In vim "word" is a natural movement motion
so it is included by default. If you decide to use this you will want to
change the talon command to be a separate word.

## The `generic_editor.talon` commands

The default actions defined in `generic_editor.talon` are supported, but in
some cases are too simple for more complicated use with vim. You can try to use
them in general but in some cases you will want to switch to use the vim
specific ones.

## Detecting VIM running inside terminals from Talon

The vim support in talon is built around supporting running vim as your
terminal and being able to pop in and out of terminal mode.

If you won't use vim from inside of a terminal you can ignore this step.

Normally by default all terminal grammars will be still loaded when VIM is
running in a terminal, because the app itself that talon detects (at least on
Linux) is the terminal. This takes some manual intervention to fix.

The current fix for this is to modify the `~/.vimrc` configuration file, so
that talon is able to differentiate between vim running in the terminal and the
terminal itself. For instance I add `VIM` in the `titlestring` and this allows
me to set the `vim` talon tag by using `win.title: /VIM/`. It also lets me
descriminate terminal vs vim tags in terminal talon files by using
`not win.title: /VIM/`.

To set your titlestring to include `VIM`, use something like the following:

```
let &titlestring ='VIM - (%f) %t'
set title " required for neovim
```

Talon will search the active terminal window title and look for `VIM`, at which
point it will correctly trigger the vim tag and disable the terminal tag.

## Detecting the code language of edited files

Currently the logic for detecting the code language inside of vim expect their
actual file name to be the last part of the titlestring that is pulled out of
`win.title`. This means you'll have to added your title string to ensure that
the last entry is the file name. This can be done using the `%t` format
specifier, which was shown in the previous example. No matter what you say your
`titlestring` to just be sure that `%t` is the last entry.

## Detecting current vim mode

`code/vim.py` currently relies on the mode being advertised in the title
string in order to make intelligent decisions about how to flip between modes.
You can disable this functionality in the settings. If you want to use it you
need to make sure that your `titlestring` includes a pattern like `MODE:<mode>`
for example:

```
let &titlestring ='VIM MODE:%{mode()} - (%f) %t'
set title
```

## Automatically switching neovim using RPC

XXX - note this isn't supported yet

Once again we can rely on the `titlestring` to tell talon where to look to
access the current neovim RPC interface.
.

```
let &titlestring ='VIM MODE:%{mode()} RPC:%{v:servername} - (%f) %t'
set title
```

## Using VIM as your terminal

Recent versions of vim and neovim both allow you to run a terminal emulator
inside of a vim buffer itself. For people that are using voice to control their
systems this is actually very useful it allows you to navigate the terminal
history using vim motions. This allows you to for instance copy and paste lines
that were printed from different terminal commands that would otherwise require
you to use a mouse to highlight.

As an alternative to vim you might be tempted to use a terminal that supports
of vim-like selection mode similar to termite, however the selection mode in
these terminals has serious drawbacks such as no line numbers, limited motion
verbs, etc.

If you choose to use them as your terminal than you have to make certain
modifications again to the talon configuration files, and the vim configuration
in order for it to differentiate between terminal mode.

First you'll have to ensure that the vim mode is correctly advertised in your
title string, similar to the previous section. The following example can be
placed into your vim config file.

```
let &titlestring ='VIM MODE:%{mode()} RPC:%{v:servername} - (%f) %t'
set title
if has ('autocmd')
    autocmd TermEnter * let &titlestring='VIM MODE:%{mode()} RPC:%{v:servername} - (%f) %t'|redraw
endif
```

In the example above we need to set up in `autocomd` because by default
terminals were lazily redraw the `titlestring`, which causes talon to not
correctly detect the mode switch.

The `apps/linux/vim_terminal.talon` file can then match based off of the
`titlestring` above holding `MODE:t`, in which case it will trigger `terminal`
mode despite being inside of vim.

### Neovim Terminal Quirks

XXX - not completed

Here I will try to document some potential problems you will encounter when
moving your workflow into vim terminal for everything, and how I solved them.

https://gist.github.com/DrSpeedy/9022d3bee63a7029570c7d3d43054329

### Working directory

```
# This function calls the script below when loaded by
# the shell inside of neovim. It must be placed somewhere in
# your default shell's rc file e.g. ~/.zshrc
neovim_autocd() {
    [[ $NVIM_LISTEN_ADDRESS ]] && ${HOME}/.ohmyzsh/custom/functions/neovim-autocd.py
}
chpwd_functions+=( neovim_autocd )
```

### Installing neovim python package inside talon

XXX - this isn't done/documented yet

# Supported command overview

In this section summarizes most of the main grammars that are supported
by the current talon vim implementation. For the most truthful representation
of what is supported you need to check the talon and python files. All of the
commands follow the typical vim grammar style such as
`[count][action][motion]`. Motions are also supported is to move along where
you are in the file or select things in VISUAL mode. By default these motions
are also accessible for the inside INSERT mode without needing to manually
change modes, to reduce voice strain.

For the most complete as you need to check `vim.py` and `vim.linux.talon`.

## Commands

Many of these can be combined with motions or text objects selection, etc.

```
    "join": "J",
    "filter": "=",
    "paste": "p",
    "undo": "u",
    "swap case": "~",
    "change": "c",
    "delete": "d",
    "trim": "d",
    "indent": ">",
    "unindent": "<",
    "yank": "y",
    "copy": "y",
    "fold": "zf",
    "format": "gq",
    "to upper": "gU",
    "to lower": "gu",
```

## Motions

These are motions that can be used in VISUAL mode, and can also be used as
motions when combined with commands.

```
    "back": "b",
    "back word": "b",
    "big back": "B",
    "big back word": "B",
    "end": "e",
    "end word": "e",
    "big end": "E",
    "word": "w",
    "words": "w",
    "big word": "W",
    "big words": "W",
    "back end": "ge",
    "back big end": "gE",
    "right": "l",
    "left": "h",
    "down": "j",
    "up": "k",
    "next": "n",
    "next reversed": "N",
    "previous": "N",
    "column zero": "0",
    "column": "|",
    "start of line": "^",
    "end of line": "$",
    "search under cursor": "*",
    "search under cursor reversed": "#",
    "again": ";",
    "again reversed": ",",
    "down sentence": ")",
    "sentence": ")",
    "up sentence": "(",
    "down paragraph": "}",
    "paragraph": "}",
    "up paragraph": "{",
    "start of next section": "]]",
    "start of previous section": "[[",
    "end of next section": "][",
    "end of previous section": "[]",
    "matching": "%",
    "down line": "+",
    "up line": "-",
    "first character": "_",
    "cursor home": "H",
    "cursor middle": "M",
    "cursor last": "L",
    "start of document": "gg",
    "start of file": "gg",
    "top of document": "gg",
    "top of file": "gg",
    "end of document": "G",
    "end of file": "G",
```

With character arguments:
```
    "jump to mark": "'",
    "find": "f",
    "find reversed": "F",
    "find previous": "F",
    "till": "t",
    "till reversed": "T",
    "till previous": "T",
    "last": "$F",  # find starting end of line
```

## Text object selection

```
    "word": "w",
    "words": "w",
    "big word": "W",
    "big words": "W",
    "block": "b",
    "blocks": "b",
    "big block": "B",
    "big blocks": "B",
    "dubquote": '"',
    "dub quote": '"',
    "double quotes": '"',
    "quote": "'",
    "single quotes": "'",
    "ticks": "'",
    "parens": "(",
    "parenthesis": "(",
    "angle brackets": "<",
    "curly braces": "{",
    "braces": "{",
    "square brackets": "[",
    "squares ": "[",
    "brackets": "[",
    "backticks": "`",
    "sentence": "s",
    "sentences": "s",
    "paragraph": "p",
    "paragraphs": "p",
    "tag block": "t",
```

# VIM Plugins

Right now plugins are sorted into their own section under
`apps/linux/vim_plugins/`. The below is a quick summary of the more heavily
tested plugins. In general if you don't need these just disable them, by
adding a `.disable` suffix.

## fugitive.vim

`vim_plugins/fugitive.talon`

## vim-plug.vim
`vim_plugins/plug.talon`

## fzf.vim
`vim_plugins/fzf.talon`

## nerdtree.vim
`vim_plugins/nerdtree.talon`

## cscope.vim
`vim_plugins/cscope.talon`

## ale.vim
`vim_plugins/ale.talon`

## surround.vim
`vim_plugins/surround.talon`

# VIM Examples and Tutorial

This section provides an interactive section where you can test certain
commands and get a feel for how to interact with the VIM plugins.

It also recommended that you check out the youtube videos related to vimspeak
since it is the original project that talon vim was originally ported from. You
could try to follow along with his demos as most of the command should be
supported.

* [vimspeak code demo](https://www.youtube.com/watch?v=TEBMlXRjhZY)
* [vimspeak vim golf demo](https://www.youtube.com/watch?v=qy84TYvXJbk)

## Simple motions and edits

Here you can try out some basic commands to get a feel for the flow of using
the VIM voice commands. Most of the commands should be fairly intuitive.

```
The quick brown fox jumps over the lazy dog.
```

With the cursor starting on the letter `T` above, try practicing with the
following commands. Note that the instructions assume you are viewing this file
from inside vim and it is the only open buffer and split.

Next let's create a little sandbox to work inside.

* `normal mode`
* `new empty vertical split`
* `split rotate`
* `split left`

Next we will set this `vim.md` file to read-only, to help prevent you
accidentally deleting things while experimenting.

* `unset modifiable`

You should now have a new empty vertical split containing on the right side of
your vim screen, and your cursor should be back in the split with the tutorial.

Speak the following commands

* `search reversed lazy  dog` (extra space is on purpose to simplify search)
* `enter`
* `yank line`
* `split right`
* `paste above`
* `unset highlights`
* `set line numbers`

Now you should have a new line in the buffer on the right on line number 1.

* `end of line`
* `start of line`
* `word`
* `two word`
* `find run`
* `append`
* `say and under`
* `normal mode`
* `find reversed air`
* `inject space`
* `back`
* `two delete word`
* `find reversed quench`
* `change word`
* `say slow`
* `normal mode`
* `back`
* `swap words`
* `two back`
* `replace gust`
* `yank line`
* `paste below`
* `repeat that twentyieth`
* `top of file`
* `go line ten`
* `gap below`
* `two down`
* `select line`
* `go down`
* `delete`
* `select paragraph`
* `swap selected`
* `say lazy`
* `go right`
* `say hyper`
* `enter` (this might be mapped differently for you. how ever you say press enter)
* `reselect`
* `swap selected`
* `space`
* `go right`
* `dash`
* `swap global`
* `backslash dot`
* `go right`
* `bang`
* `enter` (this might be mapped differently for you. however you press enter)

All done for now. You can close the sandbox buffer:

* `force close this buffer`

This really only touches the surface of the commands supported. You will need
to spend time reading `vim.talon`, `vim.py`, and experimenting to get a feel
for everything.

### Intermediate Usage

Now we will experiment with some more complicated edits
XXX - to do

### Advanced Usage

XXX - to do

# Frequently Asked Questions

## Why not just use raw vim keyboard commands

Some people would suggest that a better approach is to use explicit keyboard
shortcuts and talon alphabet to use VIM, and not break out all of the commands
into distinct grammars. If you feel this is better, simply don't use any of the
provided commands. I chose to do it this way as it feels more natural when
using voice.

## What are some advantages of using talon vim vs raw vim?

You can mix raw vim commands with talon vim interchangeably, you don't have to
entirely which over if you find parts too cumbersome. For example you might
like saying `sit` to go from NORMAL mode to INSERT mode, rather than saying
`insert mode`, and you can continue to do that, which makes sense because it's
faster.

Some of the real convenience comes from just reducing the amount you have to
say over a longer period of time. Even if you're only saying one less word every
command, over the course of an hour or more this adds up a lot.

Some basic convenience comes from more complex sequences of commands combined
with mode switching that happens automatically. For example if you were editing
a line `this is an example sentence` and your cursor is on the word `is` while
in `INSERT` mode. Imagine you want to change the word `sentence` to `line`.
Without using talon vim you would say: `escape fine sun cap word say line`,
with talon vim you would say: `find sun change word say line`

If you use things like VISUAL mode, swapping, buffers, splits, tabs,
terminal, plugins, or any other more advanced vim features they require
lots of key sequences, you will save yourself a significant amount of time and
speaking as more and more words can be eliminated.

Example: If you are in INSERT mode and want to switch to a different buffer you would
need to say: `escape colon bat number enter`. In talon vim you would say
`buffer number`.

Example: If you are in INSERT mode and you decide you want to select five lines
down and then swap cat with dog on the selected lines you would say the
following: `escape vest five jury colon sun slash say cat slash say dog slash
gust enter`. With talon vim you would say: `select five lines swap selected say
cat go right say dog enter`

It also supports intelligent mode switching, as well as the ability to stay in
INSERT mode despite calling NORMAL mode commands. So you don't need to say
`control urge` or swap in and out. For instance `this is an example sentence`,
if you are in INSERT mode with your cursor on `example` and want to move two
words back you would say `escape two bat sit` or `control urge two bat`,
whereas in talon vim you can just say `two back`

## What are some disadvantages of using talon vim v man mode?

There are noticeable slow downs in the speed of commands due to not supporting
RPC yet. In order to ensure mode switch occurs artificial delays have to be
introduced so that we can assume the mode has actually changed. In theory this
should get almost immediate once RPC is supported.

There's a lot of commands to learn, and some of them may not be intuitive right
away.
