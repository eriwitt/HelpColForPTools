#!/usr/bin/python
"""Author: Eric Witt

    This script filters pathways with missing enzyme mappings that were not considered in the PGDB from the pathway-inference-report written by PathoLogic while creating the PGDB.
    Pathways are considered in which the number of missing reactions is less than or equal to the number of existing reactions.
"""
import os
import platform
import sys
operating_system = platform.system()
#####################################################################################################
# Script Input
ld_report = sys.argv[1]
sel_report = sys.argv[2]

# Start filtering
filer = open(ld_report,"r").read()
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
out = open(sel_report,"w")
out.write("This file contains all PWYs with missing Reactions they are not added by PathoLogic:\n")
for l in pwys_miss_reac:             
    if len(pwys_miss_reac[l][1])>len(pwys_miss_reac[l][0]) and "PASSING-SCORE" not in l:
        out.write(l + "\t" + str(len(pwys_miss_reac[l][0])) +"\tof\t" + str(len(pwys_miss_reac[l][1])+len(pwys_miss_reac[l][0])) + "\treactions missing!\n")
    if len(pwys_miss_reac[l][1])==len(pwys_miss_reac[l][0]) and "PASSING-SCORE" not in l:
        out.write(l + "\t" + str(len(pwys_miss_reac[l][0])) +"\tof\t" + str(len(pwys_miss_reac[l][1])+len(pwys_miss_reac[l][0])) + "\treactions missing!\n")
out.close()