code.language: csharp
code.language: python
code.language: talon
-
state if: user.knausj_talon.code.lang.state_if()
state ellie: user.knausj_talon.code.lang.state_elif()
state else: user.knausj_talon.code.lang.state_else()
state while: user.knausj_talon.code.lang.state_while()
state switch: user.knausj_talon.code.lang.state_switch()
state case: user.knausj_talon.code.lang.state_case()
state for: user.knausj_talon.code.lang.state_for()
commenter (this | line): user.knausj_talon.code.lang.comment_begin_line()
commenter here: user.knausj_talon.code.lang.comment_here()
new comment <phrase>:
    user.knausj_talon.code.lang.comment_here()
    dictate.lower(phrase)
