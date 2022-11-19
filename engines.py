from talon import Context, speech_system
from talon.engines.webspeech import WebSpeechEngine

webspeech = WebSpeechEngine()
speech_system.add_engine(webspeech)


# from talon import speech_system, Context
# from talon.engines.w2l import W2lEngine
# from talon.engines.webspeech import WebSpeechEngine

# w2l = W2lEngine(model='en_US-conformer', debug=True)
# # w2l = W2lEngine(language='en_US', debug=False)
# speech_system.add_engine(w2l)
# speech_system.add_engine(WebSpeechEngine(language='pl_PL'))
# # speech_system.add_engine(WebSpeechEngine(language='en_US'))
# # set the default engine
# ctx = Context()
# ctx.settings = {
#     'speech.engine': 'wav2letter',
# }

# # from talon import speech_system
# # from talon.engines.w2l import W2lEngine
# # w2l = W2lEngine(model='en_US-conformer', debug=True)
# # speech_system.add_engine(w2l)
