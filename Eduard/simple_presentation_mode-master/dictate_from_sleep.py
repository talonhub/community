from talon import Module, actions

mod = Module()

@mod.action_class
class user_actions:
        def try_to_mimic(phrase: str):
            '''runs arbitrary phrase through mimic to see if it works'''
            try: 
                actions.mimic(phrase)
            except:
                print('mimic {phrase} unsuccessful')