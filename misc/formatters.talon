#provide both anchored and unachored commands via 'over'
<user.format_text>$: "{format_text}"
<user.format_text> over: "{format_text}"
phrase <user.text>$: "{text}"
phrase <user.text> over: "{text}"
(say | speak) <user.text>$: "{text}"
(say | speak) <user.text> over: "{text}"
word <user.text>: "{text}"
list formatters: user.list_formatters()
hide formatters: user.hide_formatters()
