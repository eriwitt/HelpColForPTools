Author: Eric Witt
Version: v01

#######################################################################################################################################

The script gbkrefinement was developed to enrich the gene entries of your annotation (GenBank format) with EC numbers from the 
associated gene entries of the KEGG Database (Internet connection required!). If the found EC number in the associated KEGG entrie 
is not in the gene entrie of your annotation then the EC number is added. The script generates an Report file with the EC numbers which 
were added and the improved annotation in GenBank format.

#######################################################################################################################################

"gbkrefinement" is written in Python version 2.7.14

It works under linux and windows.

INPUT:
	- Your GeneBank Annotation (.gbk) which you want to enrich with EC numbers from the KEGG database

OUTPUT:
	- Report file (.txt) with the added EC numbers 
	- EC numbers enriched GeneBank Annotation (.gbk)
	- Gene associated KEGG entries in html format (genename.html)
    
#######################################################################################################################################

The scripts uses the biopython package from Cock et al. (2009) to parse, rewrite and export the GeneBank Annotation.

Cock PA, Antao T, Chang JT, Chapman BA, Cox CJ, Dalke A, Friedberg I, Hamelryck T, Kauff F, Wilczynski B and de Hoon MJL (2009) 
Biopython: freely available Python tools for computational molecular biology and bioinformatics. Bioinformatics, 25, 1422-1423

#######################################################################################################################################
###Executables#########################################################################################################################

This folder contains the applications of the GUI version of "gbkrefinement" for the respective operating system (Windows and Linux). 
These applications are based on the "GUI_gbkrefinement_v01.py" script which is stored in the scripts directory.

#######################################################################################################################################
###Scripts#############################################################################################################################

"CLI_gbkrefinement_v01.py"
	This is the command line version of the script that could be included in pipelines. To run the script furthe spectifications are 
    necessary otherwise the script doesn't work.
    
		-storage_option:		y 	storage of gene associated KEGG entries in html format
						n	no storage of gene associated KEGG entries in html format
		-KEGG_organism_identifier:	Every organism stored in the KEGG database has a three- or four-letter organism code for identification. 
						If you know it you can enter it here (for example Escherichia coli str. K-12 substr. MG1655 has the KEGG 
						organism identifier eco). If you don't know enter n.
		-Your_annotation_path:		Enter the path of your annotation which you want to enrich with EC numbers (e.g.: C:\Input\annotation.gbk).
		-Report_file_storage_path:	Enter the path of your Report file (e.g.: C:\Output\report.txt).
		-Output_annotation_path:	Enter the path of your Report file (e.g.: C:\Output\refined_annotation.gbk).
		-Html_file_storage_path:	If you have enter y for storage_option then specify here the path for the HTML file storage (e.g.: C:\Output\HTML).

	You can run it by using python 2.7: 
		python CLI_gbkrefinement_v01.py storage_option KEGG_organism_identifier Your_annotation_path Report_file_storage_path Output_annotation_path Html_file_storage_path

	e.g.:	python CLI_gbkrefinement_v01.py y eco C:\Input\annotation.gbk C:\Output\report.txt C:\Output\refined_annotation.gbk C:\Output\HTML

"GUI_gbkrefinement_v01.py"
	This is the graphical user interface guided version of the script "gbkrefinement" controlled by the user. You can use the Executable (Executables directory) if you do not 
	know how to deal with the Python file.

	You can run it by using python 2.7: 
		python GUI_gbkrefinement_v01.py

#######################################################################################################################################
###Sample_Input########################################################################################################################

improved_ecoli_k_12.gbk
	
	This genome annotation of Escherichia coli str. K-12 substr. MG1655 is the output annotation from the 01_biopython_parser script. 
    It is based on the annotation which can be found under:
		https://www.ncbi.nlm.nih.gov/nuccore/U00096
	

#######################################################################################################################################
###Sample_Output#######################################################################################################################

gbk_ref_improved_ecoli_k_12.gbk
	This is a sample refined GenBank annotation which is produced by running "gbkrefinement" with improved_ecoli_k_12.gbk as INPUT. 
    The genes in your annotation were enriched with EC numbers from the gene associated entries from the KEGG database. 

report_improved_ecoli_k_12.txt
	This is a sample report file which is produced by running "gbkrefinement" with improved_ecoli_k_12.gbk as INPUT.

KEGG_html_files directory
	Contains the gene associated entries from the KEGG database in html format. The storage of these files is optional.
