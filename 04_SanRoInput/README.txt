Author: Eric Witt
Version: v01

#######################################################################################################################################

This script was written for creating the necessary FASTA input files for the Tool from Santos & Rocha (2016) to estimate the 
coefficients of amino acids, dNTPs and NTPs for the biomass composition.
   
   Santos, S., Rocha, I., Estimation of biomass composition from genomic and transcriptomic information. 
   Journal of integrative bioinformatics 13 (2), 2016 https://doi.org/10.2390/biecoll-jib-2016-285

   Application can be downloaded from http://darwin.di.uminho.pt/biomass/files/Application.jar

The input GenBank annotation must contain the genome sequence!

#######################################################################################################################################

"SanRoInput" is written in Python version 2.7.14

It works under linux and windows.

INPUT:
	- The GenBank annotation (.gbk) with the genome sequence of your organism.

OUTPUT:
	- Error report file (.txt) 
	- five FASTA files (.faa)
    
#######################################################################################################################################

The scripts uses the biopython package from Cock et al. (2009) to parse the GeneBank Annotation.

Cock PA, Antao T, Chang JT, Chapman BA, Cox CJ, Dalke A, Friedberg I, Hamelryck T, Kauff F, Wilczynski B and de Hoon MJL (2009) 
Biopython: freely available Python tools for computational molecular biology and bioinformatics. Bioinformatics, 25, 1422-1423

#######################################################################################################################################
###Executables#########################################################################################################################

This folder contains the applications of the GUI version of "SanRoInput" for the respective operating system (Windows and Linux). 
These applications are based on the "GUI_SanRoInput_v01.py" script which is stored in the scripts directory.

#######################################################################################################################################
###Scripts#############################################################################################################################

"CLI_SanRoInput_v01.py"
	This is the command line version of the script that could be included in pipelines. To run the script furthe spectifications 
	are necessary otherwise the script doesn't work.
    
		-genbank_annotation_path:		Enter the path of your GenBank annotation (e.g.: C:\Input\anno.gbk)
		-storage_path:	        		Enter the path to store the output files (e.g.: C:\Output).

	You can run it by using python 2.7: 
		python CLI_SanRoInput_v01.py genbank_annotation_path storage_path

	e.g.:	python CLI_getpwymissingrxn_v01.py C:\Input\anno.gbk C:\Output 

"GUI_SanRoInput_v01.py"
	This is the graphical user interface guided version of the script "SanRoInput" controlled by the user. You can use the Executable 
    (Executables directory) if you do not know how to deal with the Python file.

	You can run it by using python 2.7: 
		python GUI_SanRoInput_v01.py

#######################################################################################################################################
###Sample_Input########################################################################################################################

CP000448.1.gbk
	
	This includes the complete genome annotation of Syntrophomonas wolfei subsp. wolfei str. Goettingen G311 which can be found under:
	https://www.ncbi.nlm.nih.gov/nuccore/CP000448
	

#######################################################################################################################################
###Sample_Output#######################################################################################################################

error_report.txt
	The error_report has entries if the CDS feature has not a translation qualifier.
	If no error occurs than this file is empty.

CP000448.1_DNA_FASTA.faa
	This file contains the genome sequence in FASTA format.
		
		>record.id record.description
		sequence

CP000448.1_mRNA_FASTA.faa
	This file contains the mRNA sequences in FASTA format.

		>feature.type locus_tag location
		sequence

CP000448.1_protein_FASTA.faa
	This file contains the protein sequences in FASTA format.

		>locus_tag location
		sequence

CP000448.1_rRNA_FASTA.faa
	This file contains the rRNA sequences in FASTA format.

		>feature.type locus_tag location
		sequence

CP000448.1_tRNA_FASTA.faa
	This file contains the tRNA sequences in FASTA format.

		>feature.type locus_tag location
		sequence
