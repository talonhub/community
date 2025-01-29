# ideally you integrate this into your engines.py file
#
# from talon import speech_system, Context
# from talon.engines.vosk import VoskEngine

# vosk_ca = VoskEngine(model='vosk-model-small-ca-0.4', language='ca-ES')
# speech_system.add_engine(vosk_ca)

# # especially this should not be here but in your engines.py file:
# ctx = Context()
# ctx.settings = {
#     'speech.engine': 'wav2letter', # your default engine goes here
# }
