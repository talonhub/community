tag: user.find_and_replace
-
hunt this: user.find("")
hunt this <user.text>: user.find(text)
hunt all: user.find_everywhere("")
hunt all <user.text>: user.find_everywhere(text)
hunt case : user.find_toggle_match_by_case()
hunt word : user.find_toggle_match_by_word()
hunt expression : user.find_toggle_match_by_regex()
hunt next: user.find_next()
hunt previous: user.find_previous()
replace this [<user.text>]: user.replace(text or "")
replace all: user.replace_everywhere("")
replace <user.text> all: user.replace_everywhere(text)
replace confirm that: user.replace_confirm()
replace confirm all: user.replace_confirm_all()




