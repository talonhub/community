tag: user.find_and_replace
-
#selectation and navigration
select next <user.text> [over]: user.select_next_occurrence(text)
select last <user.text> [over]: user.select_previous_occurrence(text)
select next clippy: user.select_next_occurrence(clip.text())
select last clippy: user.select_previous_occurrence(clip.text())
go next <user.text> [over]: user.move_next_occurrence(text)
go last <user.text> [over]: user.move_previous_occurrence(text)
go next clippy: user.move_next_occurrence(clip.text())
go last clippy: user.move_previous_occurrence(clip.text())

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


