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

elm link:
  "<link></link>"
  key(left:7)

elm link style sheet:
  "<link href=\"style/style.css\" type=\"text/css\" rel=\"stylesheet\">"

elm strong:
  "<strong></strong>"
  key(left:9)

elm script:
  "<script></script>"
  key(left:9)

elm emphasize:
  "<em></em>"
  key(left:5)

elm break:
  "<br>"
  key(enter)

elm span:
  "<span></span>"
  key(left:7)

elm anchor:
  "<a href=\"\"></a>"
  key(left:6)

elm nav:
  "<nav>"
  key(enter:2)
  "</nav>"
  key(up tab)

elm div:
  "<div>"
  key(enter:2)
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

elm table:
  "<table>"
  key(enter:2)
  "</table>"
  key(up tab)

elm table header:
  "<thead>"
  key(enter:2)
  "</thead>"
  key(up tab)

elm table header cell:
  "<th></th>"
  key(left:5)

elm table row:
  "<tr></tr>"
  key(left:5)

elm table data:
  "<td></td>"
  key(left:5)

elm table body:
  "<tbody>"
  key(enter:2)
  "</tbody>"
  key(up tab) 

elm table caption:
  "<caption></caption>"
  key(left:10)

elm footer:
  "<footer>"
  key(enter:2)
  "</footer>"
  key(up tab)



# HTML FORMS

elm form:
  "<form>"
  key(enter:2)
  "</form>"
  key(up tab)

elm input:
  "<input type=\"text\" name=\"\" id=\"\">"
  key(left:8)

elm label:
  "<label for=\"\"></label>"
  key(left:10)
 
elm dropdown input:
  "<select id=\"\" name=\"\">"
  key(enter tab)
  "<option value=\"\"></option>"
  key(enter)
  "<option value=\"\"></option>"
  key(enter)
  "<option value=\"\"></option>"
  key(enter shift-tab)
  "</select>"
  key(up:4)
  edit.line_end()
  key(left:10)

elm data list input:
  "<input type=\"text\" list=\"\" id=\"\" name=\"\">"
  key(enter)
  "<datalist id=\"\">"
  key(enter tab)
  "<option value=\"\"></option>"
  key(enter)
  "<option value=\"\"></option>"
  key(enter)
  "<option value=\"\"></option>"
  key(enter shift-tab)
  "</datalist>"
  key(up:5)
  edit.line_end()
  key(left:16)

elm text area input:
  "<textarea id=\"\" name=\"\" rows=\"\" cols=\"\"></textarea>"
  key(left:37)

  


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
  key(up:2 tab)


