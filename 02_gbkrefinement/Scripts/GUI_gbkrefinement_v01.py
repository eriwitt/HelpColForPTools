#!/usr/bin/python
"""
   The script was developed to enrich the gene entries of your annotation (GenBank format)
   with EC numbers from the associated gene entries of the KEGG Database. If the found EC
   number in the associated KEGG entrie is not in the gene entrie of your annotation then the
   EC number is added. The script generates an Report file with the EC numbers which were
   added and the improved annotation in GenBank format.

   Author: Eric Witt
"""
from Bio import SeqIO
from tkinter import *
from tkinter import messagebox
import datetime
import os
import platform
import re
import ssl
import sys
import tkFileDialog
import tkSimpleDialog
import ttk
import urllib2
operating_system = platform.system()
if operating_system == "Windows":
    from os import startfile
else:
	import subprocess

time1=datetime.datetime.now()
#####################################################################################################
# Placeholder for file paths
gr_gbkfile=""
gr_report=""
gr_improved_gbk_path=""
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

#####################################################################################################
# GUI Main Window
main_window = Tk()
main_window.title("gbk_refinement")
# GUI Fixed window width and height, centered on the screen
window_width = 900
window_height = 450
window_pos_x = (main_window.winfo_screenwidth() /2) - (window_width / 2)
window_pos_y = (main_window.winfo_screenheight() /2) - (window_height / 2)
main_window.geometry('%dx%d+%d+%d' % (window_width, window_height, window_pos_x, window_pos_y))
main_window.resizable(0,0)
# GUI Program start information
main_frame = Frame(main_window)
main_frame.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
prog_label = Label(main_frame, text = "##########################################################################################################################\n\n gbk_refinement\n\n ###########################################################################################################################\n\nAuthor: Eric Witt\n\n###########################################################################################################################",  font="Arial 10 bold", relief = "groove", borderwidth = 4)
prog_label.pack(fill = X, padx = 5, pady = 10)
info_label = Label(main_frame, text = "The script was developed to add EC numbers to the annotation in GenBank format, which are stored in the KEGG database (Internet connection required!) for each gen. If EC numbers are found in the KEGG entry, they will be inserted in the annotation if they are not present. All added EC numbers will be listed in a report file and the modified annotation will be saved in GenBank format. The script only works if the organism exists in the KEGG database!", font="Arial 10 bold",  wraplength = 700, relief = "groove", borderwidth = 4)
info_label.pack(fill = X, padx = 5, pady = 10, ipadx = 10, ipady = 10)

def get_file_paths_and_start():
    main_frame.pack_forget()

    # GUI Generate Tabs
    noteb = ttk.Notebook(main_window)
    noteb.pack(fill=BOTH, expand = 1, padx = 5, pady = 5)
    noteb.pressed_index = None
    tab1 = Frame(noteb)
    tab1.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
    noteb.add(tab1, text = "Choose Files")

    # GUI Load your annotation
    def load_annotation():
		# Function for loading annotation file by user in the GUI. The selected file path is displayed in the GUI.
        gbkfile = str(tkFileDialog.askopenfilename(initialdir = os.getcwd, title = "Select the annotation to improve (.gbk)!", filetypes = (("GenBank files","*.gbk"),("all files","*.*file"))))
        load_your_annotation_label.config(text = gbkfile)
        select_report_button.config(state = "normal")

    
    load_your_annotation_framelabel = LabelFrame(tab1, text = "Load Your GenBank Annotation", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    load_your_annotation_framelabel.pack(fill = X, padx = 5, pady = 10)
    load_your_annotation_label = Label(load_your_annotation_framelabel, text = gr_gbkfile,  font = label_font, wraplength = label_wraplength) 
    load_your_annotation_label.pack(fill = X, padx = 5, pady = 5)
    load_your_annotation_button = Button(load_your_annotation_framelabel, text = "Load", command = load_annotation,  font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    load_your_annotation_button.pack(fill = X, padx = 5, pady = 5)

    # GUI Select report location
    def select_report():
		# Function to select and enter the report file name. The selected file path is displayed in the GUI.
        report = str(tkFileDialog.asksaveasfilename(initialdir = os.getcwd, title = "Select the path for the storage and enter the filename (*.txt) of the report!", filetypes = (("txt files","*.txt"),("all files","*.*"))))
        select_report_label.config(text = report)
        improved_gbk_path_button.config(state = "normal")


    select_report_framelabel = LabelFrame(tab1, text = "Select Location For Report File Storing", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    select_report_framelabel.pack(fill = X, padx = 5, pady = 10)
    select_report_label = Label(select_report_framelabel, text = gr_report, font = label_font, wraplength = label_wraplength) 
    select_report_label.pack(fill = X, padx = 5, pady = 5)
    select_report_button = Button(select_report_framelabel, text = "Select and enter name (.txt)!", state = DISABLED, command = select_report, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    select_report_button.pack(fill = X, padx = 5, pady = 5)

    # GUI Select improved annotation location
    def save_improved_annotation():
        # Select path to store the improved annotation. The selected directory path is displayed in the GUI.
        improved_gbk_path = str(tkFileDialog.asksaveasfilename(initialdir = os.getcwd, title = "Select the output file path of the improved annotation file and enter the file name (*.gbk)!", filetypes = (("GenBank files","*.gbk"),("all files","*.*"))))
        improved_gbk_path_label.config(text = improved_gbk_path)
        if improved_gbk_path_label["text"] == load_your_annotation_label["text"]:
            tkMessageBox.showerror("Error", "Your Input and Output is equal!")
        else:
            continue_button.config(state = "normal")
            

    
    improved_gbk_path_framelabel = LabelFrame(tab1, text = "Select Location For Improved Annotation Storing:",  relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    improved_gbk_path_framelabel.pack(fill = X, padx = 5, pady = 10)
    improved_gbk_path_label = Label(improved_gbk_path_framelabel, text = gr_improved_gbk_path, font = label_font, wraplength = label_wraplength)
    improved_gbk_path_label.pack(fill = X, padx = 5, pady = 5)
    improved_gbk_path_button = Button(improved_gbk_path_framelabel, text = "Select directory", state = DISABLED, command = save_improved_annotation, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    improved_gbk_path_button.pack(fill = X, padx = 5, pady = 5)
    
    
    def starting():
        # Disable "Choose Files" Buttons
        load_your_annotation_button.config(state = DISABLED)
        select_report_button.config(state = DISABLED)
        improved_gbk_path_button.config(state = DISABLED)
        continue_button.config(state = DISABLED)
        
        report = open(select_report_label["text"],"w")
        report.write("GBKREFINEMENT REPORT FILE\n"+str(datetime.datetime.now())+"\n")
        report.write("\nSelected annotation to improve:\n\t"+load_your_annotation_label["text"]+"\nLocation of the refined annotation:\n\t"+ improved_gbk_path_label["text"]+"\n")
        # GUI New Tab "General Informations"
        tab2 = Frame(noteb)
        tab2.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
        noteb.add(tab2, text = "KEGG Database Organism Identifier & Refinement")
        noteb.select(tab2)
        # GUI add objects for a scrollable tab
        mycanvas = Canvas(tab2)
        mycanvas.pack(side = "left", fill = BOTH, expand = 1)

        unacc_frame = Frame(mycanvas)
        unacc_frame.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
        mycanvas.create_window(0, 0, window = unacc_frame, anchor = "nw")

        # GUI Information Collection KEGG Organism Id
        get_kegg_orgid_framelabel = LabelFrame(unacc_frame, text = "Information Collection To Find The KEGG Organism Identifier", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
        get_kegg_orgid_framelabel.pack(fill = X, padx = 5, pady = 5)
        
        orgid_info_label = Label( get_kegg_orgid_framelabel, text = "The KEGG organism identifier is needed to find the gene entries of your organism in the KEGG database. The tool uses information from your annotation to find it. If you already know the KEGG organism identifier of your organism, you can enter it and confirm it, otherwise start the automatic search for finding the KEGG organism identifier.", font = label_font, wraplength = label_wraplength)
        orgid_info_label.pack(fill = X, padx = 5, pady = 5)
        org_id_entry_answer = Entry(get_kegg_orgid_framelabel)
        org_id_entry_answer.pack(side = "left", expand = 1, fill = X, padx = 5, pady = 5)
        org_id = ""
        
        def confirm_org_id():
            # Function checks Input from KEGG organism id Entry
            if org_id_entry_answer.get() is "":
                messagebox.showerror("Error", "Your input is empty!")
            else:
                confirm_orgid_button.config(state = DISABLED)
                org_id_entry_answer.config(state = DISABLED)
                start_orgid_finding_button.config(state = DISABLED)
                org_id = org_id_entry_answer.get()
                report.write("\nManual User Input for KEGG organism identifier:\n\t" + org_id + "\n")
                answer1 = messagebox.askyesno("Question","Do you want save the KEGG entries in html Format?")
                directory=""
                if answer1 == True:
                    directory=str(tkFileDialog.askdirectory())
                    start_gbk_refinement(org_id, directory, answer1)
                if answer1 == False:
                    start_gbk_refinement(org_id, directory, answer1)
                

        confirm_orgid_button = Button(get_kegg_orgid_framelabel, text ="Confirm & Start Refinement!", command = confirm_org_id , font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth )
        confirm_orgid_button.pack(side = "left",expand = 1, fill = X, padx = 5, pady = 5)
        
        orgid_info_label = Label( get_kegg_orgid_framelabel, text = "OR", font = "Arial 10 bold", wraplength = label_wraplength)
        orgid_info_label.pack(side = "left", expand = 1, fill = X, padx = 5, pady = 5)

        def start_orgid_finding():
            
            org_id_entry_answer.pack_forget()
            confirm_orgid_button.pack_forget()
            orgid_info_label.pack_forget()
            start_orgid_finding_button.pack_forget()
            
            auto_search_label = Label( get_kegg_orgid_framelabel, text = "Automatic Search:", font = "Arial 10 bold", wraplength = label_wraplength)
            auto_search_label.pack(fill = X, padx = 5, pady = 5)
            automatic_search_framelabel = LabelFrame(get_kegg_orgid_framelabel)
            automatic_search_framelabel.pack(fill = X, padx = 5, pady = 5)
            report.write("\nAutomatic Search of the KEGG organism identifier:\n\n")
            
            id_id = 0
            def get_KEGG_orgid(taxonomic_id, inti):
                # This function extracts from the organism KEGG entry the KEGG organism identifier. The taxonomic id is needed as an unique identifier for the organism. 
                kegg_url = "https://www.genome.jp/dbget-bin/www_bfind_sub?mode=bfind&max_hit=1000&dbkey=genome&keywords=" + taxonomic_id
                response = urllib2.urlopen(kegg_url)
                out =response.read()
                organism_url = "https://www.genome.jp/dbget-bin/www_bget?gn:" + out.split("/dbget-bin/www_bget?gn:")[1].split('">')[0]
                response = urllib2.urlopen(organism_url)
                out = response.read()
                
                org_id = out.split("<nobr>Name</nobr>")[1].split("<br>")[0].split("><")[-1].split('">')[1].split(",")[0]
                report.write("\tKEGG organism identifier:\t" + org_id + "\n")
                report.write("\tSource:\t" + organism_url + "\n")
                id_id = 1
                print org_id
                orgid_label = Label( automatic_search_framelabel, text = "KEGG organism identifier:\t" + org_id, font = label_font, wraplength = label_wraplength)
                orgid_label.grid(row = inti, column = 2, padx = 5, pady = 5)
                return id_id, org_id

            def get_KEGG_orgid_from_orgname(orgname, inti):
                # This function extracts from the organism KEGG entry the KEGG organism identifier. The organism KEGG entry is found by searching the organism name.
                name_array = orgname.split(" ")
                name_url_search_string = "https://www.genome.jp/dbget-bin/www_bfind_sub?mode=bfind&max_hit=1000&dbkey=genome&keywords="
                for i in range(len(name_array)):
                    if i == len(name_array) - 1:
                        name_url_search_string = name_url_search_string + name_array[i] 
                    else:
                        name_url_search_string = name_url_search_string + name_array[i] + "+"
                
                response = urllib2.urlopen(name_url_search_string)
                out =response.read()
                organism_url = "https://www.genome.jp/dbget-bin/www_bget?gn:" + out.split("/dbget-bin/www_bget?gn:")[1].split('">')[0]
                response = urllib2.urlopen(organism_url)
                out = response.read()
                org_id = out.split("<nobr>Name</nobr>")[1].split("<br>")[0].split("><")[-1].split('">')[1].split(",")[0]
                id_id = 1
                report.write("\tKEGG organism identifier:\t" + org_id + "\n")
                report.write("\tSource:\t" + organism_url + "\n")
                orgid_label = Label( automatic_search_framelabel, text = "KEGG organism identifier:\t" + org_id, font = label_font, wraplength = label_wraplength)
                orgid_label.grid(row = inti, column = 2, padx = 5, pady = 5)
                print org_id    
                return id_id, org_id

            gbk_file = SeqIO.parse(load_your_annotation_label["text"], "genbank")
            taxonomic_id=""
            featl = {} 
            for record in gbk_file:
                orgname = str(record).split("/source=")[1].split("\n")[0]
                if " str. " in orgname:
                   orgname = orgname.replace(" str. "," ")
                if " substr. " in orgname:
                   orgname = orgname.replace(" substr. "," ")
                for feature in record.features:
                    if feature.type not in featl:
                        featl[feature.type] = 1
                    elif feature.type in featl:
                        featl[feature.type] = featl[feature.type] + 1
        
            print featl
            gbk_file = SeqIO.parse(load_your_annotation_label["text"], "genbank")
            for record in gbk_file:
                no_tax = 0 # identifier no taxonomic id in source feature if it is 1
                no_bio = 0 # identifier no BioProject Accesion in record if it is 1
                if "source" in featl:
                    for feature in record.features:
                        # Check source qualifier in the annotation for the taxonomic id                                      
                        if feature.type == "source":
                            source_label = Label( automatic_search_framelabel, text = "Source feature:\tfound", font = label_font, wraplength = label_wraplength)
                            source_label.grid(row = 0, column = 0, padx = 5, pady = 5)
                            for entry in feature.qualifiers["db_xref"]:
                                if "taxon:" in entry:
                                    taxon_label = Label( automatic_search_framelabel, text = "taxonomic id:\t" + entry.split("taxon:")[1], font = label_font, wraplength = label_wraplength)
                                    taxon_label.grid(row = 0, column = 1, padx = 5, pady = 5)
                                    taxonomic_id = entry.split("taxon:")[1]
                                    report.write("\tSource Feature:\n\tTaxonomic ID: " + str(taxonomic_id) + "\t")
                                    anm = get_KEGG_orgid(taxonomic_id, 0)
                                    id_id = anm[0]
                                    org_id = anm[1]
                                else:
                                    taxon_label = Label( automatic_search_framelabel, text = "taxonomic id:\tnot found!", font = label_font, wraplength = label_wraplength)
                                    no_tax = 1
                                    taxon_label.grid(row = 0, column = 1, padx = 5, pady = 5)
                            break
                if "source" not in featl or no_tax == 1:
                    source_not_found_label = Label( automatic_search_framelabel, text = "Source feature:\t\tnot found in your annotation!", font = label_font, wraplength = label_wraplength)
                    source_not_found_label.grid(row = 0, column = 0, columnspan = 3,  padx = 5, pady = 5, sticky =W)
                        
                    # Extract taxonomic id from the bioproject ncbi entry. The bioproject accesion is extracted from the annotation.
                    if "BioProject:" in str(record):
                        bioproject_label = Label( automatic_search_framelabel, text = "BioProject Accesion:\t" + str(record).split("BioProject:")[1].split(",")[0], font = label_font, wraplength = label_wraplength)
                        bioproject_label.grid(row = 1, column = 0, padx = 5, pady = 5)
                        ncbi_bio_pro_url = "https://www.ncbi.nlm.nih.gov/bioproject/?term=" + str(record).split("BioProject:")[1].split(",")[0]
                        response = urllib2.urlopen(ncbi_bio_pro_url)
                        out = response.read()
                        if "No items found." in out:
                            bp_not_found_label = Label( automatic_search_framelabel, text = "BioProject Accession not found on NCBI" + taxonomic_id, font = label_font, wraplength = label_wraplength)
                            bp_not_found_label.grid(row = 1, column = 1,  padx = 5, pady = 5, sticky =W)
                        else:
                            taxonomic_id = out.split("[Taxonomy ID: ")[1].split("]")[0]
                            report.write("\tBioProject Accesion:\t" + str(record).split("BioProject:")[1].split(",")[0] + "\tTaxonomic ID: " + str(taxonomic_id) + "\n\tSource: " + ncbi_bio_pro_url + "\n")
                            taxon_label = Label( automatic_search_framelabel, text = "taxonomic id:\t" + taxonomic_id, font = label_font, wraplength = label_wraplength)
                            taxon_label.grid(row = 1, column = 1, padx = 5, pady = 5)
                            anm = get_KEGG_orgid(taxonomic_id, 1)
                            id_id = anm[0]
                            org_id = anm[1]
                            break
                    else:
                        bioproject_label = Label( automatic_search_framelabel, text = "BioProject Accesion:\tnot found in your annotation!", font = label_font, wraplength = label_wraplength)
                        no_bio = 1
                        bioproject_label.grid(row = 1, column = 0, columnspan = 3, padx = 5, pady = 5, sticky =W)
                            
                # Organism name search for KEGG organism identifier
                if orgname != "" and no_bio == 1:
                    name_search_label = Label( automatic_search_framelabel, text = "Organism:\t\t"+ orgname, font = label_font, wraplength = label_wraplength)
                    name_search_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky =W)
                    report.write("\tOrganism: " + orgname + "\n")
                    anm = get_KEGG_orgid_from_orgname(orgname, 2)
                    id_id = anm[0]
                    org_id = anm[1]
            if id_id == 0:
                orgid_not_found_label = Label( automatic_search_framelabel, text = "The automatic search could not find the KEGG organism identifier! You should do a manual search on KEGG! If your organism is not in KEGG then the tool does not work!", font = label_font, wraplength = label_wraplength)
                orgid_not_found_label.grid(row = 3, column = 0, columnspan = 3, padx = 5, pady = 5, sticky =W)
                report.write("The automatic search could not find the KEGG organism identifier! You should do a manual search on KEGG! If your organism is not in KEGG then the tool does not work!\n")

                def start_orgid_finding2():
                    auto_search_label.pack_forget()
                    automatic_search_framelabel.pack_forget()
                    starting()


                ok_button=Button(automatic_search_framelabel , text = "OK", command = start_orgid_finding2, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
                ok_button.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = W+E+N+S)
                quit_button = Button(automatic_search_framelabel, text = "Quit", command = close_program, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
                quit_button.grid(row = 4, column = 1, columnspan =2, padx = 5, pady = 5, sticky = W+E+N+S)
           
            else:
               orgid_found_label = Label( get_kegg_orgid_framelabel, text = "The KEGG organism identifier "+ org_id + " was found for your organism " + orgname + "!", font = label_font, wraplength = label_wraplength)
               orgid_found_label.pack(expand = 1, fill = X, padx = 5, pady = 5)
                                
               def start_ref():
                   start_refinement_button.config(state = DISABLED)
                   answer1 = messagebox.askyesno("Question","Do you want save the KEGG entries in html Format?")
                   directory=""
                   if answer1 == True:
                       directory=str(tkFileDialog.askdirectory())
                       start_gbk_refinement(org_id, directory, answer1)
                   if answer1 == False:
                       start_gbk_refinement(org_id, directory, answer1)
               start_refinement_button = Button(get_kegg_orgid_framelabel, text ="Start Refinement!", command = start_ref, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth )
               start_refinement_button.pack(expand = 1, fill = X, padx = 5, pady = 5)


        start_orgid_finding_button = Button(get_kegg_orgid_framelabel, text ="Automatic Search", command = start_orgid_finding, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth )
        start_orgid_finding_button.pack(side = "left", expand = 1, fill = X, padx = 5, pady = 5)


        def start_gbk_refinement(org_id,directory,answer1):
            gbk_file = SeqIO.parse(load_your_annotation_label["text"],"genbank")
            
            def get_gene_records():
                
                def search_ec_in_kegg(org_id, genename, answer1, directory):
                    """
					The genename is used for query at KEGG ("https://www.kegg.jp/")
					With the genename and the query-url we get the entry of this Gene.
					In this entry the function is looking for associated EC-Numbers.
					Returns a list of found EC-Numbers.
					The Funktion only works if the organism is in the KEGG-Database.
					"""
                    res= []
                    url="https://www.kegg.jp/dbget-bin/www_bget?"+org_id+":"+genename
                    print url
                    try:
                        res1=""
                        response = urllib2.urlopen(url)
                        out =response.read()
                        res1=re.findall("[0-9]{1}[.][0-9]{1,4}[.][0-9]{1,4}[.][0-9]{1,4}",out) # search for ec-number
                        print res1
                        if res1!=[]:
                            if answer1 == True:
                                if operating_system == "Windows":
                                    fileipid=open(directory+"\\"+genename+".html","w")
                                else:
                                    fileipid=open(directory+"/"+genename+".html","w")

                                fileipid.write(url + "\t" + str(datetime.datetime.now())+"\n")
                                fileipid.write(out)
                            if answer1 == False:
                                pass
                            for t in res1:
                                if t not in res:
                                    res.append(t)
                        return res
                    except urllib2.URLError:
                        ssl._create_default_https_context = ssl._create_unverified_context
                        search_ec_in_kegg(genename)
                
                a=0
                for record in gbk_file:
                    total_locus_tag_nr=0
                    ecs_before_refinement=[]
                    additional_ecs_after_refinement=[]
                    for feature in record.features:
                        if feature.type == "CDS":
                            if "locus_tag" in feature.qualifiers:
                                total_locus_tag_nr=total_locus_tag_nr+1
                            if "EC_number" in feature.qualifiers:
                                for ecnr in feature.qualifiers["EC_number"]:
                                    if ecnr not in ecs_before_refinement:
                                        ecs_before_refinement.append(ecnr)
                    print len(ecs_before_refinement)
                    report.write("\nThese ec numbers were already present in the annotation before refinement (delimited by TAB):\n")
                    for ecnumber in sorted(ecs_before_refinement):
                        report.write(ecnumber+"\t")
                    report.write("\n\nThe following changes were made in the annotation.\n 'add' - means the EC number was added to an existing EC qualifier\n 'new EC qualifier' - means there was no ec qualifier before, so an EC qualifier with the found EC number was added to the annotation\n\nlocus_tag\tchanges\n\n")
                    current_locus_tag_nr=0
                    for feature in record.features:
                        if feature.type == "gene":
                            a=0
                        if feature.type == "CDS":
                            a=1
                        if a==1:
                            if "locus_tag" in feature.qualifiers:
                                current_locus_tag_nr=current_locus_tag_nr+1
                                progress_nr= (100/float(total_locus_tag_nr))*current_locus_tag_nr
                                progress_label.config(text ="Gene "+str(feature.qualifiers["locus_tag"]).split("['")[1].split("']")[0] + " ("+str(current_locus_tag_nr) +" of "+ str(total_locus_tag_nr)+ " genes!) is checked!")
                                progbar["value"]=progress_nr
                                window1.update()
                                ec=search_ec_in_kegg(org_id, str(feature.qualifiers["locus_tag"]).split("['")[1].split("']")[0], answer1, directory)
                                if ec != []:
                                    if "EC_number" in feature.qualifiers:
                                        for i in ec:
                                            if i not in feature.qualifiers["EC_number"]:
                                                feature.qualifiers["EC_number"].append(i)
                                                report.write( str(feature.qualifiers["locus_tag"]).split("['")[1].split("']")[0] + "\t"+"add ec\t"+i+"\n")
                                                if i not in ecs_before_refinement and i not in additional_ecs_after_refinement:
                                                    additional_ecs_after_refinement.append(i)
                                    else:
                                        feature.qualifiers["EC_number"]=ec
                                        report.write(str(feature.qualifiers["locus_tag"]).split("['")[1].split("']")[0] + "\t"+ "new EC qualifier\t" +str(feature.qualifiers["EC_number"])+"\n")
                                        for ecnum in ec:
                                            if ecnum not in ecs_before_refinement and ecnum not in additional_ecs_after_refinement:
                                                additional_ecs_after_refinement.append(ecnum)
                    report.write("\nThese ec numbers have been added to the annotation by refinement (delimited by TAB):\n")
                    for ecnumb in sorted(additional_ecs_after_refinement):
                        report.write(ecnumb+"\t")
                    report.close()
                window1.quit()
                window1.destroy()
                SeqIO.write(record,improved_gbk_path_label["text"],"genbank")
                def open_report():
                    if operating_system == "Windows":
                        startfile(select_report_label["text"])
                    else:
                        subprocess.call(['xdg-open',select_report_label["text"]])
                

                refinment_completed_label = LabelFrame(unacc_frame ,text ='Refinement Completed!', relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
                refinment_completed_label.pack(fill = X, padx=5, pady=5)
                Information_label=Label(refinment_completed_label, text= "Total EC numbers contained in the annotation before refinement:\n"+str(len(ecs_before_refinement))+"\nNumber of ec numbers added by the refinement (These are listed in the report file!):\n"+str(len(additional_ecs_after_refinement)),font = label_font, wraplength = label_wraplength)
                Information_label.pack(fill = X, padx=5, pady=5)
                open_report_button = Button(refinment_completed_label, text="Open report file!", command=open_report,font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
                open_report_button.pack(side = LEFT, expand = 1, fill = X, padx=5, pady=5)

                def open_imp_anno():
                    if operating_system == "Windows":
                        startfile(improved_gbk_path_label["text"])
                    else:
                        subprocess.call(['xdg-open', improved_gbk_path_label["text"]])


                open_imp_anno_button = Button(refinment_completed_label, text="Open improved annotation!", command=open_imp_anno,font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
                open_imp_anno_button.pack(side = LEFT, expand = 1, fill = X, padx=5, pady=5)

                quit_button = Button(refinment_completed_label, text = "Quit", command = close_program, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
                quit_button.pack(side = LEFT, expand = 1, fill = X, padx=5, pady=5)
                
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


                time2=datetime.datetime.now()
                print str(time2 - time1)
            
            window1=Tk()
            window1.title("Progress!")
            # GUI Fixed window width and height, centered on the screen
            prog_window_width = 300
            prog_window_height = 50
            prog_window_pos_x = (window1.winfo_screenwidth() /2) - (prog_window_width / 2)
            prog_window_pos_y = (window1.winfo_screenheight() /2) - (prog_window_height / 2)
            window1.geometry('%dx%d+%d+%d' % (prog_window_width, prog_window_height, prog_window_pos_x, prog_window_pos_y))
            window1.resizable(0,0)
            progress_nr=0
            progress_label=Label(window1,text ='Refinement starts!')
            progbar=ttk.Progressbar(window1, orient="horizontal", length=300, mode="determinate",maximum=100, value=progress_nr)
            progress_label.pack()
            progbar.pack()
            get_gene_records()
            window1.mainloop()
    
    
    continue_button = Button(tab1, text = "Continue", state = DISABLED, command = starting, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    continue_button.pack(fill = BOTH, expand = 1, padx = 5, pady = 10)


start_button = Button(main_frame, text = "Start", command = get_file_paths_and_start, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
start_button.pack(side = LEFT, expand = 1, fill = BOTH, padx =  5, pady = 10)

def close_program():
    main_window.destroy()


quit_button=Button(main_frame, text = "Quit", command = close_program, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
quit_button.pack(side = RIGHT, expand = 1, fill = BOTH, padx =  5, pady = 10)
   
main_window.mainloop()