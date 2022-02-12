app: vscode
mode: command
mode: user.javascript
mode: user.auto_lang
and code.language: javascript
-

return false: "return false"
return true: "return true"
return [<user.text>]: 
    insert("return ")
    insert(text)