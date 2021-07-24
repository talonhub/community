mode: user.text_field
-
go [<phrase>]$:
    key(enter)
    user.command_mode(phrase or "")
over [<phrase>]$:
    user.command_mode(phrase or "")

# Currently this auto insert feature does not work.  see and off`dictation.py`  for more information.
# Everything here should call auto_insert to preserve the state to correctly auto-capitalize/auto-space.
<user.prose>: auto_insert(prose)
# <user.prose>: actions.user.dictation_insert(prose)

