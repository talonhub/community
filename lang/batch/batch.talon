mode: command
and mode: user.batch
mode: command
and mode: user.auto_lang
and code.language: batch
-
#tag(): user.code_operators
tag(): user.code_comment

# exit without killing cmd shell
soft exit: "exit /B 1\n"
# exit with killing cmd shell
hard exit: "exit 1\n"
echo: "echo "
echo off: "@echo off\n"
call: "call "
call shell: "call cmd \\c "
if error: "if errorlevel 1 "
go to: "goto "
delayed expansion: "SETLOCAL EnableDelayedExpansion\n"
arg <number_small>: "%{number_small}"
