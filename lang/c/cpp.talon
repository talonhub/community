code.language: cpp
language: en
-

(stood|standard) {user.cpp_standard_types}:
    insert("std::{cpp_standard_types}")
(stood|standard) {user.cpp_standard_functions}:
    insert("std::{cpp_standard_functions}(")
(stood|standard) {user.cpp_standard_constants}:
    insert("std::{cpp_standard_constants}")

from {user.cpp_namespace}:
    insert("{cpp_namespace}::")

(auto|alto) <user.text>$:
    formatted = user.formatted_text(text, "SNAKE_CASE")
    insert("auto {formatted} = ")

state template: 
    user.insert_between("template<",">")

# really shines if you have added capital letters to your alphabet (e.g. NATO ones)
typename <user.letters>$:
    insert("typename {letters}")
typename <user.text>$:
    formatted = user.formatted_text(text, "PUBLIC_CAMEL_CASE")
    insert("typename {formatted}")