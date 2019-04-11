#!/usr/bin/python
"""01_biopython_parser is a script to improve the parsability of your annotation for use in Pathway Tools PathoLogic.
   This includes removing unaccepted annotation features that can be controlled by the user. Furthermore, GO terms in 
   the /note qualifier are rewritten into a form accepted by PathoLogic if they originally exists in this form:
   /note: "GO_component: GO:0005737 - cytoplasm; GO_function: GO:0003735 - structural constituent of ribosome; GO_process: GO:0006412 - translation" 
   This entry will be changed to:
   /note: "go_component: cytoplasm [goid GO:0005737]; GO_function: GO:0003735 - structural constituent of ribosome; GO_process: GO:0006412 - translation
	Author: Eric Witt
"""
from Bio import SeqIO
from Tkinter import *
import os
import ttk
import tkMessageBox
import tkFileDialog
import datetime
import webbrowser
import platform
operating_system = platform.system()
if operating_system == "Windows":
    from os import startfile
else:
	import subprocess
	
time1=datetime.datetime.now()
#####################################################################################################
# Placeholder for file paths
gbkfile=""
report=""
improved_gbk_path=""
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
prog_label = Label(main_frame, text = "##########################################################################################################################\n\n 01_biopython_parser\n\n ###########################################################################################################################\n\nAuthor: Eric Witt\n\n###########################################################################################################################",  font="Arial 10 bold", relief = "groove", borderwidth = 4)
prog_label.pack(fill = X, padx = 5, pady = 10)

info_label = Label(main_frame, text = "Pathway Tools has certain requirements for the annotation used in GenBank format. With this script you can remove features that are not accepted by Pathway Tools PathoLogic. Furthermore, GO Terms in the /note qualifier of the annotation are converted to the appropriate form to be recognized by PathoLogic.", font="Arial 10 bold",  wraplength = 700, relief = "groove", borderwidth = 4)
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

    # GUI Load your annotation
    def load_annotation():
		# Function for loading annotation file by user in the GUI. The selected file path is displayed in the GUI.
        gbkfile = str(tkFileDialog.askopenfilename(initialdir = os.getcwd, title = "Please select Annotation file (.gbk)!", filetypes = (("GenBank files","*.gbk"),("all files","*.*file"))))
        load_your_annotation_label.config(text = gbkfile)
        select_report_button.config(state = "normal")

    
    load_your_annotation_framelabel = LabelFrame(tab1, text = "Load Your GenBank Annotation", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    load_your_annotation_framelabel.pack(fill = X, padx = 5, pady = 10)
    load_your_annotation_label = Label(load_your_annotation_framelabel, text = gbkfile,  font = label_font, wraplength = label_wraplength) 
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
    select_report_label = Label(select_report_framelabel, text = report, font = label_font, wraplength = label_wraplength) 
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
            analyze_annotation_button.config(state = "normal")
            # Write Report
            changes_report = open(select_report_label["text"], "a")
            changes_report.write("01_biopython_parser Report File (timestamp: " + str(time1) + ")\n\n")
            changes_report.write("Your Annotation:\n\t" + load_your_annotation_label["text"] + "\n")
            changes_report.write("Improved Annotation:\n\t" + improved_gbk_path_label["text"]+ "\n\n")
            changes_report.close()

    improved_gbk_path_framelabel = LabelFrame(tab1, text = "Select Location For Improved Annotation Storing:",  relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    improved_gbk_path_framelabel.pack(fill = X, padx = 5, pady = 10)
    improved_gbk_path_label = Label(improved_gbk_path_framelabel, text = improved_gbk_path, font = label_font, wraplength = label_wraplength)
    improved_gbk_path_label.pack(fill = X, padx = 5, pady = 5)
    improved_gbk_path_button = Button(improved_gbk_path_framelabel, text = "Select directory", state = DISABLED, command = save_improved_annotation, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    improved_gbk_path_button.pack(fill = X, padx = 5, pady = 5)

    
    # GUI Analyze annotation
    def analyze_annotation():
        # Disable "Choose Files" Buttons
        load_your_annotation_button.config(state = DISABLED)
        select_report_button.config(state = DISABLED)
        improved_gbk_path_button.config(state = DISABLED)
        analyze_annotation_button.config(state = DISABLED)

        # GUI New Tab "General Informations"
        tab2 = Frame(noteb)
        tab2.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
        noteb.add(tab2, text = "General Informations")
        noteb.select(tab2)

        accepted_genbank_features_framelabel = LabelFrame(tab2, text = "Accepted GenBank features by PathoLogic:", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
        accepted_genbank_features_framelabel.pack(fill = X, padx = 5, pady = 10)
        accepted_featureList=["CDS","misc_RNA","rRNA","tRNA"]
        accepted_feature_label = Label(accepted_genbank_features_framelabel, text = "This GenBank features will be accepted by Pathway Tools PathoLogic:\t\t\t\t"+str(sorted(accepted_featureList)), font = label_font)
        accepted_feature_label.pack(fill = X, padx = 5, pady = 5)
        userguide_label = Label(accepted_genbank_features_framelabel, text = "Further information about PathoLogic can be found in the Pathway Tools User's Guide.", font = label_font)
        userguide_label.pack(fill = X, padx = 5, pady = 5)

        additional_reference_framelabel = LabelFrame(tab2, text = "Additional Informations", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
        additional_reference_framelabel.pack(fill = X, padx = 5, pady = 10)
        feature_definition_label = Label(additional_reference_framelabel, text = "For further information and definitions on the respective GeneBank features, please visit the following URL:", font = label_font)
        feature_definition_label.pack(fill = X, padx = 5, pady = 5)
        
        def hyperlink(event):
            webbrowser.open_new(event.widget.cget("text"))

        
        feature_url_label = Label(additional_reference_framelabel, text = "http://www.insdc.org/files/feature_table.html#7.2", font = "Arial 10 underline", fg = "blue", cursor = "hand2")
        feature_url_label.pack(fill = X, padx = 5, pady = 5)
        feature_url_label.bind("<Button-1>", hyperlink)
        
        #List of features contained in your gbk-file
        gbk_file = SeqIO.parse(load_your_annotation_label["text"], "genbank")
        featl = {}    
        for record in gbk_file:
            for feature in record.features:
                if feature.type not in featl:
                    featl[feature.type] = 1
                elif feature.type in featl:
                    featl[feature.type] = featl[feature.type] + 1
        
        print featl
        # Write Report
        changes_report = open(select_report_label["text"], "a")
        changes_report.write("Your Annotation analyzed:\n\n\tGBK FEATURE\tNUMBER\n")
        for feature1 in featl:
            changes_report.write("\t" + feature1 + "\t" + str(featl[feature1]) + "\n")
        
        changes_report.close()

        annotation_includes_features_framelabel = LabelFrame(tab2, text="Your Annotation Includes The Following GenBank Features:", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
        annotation_includes_features_framelabel.pack(fill = X, padx = 5, pady = 10)
        annotation_feature_label = Label(annotation_includes_features_framelabel, text = str(sorted(featl)), font = label_font)
        annotation_feature_label.pack(fill = X, padx = 5, pady = 5)

        def unaccepted_gbk_features():
            # Disable "General Informations" Button
            go_to_unacc_gbk_feat_remove_button.config(state = DISABLED)
            # Array for features to remove
            remove_features = []
            # GUI New Tab "GenBank Feature Removement"
            tab3 = Frame(noteb)
            tab3.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
            noteb.add(tab3, text = "GenBank Feature Removement")
            noteb.select(tab3)

            # GUI add objects for a scrollable tab
            mycanvas = Canvas(tab3)
            mycanvas.pack(side = "left", fill = BOTH, expand = 1)

            unacc_frame = Frame(mycanvas)
            unacc_frame.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
            mycanvas.create_window(0, 0, window = unacc_frame, anchor = "nw")

            # GUI Unaccepted features
            unaccepted_gbk_features_framelabel = LabelFrame(unacc_frame, text = "Unaccepted GenBank Features:", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
            unaccepted_gbk_features_framelabel.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
            explanation_label = Label(unaccepted_gbk_features_framelabel, text = "Some unaccepted GenBank features can lead to errors (for example: more genes detected than available) in the report files generated by PathoLogic! To reduce these errors you can choose to remove the feature entries. If you are unsure whether to remove the feature, consult the above link or the Pathway Tools User's Guide. For some GenBank features recommendations from experience are given. If you are unsure you can also test if the non-removal causes errors in PathoLogic report files.", font = label_font, wraplength = label_wraplength)
            explanation_label.grid(row = 0, column = 0, columnspan = 4, padx = 5, pady = 5, sticky = W+E+N+S)
            # GUI GenBank feature table
            headline_label = Label(unaccepted_gbk_features_framelabel, text = "GenBank Feature", font = "Arial 8 bold")
            headline_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = W+E+N+S)
            headline1_label = Label(unaccepted_gbk_features_framelabel, text = "Count", font = "Arial 8 bold")
            headline1_label.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = W+E+N+S)
            headline2_label = Label(unaccepted_gbk_features_framelabel, text = "Select to remove?", font = "Arial 8 bold")
            headline2_label.grid(row = 1, column = 2, padx = 5, pady = 5, sticky = W+E+N+S)
            headline3_label = Label(unaccepted_gbk_features_framelabel, text = "Recommendation", font = "Arial 8 bold")
            headline3_label.grid(row = 1, column = 3, padx = 5, pady = 5, sticky = W+E+N+S)

            a = 1
            featurelabellist = []
            featurecountlist = []
            checkbutvarlist = []
            checkbutlist = []

            for feat in sorted(featl):
                print feat
                if feat not in accepted_featureList:
                    a = a+1
                    lb = Label(unaccepted_gbk_features_framelabel, text = feat, font = "Arial 8")
                    lb.grid(row = a, column = 0, padx = 5, pady = 5, sticky = W+E+N+S)
                    featurelabellist.append(lb)
                    var = IntVar()
                    cb = Checkbutton(unaccepted_gbk_features_framelabel, variable = var)
                    cb.grid(row = a, column = 2, padx = 5, pady = 5, sticky = W+E+N+S)
                    checkbutlist.append(cb)
                    lb1 = Label(unaccepted_gbk_features_framelabel, text = featl[feat], font = "Arial 8")
                    lb1.grid(row = a, column = 1, padx = 5, pady = 5, sticky = W+E+N+S)
                    featurecountlist.append(lb1)
                    checkbutvarlist.append(var)
                    print len(checkbutvarlist)
                    if feat == "gene":
                        Label(unaccepted_gbk_features_framelabel, text = "There should be no errors if it is not removed.", font = "Arial 8", relief = SUNKEN, wraplength = 250).grid(row = a, column = 3, padx = 5, pady = 5, sticky = W+E+N+S)
                    elif feat == "source":
                        Label(unaccepted_gbk_features_framelabel, text = "Is ignored by PathoLogic and should not lead to any errors.", font = "Arial 8", relief = SUNKEN, wraplength = 250).grid(row = a, column = 3, padx = 5, pady = 5, sticky = W+E+N+S)
                    elif "RNA" in feat:
                        Label(unaccepted_gbk_features_framelabel, text = "According to the Pathway Tools User's Guide, all other RNAs are grouped under the GenBank feature 'misc_RNA'. The entries should be removed or renamed.", font = "Arial 8", relief = SUNKEN, wraplength = 250).grid(row = a, column = 3, padx = 5, pady = 5, sticky = W+E+N+S)
                    else:
                        Label(unaccepted_gbk_features_framelabel, text = "Should be removed, could perhaps lead to errors!", font = "Arial 8", relief = SUNKEN, wraplength = 250).grid(row = a, column = 3, padx = 5, pady = 5, sticky = W+E+N+S)

            
            #GUI De/select all
            def select_all():
                # Function selects all modes
                for but in checkbutlist:
                    but.select()

            def deselect_all():
                # Function deselects all modes
                for but in checkbutlist:
                    but.deselect()

            select_all_button = Button(unaccepted_gbk_features_framelabel, text = "Select all to remove!", command = select_all, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
            deselect_all_button = Button(unaccepted_gbk_features_framelabel, text = "Deselect all!", command = deselect_all, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
            select_all_button.grid(row = a+1, column = 0, padx = 5, pady = 5, sticky = W+E+N+S)
            deselect_all_button.grid(row = a+1, column=1, padx = 5, pady = 5, sticky = W+E+N+S)
        
            def confirm_removement():
                changes_report = open(select_report_label["text"], "a")
                changes_report.write("\nYour Selection for GenBank Feature Removement:\n\n")
                for i in range(len(checkbutlist)):
                   print featurelabellist[i]["text"]+" : "+ str(checkbutvarlist[i].get())
                   # Add feature for removement if it is selected
                   if checkbutvarlist[i].get() == 1:
                       remove_features.append(featurelabellist[i]["text"])
                       changes_report = open(select_report_label["text"], "a")
                       changes_report.write("\t" + featurelabellist[i]["text"] + "\n")
                        
                   checkbutlist[i].config(state = DISABLED)
                   changes_report.close()

                print str(remove_features)    
                deselect_all_button.config(state = DISABLED)
                select_all_button.config(state = DISABLED)
                confirm_removement_button.config(state = DISABLED)
                continue_with_GO_term_refinement_button.config(state = "normal")
                    

            confirm_removement_button = Button(unaccepted_gbk_features_framelabel, text = "Confirm removement selection!", command = confirm_removement, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth) 
            confirm_removement_button.grid(row = a+1, column = 2, columnspan = 2, padx = 5, pady = 5, sticky = W+E+N+S)

            def goterm_refinement():
                # Disable button
                continue_with_GO_term_refinement_button.config(state = DISABLED)
                # GUI New Tab "GO Term Refinement"
                tab4 = Frame(noteb)
                tab4.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
                noteb.add(tab4, text = "GO Term Refinement")
                noteb.select(tab4)
                
                goterm_framelabel = LabelFrame(tab4, text = "GO Term Improvement", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
                goterm_framelabel.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)

                explanation_label = Label(goterm_framelabel, text = 'In this function the /note qualifier of the feature entries are searched for GO terms and written in a form accepted by PathoLogic.\nThis function works if the GO Terms are in this form:\n\n/note:"GO_process: GO:0009088 - threonine biosynthetic process".\n\nThe Function transform this entry to this form:\n\n/note:"go_process: threonine biosynthetic process [goid GO:0009088]"\n\nPlease check if your annotation contains Go terms in this form.\nIf GO terms are present in any other form, there is no guarantee that the function will work,\nperhaps an error could occur that aborts the process. In case of doubt just try and start the program again without selecting this function.', font = label_font)
                explanation_label.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)

                def open_anno():
                    if operating_system == "Windows":
						startfile(load_your_annotation_label["text"])
                    else:
						subprocess.call(['xdg-open', load_your_annotation_label["text"]])
                    
                    go_checkbutton.config(state = "normal")
                    confirm_gotermimp_button.config(state = "normal")

                open_annotation_button = Button(goterm_framelabel, text = "Open annotation file to check GO Term form!", command = open_anno, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
                open_annotation_button.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)

                goterm_label2 = Label(goterm_framelabel, text = "GO Term improvement", font = label_font, wraplength = label_wraplength)
                goterm_label2.pack(side = "left", fill = BOTH, expand = 1, padx = 5, pady = 5)
        
                var_go = IntVar()
                go_checkbutton = Checkbutton(goterm_framelabel, text = "Select?", variable = var_go, state = DISABLED)
                go_checkbutton.pack(side = "left", fill = BOTH, expand = 1, padx = 5, pady = 5)

                def confirm_goterm():
                    go_checkbutton.config(state = DISABLED)
                    confirm_gotermimp_button.config(state = DISABLED)
                    changes_report = open(select_report_label["text"], "a")
                    changes_report.write("\nGO Term Improvement:\t")
                    if var_go.get() == 1:
                        changes_report.write("SELECTED\n")
                    else:
                        changes_report.write("NOT SELECTED\n")

                    changes_report.close()
                    # GUI New Tab
                    tab5 = Frame(noteb)
                    tab5.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
                    noteb.add(tab5, text = "Process")
                    noteb.select(tab5)
                    # GUI add objects for a scrollable tab
                    mycanvas2 = Canvas(tab5)
                    mycanvas2.pack(side = "left", fill = BOTH, expand = 1)

                    unacc_frame2 = Frame(mycanvas2)
                    unacc_frame2.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
                    mycanvas2.create_window(0, 0, window = unacc_frame2, anchor = "nw")
                    
                    # GUI Overview

                    imp_overview_framelabel = LabelFrame(unacc_frame2, text = "Overview", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
                    imp_overview_framelabel.pack(fill = X,  padx = 5, pady = 5)
                    feat_label = Label(imp_overview_framelabel, text = "These GenBank features have been selected for removal:\t"+str(remove_features), font = label_font, wraplength = label_wraplength)
                    feat_label.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
                    if var_go.get() == 1:
                        go_label = Label(imp_overview_framelabel, text = "The GO term refinement was selected.", font = label_font)
                        go_label.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
                    else:
                        go_label = Label(imp_overview_framelabel, text = "The GO term refinement was not selected.", font = label_font)
                        go_label.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)

                    def start_refinement():
                        start_improvements_button.pack_forget()
                        # GUI Progress
                        progress_framelabel = LabelFrame(unacc_frame2, text = "Progress", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
                        progress_framelabel.pack(fill = X, expand = 1, padx = 5, pady = 5)
                        # GBK Feature Refinement 
                        def remove_selected_features_imp_goterms():
                            # This Function removes the selected GenBank features from the GenBank-file and if selected the GO terms in the /note qualifier were improved for a better parsability of the GenBank-file in PathoLogic		 
                            changes_report = open(select_report_label["text"], "a")
                            changes_report.write("\n####GenBank Feature Removement####\n\n"+"The following features were removed from " +load_your_annotation_label["text"] + " by running biopython_parser.py.\nThe changes have been made to improve the parsability of gbk-file! \nThe adjusted Genbank-File can be found in: \n" + improved_gbk_path_label["text"] + "\n--------------------------------------------------------------------------------------------------------------------------------------------\n")
                            changes_report.close()
                            gbk_file = SeqIO.parse(load_your_annotation_label["text"], "genbank")
                            remove_list = {}
                            # GenBank Feature Removement
                            for record in gbk_file:
                                featnr = 0
                                for u in remove_features:
                                    remove_number = 0
                                    featnr = featnr + 1
                                    progress_nr = (100/float(len(remove_features))*featnr)
                                    progbar["value"] = progress_nr
                                    progress_framelabel.update()
                                    print u
                                    for feature in record.features:
                                        if feature.type == u:
                                            changes_report = open(select_report_label["text"], "a")
                                            changes_report.write("\n" + str(feature))
                                            changes_report.close()
                                            record.features.remove(feature)
                                            remove_number = remove_number + 1
                                            
                                    for feature in record.features:
                                        if feature.type == u:
                                            changes_report = open(select_report_label["text"], "a")
                                            changes_report.write("\n" + str(feature))
                                            changes_report.close()
                                            record.features.remove(feature)
                                            remove_number = remove_number + 1
                                    
                                    remove_list[u] = remove_number

                                # GO Term Improvement if selected
                                changed_go_term_notes = 0
                                go_term_number = 0
                                if var_go.get() == 1:
                                    changes_report = open(select_report_label["text"], "a")
                                    changes_report.write("\n####GO Term Improvement####\n\n"+"The following qualifiers were adjusted in " + load_your_annotation_label["text"] + " by running biopython_parser.py.\nThe changes have been made to improve the parsability of gbk-file! \nThe adjusted Genbank-File can be found in: \n" + improved_gbk_path_label["text"] + "\n--------------------------------------------------------------------------------------------------------------------------------------------\n")
                                    changes_report.write("'locus_tag'\t 'old /note:'\tin\t'new/note:'\n")
                                    changes_report.close()
                                    feate_nr = 0
                                    for feature in record.features:
                                        feate_nr = feate_nr + 1
                                        progress_nr1 = (100/float(len(record.features))*feate_nr)
                                        progbar1["value"] = progress_nr1
                                        progress_framelabel.update()
                                        if "note" in feature.qualifiers:
                                            t = feature.qualifiers["note"][0]
                                            go_change_identifier = 0
                                            # if the /note qualifier have more then one information 
                                            if ";" in t:
                                                t1 = t.split("; ")
                                                for i in range(len(t1)):
					                                #print str(i) + "\t" + t1[i]
                                                    if t1[i].startswith("GO_process: ") or t1[i].startswith("GO_component: ") or t1[i].startswith("GO_function: "):
                                                        t2="go"+t1[i].split("GO")[1].split(": ")[0]+": "+t1[i].split(" - ")[1]+" "+"[goid "+t1[i].split(": ")[1].split(" - ")[0]+"]"
                                                        go_term_number = go_term_number + 1
                                                        go_change_identifier = 1
                                                        t1[i]=t2
                                                    else:
                                                        continue
                                                
                                                if go_change_identifier == 1:
                                                    # Only change the /note qualifier if GO Terms are changed
                                                    s = ""
                                                    for i in range(len(t1)):
                                                        if i==0:
                                                            s=t1[i]+"; "
                                                        if i==len(t1)-1:
                                                            s=s + t1[i]
                                                        else:
                                                            s=s+t1[i]+"; "

                                                    feature.qualifiers["note"][0]=s
                                                    changed_go_term_notes = changed_go_term_notes + 1
                                                    changes_report = open(select_report_label["text"], "a")
                                                    changes_report.write(feature.qualifiers["locus_tag"][0] + '\t/note:"' +t +'"\tin\t/note:"' +s+'"'+"\n")
                                                    changes_report.close()    
                    
                                            if (t.startswith("GO_process: ") or t.startswith("GO_component: ") or t.startswith("GO_function: ")) and ";" not in t:
                                                t2="go"+t.split("GO")[1].split(": ")[0]+": "+t.split(" - ")[1]+" "+"[goid "+t.split(": ")[1].split(" - ")[0]+"]"
                                                r=t2
                                                go_term_number = go_term_number + 1
                                                feature.qualifiers["note"][0]=r
                                                changed_go_term_notes = changed_go_term_notes + 1
                                                changes_report = open(select_report_label["text"], "a")
                                                changes_report.write(feature.qualifiers["locus_tag"][0] + '\t/note:"' +str(t) +'"\t'+"in"+"\t"+'/note:"' +str(r)+'"'+"\n")
                                                changes_report.close()


                            SeqIO.write(record, improved_gbk_path_label["text"], "genbank")
                            
                            gbk_file = SeqIO.parse(improved_gbk_path_label["text"], "genbank")
                            featl2 = {}    
                            for record in gbk_file:
                                for feature in record.features:
                                    if feature.type not in featl2:
                                        featl2[feature.type] = 1
                                    elif feature.type in featl2:
                                        featl2[feature.type] = featl2[feature.type] + 1
        
                            print featl2

                            result_framelabel = LabelFrame(unacc_frame2, text = "Result", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
                            result_framelabel.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
                            feature_result_label = Label(result_framelabel, text ="Your improved annotation contains now the following GenBank features:\n\n" + str(sorted(featl2)).split("['")[1].split("']")[0].replace("', '","\n"), font = label_font, wraplength = label_wraplength)
                            feature_result_label.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
                            if len(remove_list) == 0:
                                feature_remove_label = Label(result_framelabel, text ="Your Input for GenBank Refinement was empty!", font = label_font, wraplength = label_wraplength)
                                feature_remove_label.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
                            else:
                                feature_remove_label = Label(result_framelabel, text ="Therefore the following features were removed:\n\n" + str(remove_list).split("{'")[1].split("}")[0].replace("':",":").replace(", '","\n"), font = label_font, wraplength = label_wraplength)
                                feature_remove_label.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
                            goterm_improve_label = Label(result_framelabel, text ="GO Term Improvement:\n\n" + str(changed_go_term_notes)+" /note qualifiers with " + str(go_term_number) + " GO Terms were improved!" , font = label_font, wraplength = label_wraplength)
                            goterm_improve_label.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
                            changes_report = open(select_report_label["text"], "a")
                            if len(remove_list) == 0:
                                changes_report.write("\n####RESULT####\n\nGenBank Feature Removement:\n\n\t" + "Your Input was empty!" + "\n\nGO Term Improvement:\n\n\t" + str(changed_go_term_notes)+" /note qualifiers with " + str(go_term_number) + " GO Terms were improved!")
                            else:
                                changes_report.write("\n####RESULT####\n\nGenBank Feature Removement:\n\n\t" + str(remove_list).split("{'")[1].split("}")[0].replace("':",":").replace(", '","\n\t") + "\n\nGO Term Improvement:\n\n\t" + str(changed_go_term_notes)+" /note qualifiers with " + str(go_term_number) + " GO Terms were improved!")
                            changes_report.close()

                            def open_report():
                                if operating_system == "Windows":
									startfile(select_report_label["text"])
                                else:
									subprocess.call(['xdg-open', select_report_label["text"]])
                                
                            open_report_button = Button(unacc_frame2, text = "Open Report!",command = open_report, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
                            open_report_button.pack(fill = BOTH, padx = 5, pady = 5)
                            
                            def open_imp_anno():
                                if operating_system == "Windows":
									startfile(improved_gbk_path_label["text"])
                                else:
									subprocess.call(['xdg-open', improved_gbk_path_label["text"]])

                            open_imp_anno_button = Button(unacc_frame2, text = "Open Improved Annotation!",command = open_imp_anno, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
                            open_imp_anno_button.pack(fill = BOTH, padx = 5, pady = 5)
                            
                            quit_button2 = Button(unacc_frame2, text = "Quit!",command = close_program, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
                            quit_button2.pack(fill = BOTH, padx = 5, pady = 5)

                            # If the content of the unacc_frame is to big for the window, than add a scrollbar
                            mycanvas2.update()
                            main_window.update()
                            if unacc_frame2.winfo_height() > main_window.winfo_height()-50:
                                myscrollbar2 = Scrollbar(tab5, command = mycanvas2.yview)
                                mycanvas2.config(yscrollcommand = myscrollbar2.set, scrollregion = mycanvas2.bbox("all"))
                                myscrollbar2.pack(side=RIGHT, fill=Y)
                
                                def mousewheel2(event):
                                    if operating_system == "Windows":
										mycanvas2.yview_scroll(int(-1*(event.delta/120)), "units")
                                    if operating_system == "Linux":
                                        if event.num == 4:
                                            mycanvas2.yview_scroll(-1, "units")
                                        if event.num == 5:
                                            mycanvas2.yview_scroll(1, "units")
                                    
                                    if operating_system == "Darwin":
										mycanvas2.yview_scroll((event.delta/120), "units")


                                if operating_system == "Linux":
									mycanvas2.bind_all("<Button-4>", mousewheel2)
									mycanvas2.bind_all("<Button-5>", mousewheel2)
                                else:	
									mycanvas2.bind_all("<MouseWheel>", mousewheel2)

                        feature_progress_label = Label(progress_framelabel, text ='GenBank Feature Refinement:', font = label_font)
                        feature_progress_label.pack(fill = BOTH, padx = 5, pady = 5)
                        progress_nr = 0
                        progbar = ttk.Progressbar(progress_framelabel, orient = "horizontal", length = 800, mode = "determinate", maximum = 100, value = progress_nr)
                        progbar.pack(fill = BOTH, padx = 5, pady = 5)
                        
                        GOterm_progress_label = Label(progress_framelabel, text ='GO Term Refinement:', font = label_font)
                        GOterm_progress_label.pack(fill = BOTH, padx = 5, pady = 5)
                        progress_nr1 = 0
                        progbar1 = ttk.Progressbar(progress_framelabel, orient = "horizontal", length = 800, mode = "determinate", maximum = 100, value = progress_nr1)
                        progbar1.pack(fill = BOTH, padx = 5, pady = 5)
                        mycanvas2.update()
                        remove_selected_features_imp_goterms()

                    start_improvements_button = Button(unacc_frame2, text = " Start Refinement!",command = start_refinement, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
                    start_improvements_button.pack(fill = X, padx = 5, pady = 5)
                   

                    print var_go.get()


                confirm_gotermimp_button = Button(goterm_framelabel, text = "Confirm Selection!", command = confirm_goterm, state = DISABLED, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
                confirm_gotermimp_button.pack(side = "left", fill = BOTH, expand = 1, padx = 5, pady = 5)


            continue_with_GO_term_refinement_button = Button(unacc_frame, text = "Continue With GO Term Refinement!", command = goterm_refinement, state = DISABLED, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
            continue_with_GO_term_refinement_button.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)

            # If the content of the unacc_frame is to big for the window, than add a scrollbar
            mycanvas.update()
            main_window.update()
            if unacc_frame.winfo_height() > (main_window.winfo_height()-50):
                myscrollbar = Scrollbar(tab3, command = mycanvas.yview)
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

        go_to_unacc_gbk_feat_remove_button = Button(tab2, text = "Go to unaccepted GenBank feature removement!", command = unaccepted_gbk_features, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
        go_to_unacc_gbk_feat_remove_button.pack(fill = BOTH, expand = 1, padx = 5, pady = 10)


    analyze_annotation_button = Button(tab1, text = "Analyze Annotation!", state = DISABLED, command = analyze_annotation, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    analyze_annotation_button.pack(fill = BOTH, expand = 1, padx = 5, pady = 10)


start_button = Button(main_frame, text = "Start", command = choose_files, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
start_button.pack(side = LEFT, expand = 1, fill = BOTH, padx =  5, pady = 10)

def close_program():
    main_window.destroy()


quit_button=Button(main_frame, text = "Quit", command = close_program, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
quit_button.pack(side = RIGHT, expand = 1, fill = BOTH, padx =  5, pady = 10)
   
main_window.mainloop()