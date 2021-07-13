tag: user.tabs
-
(tick|tab) (open | new): app.tab_open()
(tick|tab) last: app.tab_previous()
(tick|tab) next: app.tab_next()
close: app.tab_close()
(tick|tab) (reopen|restore): app.tab_reopen()
go (tick|tab) <number>: user.tab_jump(number)
tick <number>: user.tab_jump(number)
(tick|tab) next <number>: user.tab_next(number)
(tick|tab) last <number>: user.tab_previous(number)
go (tick|tab) final: user.tab_final()
