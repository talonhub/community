from talon import imgui, Module, speech_system, actions

hist_len = 10
is_showing = False
history = []
def parse_phrase(word_list):
    return ' '.join(word.split('\\')[0] for word in word_list)
        
def on_phrase(j):
    global hist_len
    global history
    #print(str(actions.dictate.parse_words(j)))
    val = parse_phrase(j['phrase'])
    if val != "":
        history.append(val)
        history = history[-hist_len:]

    if is_showing:
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
        global is_showing
        gui.show()
        gui.freeze()
        is_showing = True

    def history_disable():
        """Disables the history"""
        global is_showing
        gui.hide()
        is_showing = False

    def history_clear():
        """Clear the history"""
        global history
        history = []
