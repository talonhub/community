os: windows
and app.name: WindowsTerminal.exe
os: windows
and app.exe: windowsterminal.exe
#tag: terminal
-
jupiter: "jupyter notebook "	
 
connect to locus: 
	"ssh -X ansaldoginee2@ai-submit2.niaid.nih.gov"
	key(enter)

connect to skyline: 
	"ssh -X ansaldoginee2@ai-hpcsubmit2.niaid.nih.gov"
	key(enter)

interactive session: 
	"qrsh -l h_vmem=16G"
	key(enter)


my data: 
	"cd /hpcdata/lpd_mis/Belkaid_Lab_RNASeq_Data/Eduard_Ansaldo/"
	key(enter)
	"ls"
	key(enter)

my folder: 
	"cd /hpcdata/lpd_mis/EduardAnsaldo/"
	key(enter)
	"ls"
	key(enter)

Copy from server:
	"sftp eduardansaldo@ai-appijupyterdev1.niaid.nih.gov:/home/eduardansaldo/plots_repeat_120k/* ."
	

TCR modules:
	"module load BLAST+/2.2.31-goolf-1.7.20-Python-2.7.9"
	key(enter)
	"module load Biopython/1.65-goolf-1.7.20-Python-2.7.9"	
	key(enter)


jobs status:
	"qstat -u ansaldoginee2"
	key(enter)

katie upper:
	"cd .."
	key(enter)
	"ls"
	key(enter)

open$:
	key(tab)
	key(enter)
	"ls"
	key(enter)

remove folder:
	"rm -rf "

submit job:
	"qsub jo"
	key(tab)
	key(enter)
	
new job:
	"python /nethome/ansaldoginee2/scripts/create_qsub_for_command_EA.py\n"
	