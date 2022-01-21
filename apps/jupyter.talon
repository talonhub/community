app: chrome
-
tag(): browser
tag(): user.tabs

insert cell after:      
  key(escape)
  "b"
  key(enter)

insert cell before:      
  key(escape)
  "a"
  key(enter)

execute:           
  key(shift-enter)

code cell:              
  key(escape)
  "y"
  key(enter)

markdown cell:          
  key(escape)
  "m"
  key(enter)

dock string:
  key(shift-tab)
