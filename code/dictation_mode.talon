mode: dictation
-
<phrase>:
  dictate.natural(phrase)
  insert(" ")
<user.word>:
  insert("{word} ")
enter: key(enter)
period: key(backspace . space)
comma: key(backspace , space)
question [mark]: key(backspace ? space)
(bang | exclamation [mark]): key(backspace ! space)