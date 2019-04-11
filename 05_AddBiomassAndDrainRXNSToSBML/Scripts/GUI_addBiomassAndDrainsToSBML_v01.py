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
from libsbml import *
from Tkinter import *
import tkFileDialog
import sys
import os
import platform
import ttk
operating_system = platform.system()
if operating_system == "Windows":
    from os import startfile
    sys.path.append("C:\Python27\Lib\site-packages\libsbml")
    from libsbml import *
else:
    import subprocess
    sys.path.append("/usr/local/lib/python2.7/dist-packages/libsbml")
    from libsbml import *
#####################################################################################################
# Placeholder for file paths
sbmlfile=""
fbafile=""
new_sbml=""
#####################################################################################################
# GUI myButtonSettings
button_font = "Arial 10 bold"
button_borderwidth = 4
button_bg = "light grey"
button_cursor = "hand2"
button_overrelief = "sunken"

# GUI myLabelSettings
label_font = "Arial 10"
label_wraplength = 800

# GUI myFrameLabelSettings
framelabel_font = "Arial 10 bold"
framelabel_borderwidth = 4 
framelabel_relief = "groove"


# GUI Main Window
main_window = Tk()
main_window.title("01_biopython_parser")
# GUI Fixed window width and height, centered on the screen
window_width = 900
window_height = 450
print main_window.winfo_screenwidth()
print main_window.winfo_screenheight()
window_pos_x = (main_window.winfo_screenwidth() /2) - (window_width / 2)
window_pos_y = (main_window.winfo_screenheight() /2) - (window_height / 2)
main_window.geometry('%dx%d+%d+%d' % (window_width, window_height, window_pos_x, window_pos_y))
main_window.resizable(0,0)

# GUI Program start information
main_frame = Frame(main_window)
main_frame.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
prog_label = Label(main_frame, text = "##########################################################################################################################\n\n addBiomassAndDrainsToSBML\n\n ###########################################################################################################################\n\nAuthor: Eric Witt\n\n###########################################################################################################################",  font="Arial 10 bold", relief = "groove", borderwidth = 4)
prog_label.pack(fill = X, padx = 5, pady = 10)

info_label = Label(main_frame, text = "This script adds to the SBML model of your organism exported from Pathway Tools the biomass reaction as well as the drain reactions for nutrients and secretions contained in the .fba file for the MetaFlux FBA simulation.", font="Arial 10 bold",  wraplength = 700, relief = "groove", borderwidth = 4)
info_label.pack(fill = X, padx = 5, pady = 10, ipadx = 10, ipady = 10)

def choose_files():
    main_frame.pack_forget()
   
    # GUI Generate Tabs
    noteb = ttk.Notebook(main_window)
    noteb.pack(fill=BOTH, expand = 1, padx = 5, pady = 5)
    noteb.pressed_index = None
    tab1 = Frame(noteb)
    tab1.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
    noteb.add(tab1, text = "Choose Files")
    
    # GUI Load your SBML
    def load_sbml():
		# Function for loading SBML file by user in the GUI. The selected file path is displayed in the GUI.
        sbmlfile = str(tkFileDialog.askopenfilename(initialdir = os.getcwd, title = "Select SBML file (.xml)!", filetypes = (("SBML files","*.xml"),("all files","*.*file"))))
        load_your_sbml_label.config(text = sbmlfile)
        load_fbafile_button.config(state = "normal")

    
    load_your_sbml_framelabel = LabelFrame(tab1, text = "Load Your SBML File", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    load_your_sbml_framelabel.pack(fill = X, padx = 5, pady = 5)
    load_your_sbml_label = Label(load_your_sbml_framelabel, text = sbmlfile,  font = label_font, wraplength = label_wraplength) 
    load_your_sbml_label.pack(fill = X, padx = 5, pady = 5)
    load_your_sbml_button = Button(load_your_sbml_framelabel, text = "Load", command = load_sbml,  font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    load_your_sbml_button.pack(fill = X, padx = 5, pady = 5)
    
    # GUI load .fba file
    def load_fbafile():
		# Function to load the .fba file. The selected file path is displayed in the GUI.
        fbafile = str(tkFileDialog.askopenfilename(initialdir = os.getcwd, title = "Select the .fba file (.fba)!", filetypes = ((".fba files","*.fba"),("all files","*.*"))))
        load_fbafile_label.config(text = fbafile)
        save_SBML_button.config(state = "normal")


    load_fbafile_framelabel = LabelFrame(tab1, text = "Load Your .fba File", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    load_fbafile_framelabel.pack(fill = X, padx = 5, pady = 5)
    load_fbafile_label = Label(load_fbafile_framelabel, text = fbafile, font = label_font, wraplength = label_wraplength) 
    load_fbafile_label.pack(fill = X, padx = 5, pady = 5)
    load_fbafile_button = Button(load_fbafile_framelabel, text = "Load", state = DISABLED, command = load_fbafile, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    load_fbafile_button.pack(fill = X, padx = 5, pady = 5)
    
    # GUI Select SBML file location for storinbg the new file
    def save_SBML():
        # Select path to store the improved annotation. The selected directory path is displayed in the GUI.
        new_sbml = str(tkFileDialog.asksaveasfilename(initialdir = os.getcwd, title = "Select the output file path of the new SBML file and enter the file name (*.xml)!", filetypes = (("SBML files","*.xml"),("all files","*.*"))))
        save_SBML_label.config(text = new_sbml)
        if save_SBML_label["text"] == load_your_sbml_label["text"]:
            tkMessageBox.showerror("Error", "Your Input and Output is equal!")
        else:
            start_adding_button.config(state = "normal")
            

    save_SBML_framelabel = LabelFrame(tab1, text = "Select Location For Storing The New SBML:",  relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    save_SBML_framelabel.pack(fill = X, padx = 5, pady = 5)
    save_SBML_label = Label(save_SBML_framelabel, text = new_sbml, font = label_font, wraplength = label_wraplength)
    save_SBML_label.pack(fill = X, padx = 5, pady = 5)
    save_SBML_button = Button(save_SBML_framelabel, text = "Select Location", state = DISABLED, command = save_SBML, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    save_SBML_button.pack(fill = X, padx = 5, pady = 5)
    
    def start_adding():
        # Disable "Choose Files" Buttons
        load_your_sbml_button.config(state = DISABLED)
        load_fbafile_button.config(state = DISABLED)
        save_SBML_button.config(state = DISABLED)
        start_adding_button.config(state = DISABLED)
        
        # GUI New Tab "General Informations"
        tab2 = Frame(noteb)
        tab2.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
        noteb.add(tab2, text = "Results")
        noteb.select(tab2)
        # GUI add objects for a scrollable tab
        mycanvas = Canvas(tab2)
        mycanvas.pack(side = "left", fill = BOTH, expand = 1)

        unacc_frame = Frame(mycanvas)
        unacc_frame.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
        mycanvas.create_window(0, 0, window = unacc_frame, anchor = "nw")
        
        # GUI Unaccepted features
        result_framelabel = LabelFrame(unacc_frame, text = "Added Reactions in the SBML file:", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
        result_framelabel.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
        
        read = SBMLReader()
        sbml_SBML=read.readSBML(load_your_sbml_label["text"])
        sbml_Model=sbml_SBML.getModel()

        ptools_fba_template = open(load_fbafile_label["text"]).readlines()
        
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

        oldSBMl=open(load_your_sbml_label["text"]).readlines()
        newSBML=""
        # Adding the reaction strings to the SBML file
        for i in oldSBMl:
            if i=="</listOfReactions>\n" or i=="</listOfReactions>\r\n" :
                i = BiomassRXNString + NutrientRXNsString + SecrtetionRXNsString + "</listOfReactions>\n"
                newSBML=newSBML+i
            else:
                newSBML=newSBML+i

        
        data= open(save_SBML_label["text"],"w")
        data.write(newSBML)
        data.close()

        result_label = Label(result_framelabel, text = BiomassRXNString + NutrientRXNsString + SecrtetionRXNsString, font = label_font, wraplength = label_wraplength,  justify = LEFT)
        result_label.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
        
        def open_SBML():
            if operating_system == "Windows":
				startfile(save_SBML_label["text"])
            else:
				subprocess.call(['xdg-open', save_SBML_label["text"]])
                    

        open_sbml_button = Button(result_framelabel, text = "Open New SBML File", command = open_SBML, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
        open_sbml_button.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
        
        quit_button2 = Button(result_framelabel, text = "Quit!",command = close_program, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
        quit_button2.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
        
        # If the content of the unacc_frame is to big for the window, than add a scrollbar
        mycanvas.update()
        main_window.update()
        if unacc_frame.winfo_height() > (main_window.winfo_height()-50):
            myscrollbar = Scrollbar(tab2, command = mycanvas.yview)
            mycanvas.config(yscrollcommand = myscrollbar.set, scrollregion = mycanvas.bbox("all"))
            myscrollbar.pack(side=RIGHT, fill=Y)
                
            def mousewheel(event):
                if operating_system == "Windows":
					mycanvas.yview_scroll(int(-1*(event.delta/120)), "units")
                elif operating_system == "Linux":
                    if event.num == 4:
                        mycanvas.yview_scroll(-1, "units")
                    if event.num == 5:
	                    mycanvas.yview_scroll(1, "units")
                elif operating_system == "Darwin":
					mycanvas.yview_scroll((event.delta/120), "units")


            if operating_system == "Linux":
                mycanvas.bind_all("<Button-4>", mousewheel)
                mycanvas.bind_all("<Button-5>", mousewheel)
            else:	
                mycanvas.bind_all("<MouseWheel>", mousewheel)
                    
                    
    start_adding_button = Button(tab1, text = "Start Reaction Adding!", state = DISABLED, command = start_adding, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    start_adding_button.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)

start_button = Button(main_frame, text = "Start", command = choose_files, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
start_button.pack(side = LEFT, expand = 1, fill = BOTH, padx =  5, pady = 10)

def close_program():
    main_window.destroy()


quit_button=Button(main_frame, text = "Quit", command = close_program, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
quit_button.pack(side = RIGHT, expand = 1, fill = BOTH, padx =  5, pady = 10)
   
main_window.mainloop()
