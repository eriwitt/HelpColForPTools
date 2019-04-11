Author: Eric Witt
Version: v01

#######################################################################################################################################

"addBiomassAndDrainsToSBML" is a script which adds the biomass and drain reactions from .fba file to the SBML file.
Therefore the script scans the .fba file for entries in the biomass, nutrients and secretions area to produce the reactions in the sbml file. The entries of the biomass metabolites must have an tab-seperated coefficient for the stoichiometry
    e.g.:   L-ALPHA-ALANINE[CCO-CYTOSOL]	0.428140372
    
For the entries of the nutrients and secretions it is necessary that they have the following form:
    e.g.:   CROTONATE[CCO-EXTRACELLULAR] :upper-bound 0.9258
            Pi[CCO-EXTRACELLULAR]
            ACET[CCO-EXTRACELLULAR] :lower-bound 1.9840 :upper-bound 1000
Please remove comments or so behind the numbers of the boundaries or the value will have the comment attached in the SBML file.
    
The scripts adds for every entry in the nutrients and secretions section  a single reaction.
The drain reaction for a nutrient looks like:                   --> nutrient_e
The drain reaction for a secretion looks like:   secretion_e    -->   
If ther are no boundaries defined the script sets the lower-bound to 0 and the uppper-bound to 1000.
    
The added reactions can be found at the end of the SBML file.

#######################################################################################################################################

"addBiomassAndDrainsToSBML" is written in Python version 2.7.14

It works under linux and windows.

INPUT:
	-Your SBML file (.xml) exported from your Pathway Tools model
    -Your .fba file which works for the MetaFlux Fluy Balance Analysis 

OUTPUT:
	-A new SBML file with the added reactions

#######################################################################################################################################

The scripts uses the libSBML Python library.

Bornstein, B. J., Keating, S. M., Jouraku, A., and Hucka, M. (2008) LibSBML: An API Library for SBML. Bioinformatics, 24(6):880-881.

#######################################################################################################################################
###Executables#########################################################################################################################

This folder contains the applications of the GUI version of "addBiomassAndDrainsToSBML" for the respective operating system (Windows 
and Linux). 
These applications are based on the "GUI_addBiomassAndDrainsToSBML_v01.py" script which is stored in the scripts directory.

#######################################################################################################################################
###Scripts#############################################################################################################################

"CLI_addBiomassAndDrainsToSBML_v01.py"
	Adds the biomass and drain reactions to the SBML file.
	That will be maybe an option to include it in pipelines.

	You can run it by using python 2.7: 
		python CLI_addBiomassAndDrainsToSBML_v01.py Your_SBML_path Your_fba_file_path Save_new_SBML_path

"GUI_addBiomassAndDrainsToSBML_v01.py"
	This is the graphical user interface version of the script. 

	You can run it by using python 2.7: 
		python GUI_addBiomassAndDrainsToSBML_v01.py

#######################################################################################################################################
###Sample_Input########################################################################################################################

Swe099eec_20181120.xml
	
	This is a SBML test file.
    
crot.fba
    
    The working .fba file for the MetaFlux Flux Balance Analysis with crotonate as energy source
    
butyrate.fba

    The working .fba file for the MetaFlux Flux Balance Analysis with butyrate as energy source

#######################################################################################################################################
###Sample_Output#######################################################################################################################

Swe099eec_20181120_crotonate.xml
	This is the output from the script by using Swe099eec_20181120.xml and crot.fba as input.

Swe099eec_20181120_butyrate.xml
	This is the output from the script by using Swe099eec_20181120.xml and butyrate.fba as input.

