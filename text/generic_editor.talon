find it:
    edit.find()

next one:
    edit.find_next()

tug:
    edit.left()

tug <number_small> now:
    user.left_n(number_small)

draw:
    edit.word_left()

draw <number_small> now:
    user.word_left_n(number_small)

push:
    edit.right()

push <number_small> now:
    user.right_n(number_small)

step:
    edit.word_right()

step <number_small> now:
    user.word_right_n(number_small)

raise:
    user.up_n(1)

raise <number_small> now:
    user.up_n(number_small)

drop:
    user.down_n(1)

drop <number_small> now:
    user.down_n(number_small)

head:
    edit.line_start()

tail:
    edit.line_end()

go way down:
    edit.file_end()

go way up:
    edit.file_start()

go page down:
    edit.page_down()

go page up:
    edit.page_up()

# selecting
select line:
    edit.select_line()

select all:
    edit.select_all()

select left:
    edit.extend_left()

select right:
    edit.extend_right()

select up:
    edit.extend_line_up()

select down:
    edit.extend_line_down()

select word:
    edit.select_word()

<user.select> lefter:
    edit.extend_word_left()

<user.select> writer:
    edit.extend_word_right()

select way left:
    edit.extend_line_start()

select way right:
    edit.extend_line_end()

select way up:
    edit.extend_file_start()

select way down:
    edit.extend_file_end()

# editing
indent [more]:
    edit.indent_more()

(indent less | out dent):
    edit.indent_less()

# deleting
<user.delete> line:
    edit.delete_line()

wipe <number_small> now:
    user.delete_left_n(number_small)

drill <number_small> now:
    user.delete_right_n(number_small)
    
<user.delete> up:
    edit.extend_line_up()
    edit.delete()

<user.delete> down:
    edit.extend_line_down()
    edit.delete()

<user.delete> word:
    edit.delete_word()

scratch:
    user.delete_word_left_n(1)

scratch <number_small> now:
    user.delete_word_left_n(number_small)

swallow:
    user.delete_word_right_n(1)

swallow <number_small> now:
    user.delete_word_right_n(number_small)

<user.delete> start:
    edit.extend_line_start()
    edit.delete()

<user.delete> close:
    edit.extend_line_end()
    edit.delete()

<user.delete> way up:
    edit.extend_file_start()
    edit.delete()

<user.delete> way down:
    edit.extend_file_end()
    edit.delete()

<user.delete> all:
    edit.select_all()
    edit.delete()

#copy commands
copy all:
    edit.select_all()
    edit.copy()
#to do: do we want these variants, seem to conflict
# copy left:
#      edit.extend_left()
#      edit.copy()
# copy right:
#     edit.extend_right()
#     edit.copy()
# copy up:
#     edit.extend_up()
#     edit.copy()
# copy down:
#     edit.extend_down()
#     edit.copy()

copy word:
    edit.select_word()
    edit.copy()

copy lefter:
    edit.extend_word_left()
    edit.copy()

copy righter:
    edit.extend_word_right()
    edit.copy()

copy line:
    edit.select_line()
    edit.copy()

#cut commands
cut all:
    edit.select_all()
    edit.cut()
#to do: do we want these variants
# cut left:
#      edit.select_all()
#      edit.cut()
# cut right:
#      edit.select_all()
#      edit.cut()
# cut up:
#      edit.select_all()
#     edit.cut()
# cut down:
#     edit.select_all()
#     edit.cut()

cut word:
    edit.select_word()
    edit.cut()

cut lefter:
    edit.extend_word_left()
    edit.cut()

cut righter:
    edit.extend_word_right()
    edit.cut()

cut line:
    edit.select_line()
    edit.cut()

Pokey mail: "pokey.rule@gmail.com"