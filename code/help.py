from typing import Set
from talon import Module, Context, actions, imgui, Module, registry, ui
from talon.engine import engine
import math

mod = Module()
mod.list('help_contexts', desc='list of available contexts')

ctx = Context()
context_mapping = {}

current_context_page = 1
sorted_context_map_keys = None

selected_context = None
selected_context_page = 1

total_page_count = 1

cached_active_contexts_list = []

max_contexts_per_page = 25
max_commands_per_page = 15 

live_update = True
is_context_help_showing = False
cached_window_title = None
show_enabled_contexts_only = False

def update_title(): 
    global live_update
    global show_enabled_contexts_only
    global is_context_help_showing
    global cached_window_title

    if live_update:
        if is_context_help_showing:
            if selected_context == None:
                if ui.active_window().title != cached_window_title:
                    refresh_context_mapping(show_enabled_contexts_only) 
            else:
                update_active_contexts_cache(registry.active_contexts())

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
    global total_page_count

    # if no selected context, draw the contexts
    if selected_context is None:
        total_page_count = int(math.ceil(len(sorted_context_map_keys) / max_contexts_per_page))

        if not show_enabled_contexts_only:
            gui.text("Help: All Contexts ({}/{})".format(current_context_page,total_page_count))
        else:
            gui.text("Help: Active Contexts Only ({}/{})".format(current_context_page,total_page_count))

        gui.line()

        current_item_index = 1

        for key in sorted_context_map_keys:
            target_page = math.ceil(current_item_index / max_contexts_per_page)

            if current_context_page == target_page:
                button_name = str(current_item_index) + ": {}"

                if not show_enabled_contexts_only and key in cached_active_contexts_list:
                    button_name = str(current_item_index) + " [ACTIVE]: {} "

                if gui.button(button_name.format(key)):
                    selected_context = key
            
            current_item_index += 1

        if total_page_count > 1:
            gui.spacer()
            if gui.button('Next Page...'):
                actions.user.help_next()

            if gui.button("Previous Page..."):
                actions.user.help_previous()      
    
    #if there's a selected context, draw the commands for it
    else:
        total_page_count = math.ceil(len(context_mapping[selected_context]) / max_commands_per_page)
        if selected_context in cached_active_contexts_list:
            gui.text("{} ({}/{}) [ACTIVE]".format(selected_context, selected_context_page, total_page_count))
        else:
            gui.text("{} ({}/{}) [INACTIVE]".format(selected_context, selected_context_page, total_page_count))

        gui.line()
        
        current_item_index = 1
        
        for key, val in context_mapping[selected_context].items():
            target_page = int(math.ceil(current_item_index / max_commands_per_page))

            if selected_context_page == target_page:
                val = val.split("\n")
                if len(val) > 1:
                    gui.text("{}:".format(key))
                    for line in val:
                        gui.text("    {}".format(line))
                    gui.spacer()
                else:
                    gui.text("{}: {}".format(key, val[0]))
            
            current_item_index += 1

        gui.spacer()
        if total_page_count > 1:
            if gui.button('Next Page...'):
                actions.user.help_next()
                
            if gui.button("Previous Page..."):
                actions.user.help_previous()

        if gui.button('Main Help'):
            actions.user.help_return()

    if gui.button('refresh'):
        actions.user.help_refresh()

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

def update_active_contexts_cache(active_contexts):
    #print("update_active_contexts_cache")
    global cached_active_contexts_list
    cached_active_contexts_list = []
    for context in active_contexts:
        cached_active_contexts_list.append(str(context))

def refresh_context_mapping(enabled_only = False):
    global context_mapping
    global sorted_context_map_keys
    global show_enabled_contexts_only 
    global cached_window_title

    cached_short_context_names = {}
    show_enabled_contexts_only = enabled_only
    cached_window_title = ui.active_window().title
    active_contexts = registry.active_contexts()

    update_active_contexts_cache(active_contexts)
        
    context_mapping = {}
    for context in registry.contexts.values():
        short_name = str(context).replace('(Context', '').replace(')', '').split('.')[-1].replace('_', " ")
        #print(short_name)
        context_name = str(context)
        if enabled_only and context in active_contexts or not enabled_only:
            context_mapping[context_name] = {}
            for __, val in context.commands_get().items():
                #todo figure out why somethings are functions/list
                if not callable(val.target) and not isinstance(val.target, list):
                    context_mapping[context_name][str(val.rule.rule)] = val.target.code

            if len(context_mapping[context_name]) == 0:
                context_mapping.pop(context_name)
            else: 
                cached_short_context_names[short_name] = context_name

    ctx.lists['self.help_contexts'] = cached_short_context_names
    sorted_context_map_keys = sorted(context_mapping)
    
events_registered = False
def register_events(register: bool):
    global events_registered
    if register:
        if not events_registered and live_update:
            events_registered = True
            ui.register('', ui_event)
    else:
        ui.unregister('', ui_event)

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
        register_events(False)        

    def help_context_enabled():
        """Display contextual command info"""
        global is_context_help_showing
        is_context_help_showing = True

        reset()
        refresh_context_mapping(enabled_only=True)
        gui_alphabet.hide()
        gui_context_help.show()
        register_events(True)        

    def help_context():
        """Display contextual command info"""
        global is_context_help_showing
        is_context_help_showing = True
        reset()
        refresh_context_mapping()
        gui_alphabet.hide()
        gui_context_help.show()
        register_events(True)        

    def help_selected_context(m: str):
        """Display command info for selected context"""
        global is_context_help_showing
        global selected_context
        global selected_context_page

        if not is_context_help_showing:        
            reset()
            refresh_context_mapping()
        else:
            selected_context_page = 1
            update_active_contexts_cache(registry.active_contexts())

        is_context_help_showing = True
        selected_context = m
        gui_alphabet.hide()
        gui_context_help.show()
        register_events(True)        
    
    def help_next():
        """Navigates to next page"""
        global is_context_help_showing
        global current_context_page
        global selected_context
        global selected_context_page
        global total_page_count

        if is_context_help_showing:
            if selected_context is None:
                if current_context_page != total_page_count:
                    current_context_page += 1
                else:
                    current_context_page = 1
            else:
                if selected_context_page != total_page_count:
                    selected_context_page += 1
                else:
                    selected_context_page = 1

    def help_previous():
        """Navigates to previous page"""
        global is_context_help_showing
        global current_context_page
        global selected_context
        global selected_context_page
        global total_page_count

        if is_context_help_showing:
            if selected_context is None:
                if current_context_page != 1:
                    current_context_page -= 1
                else:
                    current_context_page = total_page_count
            else:
                if selected_context_page != 1:
                    selected_context_page -= 1
                else:
                    selected_context_page = total_page_count

    def help_return():
        """Returns to the main help window"""
        global selected_context
        global selected_context_page
        global is_context_help_showing
        global show_enabled_contexts_only

        if is_context_help_showing:
            refresh_context_mapping(show_enabled_contexts_only)
            selected_context_page = 1
            selected_context = None

    def help_refresh():
        """Refreshes the help"""
        global is_context_help_showing
        global show_enabled_contexts_only
        global selected_context

        if is_context_help_showing:
            if selected_context == None:
                refresh_context_mapping(show_enabled_contexts_only)
            else:
                update_active_contexts_cache(registry.active_contexts())

    def help_hide():
        """Hides the help"""
        global is_context_help_showing
        is_context_help_showing = False

        reset()
        gui_alphabet.hide()
        gui_context_help.hide()
        refresh_context_mapping()
        register_events(False)        
        
@mod.capture
def help_contexts(m) -> str:
    "Returns a context name"

@ctx.capture(rule='{self.help_contexts}')
def help_contexts(m):
    return m.help_contexts[-1]

def ui_event(event, arg):
    if event in ('app_activate', 'app_launch', 'app_close', 'win_open', 'win_close', 'win_title', 'win_focus'):
        #print("updating...")
        update_title()

refresh_context_mapping()
