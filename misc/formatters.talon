#provide both anchored and unachored commands via 'over'
<user.format_text>$: "{format_text}"
<user.format_text> over: "{format_text}"
phrase <user.text>$: "{user.text}"
phrase <user.text> over: "{user.text}"
(say | speak) <user.text>$: "{user.text}"
(say | speak) <user.text> over: "{user.text}"
word <user.text>: "{user.text}"
list formatters: user.list_formatters()
hide formatters: user.hide_formatters()
