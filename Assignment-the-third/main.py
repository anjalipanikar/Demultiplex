#!/usr/bin/env python

########################################################################################################
# Program: Dual-Matched Index Demuliplexling Algorithm for Illumina Sequencing Data
#  
# Creator: Geethanjali Panikar 
#
# Description: An algorithm to separate dual-matched unique index bar codes of Illumina sequencing 
# data into respective unique index files. Algorithm additionally filters data for unwwanted 'swapped' 
# indexes, unidentifiable indexes, and low quality index and sequences data. Program beneficial 
# for determining which sequences came from which samples after they have all be sequenced together. 
# 
# Input: Four files, two read-pair files (Read 1 and Read 2) and two index-pair files
#
# Output: to output directory, 52 files, 48 unique index files for 24 unique indexes present between both 
# Read 1 and Read 2, 2 swapped files for swapped index data for both Read 1 and Read 2, and 2 poor quality 
# files for poor quality data in both Read 1 and Read 2. 
# 
# Arguments to Run Program: $ python3 main.py -r1 <Read 1> -r2 <Read 2> -i1 <Index 1> -i2 <Index 2> 
#########################################################################################################

import dx_functions       
import os 
from os import path
import gzip

#collect arguments
args = demux.get_args()
r1 = args.read1
r2 = args.read2
i1 = args.index1
i2 = args.index2

#create set of known indexes to search from 
known_index_set = {'GTAGCGTA', 'AACAGCGA', 'CTCTGGAT', 'CACTTCAC', 'TATGGCAC', 'TCGACAAG', 'ATCGTGGT', 'GATCTTGC', 'CGATCGAT', 'TAGCCATG', 'TACCGGAT', 'GCTACTCT', 'TGTTCCGT', 'TCTTCGAC', 'TCGAGAGT', 'AGAGTCCA', 'GATCAAGG', 'CGGTAATC', 'CTAGCTCA', 'ACGATCAG', 'GTCCTAAG', 'ATCATGCG', 'TCGGATTC', 'AGGATAGC', 'bad', 'swap'}

#initialize a dictionary to contain index-specific filehandles 
index_dict = {}
for i in known_index_set:
    index_dict[str(i + "_R1")] = ''
    index_dict[str(i + "_R2")] = ''

#initialize a dictionary to contain count of number of reads per unique index 
index_count_dict = {}
for i in known_index_set:
    index_count_dict[i] = 0

 # ------------  OPEN FILES AND INITIALIZE VARIABLES --------------------# 

#open statistics output file 
f = open("output/stats.txt", "w")

#populate dictionary with filehandle objects and open all 52 files 
for i in index_dict.keys():
    path = "output"
    file = '{}.fastq'.format(i)
    joined = os.path.join(path,file)
    index_dict[i] = open(joined, "w")

#open sequence and index fastq files 
with gzip.open(r1, "rt") as read1, gzip.open(r2, "rt") as read2, gzip.open(i1, "rt") as index1, gzip.open(i2, "rt") as index2:

    #4 lists to hold current record for each input read and index file 
    r1_record = []
    r2_record = []
    i1_record = []
    i2_record = []

    #count number of lines in file
    line_count = 0
    for line in read1:
        if line != "\n":
            line_count += 1

    #initialize counters for stats
    total_reads = (line_count/4)
    matched = 0
    swapped = 0
    low_qual = 0

    #reset read1 file pointer for next loop
    read1.seek(0)

# ----------------- ALGORITHM FOR DEMULTIPLEXING DATA ---------------------- #

    j = 1    #line counter 
    for lineR1, lineR2, lineI1, lineI2 in zip(read1, read2, index1, index2): #simultaneously loop through each file
 
        #append first line of each file to respective record lists
        r1_record.append(lineR1.strip("\n"))
        r2_record.append(lineR2.strip("\n"))
        i1_record.append(lineI1.strip("\n"))
        i2_record.append(lineI2.strip("\n"))

        #if current line is last line of record (quality score line)
        if (j % 4 == 0):

            if "N" in i1_record[1] or "N" in i2_record[1]:
                low_qual += 1
                index_header = i1_record[1] + "-" + i2_record[1]
                new_header_R1 = r1_record[0] + " " + index_header #append index header to R1 header 
                new_header_R2 = r2_record[0] + " " + index_header #append index header to R1 header 
                i = 0
                for line1, line2 in zip(r1_record, r2_record): #loop through current read 1 and read 2 record 
                    if i == 0:
                        index_dict['bad_R1'].write(new_header_R1) #write headers with index concatenated to respective files 
                        index_dict['bad_R2'].write(new_header_R2)
                        index_dict['bad_R1'].write("\n")
                        index_dict['bad_R2'].write("\n")
                    else:
                        index_dict['bad_R1'].write(line1) #write full records out to respective files
                        index_dict['bad_R2'].write(line2)
                        index_dict['bad_R1'].write("\n") 
                        index_dict['bad_R2'].write("\n")
                    i += 1

            else:

                i2revcomp = demux.revcomp(i2_record[1]) #reverse compliment Index 2 sequence
                index_header = i1_record[1] + "-" + i2revcomp #create concatenated index header 
                new_header_R1 = r1_record[0] + " " + index_header #append index header to R1 header 
                new_header_R2 = r2_record[0] + " " + index_header #append index header to R1 header 
                qual_scoreI1 = demux.qual_score(i1_record[3]) #calculate average quality score of index 1 sequence 
                qual_scoreI2 = demux.qual_score(i2_record[3]) #calculate average quality score of index 2 sequence
                qual_scoreR1 = demux.qual_score(r1_record[3]) #calculate average quality score of read 1 sequence
                qual_scoreR2 = demux.qual_score(r2_record[3]) #calculate average quality score of read 2 sequence

                #if the current index 1 sequence and index 2 sequence are not in the known index set, do not have a quality score above 30, or reads do not have a qualiy score above 20
                if i1_record[1] not in known_index_set or i2revcomp not in known_index_set or qual_scoreI1 < 30 or qual_scoreI2 < 30 or qual_scoreR1 < 20 or qual_scoreR2 < 20:
                    low_qual += 1 #increment low quality counter
                    i = 0
                    for line1, line2 in zip(r1_record, r2_record): #loop through current read 1 and read 2 record 
                        if i == 0:
                            index_dict['bad_R1'].write(new_header_R1) #write headers with index concatenated to respective files 
                            index_dict['bad_R2'].write(new_header_R2)
                            index_dict['bad_R1'].write("\n")
                            index_dict['bad_R2'].write("\n")
                        else:
                            index_dict['bad_R1'].write(line1) #write full records out to respective files
                            index_dict['bad_R2'].write(line2)
                            index_dict['bad_R1'].write("\n") 
                            index_dict['bad_R2'].write("\n")
                        i += 1
                
                #if index 1 and reverse compliment of index 2 is in known index set
                elif i1_record[1] in known_index_set and i2revcomp in known_index_set: 
                    #if index1 equals the reverse compliment of index 2
                    if i1_record[1] == i2revcomp:
                        matched += 1 #increment match couunter 
                        index_count_dict[i1_record[1]] += 1 #increment index counter dict for specific index 
                        i = 0
                        for line1, line2 in zip(r1_record, r2_record): #write to respective matched index files 
                            key1 = i1_record[1] + "_R1"
                            key2 = i2revcomp + "_R2"
                            if i == 0:
                                index_dict[key1].write(new_header_R1)
                                index_dict[key2].write(new_header_R2)
                                index_dict[key1].write("\n")
                                index_dict[key2].write("\n")
                            else:
                                index_dict[key1].write(line1)
                                index_dict[key2].write(line2)
                                index_dict[key1].write("\n")
                                index_dict[key2].write("\n")
                            i += 1

                    else: #else if index 1 is NOT the reverse compliment but they both exist in the known index set
                        swapped += 1 #indexes are swapped, increment swapped counter 
                        i = 0
                        for line1, line2 in zip(r1_record, r2_record): #write to swapped file 
                            if i == 0:
                                index_dict['swap_R1'].write(new_header_R1)
                                index_dict['swap_R2'].write(new_header_R2)
                                index_dict['swap_R1'].write("\n")
                                index_dict['swap_R2'].write("\n")
                            else:
                                index_dict['swap_R1'].write(line1)
                                index_dict['swap_R2'].write(line2)
                                index_dict['swap_R1'].write("\n")
                                index_dict['swap_R2'].write("\n")
                            i += 1

            #clear record lists for current record to start the loop again
            r1_record = []
            r2_record = []
            i1_record = []
            i2_record = []
            
        j += 1 #increment outer for loop counter 


# --------------------- END OF LOOP, CLOSE ALL FILES, REPORT STATISTICS -------------------------#

for i in index_dict.values(): #close all 52 files 
    i.close()

read1.close() #close all input read and index files 
read2.close()
index1.close()
index2.close()

#write stats to stats.txt file

f.write(str("Demultiplexing Statistics" + "\n" + "\n"))
f.write(str( "Total number of R1 and R2 reads: " + str(total_reads) + "\n" + "\n"))
f.write(str("Percentage of reads from each unique index: " + "\n"))
for i in index_count_dict:
    if i == "bad" or i == "swap": 
        pass
    else:
        f.write(str(i + ": " + (str((index_count_dict[i]/total_reads)*100)) + "%" + "\n"))
f.write(str("\n" + "Total number of dual-matched read pairs: " + str(matched) + "\n" + "\n"))
f.write(str("Total number of unknown or low quality reads pairs: " + str(low_qual) + "\n" + "\n"))
f.write(str("Total number of index hopped reads pairs: " + str(swapped) + "\n" + "\n"))
f.write(str("Percentage of index hopped reads within the dataset: " + str((swapped/total_reads)*100) + "%" + "\n" + "\n"))

f.close()
