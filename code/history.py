from talon import imgui, Module
from talon.engine import engine

hist_len = 10
history = []
def parse_phrase(phrase):
    return ' '.join(word.split('\\')[0] for word in phrase)
        
def on_phrase_post(j):
    global hist_len
    global history
    phrase = parse_phrase(j.get('phrase', []))
    cmd = j['cmd']
    if cmd == 'p.end' and phrase:
        history.append(phrase)
        history = history[-hist_len:]

#todo: dynamic rect?
@imgui.open(y=0)
def gui(gui: imgui.GUI):
    global history
    gui.text("Command History")
    gui.line()
    text = history[:]
    for line in text:
        gui.text(line)
     
engine.register('post:phrase', on_phrase_post)

mod = Module()
@mod.action_class
class Actions:           
    def history_enable():
        """Enables the history"""
        gui.show()
        
    def history_disable():
        """Disables the history"""
        gui.hide()

    def history_clear():
        """Clear the history"""
        global history
        history = []
