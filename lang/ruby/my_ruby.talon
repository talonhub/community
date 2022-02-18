mode: command
and mode: user.ruby
mode: command
and mode: user.auto_lang
and code.language: ruby
-
tag(): user.code_operators
tag(): user.code_comment
tag(): user.code_generic

# Personal changes, not for general use.
#
# substitute since recognition mismatches the way i pronounce 'boolean' as 'billion'
billion: "Boolean"

binding pry: "binding.pry"
pry (wear|where): "whereami"
pry next: "next"
pry continue: "continue"

assert equals: 'assert_equals '
