app: emacs
app: Emacs
-
tag(): user.tabs
tag(): user.splits
tag(): user.line_commands

# ----- GENERAL ----- #
#suplex: key(ctrl-x)
exchange: user.emacs("exchange-point-and-mark")
execute: user.emacs_meta_x()
execute {user.emacs_command}$: user.emacs(emacs_command)
execute <user.text>$:
    user.emacs_meta_x()
    user.insert_formatted(text, "DASH_SEPARATED")
evaluate | (evaluate | eval) (exper | expression): user.emacs("eval-expression")
prefix: user.emacs_command("universal-argument")
prefix <user.number_signed_small>: user.emacs_prefix(number_signed_small)

open directory: user.emacs("dired-jump")
other open directory: user.emacs("dired-jump-other-window")
fill paragraph: user.emacs("fill-paragraph")
occurs: user.emacs("occur")
other scroll [down]: user.emacs_meta("pagedown")
other scroll up: user.emacs_meta("pageup")
insert unicode: user.emacs("insert-char")
abort recursive [edit]: user.emacs("abort-recursive-edit")
save some buffers: user.emacs("save-some-buffers")
[toggle] read only [mode] [toggle]: user.emacs("read-only-mode")
[toggle] input method [toggle]: user.emacs("toggle-input-method")

save buffers kill emacs: user.emacs("save-buffers-kill-emacs")
package list | [package] list packages: user.emacs("list-packages")
package autoremove: user.emacs("package-autoremove")
reverse (lines | region): user.emacs("reverse-region")
browse kill ring: user.emacs("browse-kill-ring")
sort lines: user.emacs("sort-lines")
sort words: user.emacs("sort-words")
[toggle] line numbers [toggle]: user.emacs("display-line-numbers-mode")
[toggle] debug on error [toggle]: user.emacs("toggle-debug-on-error")
[toggle] truncate lines [toggle]: user.emacs("toggle-truncate-lines")
[toggle] word wrap [toggle]: user.emacs("toggle-word-wrap")

manual: user.emacs("man")
manual <user.text>:
    user.emacs("man")
    user.insert_formatted(text, "DASH_SEPARATED")

# BUFFER SWITCHING #
# many things override these keybindings, so we don't use user.emacs
switch: key(ctrl-x b)
other switch: key(ctrl-x 4 b)
display: key(ctrl-x 4 ctrl-o)

# SHELL COMMANDS #
shell command: user.emacs("shell-command")
shell command inserting:
    key(ctrl-u)
    user.emacs("shell-command")
shell command on region: user.emacs("shell-command-on-region")
shell command on region replacing:
    key(ctrl-u)
    user.emacs("shell-command-on-region")

# CUSTOMIZE #
customize face: user.emacs("customize-face")
customize group: user.emacs("customize-group")
customize variable: user.emacs("customize-variable")
(customize | custom) [theme] visit theme: user.emacs("custom-theme-visit-theme")

# MODE COMMANDS #
auto fill mode: user.emacs("auto-f")
dired omit mode: user.emacs("dired-omit-mode")
fundamental mode: user.emacs("fundamental-mode")
global highlight line mode: user.emacs("global-hl-line-mode")
global visual line mode: user.emacs("global-visual-line-mode")
global [display] line numbers [mode]: user.emacs("global-display-line-numbers-mode")
highlight line mode: user.emacs("hl-line-mode")
markdown mode: user.emacs("markdown-mode")
paredit mode: user.emacs("paredit-mode")
rainbow mode: user.emacs("rainbow-mode")
sub word mode: user.emacs("subword-mode")
text mode: user.emacs("text-mode")
visual line mode: user.emacs("visual-line-mode")
outline minor mode: user.emacs("outline-minor-mode")
emacs lisp mode: user.emacs("emacs-lisp-mode")
lisp interaction mode: user.emacs("lisp-interaction-mode")
talon script mode: user.emacs("talonscript-mode")

# MACROS #
emacs record: user.emacs("kmacro-start-macro")
emacs stop: user.emacs("kmacro-end-macro")
emacs play: user.emacs("kmacro-end-and-call-macro")

# PROFILER #
profiler start: user.emacs("profiler-start")
profiler stop: user.emacs("profiler-stop")
profiler report: user.emacs("profiler-report")

# WINDOW/SPLIT MANAGEMENT #
split solo: user.emacs("delete-other-windows")
[split] rebalance: user.emacs("balance-windows")
split shrink: user.emacs("shrink-window-if-larger-than-buffer")
other [split] shrink:
    user.split_next()
    user.emacs("shrink-window-if-larger-than-buffer")
    user.split_last()
split grow: user.emacs("enlarge-window")
split grow <number_small>: user.emacs("enlarge-window", number_small)
split shrink <number_small>:
    amount = number_small or 1
    user.emacs("enlarge-window", 0 - amount)
split widen [<number_small>]:
    user.emacs("enlarge-window-horizontally", number_small or 1)
split narrow [<number_small>]:
    user.emacs("shrink-window-horizontally", number_small or 1)

# ----- HELP ----- #
apropos: user.emacs_help("a")
describe (fun | function): user.emacs_help("f")
describe key: user.emacs_help("k")
describe key briefly: user.emacs_help("c")
describe symbol: user.emacs_help("o")
describe variable: user.emacs_help("v")
describe mode: user.emacs_help("m")
describe bindings: user.emacs_help("b")
describe (char | character): user.emacs("describe-character")
describe text properties: user.emacs("describe-text-properties")
describe face: user.emacs("describe-face")
view lossage: user.emacs_help("l")

apropos <user.text>$:
    user.emacs_help("a")
    user.insert_formatted(text, "DASH_SEPARATED")
    key(enter)
describe (fun | function) <user.text>$:
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
# many key bindings here are often overridden, so we don't use user.emacs,
# eg: C-x C-f, C-x k, C-x C-b, C-x right, C-x left
file open: key(ctrl-x ctrl-f)
file rename: user.emacs("rename-file")
(file open | find file) at point: user.emacs("ffap")
other file open: key(ctrl-x 4 ctrl-f)
(file | buffer) close: key(ctrl-x k enter)

buffer kill: key(ctrl-x k)
buffer bury: user.emacs("bury-buffer")
buffer revert | revert buffer: user.emacs("revert-buffer")
buffer finish:
    edit.save()
    user.emacs("server-edit")
buffer list: key(ctrl-x ctrl-b)
buffer next: key(ctrl-x right)
buffer last: key(ctrl-x left)
buffer rename: user.emacs("rename-buffer")

diff (buffer | [buffer] with file):
    user.emacs("diff-buffer-with-file")
    key(enter)

# ----- MOTION AND EDITING ----- #
mark: user.emacs("set-mark-command")
go back: user.emacs("pop-mark")
global [go] back: user.emacs("pop-global-mark")

cut line:
    edit.line_start()
    user.emacs_prefix(1)
    key(ctrl-k)
auto indent: user.emacs("indent-region")
indent <user.number_signed_small>: user.emacs("indent-rigidly", number_signed_small)

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
    user.emacs_prefix(-1 - number)
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

term right: user.emacs("forward-sexp")
term left: user.emacs("backward-sexp")
term up: user.emacs("backward-up-list")
term end: user.emacs("up-list")
term down: user.emacs("down-list")
term kill: user.emacs("kill-sexp")
term wipe: user.emacs("kill-sexp", -1)
term (mark | select): user.emacs("mark-sexp")
term copy:
    user.emacs("mark-sexp")
    edit.copy()
term freeze:
    user.emacs("mark-sexp")
    user.emacs("comment-region")
term [auto] indent:
    user.emacs("mark-sexp")
    user.emacs("indent-region")

(sentence | sent) (right | end): edit.sentence_end()
(sentence | sent) (left | start): edit.sentence_start()
(sentence | sent) kill: user.emacs("kill-sentence")

graph kill: user.emacs("kill-paragraph")
graph up: edit.paragraph_start()
graph down: edit.paragraph_end()
graph mark: user.emacs("mark-paragraph")
graph copy:
    user.emacs("mark-paragraph")
    edit.copy()
graph cut:
    user.emacs("mark-paragraph")
    edit.cut()

# could use these to implement "drag <X> left/right/up/down" commands
# but note that eg 'transpose line' and 'drag line down' are different
transpose [word | words]: user.emacs("transpose-words")
transpose (term | terms): user.emacs("transpose-sexps")
transpose (char | chars): user.emacs("transpose-chars")
transpose (line | lines): user.emacs("transpose-lines")
transpose (sentence | sentences): user.emacs("transpose-sentences")
transpose (graph | graphs | paragraphs): user.emacs("transpose-paragraphs")

register (copy | save): user.emacs("copy-to-register")
register (paste | insert): user.emacs("insert-register")
register jump: user.emacs("jump-to-register")
register (copy | save) rectangle: user.emacs("copy-rectangle-to-register")

rectangle clear: user.emacs("clear-rectangle")
rectangle delete: user.emacs("delete-rectangle")
rectangle kill: user.emacs("kill-rectangle")
rectangle open: user.emacs("open-rectangle")
rectangle (copy | save) [to] register: user.emacs("copy-rectangle-to-register")
rectangle (yank | paste): user.emacs("yank-rectangle")
rectangle copy: user.emacs("copy-rectangle-as-kill")
rectangle number lines: user.emacs("rectangle-number-lines")

# ----- MAJOR & MINOR MODES ----- #

# python-mode #
run python: user.emacs("run-python")
python load file: user.emacs("python-shell-send-buffer")

# smerge-mode #
merge next: user.emacs("smerge-next")
merge last: user.emacs("smerge-prev")
merge keep upper: user.emacs("smerge-keep-upper")
merge keep lower: user.emacs("smerge-keep-lower")
merge keep this: user.emacs("smerge-keep-current")
merge refine: user.emacs("smerge-refine")
merge split: user.emacs("smerge-resolve")

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
outline (backward | back) [same level]: key("ctrl-c @ ctrl-b")
outline next [visible heading]: key("ctrl-c @ ctrl-n")
outline (previous | last) [visible heading]: key("ctrl-c @ ctrl-p")
outline insert [heading]: key(ctrl-c @ RET)
outline up [heading]: key("ctrl-c @ ctrl-u")
outline promote: key(ctrl-c @ ctrl-<)
outline demote: key(ctrl-c @ ctrl->)
outline move [subtree] down: key(ctrl-c @ ctrl-v)
outline move [subtree] up: key(ctrl-c @ ctrl-^)
outline mark [subtree]: key(ctrl-c @ @)
