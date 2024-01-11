mode: command
# and mode: user.ruby
# mode: command
# and mode: user.auto_lang
and code.language: ruby
-
# tag(): user.code_operators
# tag(): user.code_comment
# tag(): user.code_generic
tag(): user.ruby

# same as python.talon:
state (def | deaf | deft): "def "
define <phrase>$:
  #user.code_default_function(user.formatted_text(phrase,"snake"))
  "def "
  user.insert_formatted(phrase, "snake")
  insert("()")
  key(left)

# this is not working
# tag(): user.code_my_models

# Personal changes, not for general use.
#
# substitute since recognition mismatches the way i pronounce 'boolean' as 'billion'
billion: "Boolean"

binding pry: "binding.pry"
binding pry remote: "binding.pry_remote"
pry binding: "binding.pry"
binding break: "binding.break"
pry (wear|where): "whereami"
pry next: "next"
pry continue: "continue"

assert equals: 'assert_equals '

# this isn't working :(
# code_my_modles is defined in lang/ruby/ruby.py
# <code_my_models> find last:
#   "{code_my_models}.last"

present [a]: "present?"

put:
  "puts \"\""
  key(left)

to jason: ".to_json"

shazam:
  "#{}"
  key(left)

prompt <phrase>:
  "# "
  insert(phrase)
  insert("\n")
  key('alt-ctrl-i')



