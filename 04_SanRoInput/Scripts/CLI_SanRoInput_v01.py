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
import os
import platform
import sys
import webbrowser
operating_system = platform.system()

#####################################################################################################
# Script Input
anno_file_name = sys.argv[1]
output_location = sys.argv[2]

#Creation of the protein FASTA file 
gbk_file = SeqIO.parse(anno_file_name,"genbank")
if operating_system == "Windows":
    prot_fasta_file= open(output_location + "\\" + anno_file_name.split("\\")[-1].split(".gbk")[0]+"_protein_FASTA.faa","w")
    report = open(output_location + "/error_report.txt","w")
else:
    prot_fasta_file= open(output_location + "/" + anno_file_name.split("/")[-1].split(".gbk")[0]+"_protein_FASTA.faa","w")
    report = open(output_location + "/error_report.txt","w")

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
report.close()

#Creation of the DNA FASTA file 
gbk_file = SeqIO.parse(anno_file_name,"genbank")
if operating_system == "Windows":
    dna_fasta_file = open(output_location + "\\" + anno_file_name.split("\\")[-1].split(".gbk")[0]+"_DNA_FASTA.faa","w")
else:
    dna_fasta_file = open(output_location + "/" + anno_file_name.split("/")[-1].split(".gbk")[0]+"_DNA_FASTA.faa","w")
    
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
    
    gbk_file = SeqIO.parse(anno_file_name,"genbank")
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
if operating_system == "Windows":
    create_rna_fasta(output_location + "\\" + anno_file_name.split("\\")[-1].split(".gbk")[0]+"_tRNA_FASTA.faa","tRNA")
    create_rna_fasta(output_location + "\\" + anno_file_name.split("\\")[-1].split(".gbk")[0]+"_rRNA_FASTA.faa","rRNA")
    create_rna_fasta(output_location + "\\" + anno_file_name.split("\\")[-1].split(".gbk")[0]+"_mRNA_FASTA.faa","CDS")
else:
    create_rna_fasta(output_location + "/" + anno_file_name.split("/")[-1].split(".gbk")[0]+"_tRNA_FASTA.faa","tRNA")
    create_rna_fasta(output_location + "/" + anno_file_name.split("/")[-1].split(".gbk")[0]+"_rRNA_FASTA.faa","rRNA")
    create_rna_fasta(output_location + "/" + anno_file_name.split("/")[-1].split(".gbk")[0]+"_mRNA_FASTA.faa","CDS")

