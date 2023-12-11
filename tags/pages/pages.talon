tag: user.pages
-
go next [<number_small>]:
    numb = number_small or 1
    user.page_next()
    repeat(numb - 1)
go last: 
    numb = number_small or 1
    user.page_previous()
    repeat(numb - 1)
go page <number>: user.page_jump(number)
go page final: user.page_final()
