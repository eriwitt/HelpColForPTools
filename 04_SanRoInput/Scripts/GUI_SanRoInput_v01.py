#!/usr/bin/python
"""
   This script was written for creating the necessary FASTA input files for the Tool from Santos & Rocha (2016)
   to estimate the coefficients of amino acids, dNTPs and NTPs for the biomass composition.
   
   Santos, S., Rocha, I., Estimation of biomass composition from genomic and transcriptomic information. 
   Journal of integrative bioinformatics 13 (2), 2016 https://doi.org/10.2390/biecoll-jib-2016-285

   Application can be downloaded from http://darwin.di.uminho.pt/biomass/files/Application.jar

   The input GenBank annotation must contain the genome sequence!
   
   Author: Eric Witt
"""

from Bio import SeqIO
from tkinter import *
import tkFileDialog
import os
import platform
import ttk
import webbrowser
operating_system = platform.system()
if operating_system == "Windows":
    from os import startfile
else:
	import subprocess

#####################################################################################################
# Placeholder for file paths
anno_file_name = ""
output_location = ""
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
main_window.title("SanRoInput")
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

prog_label = Label(main_frame, text = "##########################################################################################################################\n\n SanRoInput\n\n ###########################################################################################################################\n\nAuthor: Eric Witt\n\n###########################################################################################################################",  font="Arial 10 bold", relief = "groove", borderwidth = 4)
prog_label.pack(fill = X, padx = 5, pady = 5)
info_label = Label(main_frame, text = "This script was written for creating the necessary FASTA input files for the Tool from Santos & Rocha (2016) to estimate the coefficients of amino acids, dNTPs and NTPs for the biomass composition.", font="Arial 10 bold",  wraplength = 700, relief = "groove", borderwidth = 4)
info_label.pack(fill = X, padx = 5, pady = 5, ipadx = 5, ipady = 5)

def hyperlink(event):
	webbrowser.open_new(event.widget.cget("text"))


publication_framelabel = LabelFrame(main_frame, text="Reference", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
publication_framelabel.pack(fill = X, padx = 5, pady = 5)
publication_label = Label(publication_framelabel, text = "Santos, S., Rocha, I., Estimation of biomass composition from genomic and transcriptomic information. Journal of integrative bioinformatics 13 (2), 2016", font = "Arial 10 bold",  wraplength = 700)
publication_label.pack(fill = X, padx = 5, pady = 5)
doi_label = Label(publication_framelabel, text="https://doi.org/10.2390/biecoll-jib-2016-285", fg="blue", font="Arial 8 bold underline", cursor = button_cursor)
doi_label.pack(fill = X, padx = 5, pady = 5)
doi_label.bind("<Button-1>", hyperlink)

application_framelabel = LabelFrame(main_frame, text="Application download", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
application_framelabel.pack(fill = X, padx = 5, pady = 5)
application_label = Label(application_framelabel, text="http://darwin.di.uminho.pt/biomass/files/Application.jar", fg="blue", font="Arial 8 bold underline", cursor = button_cursor, width=80, wraplength=500)
application_label.pack(fill = X, padx = 5, pady = 5)
application_label.bind("<Button-1>", hyperlink)

def start_process():
    main_frame.pack_forget()
    
    # GUI Generate Tabs
    noteb = ttk.Notebook(main_window)
    noteb.pack(fill=BOTH, expand = 1, padx = 5, pady = 5)
    noteb.pressed_index = None
    tab1 = Frame(noteb)
    tab1.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
    noteb.add(tab1, text = "Choose Files")
    
    # GUI Process description
    process_framelabel = LabelFrame(tab1, text = "Process description", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    process_framelabel.pack(fill = X, padx = 5, pady = 10)
    process_label = Label(process_framelabel, text="The required FASTA files are derived from the annotation in GenBank format (.gbk). The annotation and the directory for the storage of the FASTA files must be selected!",  font = label_font, wraplength = label_wraplength)
    process_label.pack(fill = X, padx = 5, pady = 5)

    # GUI Load your annotation
    def load_annotation():
		# Function for loading annotation file by user in the GUI. The selected file path is displayed in the GUI.
        anno_file_name = str(tkFileDialog.askopenfilename(initialdir = os.getcwd, title = "Select the annotation to improve (.gbk)!", filetypes = (("GenBank files","*.gbk"),("all files","*.*file"))))
        load_your_annotation_label.config(text = anno_file_name)
        select_output_location_button.config(state = "normal")

    
    load_your_annotation_framelabel = LabelFrame(tab1, text = "Load Your GenBank Annotation", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    load_your_annotation_framelabel.pack(fill = X, padx = 5, pady = 10)
    load_anno_label = Label(load_your_annotation_framelabel, text="For creating the DNA sequence FASTA file it is required that the sequence is contained in the annotation file!!!", font="Arial 8 bold", wraplength = label_wraplength)
    load_anno_label.pack(fill = X, padx = 5, pady = 5)
    load_your_annotation_label = Label(load_your_annotation_framelabel, text = anno_file_name,  font = label_font, wraplength = label_wraplength) 
    load_your_annotation_label.pack(fill = X, padx = 5, pady = 5)
    load_your_annotation_button = Button(load_your_annotation_framelabel, text = "Load", command = load_annotation,  font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    load_your_annotation_button.pack(fill = X, padx = 5, pady = 5)

    # GUI Output file location
    def select_output_location():
		# Function to select and enter the report file name. The selected file path is displayed in the GUI.
        output_location = str(tkFileDialog.askdirectory())
        select_output_location_label.config(text = output_location)
        create_fasta_files_button.config(state = "normal")


    select_output_location_framelabel = LabelFrame(tab1, text = "Select Output Location", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    select_output_location_framelabel.pack(fill = X, padx = 5, pady = 10)
    select_output_location_label = Label(select_output_location_framelabel, text = output_location, font = label_font, wraplength = label_wraplength) 
    select_output_location_label.pack(fill = X, padx = 5, pady = 5)
    select_output_location_button = Button(select_output_location_framelabel, text = "Select!", state = DISABLED, command = select_output_location, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    select_output_location_button.pack(fill = X, padx = 5, pady = 5)

    def create_fasta_files():
        create_fasta_files_button.config(state = DISABLED)
        load_your_annotation_button.config(state = DISABLED)
        select_output_location_button.config(state = DISABLED)

        report = open(select_output_location_label["text"]+"/error_report.txt","w")
        
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
        #Creation of the protein FASTA file 
        gbk_file = SeqIO.parse(load_your_annotation_label["text"],"genbank")
        prot_fasta_file= open(select_output_location_label["text"]+"/"+load_your_annotation_label["text"].split("/")[-1].split(".gbk")[0]+"_protein_FASTA.faa","w")
        for record in gbk_file:
            for feature in record.features:
                if feature.type == "CDS":
                    if "translation" in feature.qualifiers:
                        prot_fasta_file.write(">"+feature.qualifiers["locus_tag"][0]+" "+str(feature.location)+"\n")
                        prot_fasta_file.write(feature.qualifiers["translation"][0]+"\n")
                    else:
                        report.write(">"+feature.qualifiers["locus_tag"][0]+" "+str(feature.location)+"\n")
                        report.write("MISSING TRANSLATION QUALIFIER\n")

        prot_fasta_file.close()

#Creation of the DNA FASTA file 
        gbk_file = SeqIO.parse(load_your_annotation_label["text"],"genbank")
        dna_fasta_file = open(select_output_location_label["text"]+"/"+load_your_annotation_label["text"].split("/")[-1].split(".gbk")[0]+"_DNA_FASTA.faa","w")
        seq=""
        for record in gbk_file:
            seq=str(record.seq)
            dna_fasta_file.write(">"+record.id+" "+record.description+"\n")
            dna_fasta_file.write(str(record.seq))
        
        dna_fasta_file.close()

#Creation of RNA FASTA files

        def rev_comp (seq):
            # This function generates the complementary sequence from the input sequence. The complementary sequence TAACCTTT is output to the input sequence AAAGGTTA.
            s=""
            for i in seq:
                if i =="A":
                    s=s+"T"
                    continue
                if i =="G":
                    s=s+"C"
                    continue
                if i =="T":
                    s=s+"A"
                    continue
                if i =="C":
                    s=s+"G"
                    continue
            s=s[::-1]
            return s
        
        def create_rna_fasta(pfad, type):
            gbk_file = SeqIO.parse(load_your_annotation_label["text"],"genbank")
            RNA_fasta = open(pfad,"w")
            for record in gbk_file:
                for feature in record.features:
                    if feature.type==type:
                        RNA_fasta.write(">"+str(feature.type)+"\t"+feature.qualifiers["locus_tag"][0]+"\t"+str(feature.location)+"\n")
                        if "(-)" in str(feature.location):
                            RNA_fasta.write(rev_comp(seq[int(str(feature.location).split("[")[1].split(":")[0]):int(str(feature.location).split(":")[1].split("]")[0])])+"\n")
                        else:
                            RNA_fasta.write(seq[int(str(feature.location).split("[")[1].split(":")[0]):int(str(feature.location).split(":")[1].split("]")[0])]+"\n")
            RNA_fasta.close()

        create_rna_fasta(select_output_location_label["text"]+"/"+load_your_annotation_label["text"].split("/")[-1].split(".gbk")[0]+"_tRNA_FASTA.faa","tRNA")
        create_rna_fasta(select_output_location_label["text"]+"/"+load_your_annotation_label["text"].split("/")[-1].split(".gbk")[0]+"_rRNA_FASTA.faa","rRNA")
        create_rna_fasta(select_output_location_label["text"]+"/"+load_your_annotation_label["text"].split("/")[-1].split(".gbk")[0]+"_mRNA_FASTA.faa","CDS")
    

        protein_framelabel = LabelFrame(unacc_frame, text="Protein FASTA file was created:",  relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
        protein_framelabel.pack(expand = 1, fill = X, padx = 5, pady = 5)
        protein_fasta_file_label = Label(protein_framelabel, text = select_output_location_label["text"]+"/"+load_your_annotation_label["text"].split("/")[-1].split(".gbk")[0]+"_protein_FASTA.faa" , font = label_font, wraplength = label_wraplength)
        protein_fasta_file_label.pack(fill = X, padx = 5, pady = 5)
        
        def open_protein():
            if operating_system == "Windows":
                startfile(protein_fasta_file_label["text"])
            else:
                subprocess.call(['xdg-open', protein_fasta_file_label["text"]])

        protein_fasta_open_button = Button(protein_framelabel,text="Open Protein FASTA!", command = open_protein, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth, width = 103)
        protein_fasta_open_button.pack(fill = X, padx = 5, pady = 5)

        dna_framelabel = LabelFrame(unacc_frame, text="DNA FASTA file was created:",  relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
        dna_framelabel.pack(fill = X, padx = 5, pady = 5)
        dna_fasta_file_label = Label(dna_framelabel, text=select_output_location_label["text"]+"/"+load_your_annotation_label["text"].split("/")[-1].split(".gbk")[0]+"_DNA_FASTA.faa", font = label_font, wraplength = label_wraplength)
        dna_fasta_file_label.pack(fill = X, padx = 5, pady = 5)
        
        def open_dna():
            if operating_system == "Windows":
                startfile(dna_fasta_file_label["text"])
            else:
                subprocess.call(['xdg-open', dna_fasta_file_label["text"]])		


        dna_fasta_open_button = Button(dna_framelabel, text="Open DNA FASTA!", command = open_dna, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth, width = 103)
        dna_fasta_open_button.pack(fill = X, padx = 5, pady = 5)

        rna_framelabel = LabelFrame(unacc_frame, text = "RNA FASTA files were created:", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
        rna_framelabel.pack(fill = X, padx = 5, pady = 5)
        mrna_fasta_file_label = Label(rna_framelabel, text = select_output_location_label["text"]+"/"+load_your_annotation_label["text"].split("/")[-1].split(".gbk")[0]+"_mRNA_FASTA.faa", font = label_font, wraplength = label_wraplength)
        mrna_fasta_file_label.pack(fill = X, padx = 5, pady = 5)
        report.close()
        
        def open_mrna():
            if operating_system == "Windows":
                startfile(mrna_fasta_file_label["text"])
            else:
                subprocess.call(['xdg-open', mrna_fasta_file_label["text"]])	
        

        mrna_fasta_open_button = Button(rna_framelabel,text="Open mRNA FASTA!", command=open_mrna, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth, width = 103)
        mrna_fasta_open_button.pack(fill = X, padx = 5, pady = 5)
        	
        rrna_fasta_file_label=Label(rna_framelabel, text=select_output_location_label["text"]+"/"+load_your_annotation_label["text"].split("/")[-1].split(".gbk")[0]+"_rRNA_FASTA.faa", font = label_font, wraplength = label_wraplength)
        rrna_fasta_file_label.pack(fill = X, padx = 5, pady = 5)
        	
        def open_rrna():
            if operating_system == "Windows":
                startfile(rrna_fasta_file_label["text"])
            else:
                subprocess.call(['xdg-open', rrna_fasta_file_label["text"]])			


        rrna_fasta_open_button = Button(rna_framelabel,text="Open rRNA FASTA!", command=open_rrna, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth, width = 103)
        rrna_fasta_open_button.pack(fill = X, padx = 5, pady = 5)
        	
        trna_fasta_file_label = Label(rna_framelabel, text=select_output_location_label["text"]+"/"+load_your_annotation_label["text"].split("/")[-1].split(".gbk")[0]+"_tRNA_FASTA.faa", font = label_font, wraplength = label_wraplength)
        trna_fasta_file_label.pack(fill = X, padx = 5, pady = 5)
        
        def open_trna():
            if operating_system == "Windows":
                startfile(trna_fasta_file_label["text"])
            else:
                subprocess.call(['xdg-open', trna_fasta_file_label["text"]])


        trna_fasta_open_button = Button(rna_framelabel, text="Open tRNA FASTA!", command = open_trna, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth, width = 103)
        trna_fasta_open_button.pack(fill = X, padx = 5, pady = 5)
        def open_report():
            if operating_system == "Windows":
                startfile(select_output_location_label["text"]+"/error_report.txt")
            else:
                subprocess.call(['xdg-open', select_output_location_label["text"]+"/error_report.txt"])	

        
        def open_directory():
            if operating_system == "Windows":
                startfile(select_output_location_label["text"])
            else:
                subprocess.call(['xdg-open', select_output_location_label["text"]])

        
        open_report_file_button = Button(unacc_frame, text="Open error report!", command = open_report, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
        open_report_file_button.pack(side = LEFT, expand = 1, fill = BOTH, padx = 5, pady = 5)
        open_directory_button = Button(unacc_frame, text="Open directory!", command = open_directory, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
        open_directory_button.pack(side = LEFT, expand = 1, fill = BOTH, padx = 5, pady = 5)
        quit_button = Button(unacc_frame, text = "Quit", command = close_program, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
        quit_button.pack(side = LEFT, expand = 1, fill = BOTH, padx = 5, pady = 5)
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


    create_fasta_files_button = Button(tab1, text= "Create FASTA files", command = create_fasta_files, state = DISABLED,font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    create_fasta_files_button.pack(expand = 1, fill = BOTH, padx = 5, pady = 5)


def quit_application():
	window.quit()
	window.destroy()
	pass

start_button = Button(main_frame, text = "Start", command = start_process, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
start_button.pack(side = LEFT, expand = 1, fill = BOTH, padx =  5, pady = 5)

def close_program():
    main_window.destroy()


quit_button=Button(main_frame, text = "Quit", command = close_program, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
quit_button.pack(side = RIGHT, expand = 1, fill = BOTH, padx =  5, pady = 5)
   
main_window.mainloop()