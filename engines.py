from talon import blobfs, speech_system
from talon_init import TALON_HOME
from talon.engines.w2l import W2lEngine, W2lModelInfo

model_path = TALON_HOME / 'w2l' / 'conformer-d-hybrid'
with open(model_path / 'ort.patch', 'rb') as f:
    ort_patch = f.read()

info = W2lModelInfo(
    id           = 'd-hybrid',
    name         = 'd-hybrid',
    language     = 'en_US',
    am_path      = str(model_path / 'acoustic.b2l'),
    lexicon_path = str(model_path / 'lexicon.txt'),
    trie_path    = str(model_path / 'lexicon_flat.bin'),
    whisper_path = str(blobfs.find('c6138d6d58ecc8322097e0f987c32f1be8bb0a18532a3f88f734d1bbf9c41e5d')), # small
    ort_patch    = ort_patch,
)

w2l = W2lEngine(info=info, debug=False)
speech_system.add_engine(w2l)
