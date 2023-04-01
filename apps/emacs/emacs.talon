app: emacs
app: Emacs
-
tag(): user.tabs
tag(): user.splits
tag(): user.line_commands

# ----- GENERAL ----- #
#suplex: key(ctrl-x)
exchange: user.emacs_command("exchange-point-and-mark")
execute: user.emacs_meta("x")
execute {user.emacs_command}$: user.emacs_command(emacs_command)
execute <user.text>$:
  user.emacs_meta("x")
  user.insert_formatted(text, "DASH_SEPARATED")
evaluate | (evaluate|eval) (exper|expression): user.emacs_meta(":")
prefix: key(ctrl-u)
prefix <number_small>: user.emacs_prefix(number_small)

open directory: user.emacs_command("dired-jump")
other open directory: user.emacs_command("dired-jump-other-window")
fill paragraph: user.emacs_command("fill-paragraph")
occurs: user.emacs_command("occur")
other scroll [down]: user.emacs_meta("pagedown")
other scroll up: user.emacs_meta("pageup")
insert unicode: user.emacs_command("insert-char")
abort recursive [edit]: user.emacs_command("abort-recursive-edit")
save some buffers: user.emacs_command("save-some-buffers")
[toggle] read only [mode] [toggle]: user.emacs_command("read-only-mode")
[toggle] input method [toggle]: user.emacs_command("toggle-input-method")

save buffers kill emacs: user.emacs_command("save-buffers-kill-emacs")
package list | [package] list packages: user.emacs_command("list-packages")
package autoremove: user.emacs_command("package-autoremove")
reverse (lines|region): user.emacs_command("reverse-region")
browse kill ring: user.emacs_command("browse-kill-ring")
sort lines: user.emacs_command("sort-lines")
sort words: user.emacs_command("sort-words")
[toggle] line numbers [toggle]: user.emacs_command("display-line-numbers-mode")
[toggle] debug on error [toggle]: user.emacs_command("toggle-debug-on-error")
[toggle] truncate lines [toggle]: user.emacs_command("toggle-truncate-lines")
[toggle] word wrap [toggle]: user.emacs_command("toggle-word-wrap")

manual: user.emacs_command("man")
manual <user.text>:
  user.emacs_command("man")
  user.insert_formatted(text, "DASH_SEPARATED")

# BUFFER SWITCHING #
# many things override these keybindings, so we don't use user.emacs_command
switch: key(ctrl-x b)
other switch: key(ctrl-x 4 b)
display: key(ctrl-x 4 ctrl-o)

# SHELL COMMANDS #
shell command: user.emacs_command("shell-command")
shell command inserting:
  key(ctrl-u)
  user.emacs_command("shell-command")
shell command on region: user.emacs_command("shell-command-on-region")
shell command on region replacing:
  key(ctrl-u)
  user.emacs_command("shell-command-on-region")

# CUSTOMIZE #
customize face: user.emacs_command("customize-face")
customize group: user.emacs_command("customize-group")
customize variable: user.emacs_command("customize-variable")
(customize|custom) [theme] visit theme: user.emacs_command("custom-theme-visit-theme")

# MODE COMMANDS #
auto fill mode: user.emacs_command("auto-f")
dired omit mode: user.emacs_command("dired-omit-mode")
fundamental mode: user.emacs_command("fundamental-mode")
global highlight line mode: user.emacs_command("global-hl-line-mode")
global visual line mode: user.emacs_command("global-visual-line-mode")
global [display] line numbers [mode]:
  user.emacs_command("global-display-line-numbers-mode")
highlight line mode: user.emacs_command("hl-line-mode")
markdown mode: user.emacs_command("markdown-mode")
paredit mode: user.emacs_command("paredit-mode")
rainbow mode: user.emacs_command("rainbow-mode")
sub word mode: user.emacs_command("subword-mode")
text mode: user.emacs_command("text-mode")
visual line mode: user.emacs_command("visual-line-mode")
outline minor mode: user.emacs_command("outline-minor-mode")
emacs lisp mode: user.emacs_command("emacs-lisp-mode")
lisp interaction mode: user.emacs_command("lisp-interaction-mode")
talon script mode: user.emacs_command("talonscript-mode")

# MACROS #
emacs record: user.emacs_command("kmacro-start-macro")
emacs stop: user.emacs_command("kmacro-end-macro")
emacs play: user.emacs_command("kmacro-end-and-call-macro")

# PROFILER #
profiler start: user.emacs_command("profiler-start")
profiler stop: user.emacs_command("profiler-stop")
profiler report: user.emacs_command("profiler-report")

# WINDOW/SPLIT MANAGEMENT #
split solo: user.emacs_command("delete-other-windows")
[split] rebalance: user.emacs_command("balance-windows")
split shrink: user.emacs_command("shrink-window-if-larger-than-buffer")
other [split] shrink:
  user.split_next()
  user.emacs_command("shrink-window-if-larger-than-buffer")
  user.split_last()
split grow: user.emacs_command("enlarge-window")
split grow <number_small>:
  user.emacs_prefix(number_small)
  user.emacs_command("enlarge-window")
split shrink <number_small>:
  amount = number_small or 1
  user.emacs_prefix(0 - amount)
  user.emacs_command("enlarge-window")
split widen [<number_small>]:
  user.emacs_prefix(number_small or 1)
  user.emacs_command("enlarge-window-horizontally")
split narrow [<number_small>]:
  user.emacs_prefix(number_small or 1)
  user.emacs_command("shrink-window-horizontally")


# ----- HELP ----- #
apropos: user.emacs_help("a")
describe (fun|function): user.emacs_help("f")
describe key: user.emacs_help("k")
describe key briefly: user.emacs_help("c")
describe symbol: user.emacs_help("o")
describe variable: user.emacs_help("v")
describe mode: user.emacs_help("m")
describe bindings: user.emacs_help("b")
describe (char|character): user.emacs_command("describe-character")
describe text properties: user.emacs_command("describe-text-properties")
describe face: user.emacs_command("describe-face")
view lossage: user.emacs_help("l")

apropos <user.text>$:
  user.emacs_help("a")
  user.insert_formatted(text, "DASH_SEPARATED")
  key(enter)
describe (fun|function) <user.text>$:
  user.emacs_help("f")
  user.insert_formatted(text, "DASH_SEPARATED")
  key(enter)
describe symbol <user.text>$:
  user.emacs_help("o")
  user.insert_formatted(text, "DASH_SEPARATED")
  key(enter)
describe variable <user.text>$:
  user.emacs_help("v")
  user.insert_formatted(text, "DASH_SEPARATED")
  key(enter)


# ----- FILES & BUFFERS -----
# many key bindings here are often overridden, so we don't use user.emacs_command,
# eg: C-x C-f, C-x k, C-x C-b, C-x right, C-x left
file open: key(ctrl-x ctrl-f)
file rename: user.emacs_command("rename-file")
(file open | find file) at point: user.emacs_command("ffap")
other file open: key(ctrl-x 4 ctrl-f)
(file | buffer) close: key(ctrl-x k enter)

buffer kill: key(ctrl-x k)
buffer bury: user.emacs_command("bury-buffer")
buffer revert | revert buffer: user.emacs_command("revert-buffer")
buffer finish:
    edit.save()
    user.emacs_command("server-edit")
buffer list: key(ctrl-x ctrl-b)
buffer next: key(ctrl-x right)
buffer last: key(ctrl-x left)
buffer rename: user.emacs_command("rename-buffer")

diff (buffer | [buffer] with file):
  user.emacs_command("diff-buffer-with-file")
  key(enter)


# ----- MOTION AND EDITING ----- #
mark: user.emacs_command("set-mark-command")
go back: user.emacs_command("pop-mark")
global [go] back: user.emacs_command("pop-global-mark")

cut line:
  edit.line_start()
  user.emacs_prefix(1)
  key(ctrl-k)
auto indent: user.emacs_command("indent-region")
indent <user.number_signed_small>:
  user.emacs_prefix(number_signed_small)
  user.emacs_command("indent-rigidly")

(search regex | regex search): user.emacs_meta("ctrl-s")
(search regex | regex search) back: user.emacs_meta("ctrl-r")
replace: user.emacs_meta("%")
replace regex | regex replace: user.emacs_meta("ctrl-%")
search edit: user.emacs_meta("e")
search toggle regex: user.emacs_meta("r")
search toggle word: user.emacs_key("meta-s w")

recenter: key(ctrl-u ctrl-l)
(center | [center] <number_small> from) top:
  user.emacs_prefix(number_small or 0)
  key(ctrl-l)
(center | [center] <number_small> from) bottom:
  number = number_small or 0
  user.emacs_prefix(-1-number)
  key(ctrl-l)
go <number> top:
  edit.jump_line(number)
  user.emacs_prefix(0)
  key(ctrl-l)
go <number> bottom:
  edit.jump_line(number)
  user.emacs_prefix(-2)
  key(ctrl-l)

next error | error next: user.emacs_key("meta-g n")
last error | error last: user.emacs_key("meta-g p")

term right: user.emacs_command("forward-sexp")
term left: user.emacs_command("backward-sexp")
term up: user.emacs_command("backward-up-list")
term end: user.emacs_command("up-list")
term down: user.emacs_command("down-list")
term kill: user.emacs_command("kill-sexp")
term wipe:
    user.emacs_prefix(-1)
    user.emacs_command("kill-sexp")
term (mark | select): user.emacs_command("mark-sexp")
term copy:
    user.emacs_command("mark-sexp")
    edit.copy()
term freeze:
    user.emacs_command("mark-sexp")
    user.emacs_command("comment-region")
term [auto] indent:
    user.emacs_command("mark-sexp")
    user.emacs_command("indent-region")

(sentence|sent) (right | end): edit.sentence_end()
(sentence|sent) (left | start): edit.sentence_start()
(sentence|sent) kill: user.emacs_command("kill-sentence")

graph kill: user.emacs_command("kill-paragraph")
graph up: edit.paragraph_start()
graph down: edit.paragraph_end()
graph mark: user.emacs_command("mark-paragraph")
graph copy:
    user.emacs_command("mark-paragraph")
    edit.copy()
graph cut:
  user.emacs_command("mark-paragraph")
  edit.cut()

# could use these to implement "drag <X> left/right/up/down" commands
# but note that eg 'transpose line' and 'drag line down' are different
transpose [word|words]: user.emacs_command("transpose-words")
transpose (term|terms): user.emacs_command("transpose-sexps")
transpose (char|chars): user.emacs_command("transpose-chars")
transpose (line|lines): user.emacs_command("transpose-lines")
transpose (sentence|sentences): user.emacs_command("transpose-sentences")
transpose (graph|graphs|paragraphs): user.emacs_command("transpose-paragraphs")

register (copy|save): user.emacs_command("copy-to-register")
register (paste|insert): user.emacs_command("insert-register")
register jump: user.emacs_command("jump-to-register")
register (copy|save) rectangle: user.emacs_command("copy-rectangle-to-register")

rectangle clear: user.emacs_command("clear-rectangle")
rectangle delete: user.emacs_command("delete-rectangle")
rectangle kill: user.emacs_command("kill-rectangle")
rectangle open: user.emacs_command("open-rectangle")
rectangle (copy|save) [to] register: user.emacs_command("copy-rectangle-to-register")
rectangle (yank|paste): user.emacs_command("yank-rectangle")
rectangle copy: user.emacs_command("copy-rectangle-as-kill")
rectangle number lines: user.emacs_command("rectangle-number-lines")


# ----- MAJOR & MINOR MODES ----- #

# python-mode #
run python: user.emacs_command("run-python")
python load file: user.emacs_command("python-shell-send-buffer")

# smerge-mode #
merge next: user.emacs_command("smerge-next")
merge last: user.emacs_command("smerge-prev")
merge keep upper: user.emacs_command("smerge-keep-upper")
merge keep lower: user.emacs_command("smerge-keep-lower")
merge keep this: user.emacs_command("smerge-keep-current")
merge refine: user.emacs_command("smerge-refine")
merge split: user.emacs_command("smerge-resolve")

# outline-minor-mode #
# frequent: overview, show, hide, next, last, forward, backward, up
outline show all: key(ctrl-c @ ctrl-a)
outline show entry: key(ctrl-c @ ctrl-e)
outline hide entry: key(ctrl-c @ ctrl-c)
outline show [subtree]: key(ctrl-c @ ctrl-s)
outline hide [subtree]: key(ctrl-c @ ctrl-d)
outline show children: key(ctrl-c @ tab)
outline show branches: key(ctrl-c @ ctrl-k)
outline hide leaves: key(ctrl-c @ ctrl-l)
outline hide sublevels: key(ctrl-c @ ctrl-q)
outline (hide body | [show] (overview | outline)): key(ctrl-c @ ctrl-t)
outline hide other: key(ctrl-c @ ctrl-o)
outline forward [same level]: key("ctrl-c @ ctrl-f")
outline (backward|back) [same level]: key("ctrl-c @ ctrl-b")
outline next [visible heading]: key("ctrl-c @ ctrl-n")
outline (previous|last) [visible heading]: key("ctrl-c @ ctrl-p")
outline insert [heading]: key(ctrl-c @ RET)
outline up [heading]: key("ctrl-c @ ctrl-u")
outline promote: key(ctrl-c @ ctrl-<)
outline demote: key(ctrl-c @ ctrl->)
outline move [subtree] down: key(ctrl-c @ ctrl-v)
outline move [subtree] up: key(ctrl-c @ ctrl-^)
outline mark [subtree]: key(ctrl-c @ @)
