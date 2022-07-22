app: emacs
app: Emacs
-
tag(): user.tabs
tag(): user.splits
tag(): user.line_commands


# ----- GENERAL ----- #
#suplex: key(ctrl-x)
exchange: key(ctrl-x ctrl-x)
execute: user.emacs_meta("x")
execute <user.text>$:
  user.emacs_meta("x")
  user.insert_formatted(text, "DASH_SEPARATED")
evaluate | (evaluate|eval) (exper|expression): user.emacs_meta(":")
prefix: key(ctrl-u)
prefix <number_small>: user.emacs_prefix(number_small)

open directory: key(ctrl-x ctrl-j)
other open directory: key(ctrl-x 4 ctrl-j)
fill paragraph: user.emacs_meta("q")
occurs: key(ctrl-c o)
other scroll [down]: user.emacs_meta("pagedown")
other scroll up: user.emacs_meta("pageup")
insert unicode: key(ctrl-x 8 enter)
abort recursive [edit]: key("ctrl-]")
save some buffers: key(ctrl-x s)
[toggle] read only [mode] [toggle]: key(ctrl-x ctrl-q)
[toggle] input method [toggle]: key(ctrl-\)

save buffers kill emacs: user.emacs_command("s-b-k-e")
package list | [package] list packages: user.emacs_command("list-packages")
package autoremove: user.emacs_command("package-autoremove")
reverse (lines|region): user.emacs_command("reverse-region")
browse kill ring: user.emacs_command("b-k-r")
sort lines: user.emacs_command("sort-lines")
sort words: user.emacs_command("sort-words")
[toggle] line numbers [toggle]: user.emacs_command("dis-num")
[toggle] debug on error [toggle]: user.emacs_command("toggle-debug-on-error")
[toggle] truncate lines [toggle]: user.emacs_command("toggle-truncate-lines")
[toggle] word wrap [toggle]: user.emacs_command("toggle-word-wrap")

manual: user.emacs_command("man")
manual <user.text>:
  user.emacs_command("man")
  user.insert_formatted(text)

# BUFFER SWITCHING #
switch: key(ctrl-x b)
other switch: key(ctrl-x 4 b)
display: key(ctrl-x 4 ctrl-o)

# SHELL COMMANDS #
shell command: user.emacs_meta("!")
shell command inserting:
  key(ctrl-u)
  user.emacs_meta("!")
shell command on region: user.emacs_meta("|")
shell command on region replacing:
  key(ctrl-u)
  user.emacs_meta("|")

# CUSTOMIZE #
customize face: user.emacs_command("customize-face")
customize group: user.emacs_command("customize-group")
customize variable: user.emacs_command("customize-variable")
(customize|custom) [theme] visit theme: user.emacs_command("custom-theme-visit-theme")

# MODE COMMANDS #
auto fill mode: user.emacs_command("auto-f")
dired omit mode: user.emacs_command("dired-omit-mode")
fundamental mode: user.emacs_command("fun-m")
global highlight line mode: user.emacs_command("g-hl-l-m")
global visual line mode: user.emacs_command("gl-v-l-m")
global [display] line numbers [mode]:
  user.emacs_command("global-display-line-numbers-mode")
highlight line mode: user.emacs_command("hl-l-m")
markdown mode: user.emacs_command("markdown-mode")
paredit mode: user.emacs_command("paredit-mode")
rainbow mode: user.emacs_command("rainbow-mode")
sub word mode: user.emacs_command("subword-mode")
text mode: user.emacs_command("text-m")
visual line mode: user.emacs_command("visu-l-m")
outline minor mode: user.emacs_command("outline-minor-mode")
emacs lisp mode: user.emacs_command("emacs-lisp-mode")
lisp interaction mode: user.emacs_command("lisp-interaction-mode")
talon script mode: user.emacs_command("tal-m")

# MACROS #
emacs record: key("ctrl-x (")
emacs stop: key("ctrl-x )")
emacs play: key("ctrl-x e")

# PROFILER #
profiler start: user.emacs_command("profiler-start")
profiler stop: user.emacs_command("profiler-stop")
profiler report: user.emacs_command("profiler-report")

# WINDOW/TAB/SPLIT MANAGEMENT #
# What emacs calls windows, I call tabs.
# Probably most folks would call them splits?
tab solo: key(ctrl-x 1)
[split|tab] rebalance: key(ctrl-x +)
tab shrink: key(ctrl-x -)
other shrink:
  user.split_next()
  key(ctrl-x -)
  user.split_last()
tab grow: key(ctrl-x ^)
tab grow <number_small>:
  user.emacs_prefix(number_small)
  key(ctrl-x ^)
tab shrink <number_small>:
  amount = number_small or 1
  user.emacs_prefix(0 - amount)
  key(ctrl-x ^)
tab widen [<number_small>]:
  user.emacs_prefix(number_small or 1)
  key("ctrl-x }")
tab narrow [<number_small>]:
  user.emacs_prefix(number_small or 1)
  key("ctrl-x {")


# ----- HELP ----- #
apropos: user.emacs_help("a")
describe (fun|function): user.emacs_help("f")
describe key: user.emacs_help("k")
describe key briefly: user.emacs_help("c")
describe symbol: user.emacs_help("o")
describe variable: user.emacs_help("v")
describe mode: user.emacs_help("m")
describe bindings: user.emacs_help("b")
describe (char|character): user.emacs_command("desc-char")
describe text properties: user.emacs_command("describe-text-properties")
describe face: user.emacs_command("describe-face")

apropos <user.text>$:
  user.emacs_help()
  key(a)
  user.insert_formatted(text, "DASH_SEPARATED")
  key(enter)
describe (fun|function) <user.text>$:
  user.emacs_help()
  key(f)
  user.insert_formatted(text, "DASH_SEPARATED")
  key(enter)
describe symbol <user.text>$:
  user.emacs_help()
  key(o)
  user.insert_formatted(text, "DASH_SEPARATED")
  key(enter)
describe variable <user.text>$:
  user.emacs_help()
  key(v)
  user.insert_formatted(text, "DASH_SEPARATED")
  key(enter)


# ----- FILES & BUFFERS -----
file open: key(ctrl-x ctrl-f)
file rename: user.emacs_command("rename-file")
(file open | find file) at point: user.emacs_command("ffap")
other file open: key(ctrl-x 4 ctrl-f)
(file | buffer) close: key(ctrl-x k enter)

buffer kill: key(ctrl-x k)
buffer bury: user.emacs_command("bur")
buffer revert | revert buffer: user.emacs_command("rev-buf")
buffer finish: key(ctrl-x ctrl-s ctrl-x #)
buffer list: key(ctrl-x ctrl-b)
buffer next: key(ctrl-x right)
buffer last: key(ctrl-x left)
buffer rename: user.emacs_command("ren-b")

diff (buffer | [buffer] with file):
  user.emacs_command("dbwf")
  key(enter)
kill buffers matching [file name | filename]: user.emacs_command("k-b-m-f")


# ----- MOTION AND EDITING ----- #
mark: key(ctrl-space)
go back: key("ctrl-u ctrl-space")
global [go] back: key("ctrl-x ctrl-@")

cut line:
  edit.line_start()
  user.emacs_prefix(1)
  key(ctrl-k)
auto indent: user.emacs_meta("ctrl-\\")
indent <user.number_signed_small>:
  user.emacs_prefix(number_signed_small)
  key(ctrl-x tab)

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

next error | error next:
  user.emacs_meta("g")
  key(n)
last error | error last:
  user.emacs_meta("g")
  key(p)

term right: user.emacs_meta("ctrl-f")
term left: user.emacs_meta("ctrl-b")
term up: key(escape ctrl-up)
term end: key(escape - 1 escape ctrl-up)
term down: key(escape ctrl-down)
term kill: key(escape ctrl-k)
term wipe: key(escape - 1 escape ctrl-k)
term (mark | select): key(escape ctrl-@)
term copy: key(escape ctrl-@ escape w)
term freeze: key(escape ctrl-@ ctrl-c ;)
term [auto] indent: key(escape ctrl-@ escape ctrl-\)

(sentence|sent) (right | end): edit.sentence_end()
(sentence|sent) (left | start): edit.sentence_start()
(sentence|sent) kill: user.emacs_meta("k")

graph kill: user.emacs_command("kill-par")
graph up: edit.paragraph_start()
graph down: edit.paragraph_end()
graph mark: user.emacs_meta("h")
graph copy: user.emacs_meta("h w")
graph cut:
  user.emacs_meta("h")
  key(ctrl-w)

# maybe we should call these "drag <X> left/right/up/down"
transpose [word|words]: user.emacs_meta("t")
transpose (term|terms): user.emacs_meta("ctrl-t")
transpose (char|chars): key(ctrl-t)
transpose (line|lines): key(ctrl-x ctrl-t)
transpose (sentence|sentences): user.emacs_command("tr-sen")
transpose (graph|graphs|paragraphs): user.emacs_command("tr-par")

register (copy|save): key("ctrl-x r s")
register (paste|insert): key("ctrl-x r i")
register jump: key(ctrl-x r j)

(search regex | regex search): user.emacs_meta("ctrl-s")
(search regex | regex search) back: user.emacs_meta("ctrl-r")
replace: user.emacs_meta("%")
replace regex | regex replace: user.emacs_meta("ctrl-%")
search edit: user.emacs_meta("e")
search toggle regex: user.emacs_meta("r")
search toggle word:
  user.emacs_meta("s")
  key(w)


# ----- MAJOR & MINOR MODES ----- #

# python-mode #
run python: user.emacs_command("run-python")
python load file: key(ctrl-c ctrl-l enter)

# smerge-mode #
merge next: key("ctrl-c ^ n")
merge last: key("ctrl-c ^ p")
merge keep upper: key("ctrl-c ^ u")
merge keep lower: key("ctrl-c ^ l")
merge keep this: key("ctrl-c ^ enter")
merge refine: key("ctrl-c ^ R")
merge split: key("ctrl-c ^ r")

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
