tag: user.history
-
go back [<number_small>]: 
    numb  = number_small or 1
    user.history_go_back()
    repeat(numb - 1)

go forward [<number_small>]:
    numb  = number_small or 1
    user.history_go_forward()
    repeat(numb - 1)