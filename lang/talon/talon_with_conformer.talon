# enables the user.talon_populate_lists tag with conformer
# for TalonScript and Talon Python
# dragon cannot handle the resulting grammar complexity
code.language: talon
and speech.engine: wav2letter
code.language: python
and tag: user.talon_python
and speech.engine: wav2letter
-

tag(): user.talon_populate_lists
