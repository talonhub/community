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