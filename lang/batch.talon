mode: user.batch
mode: user.auto_lang
and code.language: batch
-
#tag(): user.code_operators
tag(): user.code_comment
#tag(): user.code_generic


action(user.code_comment): "REM "

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
