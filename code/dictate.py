from talon import Context, actions, ui, Module
import re
import os 
ctx = Context()
key = actions.key

#TODO: temporary until the built-in actions are fixed.
@ctx.action_class('dictate')
class DictateActions:
    def lower(m):
        '''Insert lowercase text'''
        words = actions.dictate.parse_words(m)
        words = actions.dictate.replace_words(words)
        text = actions.dictate.join_words(words)
        actions.insert(text.lower())
    
    def natural(m):
        '''Insert naturally-capitalized text'''
        words = actions.dictate.parse_words(m)
        words = actions.dictate.replace_words(words)
        text = actions.dictate.join_words(words)
        actions.insert(text)
    
    def parse_words(m):
        '''Extract words from a spoken Capture'''
        words = m._words
        out = []
        for word in words:
            word = word.lstrip("\\").split("\\", 1)[0]
            out += word.split(' ')
        return out
    