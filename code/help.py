from typing import Set
from talon import Module, Context, actions, imgui, Module, registry, ui
import math

mod = Module()
mod.list('help_contexts', desc='list of available contexts')
mod.list('help_context_index', desc='available selection numbers for the active help page')
selection_numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty',]
selection_map = {n: i for i, n in enumerate(selection_numbers)}

ctx = Context()
#context name -> commands
context_command_map = {}

#context name -> actual context
context_map = {}

current_context_page = 1
sorted_context_map_keys = None

selected_context = None
selected_context_page = 1

total_page_count = 1

cached_active_contexts_list = []

max_contexts_per_page = len(selection_numbers)
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
                    refresh_context_command_map(show_enabled_contexts_only) 
            else:
                update_active_contexts_cache(registry.active_contexts())

#todo: dynamic rect?
@imgui.open(y=0,x=10)
def gui_alphabet(gui: imgui.GUI):
    global alphabet
    gui.text("Alphabet help")
    gui.line()

    for key,val in alphabet.items():
        gui.text("{}: {}".format(val, key))

    gui.spacer()
    if gui.button('close'):
        gui_alphabet.hide()

# translates 1-based index -> actual index in sorted_context_map_keys
def get_context_page(index):
    return math.ceil(index / max_contexts_per_page)

def get_total_context_pages():
    return math.ceil(len(sorted_context_map_keys) / max_contexts_per_page)

def get_current_context_page_length():
    start_index = (current_context_page -1) * max_contexts_per_page
    return len(sorted_context_map_keys[start_index:start_index + max_contexts_per_page])

# translates 1-based index -> actual index in sorted_context_map_keys
def get_command_page(index):
    return math.ceil(index / max_commands_per_page)

def get_selected_context_command_pages():
    return math.ceil(len(context_command_map[selected_context]) / max_commands_per_page)

@imgui.open(y=0,x=1400)
def gui_context_help(gui: imgui.GUI):
    global context_command_map
    global current_context_page
    global selected_context
    global selected_context_page
    global sorted_context_map_keys
    global show_enabled_contexts_only
    global cached_active_contexts_list
    global total_page_count

    # if no selected context, draw the contexts
    if selected_context is None:
        total_page_count = get_total_context_pages()

        if not show_enabled_contexts_only:
            gui.text("Help: All ({}/{})".format(current_context_page, total_page_count))
        else:
            gui.text("Help: Active Contexts Only ({}/{})".format(current_context_page,total_page_count))

        gui.line()
    
        current_item_index = 1
        current_selection_index = 1
        for key in sorted_context_map_keys:
            target_page = get_context_page(current_item_index)

            if current_context_page == target_page:
                button_name = str(current_selection_index) + ": {}"

                if not show_enabled_contexts_only and key in cached_active_contexts_list:
                    button_name = str(current_selection_index) + " [ACTIVE]: {} "

                if gui.button(button_name.format(key)):
                    selected_context = ctx.lists['self.help_contexts'][key]
                current_selection_index = current_selection_index + 1

            current_item_index += 1

        if total_page_count > 1:
            gui.spacer()
            if gui.button('Next...'):
                actions.user.help_next()

            if gui.button("Previous..."):
                actions.user.help_previous()      
    
    #if there's a selected context, draw the commands for it
    else:
        total_page_count = get_selected_context_command_pages()
        if context_map[selected_context] in cached_active_contexts_list:
            gui.text("{} ({}/{}) [ACTIVE]".format(selected_context, selected_context_page, total_page_count))
        else:
            gui.text("{} ({}/{}) [INACTIVE]".format(selected_context, selected_context_page, total_page_count))

        gui.line()
        
        current_item_index = 1
        for key, val in context_command_map[selected_context].items():
            #print(key + ": " + val)
            target_page = get_command_page(current_item_index)

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
            if gui.button('Next...'):
                actions.user.help_next()
                
            if gui.button("Previous..."):
                actions.user.help_previous()

        if gui.button('Return'):
            actions.user.help_return()

    if gui.button('Refresh'):
        actions.user.help_refresh()

    if gui.button('Close'):
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
    cached_active_contexts_list = active_contexts

#example usage todo: make a list definable in .talon
#overrides = {"generic browser" : "broswer"}
overrides = {}
def refresh_context_command_map(enabled_only = False):
    global context_command_map
    global context_map
    global sorted_context_map_keys
    global show_enabled_contexts_only 
    global cached_window_title
    global context_map

    context_map = {}
    cached_short_context_names = {}
    show_enabled_contexts_only = enabled_only
    cached_window_title = ui.active_window().title
    active_contexts = registry.active_contexts()

    update_active_contexts_cache(active_contexts)
        
    context_command_map = {}
    for context_name, context in registry.contexts.items():
        short_name = context_name.replace('(Context', '').replace('.talon', '').replace(')', '').split('.')[-1].replace('_', " ")
        #print("short name: " + short_name)
        if short_name in overrides:
            short_name = overrides[short_name]

        if enabled_only and context in active_contexts or not enabled_only:
            context_command_map[context_name] = {}
            for __, val in context.commands_get().items():
                #print(str(val.rule.rule) + ": " + val.target.code)
                context_command_map[context_name][str(val.rule.rule)] = val.target.code
            #print(short_name)  
            #print("length: " + str(len(context_command_map[context_name])))
            if len(context_command_map[context_name]) == 0:
                context_command_map.pop(context_name)
            else: 
                cached_short_context_names[short_name] = context_name
                context_map[context_name] = context

    ctx.lists['self.help_contexts'] = cached_short_context_names
    sorted_context_map_keys = sorted(cached_short_context_names)
    refresh_help_context_indexes()

def refresh_help_context_indexes():
    global is_context_help_showing
    if not is_context_help_showing or selected_context is not None:
        ctx.lists["self.help_context_index"] = []
    elif selected_context is None:
        length = get_current_context_page_length()
        #print("length = " + str(length))
        if length < len(selection_numbers):
           ctx.lists['self.help_context_index'] = selection_numbers[:length]
        else:
            ctx.lists['self.help_context_index'] = selection_numbers
    #print(str(ctx.lists['self.help_context_index']))
    
events_registered = False
def register_events(register: bool):
    global events_registered
    if register:
        if not events_registered and live_update:
            events_registered = True
            ui.register('', ui_event)
    else:
        events_registered = False
        ui.unregister('', ui_event)

@mod.action_class
class Actions:
    def help_alphabet(ab: dict):
        """Provides the alphabet dictionary"""
        # what you say is stored as a trigger
        global alphabet, is_context_help_showing
        is_context_help_showing = False
        alphabet = ab
        reset()
        gui_context_help.hide()        
        gui_alphabet.show()
        register_events(False)

        #refresh since context help is no longer showing...
        refresh_help_context_indexes()
                
    def help_context_enabled():
        """Display contextual command info"""
        global is_context_help_showing
        is_context_help_showing = True

        reset()
        refresh_context_command_map(enabled_only=True)
        gui_alphabet.hide()
        gui_context_help.show()
        register_events(True)       

    def help_context():
        """Display contextual command info"""
        global is_context_help_showing
        is_context_help_showing = True
        reset()
        refresh_context_command_map()
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
            refresh_context_command_map()
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

            refresh_help_context_indexes()

    def help_select_index(index: int):
        """Select the context by a number"""
        global sorted_context_map_keys, selected_context
        if is_context_help_showing:
            #print("help_select_index")
            if selected_context is None:
                selected_context = ctx.lists['self.help_contexts'][sorted_context_map_keys[(current_context_page - 1) * max_contexts_per_page + index]]
                refresh_help_context_indexes()
                
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
                    
            refresh_help_context_indexes()

    def help_return():
        """Returns to the main help window"""
        global selected_context
        global selected_context_page
        global is_context_help_showing
        global show_enabled_contexts_only
        
        if is_context_help_showing:
            refresh_context_command_map(show_enabled_contexts_only)
            selected_context_page = 1
            selected_context = None
            refresh_help_context_indexes()

    def help_refresh():
        """Refreshes the help"""
        global is_context_help_showing
        global show_enabled_contexts_only
        global selected_context

        if is_context_help_showing:
            if selected_context == None:
                refresh_context_command_map(show_enabled_contexts_only)
            else:
                update_active_contexts_cache(registry.active_contexts())

            refresh_help_context_indexes()

            
    def help_hide():
        """Hides the help"""
        global is_context_help_showing
        is_context_help_showing = False
        reset()
        gui_alphabet.hide()
        gui_context_help.hide()
        refresh_context_command_map()
        register_events(False)        

@mod.capture
def help_contexts(m) -> str:
    "Returns a context name"

@mod.capture
def help_context_index(m) -> int:
    "help context selection index"

@ctx.capture(rule='{self.help_contexts}')
def help_contexts(m):
    return m.help_contexts

@ctx.capture(rule='{self.help_context_index}')
def help_context_index(m):
    return selection_map[m.help_context_index]

def ui_event(event, arg):
    if event in ('app_activate', 'app_launch', 'app_close', 'win_open', 'win_close', 'win_title', 'win_focus'):
        #print("updating...")
        update_title()

ctx.lists['self.help_context_index'] = []
refresh_context_command_map()
