^language force see sharp$: user.code_set_language_mode("csharp")
^language force see plus plus$: user.code_set_language_mode("cplusplus")
^language force go$: user.code_set_language_mode("go")
^language force java$: user.code_set_language_mode("java")
^language force java script$: user.code_set_language_mode("javascript")
^language force type script$: user.code_set_language_mode("typescript")
^language force markdown$: user.code_set_language_mode("markdown")
^language force python$: user.code_set_language_mode("python")
^language force are language$: user.code_set_language_mode("r")
^language force talon [language]$: user.code_set_language_mode("talon")
^language force sql|(s q l)$: user.code_set_language_mode("sql")
^clear language modes$: user.code_clear_language_mode()
[enable] debug mode:
    mode.enable("user.gdb")
disable debug mode:
    mode.disable("user.gdb")
    