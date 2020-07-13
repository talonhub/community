# Requires https://plugins.jetbrains.com/plugin/10504-voice-code-idea
app: /jetbrains/
app: IntelliJ IDEA
app: idea64.exe
app: PyCharm
app: PyCharm64.exe
app: pycharm64.exe
app: webstorm64.exe
-
tag(): ide
tag(): tabs
tag(): line_commands
tag(): splits 

# Auto complete
action(code.complete): user.idea("action CodeCompletion")
action(user.ide_perfect): user.idea("action CodeCompletion,action CodeCompletion")
action(user.ide_smart): user.idea("action SmartTypeCompletion")
action(user.ide_done):  user.idea("action EditorCompleteStatement")
action(user.ide_toggle_tools):  user.idea("action HideAllWindows")

# Movement
action(edit.line_swap_up):  user.idea("action MoveLineUp")
action(edit.line_swap_down):  user.idea("action MoveLineDown")
action(user.ide_multi_cursor): key(shift-alt-insert)
action(user.ide_multi_cursor_stop): key(escape)
action(user.ide_up_cursor): user.idea("action EditorCloneCaretAbove")
action(user.ide_down_cursor): user.idea("action EditorCloneCaretBelow")

# Copying
action(edit.line_clone):  user.idea("action EditorDuplicate")
clone <number>: user.idea("clone {number}")
grab <number>: user.idea_grab(number)

# Actions
(action | please): user.idea("action GotoAction")
(action | please) <phrase>:
  user.idea("action GotoAction")
  insert(dictate.join_words(phrase))
extend <number>: user.extend_action(number)

# Refactoring
action(user.ide_refactor): user.idea("action Refactorings.QuickListPopupAction")
refactor <phrase>:
  user.idea("action Refactorings.QuickListPopupAction")
  insert(dictate.join_words(phrase))
action(user.ide_extract_variable): user.idea("action IntroduceVariable")
action(user.ide_extract_field): user.idea("action IntroduceField")
action(user.ide_extract_constant): user.idea("action IntroduceConstant")
action(user.ide_extract_parameter): user.idea("action IntroduceParameter")
action(user.ide_extract_interface): user.idea("action ExtractInterface")
action(user.ide_extract_method): user.idea("action ExtractMethod")
action(user.ide_refactor_in_line): user.idea("action Inline")
action(user.ide_refactor_move): user.idea("action Move")
action(user.ide_refactor_rename): user.idea("action RenameElement")
action(user.ide_rename_file): user.idea("action RenameFile")

action(user.ide_fix_format): user.idea("action ReformatCode")
action(user.ide_fix_imports): user.idea("action OptimizeImports")

action(user.ide_follow): user.idea("action GotoDeclaration")
action(user.ide_go_implementation): user.idea("action GotoImplementation")
action(user.ide_go_usage): user.idea("action FindUsages")
action(user.ide_go_type): user.idea("action GotoTypeDeclaration")
action(user.ide_go_test): user.idea("action GotoTest")
action(user.ide_go_back): user.idea("action Back")
action(user.ide_go_forward): user.idea("action Forward")

# Special Selects
action(user.ide_select_less): user.idea("action EditorUnSelectWord")
action(user.ide_select_more): user.idea("action EditorSelectWord")
action(user.ide_multi_select_fewer): user.idea("action UnselectPreviousOccurrence")
action(user.ide_multi_select_more): user.idea("action SelectNextOccurrence")
action(user.ide_multi_select_all): user.idea("action SelectAllOccurrences")

# Search
action(edit.find): user.idea("action Find")
action(user.ide_find_everywhere): user.idea("action SearchEverywhere")
find (everywhere | all) <phrase> [over]:
  user.idea("action SearchEverywhere")
  sleep(500ms)
  insert(phrase)

action(user.ide_find_class): user.idea("action GotoClass")
action(user.ide_find_file): user.idea("action GotoFile")
action(user.ide_recent): user.idea("action RecentFiles")
action(edit.find_next): user.idea("action FindNext")
action(edit.find_previous): user.idea("action FindPrevious")
action(user.ide_find_in_path): user.idea("action FindInPath")

surround [this] with <phrase> [over]:
    idea("action SurroundWith")
    sleep(500ms)
    insert(phrase)

# Making these longer to reduce collisions with real code dictation.
insert generated <phrase> [over]:
    user.idea("action Generate")
    sleep(500ms)
    insert(phrase)
insert template <phrase> [over]:
    idea("action InsertLiveTemplate")
    sleep(500ms)
    insert(phrase)

action(user.ide_create_template): user.idea("action SaveAsTemplate")

action(user.ide_run_menu): user.idea("action ChooseRunConfiguration")
action(user.ide_run_again): user.idea("action Run")
# Recording
action(user.ide_toggle_recording): user.idea("action StartStopMacroRecording")
action(user.ide_change_recording): user.idea("action EditMacros")
action(user.ide_play_recording): user.idea("action PlaybackLastMacro")

play recording <phrase> [over]:
    idea("action PlaySavedMacrosAction")
    insert(phrase)
    sleep(500ms)
    Key("enter")

 # Marks
action(user.ide_go_mark): user.idea("action ShowBookmarks")
action(user.ide_toggle_mark): user.idea("action ToggleBookmark")

action(user.ide_go_next_mark): user.idea("action GotoNextBookmark")
action(user.ide_go_last_mark): user.idea("action GotoPreviousBookmark")
toggle mark <number>: user.idea("action ToggleBookmark{number}")
go mark <number>: user.idea("action GotoBookmark{number}")
# Folding
action(user.ide_expand_deep): user.idea("action ExpandRegionRecursively")
action(user.ide_expand_all): user.idea("action ExpandAllRegions")
action(user.ide_collapse_deep): user.idea("action CollapseRegionRecursively")
action(user.ide_collapse_all): user.idea("action CollapseAllRegions")
# miscellaneous
# XXX These might be better than the structural ones depending on language.
action(user.ide_go_next_method): user.idea("action MethodDown")
action(user.ide_go_last_method): user.idea("action MethodUp")
# Clipboard
action(user.ide_clippings): user.idea("action PasteMultiple")
action(user.ide_copy_path): user.idea("action CopyPaths")
action(user.ide_copy_reference): user.idea("action CopyReference")
action(user.ide_copy_pretty): user.idea("action CopyAsRichText")
# File Creation
action(user.ide_create_sibling): user.idea("action NewElementSamePlace")
create sibling <phrase> [over]:
    user.idea("action NewElementSamePlace")
    sleep(500ms)
    insert(phrase)
action(user.ide_create_file): user.idea("action NewElement")
create file <phrase> [over]:
  user.idea("action NewElement")
  sleep(500ms)
  insert(phrase)
# Task Management
action(user.ide_go_task): user.idea("action tasks.goto")
action(user.ide_go_browser_task): user.idea("action tasks.open.in.browser")
action(user.ide_switch_task): user.idea("action tasks.switch")
action(user.ide_clear_task): user.idea("action tasks.close")
action(user.ide_configure_servers): user.idea("action tasks.configure.servers")
# Git / Github (not using verb-noun-adjective pattern, mirroring terminal commands.)
action(user.ide_git_pull): user.idea("action Vcs.UpdateProject")
action(user.ide_git_commit): user.idea("action CheckinProject")
action(user.ide_git_push): user.idea("action CheckinProject")
action(user.ide_git_log): user.idea("action Vcs.ShowTabbedFileHistory")
action(user.ide_git_browse): user.idea("action Github.Open.In.Browser")
action(user.ide_git_get): user.idea("action Github.Create.Gist")
action(user.ide_git_pull_request): user.idea("action Github.Create.Pull.Request")
action(user.ide_git_list_requests): user.idea("action Github.View.Pull.Request")
action(user.ide_git_annotate): user.idea("action Annotate")
action(user.ide_git_menu): user.idea("action Vcs.QuickListPopupAction")
# Tool windows:
# Toggling various tool windows
action(user.ide_toggle_project): user.idea("action ActivateProjectToolWindow")
action(user.ide_toggle_find): user.idea("action ActivateFindToolWindow")
action(user.ide_toggle_run): user.idea("action ActivateRunToolWindow")
action(user.ide_toggle_debug): user.idea("action ActivateDebugToolWindow")
action(user.ide_toggle_events): user.idea("action ActivateEventLogToolWindow")
action(user.ide_toggle_terminal): user.idea("action ActivateTerminalToolWindow")
action(user.ide_toggle_git): user.idea("action ActivateVersionControlToolWindow")
action(user.ide_toggle_structure): user.idea("action ActivateStructureToolWindow")
action(user.ide_toggle_database): user.idea("action ActivateDatabaseToolWindow")
action(user.ide_toggle_database_changes): user.idea("action ActivateDatabaseChangesToolWindow")
action(user.ide_toggle_make): user.idea("action ActivatemakeToolWindow")
action(user.ide_toggle_to_do): user.idea("action ActivateTODOToolWindow")
action(user.ide_toggle_docker): user.idea("action ActivateDockerToolWindow")
action(user.ide_toggle_favorites): user.idea("action ActivateFavoritesToolWindow")
action(user.ide_toggle_last): user.idea("action JumpToLastWindow")
# Pin/dock/float
action(user.ide_toggle_pinned): user.idea("action TogglePinnedMode")
action(user.ide_toggle_docked): user.idea("action ToggleDockMode")
action(user.ide_toggle_floating): user.idea("action ToggleFloatingMode")
action(user.ide_toggle_windowed): user.idea("action ToggleWindowedMode")
action(user.ide_toggle_split): user.idea("action ToggleSideMode")
# Settings, not windows
action(user.ide_toggle_tool_buttons): user.idea("action ViewToolButtons")
action(user.ide_toggle_toolbar): user.idea("action ViewToolBar")
action(user.ide_toggle_status_bar): user.idea("action ViewStatusBar")
action(user.ide_toggle_navigation_bar): user.idea("action ViewNavigationBar")
# Active editor settings
action(user.ide_toggle_power_save): user.idea("action TogglePowerSave")
action(user.ide_toggle_whitespace): user.idea("action EditorToggleShowWhitespaces")
action(user.ide_toggle_indents): user.idea("action EditorToggleShowIndentLines")
action(user.ide_toggle_line_numbers): user.idea("action EditorToggleShowLineNumbers")
action(user.ide_toggle_breadcrumbs): user.idea("action EditorToggleShowBreadcrumbs")
action(user.ide_toggle_gutter_icons): user.idea("action EditorToggleShowGutterIcons")
action(user.ide_toggle_wrap): user.idea("action EditorToggleUseSoftWraps")
action(user.ide_toggle_parameters): user.idea("action ToggleInlineHintsAction")
# Toggleable views
action(user.ide_toggle_fullscreen): user.idea("action ToggleFullScreen")
action(user.ide_toggle_distraction_free): user.idea("action ToggleDistractionFreeMode")
action(user.ide_toggle_presentation_mode): user.idea("action TogglePresentationMode")
# Tabs
action(user.tab_final): user.idea("action GoToLastTab")
action(app.tab_next): user.idea("action NextTab")
action(app.tab_previous): user.idea("action PreviousTab")
action(app.tab_close): user.idea("action CloseActiveTab")
# Quick popups
action(user.ide_change_scheme): user.idea("action QuickChangeScheme")
 # Always javadoc
action(user.ide_toggle_documentation): user.idea("action QuickJavaDoc")
action(user.ide_toggle_definition): user.idea("action QuickImplementations")
action(user.ide_pop_type): user.idea("action ExpressionTypeInfo")
action(user.ide_pop_parameters): user.idea("action ParameterInfo")
# Breakpoints / debugging
action(user.ide_run_test): user.idea("action RunClass")
action(user.ide_run_test_again): user.idea("action Rerun")
action(user.ide_debug_test): user.idea("action DebugClass")
action(user.ide_go_breakpoints): user.idea("action ViewBreakpoints")
action(user.ide_toggle_breakpoint): user.idea("action ToggleLineBreakpoint")
action(user.ide_toggle_method_breakpoint): user.idea("action ToggleMethodBreakpoint")
action(user.ide_step_over): user.idea("action StepOver")
action(user.ide_step_into): user.idea("action StepInto")
action(user.ide_step_smart): user.idea("action SmartStepInto")
action(user.ide_step_to_line): user.idea("action RunToCursor")
action(user.ide_continue): user.idea("action Resume")
# Grow / Shrink
action(user.ide_resize_window_right): user.idea("action ResizeToolWindowRight")
action(user.ide_resize_window_left): user.idea("action ResizeToolWindowLeft")
action(user.ide_resize_window_up): user.idea("action ResizeToolWindowUp")
action(user.ide_resize_window_down): user.idea("action ResizeToolWindowDown")

# splits.py support
#action(user.split_window_left): user.idea("action MoveTabLeft")
action(user.split_window_right): user.idea("action MoveTabRight")
action(user.split_window_down): user.idea("action MoveTabDown")
#action(user.split_window_up): user.idea("action MoveTabUp")
action(user.split_window_vertically): user.idea("action SplitVertically")
action(user.split_window_horizontally): user.idea("action SplitHorizontally")
action(user.split_flip): user.idea("action ChangeSplitOrientation")
action(user.split_window): user.idea("action EditSourceInNewWindow")
action(user.split_clear): user.idea("action Unsplit")
action(user.split_clear_all): user.idea("action UnsplitAll")
action(user.split_next): user.idea("action NextSplitter")
action(user.split_last): user.idea("action LastSplitter")

# Movement
<user.navigation_verbs> next (error | air): user.idea_movement(navigation_verbs, "action GotoNextError")
<user.navigation_verbs> last (error | air): user.idea_movement(navigation_verbs, "action GotoPreviousError")

