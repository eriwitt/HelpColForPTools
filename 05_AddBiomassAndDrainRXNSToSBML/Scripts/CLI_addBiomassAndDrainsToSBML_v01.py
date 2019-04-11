#!/usr/bin/python
""" addBiomassAndDrainsToSBML_final is a script which adds the biomass and drain reactions from .fba file    
    to the SBML file.
    Therefore the script scans the .fba file for entries in the biomass, nutrients and secretions area to
    produce the reactions in the sbml file.
    The entries of the biomass metabolites must have an tab-seperated coefficient for the stoichiometry
    e.g.:   L-ALPHA-ALANINE[CCO-CYTOSOL]	0.428140372
    
    For the entries of the nutrients and secretions it is necessary that they have the following form:
    e.g.:   CROTONATE[CCO-EXTRACELLULAR] :upper-bound 0.9258
            Pi[CCO-EXTRACELLULAR]
            ACET[CCO-EXTRACELLULAR] :lower-bound 1.9840 :upper-bound 1000
    Please remove comments or so behind the numbers of the boundaries or the value will have the comment attached
    in the SBML file.
    
    The scripts adds for every entry in the nutrients and secretions section  a single reaction.
    The drain reaction for a nutrient looks like:                   --> nutrient_e
    The drain reaction for a secretion looks like:   secretion_e    -->   
    If ther are no boundaries defined the script sets the lower-bound to 0 and the uppper-bound to 1000.
    
    The added reactions can be found at the end of the SBML file.
    Author: Eric Witt
"""
import sys
from libsbml import *
read = SBMLReader()


sbml_path = sys.argv[1]
sbml_SBML=read.readSBML(sbml_path)
sbml_Model=sbml_SBML.getModel()
ptools_fba_template = open(sys.argv[2]).readlines()

def extractBiomassReactantsAndProducts(ptools_fba_template, sbml_Model):
    Reactants  = []
    Products = []
    ProductsN = []
    ReactantsS  = []
    a = 0
    b = 0
    c = 0
    for i in ptools_fba_template:
        #print i
        if "\r\n" in i:
            i = i.replace("\r\n","\n")
        if i == "biomass:\n":
            a = 1
        if i == "try-biomass:\n":
            a = 0
        if i == "nutrients:\n":
            b = 1
            print i
        if i == "try-nutrients:\n":
            b = 0
        if i == "secretions:\n":
            c = 1
            print i
        if i == "try-secretions:\n":
            c = 0
        if a==1:
            # Extraction of the biomass reactants and products. The products are ADP, Pi, Proton and PPI.
            # All other entries will be placed in the reactant block.
            # For each entry in the .fba file the species-id in the SBML file is determined and the coefficient
            # is extracted.
            if i.startswith("#") or i=="\n":
                continue
            else:
                for species in sbml_Model.getListOfSpecies():
                    if "<p>BIOCYC: " in species.getNotesString():
                        biocycid = species.getNotesString().split("<p>BIOCYC: ")[1].split("</p>")[0]
                        if "|" in biocycid: 
                            biocycid = biocycid.replace("|","")
                        if (i.split("[CCO-CYTOSOL]")[0] == biocycid or i.split("[CCO-CYTOSOL]")[0].upper() == biocycid ) and species.getId().endswith("_c"):
                            if i.split("[CCO-CYTOSOL]")[0] == "ADP" or i.split("[CCO-CYTOSOL]")[0]== "Pi" or i.split("[CCO-CYTOSOL]")[0] =="Proton" or i.split("[CCO-CYTOSOL]")[0] == "PPI":
                                if "\n" in i.split("\t")[1]:
                                    product = (species.getId(),i.split("\t")[1].split("\n")[0])
                                    print product
                                    Products.append(product)
                                else:
                                    product = (species.getId(),i.split("\t")[1])
                                    print product
                                    Products.append(product)
                            else: 
                                if "\n" in i.split("\t")[1]:
                                    reactant = (species.getId(),i.split("\t")[1].split("\n")[0])
                                    Reactants.append(reactant)
                                else:
                                    reactant = (species.getId(),i.split("\t")[1])
                                    Reactants.append(reactant)
        if b==1:
            # For every entry in the nutrient area of the .fba file the species-id is determined.
            # The stoichiometry is 1. If informations for lower and/ or upper-bounds is available
            # it will be coinsidered, otherwise the lower-bound is 0 and the upper-bound is 1000.
            if i.startswith("#") or i=="\n":
                continue
            else:
                for species in sbml_Model.getListOfSpecies():
                    #print species
                    if "<p>BIOCYC: " in species.getNotesString():
                        biocycid = species.getNotesString().split("<p>BIOCYC: ")[1].split("</p>")[0]
                        if "|" in biocycid: 
                            biocycid = biocycid.replace("|","")
                        if (i.split("[CCO-EXTRACELLULAR]")[0] == biocycid or i.split("[CCO-EXTRACELLULAR]")[0].upper() == biocycid ) and species.getId().endswith("_e"):
                            print i
                            if " :upper-bound " in i and " :lower-bound " in i:
                                productn = (species.getId(), 1, i.split(" :lower-bound ")[1].split(" ")[0],i.split(" :upper-bound ")[1].split("\n")[0])
                                print productn
                                ProductsN.append(productn)
                            elif " :upper-bound " in i:
                                #productn = (speciesID, stoichiometry, lower-bound, upper-bound)
                                productn = (species.getId(), 1, 0,i.split(" :upper-bound ")[1].split("\n")[0])
                                print productn
                                ProductsN.append(productn)
                            elif " :lower-bound " in i:
                                #productn = (speciesID, stoichiometry, lower-bound, upper-bound)
                                productn = (species.getId(), 1, i.split(" :lower-bound ")[1].split("\n")[0], 1000)
                                print productn
                                ProductsN.append(productn)
                            else:
                                productn = (species.getId(), 1, 0, 1000)
                                print productn
                                ProductsN.append(productn)
                        if (i.split("[CCO-CYTOSOL]")[0] == biocycid or i.split("[CCO-CYTOSOL]")[0].upper() == biocycid ) and species.getId().endswith("_c"):
                            print i
                            if " :upper-bound " in i and " :lower-bound " in i:
                                productn = (species.getId(), 1, i.split(" :lower-bound ")[1].split(" ")[0],i.split(" :upper-bound ")[1].split("\n")[0])
                                print productn
                                ProductsN.append(productn)
                            elif " :upper-bound " in i:
                                #productn = (speciesID, stoichiometry, lower-bound, upper-bound)
                                productn = (species.getId(), 1, 0,i.split(" :upper-bound ")[1].split("\n")[0])
                                print productn
                                ProductsN.append(productn)
                            elif " :lower-bound " in i:
                                #productn = (speciesID, stoichiometry, lower-bound, upper-bound)
                                productn = (species.getId(), 1, i.split(" :lower-bound ")[1].split("\n")[0], 1000)
                                print productn
                                ProductsN.append(productn)
                            else:
                                productn = (species.getId(), 1, 0, 1000)
                                print productn
                                ProductsN.append(productn)
        if c==1:
            # For every entry in the secretion area of the .fba file the species-id is determined.
            # The stoichiometry is 1. If informations for lower and/ or upper-bounds is available
            # it will be coinsidered, otherwise the lower-bound is 0 and the upper-bound is 1000.
            if i.startswith("#") or i=="\n":
                continue
            else:
                for species in sbml_Model.getListOfSpecies():
                    #print species
                    if "<p>BIOCYC: " in species.getNotesString():
                        biocycid = species.getNotesString().split("<p>BIOCYC: ")[1].split("</p>")[0]
                        if "|" in biocycid: 
                            biocycid = biocycid.replace("|","")
                        if (i.split("[CCO-EXTRACELLULAR]")[0] == biocycid or i.split("[CCO-EXTRACELLULAR]")[0].upper() == biocycid ) and species.getId().endswith("_e"):
                            print i
                            if " :upper-bound " in i and " :lower-bound " in i:
                                reactantn = (species.getId(), 1, i.split(" :lower-bound ")[1].split(" ")[0],i.split(" :upper-bound ")[1].split("\n")[0])
                                print reactantn
                                ReactantsS.append(reactantn)
                            elif " :upper-bound " in i:
                                #productn = (speciesID, stoichiometry, lower-bound, upper-bound)
                                reactantn = (species.getId(), 1, 0,i.split(" :upper-bound ")[1].split("\n")[0])
                                print reactantn
                                ReactantsS.append(reactantn)
                            elif " :lower-bound " in i:
                                #productn = (speciesID, stoichiometry, lower-bound, upper-bound)
                                reactantn = (species.getId(), 1, i.split(" :lower-bound ")[1].split("\n")[0], 1000)
                                print reactantn
                                ReactantsS.append(reactantn)
                            else:
                                reactantn = (species.getId(), 1, 0, 1000)
                                print reactantn
                                ReactantsS.append(reactantn)
                        if (i.split("[CCO-CYTOSOL]")[0] == biocycid or i.split("[CCO-CYTOSOL]")[0].upper() == biocycid ) and species.getId().endswith("_c"):
                            print i
                            if " :upper-bound " in i and " :lower-bound " in i:
                                reactantn = (species.getId(), 1, i.split(" :lower-bound ")[1].split(" ")[0],i.split(" :upper-bound ")[1].split("\n")[0])
                                print reactantn
                                ReactantsS.append(reactantn)
                            elif " :upper-bound " in i:
                                #productn = (speciesID, stoichiometry, lower-bound, upper-bound)
                                reactantn = (species.getId(), 1, 0,i.split(" :upper-bound ")[1].split("\n")[0])
                                print reactantn
                                ReactantsS.append(reactantn)
                            elif " :lower-bound " in i:
                                #productn = (speciesID, stoichiometry, lower-bound, upper-bound)
                                reactantn = (species.getId(), 1, i.split(" :lower-bound ")[1].split("\n")[0], 1000)
                                print reactantn
                                ReactantsS.append(reactantn)
                            else:
                                reactantn = (species.getId(), 1, 0, 1000)
                                print reactantn
                                ReactantsS.append(reactantn)
                            
    return Reactants, Products, ReactantsS, ProductsN


def createBiomassReaction(ListReactants, ListProducts):
	# The biomass reaction string will be created from the list of reactants and products
    s='<reaction id="RXN_Biomass" name="biomass" reversible="false">\n      <notes>\n        <body xmlns="http://www.w3.org/1999/xhtml">\n          <p>GENE_ASSOCIATION: </p>\n          <p>SUBSYSTEM: Other </p>\n          <p>Confidence Level: 1</p>\n        </body>\n      </notes>\n   <listOfReactants>\n'
	
    for reactant in ListReactants:
		s=s+'      <speciesReference species="'+reactant[0]+'" stoichiometry="'+reactant[1]+'"/>\n'
	
    s=s+'   </listOfReactants>\n   <listOfProducts>\n'
	
    for product in ListProducts:
		s=s+'      <speciesReference species="'+product[0]+'" stoichiometry="'+product[1]+'"/>\n'
    
    s=s+'   </listOfProducts>\n\t\t<kineticLaw>\n\t\t\t<math xmlns="http://www.w3.org/1998/Math/MathML">\n\t\t\t\t<ci> FLUX_VALUE </ci>\n\t\t\t</math>\n\t\t\t<listOfParameters>\n\t\t\t\t<parameter id="LOWER_BOUND" value="0" units="mmol_per_gDW_per_hr"/>\n\t\t\t\t<parameter id="UPPER_BOUND" value="1000" units="mmol_per_gDW_per_hr"/>\n\t\t\t\t<parameter id="OBJECTIVE_COEFFICIENT" value="1"/>\n\t\t\t\t<parameter id="FLUX_VALUE" value="0" units="mmol_per_gDW_per_hr"/>\n\t\t\t\t<parameter id="REDUCED_COST" value="0.000000"/>\n\t\t\t</listOfParameters>\n\t\t</kineticLaw>\n</reaction>\n'
    return s


def createNutrientReactions(ListProductsN):
    # All drain reactions for the nutrients will be created in one string from the list of Nutrients.
    n=""
    for nutrient in ListProductsN:
        n = n + '<reaction id="RXN_Nutrient_' + nutrient[0] + '" name="nutrient_' + nutrient[0] + '" reversible="false">\n      <notes>\n        <body xmlns="http://www.w3.org/1999/xhtml">\n          <p>GENE_ASSOCIATION: </p>\n          <p>SUBSYSTEM: Other </p>\n          <p>Confidence Level: 1</p>\n        </body>\n      </notes>\n   <listOfProducts>\n      <speciesReference species="' + nutrient[0] + '" stoichiometry="' + str(nutrient[1]) + '"/>\n   </listOfProducts>\n\t\t<kineticLaw>\n\t\t\t<math xmlns="http://www.w3.org/1998/Math/MathML">\n\t\t\t\t<ci> FLUX_VALUE </ci>\n\t\t\t</math>\n\t\t\t<listOfParameters>\n\t\t\t\t<parameter id="LOWER_BOUND" value="' + str(nutrient[2]) + '" units="mmol_per_gDW_per_hr"/>\n\t\t\t\t<parameter id="UPPER_BOUND" value="' + str(nutrient[3]) + '" units="mmol_per_gDW_per_hr"/>\n\t\t\t\t<parameter id="OBJECTIVE_COEFFICIENT" value="0"/>\n\t\t\t\t<parameter id="FLUX_VALUE" value="0" units="mmol_per_gDW_per_hr"/>\n\t\t\t\t<parameter id="REDUCED_COST" value="0.000000"/>\n\t\t\t</listOfParameters>\n\t\t</kineticLaw>\n</reaction>\n'
	
    return n
    
    
def createSecretionReactions(ListReactantsS):
    # All drain reactions for the secretions will be created in one string from the list of Nutrients.
    t=""
    for secretion in ListReactantsS:
        t = t + '<reaction id="RXN_Secretion_' + secretion[0] + '" name="secretion_' + secretion[0] + '" reversible="false">\n      <notes>\n        <body xmlns="http://www.w3.org/1999/xhtml">\n          <p>GENE_ASSOCIATION: </p>\n          <p>SUBSYSTEM: Other </p>\n          <p>Confidence Level: 1</p>\n        </body>\n      </notes>\n   <listOfReactants>\n      <speciesReference species="' + secretion[0] + '" stoichiometry="' + str(secretion[1]) + '"/>\n   </listOfReactants>\n\t\t<kineticLaw>\n\t\t\t<math xmlns="http://www.w3.org/1998/Math/MathML">\n\t\t\t\t<ci> FLUX_VALUE </ci>\n\t\t\t</math>\n\t\t\t<listOfParameters>\n\t\t\t\t<parameter id="LOWER_BOUND" value="' + str(secretion[2]) + '" units="mmol_per_gDW_per_hr"/>\n\t\t\t\t<parameter id="UPPER_BOUND" value="' + str(secretion[3]) + '" units="mmol_per_gDW_per_hr"/>\n\t\t\t\t<parameter id="OBJECTIVE_COEFFICIENT" value="0"/>\n\t\t\t\t<parameter id="FLUX_VALUE" value="0" units="mmol_per_gDW_per_hr"/>\n\t\t\t\t<parameter id="REDUCED_COST" value="0.000000"/>\n\t\t\t</listOfParameters>\n\t\t</kineticLaw>\n</reaction>\n'
	
    return t
    

ListReactants, ListProducts, ListReactantsS, ListProductsN = extractBiomassReactantsAndProducts(ptools_fba_template, sbml_Model)
BiomassRXNString = createBiomassReaction(ListReactants, ListProducts)
NutrientRXNsString = createNutrientReactions(ListProductsN)  
SecrtetionRXNsString = createSecretionReactions(ListReactantsS)

oldSBMl=open(sbml_path).readlines()
newSBML=""

# Adding the reaction strings to the SBML file
for i in oldSBMl:
	if i=="</listOfReactions>\n" or i=="</listOfReactions>\r\n":
		i = BiomassRXNString + NutrientRXNsString + SecrtetionRXNsString + "</listOfReactions>\n"
		newSBML=newSBML+i
	else:
		newSBML=newSBML+i

output = sys.argv[3]
data= open(str(output),"w")
data.write(newSBML)
data.close()