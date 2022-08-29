app: Naheulbeuk
os: mac
-
parrot(ch): mouse_click(0)
parrot(tut): user.mouse_toggle_control_mouse()

pan up: key(w)
pan left: key(a)
pan down: key(s)
pan right: key(d)

camera left: key(q:20)
camera right: key(e:20)
camera center: key(g)

# you will have to set these in the game
zoom in: key(i)
zoom out: key(o)

battle start: key(space)

turn end: key(f)
turn delay: key(r)

tool tips: key(t)

confirm that: key(enter)
# set this in game
cancel that: key(escape)

hurry up: 
    key(space:down)
    sleep(200ms)
    key(space:up)

# set this in game
place waypoint: key(p)
start waypoints: key(p:down)
end way points: key(p:up)

skill one: key(h)
skill to: key(j)
skill three: key(k)
skill for: key(l)
belt one: key(b)
belt too: key(n)
belt three: key(m)

attack ranged: key(x)
attack melee: key(z)
enter defense: key(c)
enter overwatch: key(v)

show characters: key(tab)
# set this in game
show overwatch: key(,)

heal all: key(r)
take all: key(t)

show traps: 
    key(shift)
    #key(shift:down)
    #sleep(500ms)
    #key(shift:up)

show interactive: 
    key(tab:down)
    sleep(500ms)
    key(tab:up)

toggle run: key(ctrl)

show menu: key(escape)
#set in game
show inventory: key(.)
show skill tree: key(f)
show map: key(m)

go back: key(escape)

game save: key(F1)
game load: key(F2)






