tag: find_and_replace
-
search this: user.find("")
search this <user.text>: user.find(text)
search all: user.find_everywhere("")
search all <user.text>: user.find_everywhere(text)
search case : user.find_toggle_match_by_case()
search word : user.find_toggle_match_by_word()
search expression : user.find_toggle_match_by_regex()
search next: user.find_next()
search previous: user.find_previous()
replace this: user.replace("")
replace this <user.text>: user.replace(text)
replace all: user.replace_everywhere("")
replace <user.text> all: user.replace_everywhere(text)
replace confirm that: user.replace_confirm()
replace confirm all: user.replace_confirm_all()


