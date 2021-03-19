# HTML Basic Tags

elm header <number_small>:
  "<h"
  insert(number_small)
  "></h"
  insert(number_small)
  ">"
  key(left:5)

elm paragraph:
  "<p></p>"
  key(left:4)

elm strong:
  "<strong></strong>"
  key(left:9)

elm emphasize:
  "<em></em>"
  key(left:5)

elm break:
  "<br>"
  key(enter)

elm anchor:
  "<a href=\"\"></a>"
  key(left:6)

elm div:
  "<div>"
  key(enter enter)
  "</div>"
  key(up tab)

elm image:
  "<img src=\"\" alt=\"\"></img>"
  key(left:15)

elm video long:
  "<video autoplay mute controls>"
  key(enter tab)
  "<source src=\"\" type=\"video/\">"
  key(enter)
  "Sorry, your browser doesn't support embedded videos."
  key(enter shift-tab)
  "</video>"
  key(up:2 right:7)
  
 elm video short:
  "<video src=\"\" controls>"
  key(left:11)
 
elm ordered list:
  "<ol>"
  key(enter tab)
  "<li></li>"
  key(enter shift-tab)
  "</ol>"
  key(up right)

elm unordered list:
  "<ul>"
  key(enter tab)
  "<li></li>"
  key(enter shift-tab)
  "</ul>"
  key(up right)

elm list item:
  "<li></li>"
  key(left:5)

elm five list items:
  "<li></li>"
  key(enter)
  "<li></li>"
  key(enter)
  "<li></li>"
  key(enter)
  "<li></li>"
  key(enter)
  "<li></li>"
  key(left:5)


# HTML Attributes

elm class:
  " class=\"\""
  key(left)

elm id:
  " id=\"\""
  key(left)

elm source:
  " src=\"\""
  key(left)

elm width:
  " width=\"\""
  key(left)

elm height:
  " height=\"\""
  key(left)



# HTML Document Set-up

elm comment:
  "<!--  -->"
  key(left:4)

elm boilerplate:
  "<!DOCTYPE html>"
  key(enter)
  "<html lang=\"en\">"
  key(enter tab)
  "<head>"
  key(enter tab)
  "<meta charset=\"utf-8\">"
  key(enter)
  "<title>Title</title>"
  key(enter)
  "<link href=\"style/style.css\" type=\"text/css\" rel=\"stylesheet\">"
  key(enter)
  "<script src=\"script.js\"></script>"
  key(enter shift-tab)
  "</head>"
  key(enter)
  "<body>"
  key(enter enter)
  "</body>"
  key(enter shift-tab)
  "</html>"


