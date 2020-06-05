from talon import imgui, Module, speech_system, actions

hist_len = 10
history = []
def parse_phrase(word_list):
    return ' '.join(word.split('\\')[0] for word in word_list)
        
def on_phrase(j):
    global hist_len
    global history

    try:
        val = parse_phrase(getattr(j['parsed'], '_unmapped', j['phrase']))
    except:
        val = parse_phrase(j['phrase'])
    
    if val != "":
        history.append(val)
        history = history[-hist_len:]

        if gui.showing:
            gui.freeze()
   
#todo: dynamic rect?
@imgui.open(y=0)
def gui(gui: imgui.GUI):
    global history
    gui.text("Command History")
    gui.line()
    text = history[:]
    for line in text:
        gui.text(line)

speech_system.register('phrase', on_phrase)

mod = Module()
@mod.action_class
class Actions:           
    def history_enable():
        """Enables the history"""
        gui.freeze()

    def history_disable():
        """Disables the history"""
        gui.hide()

    def history_clear():
        """Clear the history"""
        global history
        history = []
