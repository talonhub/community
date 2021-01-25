from talon import speech_system
from talon.engines.w2l import W2lEngine

w2l = W2lEngine(model="en_US-sconv", debug=False)
speech_system.add_engine(w2l)
