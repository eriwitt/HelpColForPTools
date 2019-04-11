#!/usr/bin/python
"""01_biopython_parser is a script to improve the parsability of your annotation for use in Pathway Tools PathoLogic.
   This includes removing unaccepted annotation features which will be removed automatically by using the command line inteface. 
   Furthermore, GO terms in the /note qualifier are rewritten into a form accepted by PathoLogic if they originally exists in this form:
   /note: "GO_component: GO:0005737 - cytoplasm; GO_function: GO:0003735 - structural constituent of ribosome; GO_process: GO:0006412 - translation" 
   This entry will be changed to:
   /note: "go_component: cytoplasm [goid GO:0005737]; GO_function: GO:0003735 - structural constituent of ribosome; GO_process: GO:0006412 - translation
	Author: Eric Witt
"""
from Bio import SeqIO
import datetime

time1=datetime.datetime.now()

# File Path Inputs
file_name = raw_input("Please enter your gbk-File path!")
file_name2 = raw_input("Please enter Report Output path (.txt)!")
file_name3 = raw_input("Please enter Improved gbk-File Output path!")
if '"' in file_name:
    file_name = file_name.split('"')[1]

if '"' in file_name2:
    file_name2 = file_name2.split('"')[1]

if '"' in file_name3:
    file_name3 = file_name3.split('"')[1]


# Write Report
changes_report=open(file_name2, "a")
changes_report.write("01_biopython_parser_cli Report File (timestamp: " + str(time1) + ")\n\n")
changes_report.write("Your Annotation:\n\t" + file_name + "\n")
changes_report.write("Improved Annotation:\n\t" + file_name3+ "\n\n")
changes_report.close()

# Parse GenBank file
gbk_file = SeqIO.parse(file_name,"genbank")

#List of features which will be accepted by PathoLogic
featureList=["CDS","misc_RNA","rRNA","tRNA"]
# Analyze Your Annotation
featl = {}    
for record in gbk_file:
    for feature in record.features:
        if feature.type not in featl:
            featl[feature.type] = 1
        elif feature.type in featl:
            featl[feature.type] = featl[feature.type] + 1
  
print "Your Annotation contains this GenBank features:\n"  
print featl
# Write Report
changes_report = open(file_name2, "a")
changes_report.write("Your Annotation analyzed:\n\n\tGBK FEATURE\tNUMBER\n")
for feature1 in featl:
    changes_report.write("\t" + feature1 + "\t" + str(featl[feature1]) + "\n")
        
changes_report.close()

gbk_file = SeqIO.parse(file_name,"genbank")
remove_list = {}
for record in gbk_file:
	#Update remove list
	remove_features = []
	for feat in featl:
		if feat not in featureList:
			remove_features.append(feat)
	
	print remove_features
	changes_report=open(file_name2, "a")
	changes_report.write("\nThis GenBank Features will be removed automatically:\n\n")
	for featur in remove_features:
		changes_report.write("\t" + str(featur) + "\n")
	
	changes_report.write("\n####GenBank Feature Removement####\n\n"+"The following features were removed from " +file_name+" by running biopython_parser.py.\nThe changes have been made to improve the parsability of gbk-file! \nThe adjusted Genbank-File can be found in: \n"+file_name3+"\n---------------------------------------------------------------------------------------------------------\n")
	changes_report.close()
	# GenBank Feature Removement
	for u in remove_features:
		remove_number = 0
		for feature in record.features:
			if feature.type== u:
				changes_report=open(file_name2, "a")
				changes_report.write("\n" + str(feature))
				changes_report.close()
				# Remove feature from record
				record.features.remove(feature)
				remove_number = remove_number + 1
				
		remove_list[u] = remove_number
	
	changed_go_term_notes = 0
	go_term_number = 0
	changes_report=open(file_name2, "a")
	changes_report.write("\n####GO Term Improvement####\n\n"+"The following qualifiers were adjusted in " + file_name + " by running biopython_parser.py.\nThe changes have been made to improve the parsability of gbk-file! \nThe adjusted Genbank-File can be found in: \n" + file_name3 + "\n--------------------------------------------------------------------------------------------------------------------------------------------\n")
	changes_report.write("'locus_tag'\t 'old /note:'\tin\t'new/note:'\n")
	changes_report.close()
	for feature in record.features:
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
						t1[i]=t2
						go_term_number = go_term_number + 1
						go_change_identifier = 1
					else:
						continue
				
				if go_change_identifier == 1:
                # Only change the /note qualifier if GO Terms are changed
					s=""
					for i in range(len(t1)):
						if i==0:
							s=t1[i]+"; "
						if i==len(t1)-1:
							s=s + t1[i]
						else:
							s=s+t1[i]+"; "
								
					feature.qualifiers["note"][0]=s
					changed_go_term_notes = changed_go_term_notes + 1
					changes_report=open(file_name2, "a")
					changes_report.write(feature.qualifiers["locus_tag"][0] + '\t/note:"' +t +'"\tin\t/note:"' +s+'"'+"\n")
					changes_report.close()
								
			if (t.startswith("GO_process: ") or t.startswith("GO_component: ") or t.startswith("GO_function: ")) and ";" not in t:
				t2="go"+t.split("GO")[1].split(": ")[0]+": "+t.split(" - ")[1]+" "+"[goid "+t.split(": ")[1].split(" - ")[0]+"]"
				r=t2
				go_term_number = go_term_number + 1
				feature.qualifiers["note"][0]=r
				changed_go_term_notes = changed_go_term_notes + 1
				changes_report=open(file_name2, "a")
				changes_report.write(feature.qualifiers["locus_tag"][0] + '\t/note:"' +str(t) +'"\t'+"in"+"\t"+'/note:"' +str(r)+'"'+"\n")
				changes_report.close()
	
SeqIO.write(record,file_name3,"genbank")

changes_report=open(file_name2, "a")
changes_report.write("\n####RESULT####\n\nGenBank Feature Removement:\n\n\t" + str(remove_list).split("{'")[1].split("}")[0].replace("':",":").replace(", '","\n\t") + "\n\nGO Term Improvement:\n\n\t" + str(changed_go_term_notes)+" /note qualifiers with " + str(go_term_number) + " GO Terms were improved!")
changes_report.close()
