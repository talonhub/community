tag: terminal
-
# tags should be activated for each specific terminal in the respective talon file

rails (console|client):
  user.rails_console()
rails server:
  user.rails_server()
rails (my grate|migrate):
  'rails db:migrate '
rails (my grate|migrate) test:
  'rails db:migrate RAIL_ENV=test'
rails test:
  'rails test '
pry (wear|where): "whereami\n"
pry next: "next\n"
pry continue: "continue\n"
pry finish: "finish\n"
pry dupe:
  edit.copy()
  sleep(50ms)
  edit.paste()
  # sleep(500ms)
  # actions.key("enter")
pry history: "history -n 10\n"
pry history <number>: "history -tail {number}\n"
pry history all: "history\n"
pry replay <number>: "history --replay {number}"
pry find method: "find-method "
pry show dock: "show-doc "
pry show source: "show-source "
pry back trace: "backtrace\n"
pry frame <number>: "frame {number}"
pry frame up: "up\n"
pry frame down: "down\n"
silence: ";\n"

light user: 'Lti13User.'
light launch: 'Lti13Launch.'