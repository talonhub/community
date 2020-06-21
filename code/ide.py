from talon import Module

mod = Module()


@mod.action_class
class Actions:
    def ide_refactor():
        """Trigger refactoring menu of the ide"""

    def ide_perfect():
        """Trigger better auto complete in the ide"""

    def ide_smart():
        """Trigger suggestion / type completion in the ide"""

    def ide_finish():
        """Select auto complete statement"""

    def ide_done():
        """Select auto complete statement"""

    def ide_intellisense_suggest_parameters():
        """Trigger parameter hints"""

    def ide_toggle_tools():
        """Hide all windows"""

    def ide_editor_copylines_down():
        """Editor copy line down"""

    def ide_editor_copylines_up():
        """Editor copy line up"""

    def ide_extract_variable():
        """Trigger extract variable functionality of IDE"""

    def ide_extract_field():
        """Trigger extract field functionality of IDE"""

    def ide_extract_constant():
        """Trigger extract constant functionality of IDE"""

    def ide_extract_parameter():
        """Trigger extract parameter functionality of IDE"""

    def ide_extract_interface():
        """Trigger extract interface functionality of IDE"""

    def ide_extract_method():
        """Trigger extract method functionality of IDE"""

    def ide_refactor_in_line():
        """Trigger inline refactoring method of IDE"""

    def ide_refactor_move():
        """Trigger refactor move functionality of IDE"""

    def ide_refactor_rename():
        """Trigger refactor rename functionality of IDE"""

    def ide_rename_file():
        """Trigger rename file of IDE"""

    def ide_fix_format():
        """Trigger format code function"""

    def ide_fix_imports():
        """Trigger fix imports function"""

    def ide_follow():
        """Go to definition of selected item"""

    def ide_go_implementation():
        """Go to implementation of selected item"""

    def ide_go_usage():
        """Go to usage of selected item"""

    def ide_go_type():
        """Go to type of selected item"""

    def ide_go_test():
        """Go to test of selected item"""

    def ide_go_back():
        """Go to previous cursor position"""

    def ide_go_forward():
        """Go to next"""

    def ide_find_everywhere():
        """Searches the entire project"""

    def ide_find_class():
        """Open search for class functionality of ide"""

    def ide_find_in_path():
        """Open search filtered to selected path"""

    def ide_find_file():
        """Open search for file functionality of ide"""

    def ide_replace_everywhere():
        """Search and replaces in the entire project"""

    def ide_replace_local():
        """Search and replaces in the active editor"""

    def ide_replace_confirm_current():
        """Confirm replaces at current position"""
    def ide_replace_confirm_all():
        """Confirm replaces all"""

    def ide_find_match_by_case():
        """Toggles find match by case sensitivity"""

    def ide_find_match_by_word():
        """Toggles find match by whole words"""

    def ide_find_match_by_regex():
        """Toggles find match by regex"""

    def ide_recent():
        """Open recent files list"""

    def ide_multi_cursor():
        """Activate multi cursor mode"""

    def ide_multi_cursor_stop():
        """Deactivate multi cursor mode"""

    def ide_up_cursor():
        """Add a cursor above current cursors"""

    def ide_down_cursor():
        """Add a cursor below current cursors"""

    def ide_select_less():
        """Unselect current word"""

    def ide_select_more():
        """Select next word"""

    def ide_multi_select_fewer():
        """Unselect previously selected word"""

    def ide_multi_select_more():
        """Select next occurrence of word"""

    def ide_multi_select_all():
        """Select all occurrences of word"""

    def ide_create_template():
        """Trigger create template (snippet) functionality of ide"""

    def ide_run_menu():
        """Trigger run menu of IDE"""

    def ide_run_again():
        """Run the last item"""

    def ide_toggle_recording():
        """Start/finish recording"""

    def ide_change_recording():
        """Trigger menu to select recording"""

    def ide_play_recording():
        """Play last recording"""

    def ide_go_mark():
        """Go to bookmarks"""

    def ide_toggle_mark():
        """Add/remove bookmark"""

    def ide_go_next_mark():
        """Go the the next bookmark"""

    def ide_go_last_mark():
        """Go to the last bookmark"""

    def ide_expand_deep():
        """Expand code recursively"""

    def ide_expand_all():
        """Expand all blocks in file"""

    def ide_expand_region():
        """Expand current block in file"""

    def ide_collapse_deep():
        """Collapse code recursively"""

    def ide_collapse_all():
        """Collapse all code in file"""

    def ide_collapse_region():
        """Collapse current block in file"""

    def ide_split_right():
        """Copy current tab to the right pane"""

    def ide_split_left():
        """Copy current tab to the left pane"""

    def ide_split_down():
        """Copy tab to the pane below"""

    def ide_split_up():
        """Copy tab to the pane above"""

    def ide_split_vertically():
        """Split the view into panes vertically"""

    def ide_split_horizontally():
        """Split the view into panes horizontally"""

    def ide_split_flip():
        """Change split orientation"""

    def ide_split_window():
        """Open the current file in a new window"""

    def ide_clear_split():
        """Unsplit the current view (collapse this and previous pane into one)"""

    def ide_clear_all_splits():
        """Unsplit all views (back to single pane)"""

    def ide_go_next_split():
        """Go to next pane"""

    def ide_go_last_split():
        """Go to the previous pane"""

    def ide_go_next_method():
        """Go to the next method in the file"""

    def ide_go_last_method():
        """Go to the previous method in the file"""

    def ide_command_palette():
        """Open the command palette"""

    def ide_clippings():
        """Show copy history"""

    def ide_copy_path():
        """Copy path of file"""

    def ide_copy_reference():
        """Copy reference (code path to current location)"""

    def ide_copy_pretty():
        """Copy with formatting"""

    def ide_create_sibling():
        """Create a new element in the current folder"""

    def ide_create_file():
        """Create a new element"""

    def ide_go_task():
        """Open the search for task view"""

    def ide_go_browser_task():
        """Trigger "open in browser" task"""

    def ide_switch_task():
        """Open task switcher"""

    def ide_clear_task():
        """Close tasks list"""

    def ide_configure_servers():
        """Configure servers in IDE"""

    def ide_git_pull():
        """Trigger git pull command"""

    def ide_git_commit():
        """Trigger git commit command"""

    def ide_git_push():
        """Trigger git push command"""

    def ide_git_log():
        """Trigger git log command"""

    def ide_git_browse():
        """Trigger git browsing (open in browser)"""

    def ide_git_get():
        """Trigger create in git (Github gist)"""

    def ide_git_pull_request():
        """Trigger create pull request"""

    def ide_git_list_requests():
        """Show list of pull requests"""

    def ide_git_annotate():
        """Show git annotate/blame in IDE"""

    def ide_git_menu():
        """Show the git menu for IDE"""

    def ide_reveal_in_file_manager():
        """Reveal in OS file manager. window"""

    def ide_toggle_project():
        """Hide/Show project (file system) browser window"""

    def ide_toggle_find():
        """Hide/Show find view"""

    def ide_toggle_run():
        """Hide/Show run view"""

    def ide_toggle_debug():
        """Hide/Show debug view"""

    def ide_toggle_events():
        """Hide/Show events view"""

    def ide_toggle_terminal():
        """Hide/Show terminal window"""

    def ide_toggle_extensions():
        """Hide/Show extensions window"""

    def ide_terminal_new():
        """Create new terminal"""

    def ide_terminal_focus_previous():
        """Focus the previous terminal pane"""

    def ide_terminal_focus_next():
        """Focus the next terminal pane"""

    def ide_terminal_trash():
        """Trash the current terminal pane"""

    def ide_terminal_scroll_up():
        """Scroll the terminal up"""

    def ide_terminal_scroll_down():
        """Scroll the terminal down"""

    def ide_toggle_git():
        """Hide/Show git view"""

    def ide_toggle_structure():
        """Hide/Show file/class structure view"""

    def ide_toggle_database():
        """Hide/Show database view"""

    def ide_toggle_database_changes():
        """Hide/Show database changes view"""

    def ide_toggle_make():
        """Hide/Show Make view"""

    def ide_toggle_to_do():
        """Hide/Show to-do view"""

    def ide_toggle_docker():
        """Hide/Show Docker view"""

    def ide_toggle_favorites():
        """Hide/Show favourites"""

    def ide_toggle_last():
        """Hide/Show the last view you toggled"""

    def ide_toggle_pinned():
        """Hide/Show pinned view"""

    def ide_toggle_docked():
        """Dock/undock view"""

    def ide_toggle_floating():
        """Float/Sink view"""

    def ide_toggle_windowed():
        """Change windowed mode of view"""

    def ide_toggle_split():
        """Move where current view is grouped to"""

    def ide_toggle_tool_buttons():
        """Hide/Show tool buttons"""

    def ide_toggle_toolbar():
        """Hide/Show toolbar"""

    def ide_toggle_status_bar():
        """Hide/Show status bar"""

    def ide_toggle_navigation_bar():
        """Hide/Show navigation bar"""

    def ide_toggle_power_save():
        """Enable disable power save mode"""

    def ide_toggle_whitespace():
        """Hide/Show whitespaces"""

    def ide_toggle_indents():
        """Hide/Show indents"""

    def ide_toggle_line_numbers():
        """Hide/Show line numbers"""

    def ide_toggle_breadcrumbs():
        """Hide/Show breadcrumbs"""

    def ide_toggle_gutter_icons():
        """Hide/Show gutter icons (e.g. breakpoints)"""

    def ide_toggle_wrap():
        """Enable/disable word wrap"""

    def ide_toggle_parameters():
        """Enable/Disable inline hints"""

    def ide_toggle_fullscreen():
        """Enable/Disable full screen"""

    def ide_toggle_distraction_free():
        """Enable/Disable distraction free mode"""

    def ide_toggle_presentation_mode():
        """Enable/Disable presentation mode """

    def ide_go_first_tab():
        """Go to first tab"""

    def ide_go_second_tab():
        """Go to second tab"""

    def ide_go_third_tab():
        """Go to third tab"""

    def ide_go_fourth_tab():
        """Go to fourth tab"""

    def ide_go_fifth_tab():
        """Go to fifth tab"""

    def ide_go_sixth_tab():
        """Go to sixth tab"""

    def ide_go_seventh_tab():
        """Go to seventh tab"""

    def ide_go_eighth_tab():
        """Go to eighth tab"""

    def ide_go_ninth_tab():
        """Go to ninth tab"""

    def ide_go_final_tab():
        """Go to the final tab in the list"""

    def ide_clear_tab():
        """Close current open view"""

    def ide_change_scheme():
        """Trigger scheme menu (e.g. to change colour scheme)"""

    def ide_toggle_documentation():
        """Hide/Show documentation"""

    def ide_toggle_definition():
        """Hide/Show definition view"""

    def ide_pop_type():
        """Hide/Show type view"""

    def ide_pop_parameters():
        """Hide/Show parameters view"""

    def ide_go_breakpoints():
        """Show list of breakpoints"""

    def ide_toggle_breakpoint():
        """Add/Remove breakpoint"""

    def ide_toggle_method_breakpoint():
        """Add/Remove method breakpoint"""

    def ide_run_test():
        """Run the current test"""

    def ide_run_test_again():
        """Rerun the last-run test"""

    def ide_debug_test():
        """Run the current test in debug"""

    def ide_step_over():
        """Step over current statement"""

    def ide_step_into():
        """Step into current statement"""
    def ide_step_out():
        """Step out of current execution level"""

    def ide_step_smart():
        """Trigger smart step into"""

    def ide_step_to_line():
        """Trigger step to current line"""

    def ide_continue():
        """Continue running from current statement"""

    def ide_resize_window_right():
        """Resize window right"""

    def ide_resize_window_left():
        """Resize window left"""

    def ide_resize_window_up():
        """Resize window up"""

    def ide_resize_window_down():
        """Resize window down"""

    def ide_toggle_comment():
        """Toggle comment for selected text"""



