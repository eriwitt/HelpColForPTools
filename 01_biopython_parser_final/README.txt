Author: Eric Witt
Version: v01

##########################################################################################################################################################

"01_biopython_parser" is a script to improve the parsability of your annotation for use in Pathway Tools PathoLogic.
This includes removing unaccepted annotation features which will be removed automatically by using the command line inteface (CLI) or which can be 
controlled by the user in the graphical user interface (GUI). 
Furthermore, GO terms in the "/note" qualifier are rewritten into a form accepted by PathoLogic if they originally exists in this form:

/note: "GO_component: GO:0005737 - cytoplasm; GO_function: GO:0003735 - structural constituent of ribosome; GO_process: GO:0006412 - translation" 

This entry will be changed to:

/note: "go_component: cytoplasm [goid GO:0005737]; GO_function: GO:0003735 - structural constituent of ribosome; GO_process: GO:0006412 - translation

##########################################################################################################################################################

"01_biopython_parser" is written in Python version 2.7.14

It works under linux and windows.

INPUT:
	-Your GeneBank Annotation (.gbk) which should be improved for using Pathway Tools PathoLogic 

OUTPUT:
	-Report file (.txt) with the selections and changes that have been made 
	-Improved GeneBank Annotation (.gbk)

##########################################################################################################################################################

The scripts uses the biopython package from Cock et al. (2009) to parse, rewrite and export the GeneBank Annotation.

Cock PA, Antao T, Chang JT, Chapman BA, Cox CJ, Dalke A, Friedberg I, Hamelryck T, Kauff F, Wilczynski B and de Hoon MJL (2009) 
Biopython: freely available Python tools for computational molecular biology and bioinformatics. Bioinformatics, 25, 1422-1423

##########################################################################################################################################################
###Executables############################################################################################################################################

This folder contains the applications of the GUI version of "01_biopython_parser" for the respective operating system (Windows and Linux). 
These applications are based on the "GUI_01_biopython_parser_v01.py" script which is stored in the scripts directory.

##########################################################################################################################################################
###Scripts################################################################################################################################################

"CLI_01_biopython_parser_v01.py"
	Removes all unaccepted GenBank features automatically and improves the /note qualifiers if GO Terms contained.
	That will be maybe an option to include it in pipelines.

	You can run it by using python 2.7: 
		python CLI_01_biopython_parser_v01.py

"GUI_01_biopython_parser_v01.py"
	Is controlled by the user in an graphical user interface. You get more information and you decide which changes will be made to your GeneBank 
	annotation.

	You can run it by using python 2.7: 
		python GUI_01_biopython_parser_v01.py

##########################################################################################################################################################
###Sample_Input###########################################################################################################################################

ecoli_k_12.gbk
	
	This includes the complete genome annotation of Escherichia coli str. K-12 substr. MG1655 which can be found under:
	https://www.ncbi.nlm.nih.gov/nuccore/U00096

##########################################################################################################################################################
###Sample_Output##########################################################################################################################################

improved_ecoli_k_12.gbk
	This is a sample improved GenBank annotation which is produced by running "01_biopython_parser" with ecoli_k_12.gbk as INPUT. All unaccepted 
	GenBank feature were removed and the "/note" qualifiers where improved if GO Terms are contained.

report_ecoli_k_12.txt
	This is a sample report file which is produced by running "01_biopython_parser" with ecoli_k_12.gbk as INPUT.

