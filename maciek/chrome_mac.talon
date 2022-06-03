os: mac
app: chrome
-

###############################################################################
### vimium
###############################################################################
next page: 
    insert("]]")
last page: 
    insert("[[")
    
show links: key("f")
link: key("f")

new link: key(shift-f)

search [<user.text>]$: 
    key("o")
    sleep(200ms)
    insert(text or "")
    
search that: 
    key("o")
    sleep(200ms)
    key(cmd-v)

copy link: key(y f)
(address | url) copy: 
    key(escape y y)
    sleep(100ms)

address [<user.text>]:
    key(cmd-l)
    sleep(50ms)
    insert(text or "")

jump [<user.text>]:
    key(cmd-shift-a)         
    sleep(100ms)
    insert(text or "")
    
close: 
    app.tab_close()
    sleep(40ms)
go front: browser.go_forward()

next$: app.tab_next()
last$: app.tab_previous()
back$: browser.go_back()
front$: browser.go_forward()

google [<user.text>]$: 
password fill:
    key(cmd-shift-l)
    
tab open [<user.text>]$: 
    app.tab_open()
    sleep(100ms)
    insert(text or "")



find [<user.text>]$: 
    key(cmd-f)
    sleep(200ms)
    insert(text or "")
    # user.text_field_mode(phrase or "")

find this:
    key(cmd-c)
    key(cmd-f)
    sleep(200ms)
    key(cmd-v)
    
password fill: 
    key(cmd-shift-l)

###############################################################################
### Keyboard shortcuts
###############################################################################
key(cmd-g):
    text = edit.selected_text()
    user.search_with_search_engine("https://www.google.com/search?q=%s", text)
    
###############################################################################
### KeyPad shortcuts
###############################################################################    
key(shift-cmd-alt-ctrl-9):
    key(cmd-right)
key(shift-cmd-alt-ctrl-8):
    key(cmd-left)
# asterisk
key(shift-cmd-alt-ctrl-a):
    key(cmd-alt-right)
key(shift-cmd-alt-ctrl-/):
    key(cmd-alt-left)
key(shift-cmd-alt-ctrl-m):
        key(cmd-w)
        
test google:
    text = edit.selected_text()
    
    user.search_with_search_engine("https://www.google.com/search?q=%s", text)
    
history:
    key(cmd-y)
bookmark:
    key(cmd-d)    

# This is for the search
key(cmd-enter): key(ctrl-enter)