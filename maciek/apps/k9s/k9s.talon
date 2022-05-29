app: k9s
-
name <number_small>: insert(number_small)
{user.k8s_resources}: insert(":{user.k8s_resources}\n")

alias|aliases [<user.text>]: 
    key(escape)
    sleep(10ms)
    key(escape)
    sleep(10ms)
    key(ctrl-a)
    insert("/")
    insert(text or "")
search [<user.text>]:
    insert("/")
    insert(text or "")
remove:
    key(ctrl-d)
describe:
    insert("d\n")
edit:
    insert("e\n")
