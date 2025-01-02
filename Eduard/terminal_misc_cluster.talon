os: windows
and app.name: WindowsTerminal.exe
os: windows
and app.exe: WindowsTerminal.exe
-
lisa:
	"ls"
	key(enter)

folder <user.prose>$:
	"cd "
	insert(prose)
	sleep(500ms)
	key(tab)
	key(enter)
	"ls"
	key(enter)

folder <user.letters>$:
	"cd "
	key(letters)
	sleep(300ms)
	key(tab)
	key(enter)
	"ls"
	key(enter)

folder (ship | uppercase) <user.letters> [(lowercase | sunk)]:
	"cd "
	user.insert_formatted(letters, "ALL_CAPS")
	sleep(300ms)
	key(tab)
	key(enter)
	"ls"
	key(enter)

folder <number_small>$:
	"cd "
	key('{number_small}')
	sleep(300ms)
	key(tab)
	key(enter)
	"ls"
	key(enter)

folder scratch: 
	"cd /hpcdata/scratch/Eduard_Ansaldo/"
	key(enter)
	"ls"
	key(enter)

create sample sheet:
	"python /nethome/ansaldoginee2/scripts/make_bcl_convert.py"
	key(enter)	