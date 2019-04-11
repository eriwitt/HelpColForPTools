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
import datetime
import os
import platform
import re
import ssl
import sys
import urllib2
operating_system = platform.system()

time1=datetime.datetime.now()
#####################################################################################################
# Functions
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
    out = response.read()
    organism_url = "https://www.genome.jp/dbget-bin/www_bget?gn:" + out.split("/dbget-bin/www_bget?gn:")[1].split('">')[0]
    response = urllib2.urlopen(organism_url)
    out = response.read()
    org_id = out.split("<nobr>Name</nobr>")[1].split("<br>")[0].split("><")[-1].split('">')[1].split(",")[0]
    id_id = 1
    report.write("\tKEGG organism identifier:\t" + org_id + "\n")
    report.write("\tSource:\t" + organism_url + "\n")
    print org_id    
    return id_id, org_id


def start_orgid_finding(gr_gbkfile):
    report.write("\nAutomatic Search of the KEGG organism identifier:\n\n")
    id_id = 0
    gbk_file = SeqIO.parse(gr_gbkfile, "genbank")
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
    gbk_file = SeqIO.parse(gr_gbkfile, "genbank")
    for record in gbk_file:
        no_tax = 0 # identifier no taxonomic id in source feature if it is 1
        no_bio = 0 # identifier no BioProject Accesion in record if it is 1
        if "source" in featl:
            for feature in record.features:
                # Check source qualifier in the annotation for the taxonomic id                                      
                if feature.type == "source":
                    for entry in feature.qualifiers["db_xref"]:
                        if "taxon:" in entry:
                            taxonomic_id = entry.split("taxon:")[1]
                            report.write("\tSource Feature:\n\tTaxonomic ID: " + str(taxonomic_id) + "\t")
                            anm = get_KEGG_orgid(taxonomic_id, 0)
                            id_id = anm[0]
                            org_id = anm[1]
                        else:
                            no_tax = 1
                    break
        if "source" not in featl or no_tax == 1:  
            # Extract taxonomic id from the bioproject ncbi entry. The bioproject accesion is extracted from the annotation.
            if "BioProject:" in str(record):
                ncbi_bio_pro_url = "https://www.ncbi.nlm.nih.gov/bioproject/?term=" + str(record).split("BioProject:")[1].split(",")[0]
                response = urllib2.urlopen(ncbi_bio_pro_url)
                out = response.read()
                if "No items found." not in out:
                    taxonomic_id = out.split("[Taxonomy ID: ")[1].split("]")[0]
                    report.write("\tBioProject Accesion:\t" + str(record).split("BioProject:")[1].split(",")[0] + "\tTaxonomic ID: " + str(taxonomic_id) + "\n\tSource: " + ncbi_bio_pro_url + "\n")
                    anm = get_KEGG_orgid(taxonomic_id, 1)
                    id_id = anm[0]
                    org_id = anm[1]
                    break
            else:
                no_bio = 1
                    
        # Organism name search for KEGG organism identifier
        if orgname != "" and no_bio == 1:
            report.write("\tOrganism: " + orgname + "\n")
            anm = get_KEGG_orgid_from_orgname(orgname, 2)
            id_id = anm[0]
            org_id = anm[1]
    if id_id == 0:
        report.write("The automatic search could not find the KEGG organism identifier! You should do a manual search on KEGG! If your organism is not in KEGG then the tool does not work!\n")
        print "The script couldn't find the KEGG organism identifier!!!"
        sys.exit(0)
    else:
        return org_id


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
            if answer1 == "y":
                if operating_system == "Windows":
                    fileipid=open(directory+"\\"+genename+".html","w")
                else:
                    fileipid=open(directory+"/"+genename+".html","w")

                fileipid.write(url + "\t" + str(datetime.datetime.now())+"\n")
                fileipid.write(out)
            for t in res1:
                if t not in res:
                    res.append(t)
        return res
    except urllib2.URLError:
        ssl._create_default_https_context = ssl._create_unverified_context
        search_ec_in_kegg(genename)
        


#####################################################################################################
# Script Input
storage_option = sys.argv[1]
kegg_organism_identifier = sys.argv[2]
gr_gbkfile = sys.argv[3]
gr_report = sys.argv[4]
gr_improved_gbk_path = sys.argv[5]
html_storage = ""
if storage_option == "y":
    if os.path.exists(sys.argv[6]):
        html_storage = sys.argv[6]
    else:
        os.mkdir(sys.argv[6])
        html_storage = sys.argv[6]
#####################################################################################################
report = open(gr_report,"w")
report.write("GBKREFINEMENT REPORT FILE\n"+str(datetime.datetime.now())+"\n")
report.write("\nSelected annotation to improve:\n\t" + gr_gbkfile + "\nLocation of the refined annotation:\n\t" + gr_improved_gbk_path + "\n")
if kegg_organism_identifier != "n":
	report.write("\nManual User Input for KEGG organism identifier:\n\t" + kegg_organism_identifier + "\n")
else:
	kegg_organism_identifier = start_orgid_finding(gr_gbkfile)

gbk_file = SeqIO.parse(gr_gbkfile,"genbank")
for record in gbk_file:
    ecs_before_refinement=[]
    additional_ecs_after_refinement=[]
    for feature in record.features:
        if feature.type == "CDS":
            if "EC_number" in feature.qualifiers:
                for ecnr in feature.qualifiers["EC_number"]:
                    if ecnr not in ecs_before_refinement:
                        ecs_before_refinement.append(ecnr)
    print len(ecs_before_refinement)
    report.write("\nThese ec numbers were already present in the annotation before refinement (delimited by TAB):\n")
    for ecnumber in sorted(ecs_before_refinement):
        report.write(ecnumber+"\t")
    report.write("\n\nThe following changes were made in the annotation.\n 'add' - means the EC number was added to an existing EC qualifier\n 'new EC qualifier' - means there was no ec qualifier before, so an EC qualifier with the found EC number was added to the annotation\n\nlocus_tag\tchanges\n\n")
    for feature in record.features:
        if feature.type == "CDS":
            if "locus_tag" in feature.qualifiers:
                ec = search_ec_in_kegg(kegg_organism_identifier, str(feature.qualifiers["locus_tag"]).split("['")[1].split("']")[0], storage_option, html_storage)
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
SeqIO.write(record,gr_improved_gbk_path,"genbank")
    
