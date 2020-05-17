#provide both anchored and unachored commands via 'over'
<user.format_text>$: insert(format_text)
<user.format_text> over: insert(format_text)
phrase <user.text>$: insert(user.text)
phrase <user.text> over: insert(user.text)
(say | speak) <user.text>$: insert(user.text)
(say | speak) <user.text> over: insert(user.text)
word <user.text>: insert(user.text)
