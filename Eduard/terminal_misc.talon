tag: terminal
-
jupiter: "jupyter notebook "	
 
connect to locus: 
	"ssh -X ansaldoginee2@ai-submit2.niaid.nih.gov"
	key(enter)

interactive session: 
	"qrsh -l h_vmem=16G"
	key(enter)


open my data: 
	"cd /hpcdata/lpd_mis/Belkaid_Lab_RNASeq_Data/Eduard_Ansaldo/"
	key(enter)
	"ls"
	key(enter)

open my folder: 
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

katie up:
	insert("cd ..")
	key(enter)
	"ls"
	key(enter)

jobs status:
	"qstat -u ansaldoginee2"
	key(enter)