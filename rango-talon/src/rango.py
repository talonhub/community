from typing import Union

from talon import Context, Module, actions, app, ctrl

from .command import run_simple_command, run_targeted_command
from .get_click_coordinates import get_click_coordinates

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
    # Click
    def rango_click_element(target: dict):
        """Clicks an element"""
        run_targeted_command("clickElement", target)

    def rango_mouse_click_element(target: dict, button: int):
        """Clicks an element using mouse"""
        x, y = get_click_coordinates(target)

        actions.mouse_move(x, y)
        actions.sleep("50ms")
        ctrl.mouse_click(button=button)

    def rango_mouse_move_to_element(target: dict):
        """Moves the cursor to an element"""
        x, y = get_click_coordinates(target)
        actions.mouse_move(x, y)

    def rango_direct_click_element(target: dict):
        """Clicks an element using direct clicking"""
        try:
            run_targeted_command("directClickElement", target)
        except TimeoutError as e:
            app.notify(
                "Rango direct clicking failed. Make sure the Rango browser extension is installed and enabled."
            )
            raise e

    def rango_focus_and_activate_element(target: dict):
        """Focuses and clicks an element"""
        run_targeted_command("focusAndActivateElement", target)

    # Focus
    def rango_focus_element(target: dict):
        """Focuses an element"""
        run_targeted_command("focusElement", target)

    def rango_focus_first_input():
        """Focuses the first input element on the page"""
        run_simple_command("focusFirstInput")

    # Focus tab
    def rango_activate_tab(tab_target: dict):
        """Switches to a tab using its hint"""
        run_targeted_command("activateTab", tab_target)

    def rango_refresh_tab_markers():
        """Refreshes the tab hints"""
        run_simple_command("refreshTabMarkers")

    # Focus tab with audio
    def rango_focus_next_tab_with_sound():
        """Focuses the next tab that is producing sound"""
        run_simple_command("focusNextTabWithSound")

    def rango_focus_next_audible_tab():
        """Focuses the next audible tab"""
        run_simple_command("focusNextAudibleTab")

    def rango_focus_next_muted_tab():
        """Focuses the next muted tab"""
        run_simple_command("focusNextMutedTab")

    def rango_focus_tab_last_sounded():
        """Focuses the tab that last started to play sound"""
        run_simple_command("focusTabLastSounded")

    # Mute tabs
    def rango_mute_current_tab():
        """Mutes the current tab"""
        run_simple_command("muteCurrentTab")

    def rango_unmute_current_tab():
        """Unmutes the current tab"""
        run_simple_command("unmuteCurrentTab")

    def rango_mute_next_tab_with_sound():
        """Mutes the next tab that has sound"""
        run_simple_command("muteNextTabWithSound")

    def rango_unmute_next_muted_tab():
        """Unmutes the next muted tab"""
        run_simple_command("unmuteNextMutedTab")

    def rango_mute_tab(tab_target: dict):
        """Mutes a tab using its hint"""
        run_targeted_command("muteTab", tab_target)

    def rango_unmute_tab(tab_target: dict):
        """Unmutes a tab using its hint"""
        run_targeted_command("unmuteTab", tab_target)

    def rango_mute_all_tabs_with_sound():
        """Mutes all tabs that have sound"""
        run_simple_command("muteAllTabsWithSound")

    def rango_unmute_all_muted_tabs():
        """Unmutes all muted tabs"""
        run_simple_command("unmuteAllMutedTabs")

    # Close tab
    def rango_close_tab(tab_target: dict):
        """Closes a tab using its hint"""
        run_targeted_command("closeTab", tab_target)

    # Open in new tab
    def rango_open_in_new_tab(target: dict):
        """Opens a link in a new tab"""
        run_targeted_command("openInNewTab", target)

    def rango_open_in_background_tab(target: dict):
        """Opens a link in a background tab"""
        run_targeted_command("openInBackgroundTab", target)

    # Navigation
    def rango_navigate_to_page_root():
        """Navigates to the root of the current page"""
        run_simple_command("navigateToPageRoot")

    def rango_navigate_to_next_page():
        """Navigates to the next page"""
        run_simple_command("navigateToNextPage")

    def rango_navigate_to_previous_page():
        """Navigates to the previous page"""
        run_simple_command("navigateToPreviousPage")

    # Move tab to new window
    def rango_move_tab_to_new_window():
        """Moves the current tab to a new window"""
        run_simple_command("moveCurrentTabToNewWindow")

    # Focus previous tab
    def rango_focus_previous_tab():
        """Focuses the previously active tab"""
        run_simple_command("focusPreviousTab")

    # Focus or create tab
    def rango_focus_or_create_tab_by_url(url: str):
        """Focuses an existing tab with the given URL or creates a new one"""
        run_simple_command("focusOrCreateTabByUrl", url=url)

    # Focus tab by text
    def rango_focus_tab_by_text(text: str):
        """Focuses a tab matching the given text"""
        run_simple_command("focusTabByText", text=text)

    def rango_cycle_tabs_by_text(step: int):
        """Cycles through tabs matching the current search text"""
        run_simple_command("cycleTabsByText", step=step)

    # Close tabs
    def rango_close_other_tabs():
        """Closes all other tabs in the window"""
        run_simple_command("closeOtherTabsInWindow")

    def rango_close_tabs_to_left():
        """Closes all tabs to the left in the window"""
        run_simple_command("closeTabsToTheLeftInWindow")

    def rango_close_tabs_to_right():
        """Closes all tabs to the right in the window"""
        run_simple_command("closeTabsToTheRightInWindow")

    def rango_close_tabs_left_end(amount: int = 1):
        """Closes a number of tabs from the left end"""
        run_simple_command("closeTabsLeftEndInWindow", amount=amount)

    def rango_close_tabs_right_end(amount: int = 1):
        """Closes a number of tabs from the right end"""
        run_simple_command("closeTabsRightEndInWindow", amount=amount)

    def rango_close_previous_tabs(amount: int = 1):
        """Closes a number of tabs to the left of current tab"""
        run_simple_command("closePreviousTabsInWindow", amount=amount)

    def rango_close_next_tabs(amount: int = 1):
        """Closes a number of tabs to the right of current tab"""
        run_simple_command("closeNextTabsInWindow", amount=amount)

    # Clone tab
    def rango_clone_current_tab():
        """Clones the current tab"""
        run_simple_command("cloneCurrentTab")

    # Hover
    def rango_hover_element(target: dict):
        """Hovers over an element"""
        run_targeted_command("hoverElement", target)

    def rango_unhover_all():
        """Removes all hover effects"""
        run_simple_command("unhoverAll")

    # Show link
    def rango_show_link(target: dict):
        """Shows the address of a link"""
        run_targeted_command("showLink", target)

    # Hide hint
    def rango_hide_hint(target: dict):
        """Hides a specific hint"""
        run_targeted_command("hideHint", target)

    # Scroll
    def rango_scroll(region: str, direction: str, factor: float = 0.66):
        """Scrolls the specified region of the page"""
        run_simple_command("scroll", region=region, direction=direction, factor=factor)

    def rango_scroll_at_element(target: dict, direction: str, factor: float = 0.66):
        """Scrolls at an element in the given direction"""
        run_targeted_command(
            "scrollAtElement", target, direction=direction, factor=factor
        )

    def rango_snap_scroll(target: dict, position: str):
        """Scrolls an element to the specified position (top/bottom/center)"""
        run_targeted_command("snapScroll", target, position=position)

    def rango_snap_scroll_text(text: str, position: str):
        """Scrolls to the specified text (top/bottom/center)"""
        mark = {
            "type": "textSearch",
            "value": text,
            "viewportOnly": True,
        }
        run_targeted_command(
            "snapScroll", {"type": "primitive", "mark": mark}, position=position
        )

    # Scroll positions
    def rango_store_scroll_position(positionName: str):
        """Stores the current scroll position with the given name"""
        run_simple_command("storeScrollPosition", positionName=positionName)

    def rango_scroll_to_position(positionName: str):
        """Scrolls to a previously stored position"""
        run_simple_command("scrollToPosition", positionName=positionName)

    # Copy
    def rango_copy_link(target: dict):
        """Copies a link address"""
        run_targeted_command("copyLink", target)

    def rango_copy_markdown_link(target: dict):
        """Copies a link in markdown format"""
        run_targeted_command("copyMarkdownLink", target)

    def rango_copy_element_text(target: dict):
        """Copies the text content of an element"""
        run_targeted_command("copyElementTextContent", target)

    # Paste and Insert
    def rango_insert_text_to_input(text: str, target: dict, pressEnter: bool = False):
        """Inserts a given text to an input marked with the target hint"""
        if actions.user.rango_try_to_focus_and_check_is_editable(target):
            actions.edit.select_all()
            actions.edit.delete()
            actions.user.paste(text)
            if pressEnter:
                actions.sleep("400ms")
                actions.key("enter")

    # Cursor position
    def rango_set_selection_before(target: dict):
        """Sets the cursor position before an element"""
        run_targeted_command("setSelectionBefore", target)

    def rango_set_selection_after(target: dict):
        """Sets the cursor position after an element"""
        run_targeted_command("setSelectionAfter", target)

    # Clear field
    def rango_clear_input(target: dict):
        """Removes the contents of an input"""
        if actions.user.rango_try_to_focus_and_check_is_editable(target):
            actions.edit.select_all()
            actions.edit.delete()

    # Copy page info
    def rango_copy_location_property(property: str):
        """Copies a property of the current page location"""
        run_simple_command("copyLocationProperty", property=property)

    def rango_copy_current_tab_markdown_url():
        """Copies the current tab's URL in markdown format"""
        run_simple_command("copyCurrentTabMarkdownUrl")

    # Hint appearance
    def rango_increase_hint_size():
        """Increases the size of hints"""
        run_simple_command("increaseHintSize")

    def rango_decrease_hint_size():
        """Decreases the size of hints"""
        run_simple_command("decreaseHintSize")

    # Extra hints
    def rango_display_extra_hints():
        """Displays extra hints"""
        run_simple_command("displayExtraHints")

    def rango_display_excluded_hints():
        """Displays excluded hints"""
        run_simple_command("displayExcludedHints")

    def rango_display_less_hints():
        """Displays fewer hints"""
        run_simple_command("displayLessHints")

    def rango_include_extra_selectors(target: dict):
        """Includes extra selectors for hints"""
        run_targeted_command("includeExtraSelectors", target)

    def rango_exclude_extra_selectors(target: dict):
        """Excludes extra selectors for hints"""
        run_targeted_command("excludeExtraSelectors", target)

    def rango_exclude_all_hints():
        """Excludes all hints"""
        run_simple_command("excludeAllHints")

    def rango_include_or_exclude_more_selectors():
        """Includes or excludes more selectors"""
        run_simple_command("includeOrExcludeMoreSelectors")

    def rango_include_or_exclude_less_selectors():
        """Includes or excludes fewer selectors"""
        run_simple_command("includeOrExcludeLessSelectors")

    def rango_confirm_selectors_customization():
        """Confirms the customization of selectors"""
        run_simple_command("confirmSelectorsCustomization")

    def rango_reset_custom_selectors():
        """Resets custom selectors"""
        run_simple_command("resetCustomSelectors")

    # Show and hide hints
    def rango_refresh_hints():
        """Refreshes all hints"""
        run_simple_command("refreshHints")

    def rango_toggle_hints():
        """It toggles the Rango hints globally on or off"""
        run_simple_command("toggleHints")

    def rango_enable_hints(level: str = "global"):
        """Enables hints at specified level"""
        run_simple_command("enableHints", level=level)

    def rango_disable_hints(level: str = "global"):
        """Disables hints at specified level"""
        run_simple_command("disableHints", level=level)

    def rango_reset_toggle_level(level: str):
        """Resets hint toggle at specified level"""
        run_simple_command("resetToggleLevel", level=level)

    def rango_display_toggles_status():
        """Displays the status of all toggles"""
        run_simple_command("displayTogglesStatus")

    # Toggle tab markers
    def rango_toggle_tab_markers():
        """Toggles tab hints"""
        run_simple_command("toggleTabMarkers")

    # Toggle keyboard clicking
    def rango_toggle_keyboard_clicking():
        """Toggles keyboard clicking"""
        run_simple_command("toggleKeyboardClicking")

    # Settings page
    def rango_open_settings_page():
        """Opens the settings page"""
        run_simple_command("openSettingsPage")

    def rango_open_whats_new_page():
        """Opens the what's new page"""
        run_simple_command("openWhatsNewPage")

    # Pages
    def rango_open_page_in_new_tab(url: str):
        """Opens a specific page in a new tab"""
        run_simple_command("openPageInNewTab", url=url)

    # References
    def rango_save_reference(target: dict, referenceName: str):
        """Saves a reference to an element"""
        run_targeted_command("saveReference", target, referenceName=referenceName)

    def rango_save_reference_for_active_element(referenceName: str):
        """Saves a reference for the currently active element"""
        run_simple_command("saveReferenceForActiveElement", referenceName=referenceName)

    def rango_show_references():
        """Shows all saved references"""
        run_simple_command("showReferences")

    def rango_remove_reference(referenceName: str):
        """Removes a saved reference"""
        run_simple_command("removeReference", referenceName=referenceName)

    # Helper functions
    def rango_try_to_focus_and_check_is_editable(target: dict):
        """Tries to focus an element marked with a hint (clicking if it's not a link) and returns true if the active element is editable"""
        return run_targeted_command("tryToFocusElementAndCheckIsEditable", target)

    def rango_get_bare_title() -> str:
        """Returns the title of the currently focused tab without including the decorations"""
        return run_simple_command("getBareTitle")

    def rango_run_action_on_reference(actionName: str, referenceName: str):
        """Runs a Rango command on a mark"""
        target = {
            "type": "primitive",
            "mark": {"type": "elementReference", "value": referenceName},
        }
        run_targeted_command(actionName, target)

    def rango_run_action_on_text_matched_element(
        actionName: str, text: str, viewport_only: Union[bool, None] = False
    ):
        """Runs a Rango command on a hintable element found using fuzzy search"""
        target = {
            "type": "primitive",
            "mark": {
                "type": "textSearch",
                "value": text,
                "viewportOnly": viewport_only,
            },
        }
        run_targeted_command(actionName, target)

    def rango_force_explicit_clicking():
        """Forces Rango explicit clicking"""
        ctx.tags = ["user.rango_explicit_clicking_forced"]

    def rango_force_direct_clicking():
        """Forces Rango direct clicking"""
        ctx.tags = ["user.rango_direct_clicking_forced"]
