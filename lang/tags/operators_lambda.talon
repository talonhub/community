tag: user.code_operators_lambda
-

# In many languages, anonymous functions aren't merely infix syntax:
#
#       Haskell  '\x -> bla'
#       OCaml    'fun x -> bla'
#       Rust     '|x| { bla }'
#
# Therefore a revision of this command may be in order.

# syntax for anonymous functions
op lambda: user.code_operator_lambda()
