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
tag(): user.code_my_models

# Personal changes, not for general use.
#
# substitute since recognition mismatches the way i pronounce 'boolean' as 'billion'
billion: "Boolean"

binding pry: "binding.pry"
pry binding: "binding.pry"

assert equals: 'assert_equals '

# this isn't working :(
# code_my_modles is defined in lang/ruby/ruby.py
<code_my_models> find last:
  "{code_my_models}.last"