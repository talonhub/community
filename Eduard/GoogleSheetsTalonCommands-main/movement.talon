tag: user.google_sheets
-
move: user.google_sheets_toggle_movement_tool()

cell go <user.google_sheets_cell_location>: user.google_sheets_go_to_cell(google_sheets_cell_location)

row go <number>: user.google_sheets_go_to_row(number)

column go <user.google_sheets_cell_column>: user.google_sheets_go_to_column(google_sheets_cell_column)