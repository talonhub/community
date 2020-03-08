from typing import Set
from talon import Module, Context, actions, imgui, Module, registry, ui
import math

mod = Module()
mod.list('help_actions', desc='list of available actions')

ctx = Context()
context_mapping = {}

current_context_page = 1
sorted_context_map_keys = None

selected_context = None
selected_context_page = 1

cached_active_contexts_list = []

max_items_per_page = 25
live_update = True
is_context_help_showing = False
cached_window_title = None
show_enabled_contexts_only = False

def on_title(win): 
    global live_update
    global show_enabled_contexts_only
    global is_context_help_showing

    if is_context_help_showing and live_update and win.title != cached_window_title and selected_context == None:
        refresh_context_mapping(show_enabled_contexts_only)

#todo: dynamic rect?
@imgui.open(y=0)
def gui_alphabet(gui: imgui.GUI):
    global alphabet
    gui.text("Alphabet help")
    gui.line()

    for key,val in alphabet.items():
        gui.text("{}: {}".format(val, key))

    gui.spacer()
    if gui.button('close'):
        gui_alphabet.hide()

@imgui.open(y=0)
def gui_context_help(gui: imgui.GUI):
    global context_mapping
    global current_context_page
    global selected_context
    global selected_context_page
    global sorted_context_map_keys
    global show_enabled_contexts_only
    global cached_active_contexts_list

    # if no selected context, draw the contexts
    if selected_context is None:
        total_page_count = int(math.ceil(len(sorted_context_map_keys) / max_items_per_page))

        if not show_enabled_contexts_only:
            gui.text("Context help ({}/{})".format(current_context_page,total_page_count))
        else:
            gui.text("Active Context help ({}/{})".format(current_context_page,total_page_count))
        gui.line()

        current_item_index = 1

        for key in sorted_context_map_keys:
            target_page = int(math.ceil(current_item_index / max_items_per_page))

            if current_context_page == target_page:
                button_name = "{}"

                if not show_enabled_contexts_only and key in cached_active_contexts_list:
                    button_name = ("*{}")

                if gui.button(button_name.format(key)):
                    selected_context = key
            
            current_item_index += 1

        if total_page_count > 1:
            gui.spacer()
            if gui.button('Next Page...'):
                if current_context_page != total_page_count:
                    current_context_page += 1
                else:
                    current_context_page = 1
            
            if gui.button("Previous Page..."):
                if current_context_page != 1:
                    current_context_page-=1
                else:
                    current_context_page = total_page_count
    
    #if there's a selected context, draw the commands for it
    else:
        total_page_count = int(math.ceil(len(context_mapping[selected_context]) / max_items_per_page))
        gui.text("{} ({}/{})".format(selected_context, selected_context_page, total_page_count))
        gui.line()

        current_item_index = 1
        
        for key, val in context_mapping[selected_context].items():
            target_page = int(math.ceil(current_item_index / max_items_per_page))

            if selected_context_page == target_page:
                gui.text("{}: {}".format(key, val))
            
            current_item_index += 1

        gui.spacer()
        if total_page_count > 1:
            if gui.button('More...'):
                if selected_context_page != total_page_count:
                    selected_context_page += 1
                else:
                    selected_context_page = 1
                
                if gui.button("Previous Page..."):
                    if selected_context_page != 1:
                        selected_context_page -= 1
                    else:
                        selected_context_page = total_page_count

        if gui.button('Main Help'):
            refresh_context_mapping(show_enabled_contexts_only)
            selected_context = None

    if gui.button('refresh'):
        refresh_context_mapping()

    if gui.button('close'):
        actions.user.help_hide()

def reset():
    global current_context_page
    global sorted_context_map_keys
    global selected_context
    global selected_context_page
    global cached_window_title
    global show_enabled_contexts_only 

    current_context_page = 1
    sorted_context_map_keys = None
    selected_context = None
    selected_context_page = 1
    cached_window_title = None
    show_enabled_contexts_only = False
    
def refresh_context_mapping(enabled_only = False):
    global context_mapping
    global sorted_context_map_keys
    global show_enabled_contexts_only 
    global cached_window_title
    global cached_active_contexts_list

    show_enabled_contexts_only = enabled_only
    cached_window_title = ui.active_window().title
    active_contexts = registry.active_contexts()

    cached_active_contexts_list = []
    for context in active_contexts:
        cached_active_contexts_list.append(str(context))
        
    context_mapping = {}
    for context in registry.contexts.values():
        context_name = str(context)
        if enabled_only and context in active_contexts or not enabled_only:
            context_mapping[context_name] = {}
            for __, val in context.commands_get().items():
                #todo figure out why somethings are functions/list
                if not callable(val.target) and not isinstance(val.target, list):
                    context_mapping[context_name][str(val.rule.rule)] = val.target.code

            if len(context_mapping[context_name]) == 0:
                context_mapping.pop(context_name)

    sorted_context_map_keys = sorted(context_mapping)
    
@mod.action_class
class Actions:
    def help_alphabet(ab: dict):
        """Provides the alphabet dictionary"""
        # what you say is stored as a trigger
        global alphabet
        alphabet = ab
        reset()
        gui_context_help.hide()        
        gui_alphabet.show()

    def help_context_enabled():
        """Display contextual command info"""
        global is_context_help_showing
        is_context_help_showing = True

        reset()
        refresh_context_mapping(enabled_only=True)
        gui_alphabet.hide()
        gui_context_help.show()        

    def help_context():
        """Display contextual command info"""
        global is_context_help_showing
        is_context_help_showing = True
        reset()
        refresh_context_mapping()
        gui_alphabet.hide()
        gui_context_help.show()

    def help_hide():
        """Hides the help"""
        global is_context_help_showing
        is_context_help_showing = False
        reset()
        gui_alphabet.hide()
        gui_context_help.hide()

@ctx.capture(rule='{self.help_actions}')
def homophones_canonical(m):
    return m.help_actions[-1]

if live_update:
    ui.register('win_title', on_title)
    ui.register("win_focus", on_title)
