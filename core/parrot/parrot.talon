#parrot(pop):
#    user.debug("pop {power}")
#    user.noise_pop()

#parrot(cluck):
#    user.debug("cluck {power}")
#    user.noise_cluck()

#parrot(shush):              print("shush")
#parrot(hiss):              print("hiss")
#parrot(cluck):              print("cluck")

#parrot(cluck): edit.undo()

parrot(shush):
	user.noise_debounce("shush", true)
parrot(shush:stop):
	user.noise_debounce("shush", false)

parrot(hiss):
	user.noise_debounce("hiss", true)
parrot(hiss:stop): 
	user.noise_debounce("hiss", false)