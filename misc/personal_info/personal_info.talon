-
settings():
    # if set and a list has more than one entry autos select the specified one
    # otherwise will use a gui selector by default
    user.personal_info_auto_select = 0
my <user.personal_info>: user.personal_info(personal_info)
my full name:
    user.personal_info("first-name")
    key(space)
    user.personal_info("last-name")

my <user.ordinals> <user.personal_info>: user.personal_info_by_id(personal_info, ordinals)
