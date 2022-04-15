tag: user.code_object_oriented
-

# quick way to say dot accessor for thing.accessor
dot [<user.text>]:
      insert(".")
      insert(user.formatted_text(text, "PRIVATE_CAMEL_CASE"))

      
