go word left: 
	edit.word_left()
	
go word right: 
	edit.word_right()

go left: 
	edit.left()

go right: 
	edit.right()

go up: 
	edit.up()

go down: 
	edit.down()

go line start: 
	edit.line_start()
	
go line end: 
	edit.line_end()

go way left: 
	edit.line_start()
	edit.line_start()
	
go way right: 
	edit.line_end()

go way down: 
	edit.file_end()
	
go way up: 
	edit.file_start()

# selecting
select line: 
	edit.line_start()
	edit.extend_line_end()

select left: 
	edit.extend_left()
	
select right: 
	edit.extend_right()

select up: 
	edit.extend_line_up()
	
select down: 
	edit.extend_line_down()

select word left:
	edit.extend_word_left()
	
select word right: 
	edit.extend_word_right()

select way left: 
	edit.extend_line_start()
	
select way right: 
	edit.extend_line_end()
	
select way up: 
	edit.extend_file_start()
	
select way down: 
	edit.extend_file_end()

# deleting
clear line: 
	edit.delete_line()
    
clear left: 
	edit.extend_line_start()
	edit.delete()
	
clear right: 
	edit.extend_line_end()
	edit.delete()
	
clear up: 
	edit.extend_line_up()
	edit.delete()

clear down: 
	edit.extend_line_down()
	edit.delete()

clear word left: 
	edit.extend_word_left()
	edit.delete()
	
clear word right: 
	edit.extend_word_right()
	edit.delete()

clear way left: 
	edit.extend_line_start()
	
clear way right: 
	edit.extend_line_end()
	edit.delete()

clear way up: 
	edit.extend_file_start()
	edit.delete()
	
clear way down: 
	edit.extend_file_end()
	edit.delete()
