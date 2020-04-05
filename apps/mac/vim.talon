app: Vim
app: Code
app: /.*/
and title: /vim/i

-
delete [around] word:
    key(d)
    key(a)
    key(w)

change [inner] word:
    key(c)
    key(i)
    key(w)

change until:
    key(d)
    key(t)

delete until:
    key(d)
    key(t)

easy [motion] up:
    key(,)
    key(,)
    key(k)

easy [motion] down:
    key(,)
    key(,)
    key(j)

delete line:
    key(d)
    key(d)

insert line up:
    key(m)
    key(z)
    key(shift-o)
    key(escape)
    key(`)
    key(z)

insert line down:
    key(m)
    key(z)
    key(o)
    key(escape)
    sleep(50ms)
    key(`)
    key(z)
