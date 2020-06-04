app: /jetbrains/

app: IntelliJ IDEA
app: PyCharm
app: PyCharm64.exe
app: Visual Studio Code
app: Code - OSS
app: Code
app: Code.exe
app: Atom
app: atom.exe

# TODO When tags are supported
#tags: ide
-
refactor: user.ide_refactor()


#Intellisense, Rich language support
suggest (parameters | (args | arguments)): user.ide_intellisense_suggest_parameters()
complete: code.complete()
perfect: user.ide_perfect()
smart: user.ide_smart()
done: user.ide_done()
finish: user.ide_done()

extract variable: user.ide_extract_variable()
extract field: user.ide_extract_field()
extract constant: user.ide_extract_constant()
extract parameter: user.ide_extract_parameter()
extract interface: user.ide_extract_interface()
extract method: user.ide_extract_method()
refactor in line: user.ide_refactor_in_line()
refactor move: user.ide_refactor_move()
refactor rename: user.ide_refactor_rename()
rename file: user.ide_rename_file()

fix (format | formatting): user.ide_fix_format()
fix imports: user.ide_fix_imports()
(go declaration | follow): user.ide_follow()
go implementation: user.ide_go_implementation()
go usage: user.ide_go_usage()
go type: user.ide_go_type()
go test: user.ide_go_test()
go back: user.ide_go_back()
go forward: user.ide_go_forward()

find (everywhere | all): user.ide_find_everywhere()
(search | find) class: user.ide_find_class()
(search | find) file: user.ide_find_file()
(search | find) path: user.ide_find_in_path()
recent: user.ide_recent()

create (template|snippet): user.ide_create_template()
run menu: user.ide_run_menu()
run again: user.ide_run_again()
# Recording
toggle recording: user.ide_toggle_recording()
change (recording | recordings): user.ide_change_recording()
play recording: user.ide_play_recording()

# Marks
go mark: user.ide_go_mark()
toggle mark: user.ide_toggle_mark()

go next mark: user.ide_go_next_mark()
go last mark: user.ide_go_last_mark()
# Folding
expand deep: user.ide_expand_deep()
expand all: user.ide_expand_all()
expand that: user.ide_expand_region()
collapse deep: user.ide_collapse_deep()
collapse all: user.ide_collapse_all()
collapse that: user.ide_collapse_region()
# Splits
split right: user.ide_split_right()
split left: user.ide_split_left()
split down: user.ide_split_down()
split up: user.ide_split_up()
split vertically: user.ide_split_vertically()
split horizontally: user.ide_split_horizontally()
split flip: user.ide_split_flip()
split window: user.ide_split_window()
clear split: user.ide_clear_split()
clear all splits: user.ide_clear_all_splits()
go next split: user.ide_go_next_split()
go last split: user.ide_go_last_split()
# miscellaneous
# XXX These might be better than the structural ones depending on language.
go next (method | function): user.ide_go_next_method()
go last (method | function): user.ide_go_last_method()
# Clipboard
clippings: user.ide_clippings()
copy path: user.ide_copy_path()
copy reference: user.ide_copy_reference()
copy pretty: user.ide_copy_pretty()
# File Creation
create sibling: user.ide_create_sibling()
create file: user.ide_create_file()

# Task Management
go task: user.ide_go_task()
go browser task: user.ide_go_browser_task()
switch task: user.ide_switch_task()
clear task: user.ide_clear_task()

configure servers: user.ide_fix_task_settings()
# Git / Github (not using verb-noun-adjective pattern, mirroring terminal commands.)
git pull: user.ide_git_pull()
git commit: user.ide_git_commit()
git push: user.ide_git_push()
git log: user.ide_git_log()
git browse: user.ide_git_browse()
git (gets | gist): user.ide_git_get()
git (pull request | request): user.ide_git_pull_request()
git (view | show | list) (requests | request): user.ide_git_list_requests()
git (annotate | blame): user.ide_git_annotate()
git menu: user.ide_git_menu()

# Terminal
new terminal: user.ide_terminal_new()
next terminal: user.ide_terminal_focus_next()
trash terminal: user.ide_terminal_trash()
(previous | last) terminal: user.ide_terminal_focus_previous()
terminal scroll up: user.ide_terminal_scroll_up()
terminal scroll down: user.ide_terminal_scroll_down()


# Tool windows:
command palette: user.ide_command_palette()
reveal in manager: user.ide_reveal_in_file_manager()

# Toggling various tool windows
toggle project: user.ide_toggle_project()
toggle find: user.ide_toggle_find()
toggle run: user.ide_toggle_run()
toggle debug: user.ide_toggle_debug()
toggle extensions: user.ide_toggle_extensions()
toggle events: user.ide_toggle_events()
toggle terminal: user.ide_toggle_terminal()
toggle git: user.ide_toggle_git()
toggle structure: user.ide_toggle_structure()
toggle database: user.ide_toggle_database()
toggle database changes: user.ide_toggle_database_changes()
toggle make: user.ide_toggle_make()
toggle to do: user.ide_toggle_to_do()
toggle docker: user.ide_toggle_docker()
toggle favorites: user.ide_toggle_favorites()
toggle last: user.ide_toggle_last()
# Pin/dock/float
toggle pinned: user.ide_toggle_pinned()
toggle docked: user.ide_toggle_docked()
toggle floating: user.ide_toggle_floating()
toggle windowed: user.ide_toggle_windowed()
toggle split: user.ide_toggle_split()
# Settings, not windows
toggle tool buttons: user.ide_toggle_tool_buttons()
toggle toolbar: user.ide_toggle_toolbar()
toggle status [bar]: user.ide_toggle_status_bar()
toggle navigation [bar]: user.ide_toggle_navigation_bar()
# Active editor settings
toggle power save: user.ide_toggle_power_save()
toggle whitespace: user.ide_toggle_whitespace()
toggle indents: user.ide_toggle_indents()
toggle line numbers: user.ide_toggle_line_numbers()
toggle bread crumbs: user.ide_toggle_breadcrumbs()
toggle gutter icons: user.ide_toggle_gutter_icons()
toggle wrap: user.ide_toggle_wrap()
toggle parameters: user.ide_toggle_parameters()

# Toggleable views
toggle fullscreen: user.ide_toggle_fullscreen()
toggle distraction [free mode]: user.ide_toggle_distraction_free()
toggle presentation [mode]: user.ide_toggle_presentation_mode()
# Toggle additionals
toggle comment: user.ide_toggle_comment()
# Tabs
go first tab: user.ide_go_first_tab()
go second tab: user.ide_go_second_tab()
go third tab: user.ide_go_third_tab()
go fourth tab: user.ide_go_fourth_tab()
go fifth tab: user.ide_go_fifth_tab()
go sixth tab: user.ide_go_sixth_tab()
go seventh tab: user.ide_go_seventh_tab()
go eighth tab: user.ide_go_eighth_tab()
go ninth tab: user.ide_go_ninth_tab()
go final tab: user.ide_go_final_tab()
clear tab: user.ide_clear_tab()
# Quick popups
change scheme: user.ide_change_scheme()
(toggle | pop) (doc | documentation): user.ide_toggle_documentation()
(pop deaf | toggle definition): user.ide_toggle_definition()
pop type: user.ide_pop_type()
pop parameters: user.ide_pop_parameters()
# Breakpoints / debugging
go breakpoints: user.ide_go_breakpoints()
toggle [line] breakpoint: user.ide_toggle_breakpoint()
toggle method breakpoint: user.ide_toggle_method_breakpoint()
run test: user.ide_run_test()
run test again: user.ide_run_test_again()
debug test: user.ide_debug_test()
step over: user.ide_step_over()
step into: user.ide_step_into()
step out: user.ide_step_out()
step smart: user.ide_step_smart()
step to line: user.ide_step_to_line()
continue: user.ide_continue()
# Grow / Shrink
(grow | shrink) window right: user.ide_resize_window_right()
(grow | shrink) window left: user.ide_resize_window_left()
(grow | shrink) window up: user.ide_resize_window_up()
(grow | shrink) window down: user.ide_resize_window_down()

drag up:
	edit.line_swap_up()

drag down:
	edit.line_swap_down()

clone (line|this):
	edit.line_clone()

multiple cursor:
	user.ide_multi_cursor()

(end|stop) multiple cursor:
	user.ide_multi_cursor_stop()

multi select up:
	user.ide_up_cursor()

multi select down:
	user.ide_down_cursor()

multi select fewer:
	user.ide_multi_select_fewer()

multi select more:
	user.ide_multi_select_more()

multi select all:
	user.ide_multi_select_all()

select less:
	user.ide_select_less()

select (more|this):
	user.ide_select_more()
