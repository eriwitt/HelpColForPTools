Author: Eric Witt
Version: v01

#######################################################################################################################################

This script filters pathways with missing enzyme mappings that were not considered in the PGDB from the pathway-inference-report 
written by PathoLogic while creating the PGDB. Pathways are considered in which the number of missing reactions is less than or equal 
to the number of existing reactions.

A possible strategy could be to add all filtered pathways to the PGDB and run Pathway Tools Pathway Hole Filler. All pathways that are 
complete after this step could be kept and the others should be searched for possible gene candidates in the report file of the pathway 
hole filler. If no gene could be assigned to the missing reaction, remove the pathway.

#######################################################################################################################################

"getpwymissingrxn" is written in Python version 2.7.14

It works under linux and windows.

INPUT:
	- The pathway-inference-report (.txt) produced by PathoLogic during the creation of your PGDB

OUTPUT:
	- Report file (.txt) with a set of pathways that were not added to the PGDB due to missing reactions

#######################################################################################################################################
###Executables#########################################################################################################################

This folder contains the applications of the GUI version of "getpwymissingrxn" for the respective operating system (Windows and Linux). 
These applications are based on the "GUI_getpwymissingrxn_v01.py" script which is stored in the scripts directory.

#######################################################################################################################################
###Scripts#############################################################################################################################

"CLI_getpwymissingrxn_v01.py"
	This is the command line version of the script that could be included in pipelines. To run the script furthe spectifications 
	are necessary otherwise the script doesn't work.
		-pathway_inference_report_path:		Enter the path of the pathway-inference-report produced by PathoLogic
		-report_file_storage_path:	        Enter the path of your Report file (e.g.: C:\Output\report.txt).

	You can run it by using python 2.7: 
		python CLI_getpwymissingrxn_v01.py pathway_inference_report_path report_file_storage_path 

	e.g.:	python CLI_getpwymissingrxn_v01.py C:\Input\pathway-inference-report.gbk C:\Output\report.txt 

"GUI_getpwymissingrxn_v01.py"
	This is the graphical user interface guided version of the script "gbkrefinement" controlled by the user. You can use the 
	Executable (Executables directory) if you do not know how to deal with the Python file.

	You can run it by using python 2.7: 
		python GUI_getpwymissingrxn_v01.py

#######################################################################################################################################
###Sample_Input########################################################################################################################

pathway-inference-report.txt
	
	This is a sample file produced by PathoLogic.
	

#######################################################################################################################################
###Sample_Output#######################################################################################################################

report.txt
	This is a sample report file which is produced by running "getpwymissingrxn" with pathway-inference-report.txt as INPUT.

