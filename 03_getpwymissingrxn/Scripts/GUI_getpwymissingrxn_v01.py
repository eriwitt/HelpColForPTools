#!/usr/bin/python
"""Author: Eric Witt

    This script filters pathways with missing enzyme mappings that were not considered in the PGDB from the pathway-inference-report written by PathoLogic while creating the PGDB.
    Pathways are considered in which the number of missing reactions is less than or equal to the number of existing reactions.
"""
from tkinter import *
import tkFileDialog
import os
import platform
import ttk
operating_system = platform.system()
if operating_system == "Windows":
    from os import startfile
else:
	import subprocess
#####################################################################################################
# Placeholder for file paths
ld_report = ""
sel_report = ""
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
main_window.title("getpwymissingrxn")
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
prog_label = Label(main_frame, text = "##########################################################################################################################\n\ngetpwymissingrxn\n\n ###########################################################################################################################\n\nAuthor: Eric Witt\n\n###########################################################################################################################",  font="Arial 10 bold", relief = "groove", borderwidth = 4)
prog_label.pack(fill = X, padx = 5, pady = 10)
info_label = Label(main_frame, text = "The script getpwymissingrxn was developed to filter pathways with missing enzyme mappings that were not considered in the Pathway Genome Database (PGDB) from the pathway-inference-report written by Pathway Tools PathoLogic while creating the PGDB. Pathways are considered in which the number of missing reactions is less than or equal to the number of existing reactions.", font="Arial 10 bold",  wraplength = 700, relief = "groove", borderwidth = 4)
info_label.pack(fill = X, padx = 5, pady = 10, ipadx = 10, ipady = 10)

def start():
    main_frame.pack_forget()

    # GUI Generate Tabs
    noteb = ttk.Notebook(main_window)
    noteb.pack(fill=BOTH, expand = 1, padx = 5, pady = 5)
    noteb.pressed_index = None
    tab1 = Frame(noteb)
    tab1.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)
    noteb.add(tab1, text = "Choose Files")

    # GUI Load your annotation
    def load_report():
		# Function for loading pwy-inference-report file by user in the GUI. The selected file path is displayed in the GUI.
        ld_report = str(tkFileDialog.askopenfilename(initialdir = os.getcwd, title = "Select", filetypes = (("TXT files","*.txt"),("all files","*.*file"))))
        load_your_report_label.config(text = ld_report)
        select_report_button.config(state = "normal")

    
    load_your_report_framelabel = LabelFrame(tab1, text = "Load pwy-inference-report", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    load_your_report_framelabel.pack(fill = X, padx = 5, pady = 10)
    load_your_report_label = Label(load_your_report_framelabel, text = ld_report,  font = label_font, wraplength = label_wraplength) 
    load_your_report_label.pack(fill = X, padx = 5, pady = 5)
    load_your_report_button = Button(load_your_report_framelabel, text = "Load", command = load_report,  font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    load_your_report_button.pack(fill = X, padx = 5, pady = 5)

    # GUI Select report location
    def select_report():
		# Function to select and enter the report file name. The selected file path is displayed in the GUI.
        sel_report = str(tkFileDialog.asksaveasfilename(initialdir = os.getcwd, title = "Select the path for the storage and enter the filename (*.txt) of the report!", filetypes = (("txt files","*.txt"),("all files","*.*"))))
        select_report_label.config(text = sel_report)
        get_pwys_button.config(state = "normal")


    select_report_framelabel = LabelFrame(tab1, text = "Select Location For Report File Storing", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
    select_report_framelabel.pack(fill = X, padx = 5, pady = 10)
    select_report_label = Label(select_report_framelabel, text = sel_report, font = label_font, wraplength = label_wraplength) 
    select_report_label.pack(fill = X, padx = 5, pady = 5)
    select_report_button = Button(select_report_framelabel, text = "Select and enter name (.txt)!", state = DISABLED, command = select_report, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    select_report_button.pack(fill = X, padx = 5, pady = 5)

    def get_pwys():
        # Disable "Choose Files" Buttons
        load_your_report_button.config(state = DISABLED)
        select_report_button.config(state = DISABLED)
        get_pwys_button.config(state = DISABLED)
        
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
        
        # Start filtering
        filer = open(load_your_report_label["text"],"r").read()
        if operating_system == "Windows":
            pwyblock = filer.split("Here is the result of determine-pathways-with-cf:")[1].split("\nList of pathways pruned")[0]
            pwys = pwyblock.split("\n (")[1:]
        else:
            pwyblock = filer.split("Here is the result of determine-pathways-with-cf:")[1].split("\r\nList of pathways pruned")[0]
            pwys = pwyblock.split("\r\n (")[1:]
        pwys_miss_reac={}
        for i in range(len(pwys)):
            if operating_system == "Windows":
                pwys[i] = pwys[i].replace("\n","")
            else:
                pwys[i] = pwys[i].replace("\r\n","")
        
        for i in pwys:
            c=0
            missingreac=[]
            presentreac=[]
            i=i.replace(" (","-(")
            if "REACTIONS-MISSING" in i:
                c=1
                pwy_name_reason = i.split(" ")[0]+"\t"+i.split("-(")[1]

                if "REACTIONS-PRESENT" in i:
                    o= i.split("REACTIONS-PRESENT")[1]
                    if " NIL)" not in o.split(") ")[0]:
                        oo=o.split("-(")[1].split(")")[0]
                        if " " in oo:
                            for tt in oo.split(" "):
                                if tt !="":
                                    presentreac.append(tt)
                        else:
                            presentreac.append(oo)
                z= i.split("REACTIONS-MISSING")[1]
                if " NIL)" not in z.split(") ")[0]:
                    r=z.split("-(")[1].split(")")[0]
                    if " " in r:
                        for t in r.split(" "):
                            if t !="":
                                missingreac.append(t)
                    else:
                        missingreac.append(r)
            if c==1:
                react=(missingreac,presentreac)
                pwys_miss_reac[pwy_name_reason]=react
        out = open(select_report_label["text"],"w")
        out.write("This file contains all PWYs with missing Reactions they are not added by PathoLogic:\n")
        for l in pwys_miss_reac:             
            if len(pwys_miss_reac[l][1])>len(pwys_miss_reac[l][0]) and "PASSING-SCORE" not in l:
                out.write(l + "\t" + str(len(pwys_miss_reac[l][0])) +"\tof\t" + str(len(pwys_miss_reac[l][1])+len(pwys_miss_reac[l][0])) + "\treactions missing!\n")
            if len(pwys_miss_reac[l][1])==len(pwys_miss_reac[l][0]) and "PASSING-SCORE" not in l:
                out.write(l + "\t" + str(len(pwys_miss_reac[l][0])) +"\tof\t" + str(len(pwys_miss_reac[l][1])+len(pwys_miss_reac[l][0])) + "\treactions missing!\n")
        out.close()

        result_framelabel  = LabelFrame(unacc_frame, relief = framelabel_relief, borderwidth = framelabel_borderwidth)
        result_framelabel.pack(fill = X, padx = 5, pady = 5)
        result_label = Label(result_framelabel, text = "The pathways have been filtered and were listed below as well as in the report file.\n\nA possible strategy could be to add all filtered pathways to the PGDB and run Pathway Tools Pathway Hole Filler. All pathways that are complete after this step could be kept and the others should be searched for possible gene candidates in the report file of the pathway hole filler. If no gene could be assigned to the missing reaction, remove the pathway.", font = label_font, wraplength = label_wraplength)
        result_label.pack(fill = X, padx = 5, pady = 5)
        
        result2_framelabel  = LabelFrame(unacc_frame, text = "Filtered Pathways:", relief = framelabel_relief, font = framelabel_font, borderwidth = framelabel_borderwidth)
        result2_framelabel.pack(fill = X, padx = 5, pady = 5)
        read_report = open(select_report_label["text"],"r")
        header1_label = Label(result2_framelabel, text = "FRAME-ID", font = "Arial 10 bold", wraplength = label_wraplength)
        header1_label.grid(row = 0, column = 0, padx = 5, sticky = W+E+N+S)
        header2_label = Label(result2_framelabel, text = "REASON", font = "Arial 10 bold", wraplength = label_wraplength)
        header2_label.grid(row = 0, column = 1, padx = 5, sticky = W+E+N+S)
        header3_label = Label(result2_framelabel, text = "NUMBER OF MISSING REACTIONS", font = "Arial 10 bold", wraplength = label_wraplength)
        header3_label.grid(row = 0, column = 2, padx = 5, sticky = W+E+N+S)
        row_nr = 0
        for line in read_report:
            if "This file contains all PWYs with missing Reactions they are not added by PathoLogic:\n" not in line:
                row_nr = row_nr + 1
                result2_label = Label(result2_framelabel, text = line.split("\t")[0], font = label_font, wraplength = label_wraplength)
                result2_label.grid(row = row_nr, column = 0, padx = 5, sticky = W+E+N+S)
                result3_label = Label(result2_framelabel, text = line.split("\t")[1], font = label_font, wraplength = label_wraplength)
                result3_label.grid(row = row_nr, column = 1, padx = 5, sticky = W+E+N+S)
                result4_label = Label(result2_framelabel, text = line.split("\t")[2:-1], font = label_font, wraplength = label_wraplength)
                result4_label.grid(row = row_nr, column = 2, padx = 5, sticky = W+E+N+S)

        def open_report():
            if operating_system == "Windows":
                startfile(select_report_label["text"])
            else:
                subprocess.call(['xdg-open',select_report_label["text"]])


        open_report_button = Button(unacc_frame, text="Open report file!", command = open_report,font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
        open_report_button.pack(expand = 1, fill = X, padx=5, pady=5)

        quit_button = Button(unacc_frame, text = "Quit", command = close_program, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
        quit_button.pack(expand = 1, fill = X, padx=5, pady=5)
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


    get_pwys_button = Button(tab1, text = "Get Pathways", command = get_pwys, state = DISABLED, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
    get_pwys_button.pack(expand = 1, fill = BOTH, padx =  5, pady = 10)


start_button = Button(main_frame, text = "Start", command = start, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
start_button.pack(side = LEFT, expand = 1, fill = BOTH, padx =  5, pady = 10)

def close_program():
    main_window.destroy()


quit_button=Button(main_frame, text = "Quit", command = close_program, font = button_font, cursor = button_cursor, overrelief = button_overrelief, bg = button_bg, borderwidth = button_borderwidth)
quit_button.pack(side = RIGHT, expand = 1, fill = BOTH, padx =  5, pady = 10)
   
main_window.mainloop()

