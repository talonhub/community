mode: dictation
mode: command 
-
(rejection|reject) history: user.rejection_history_toggle()
copy (lest|last) (reject|rejection): user.rejection_copy_last()
[move] reject [category] [good] one: user.rejection_move_last(1)
[move] reject [category] [good] two: user.rejection_move_last(2)
[move] reject [category] bad [three]: user.rejection_move_last(3)
[move] reject [category] (review|four): user.rejection_move_last(4)
