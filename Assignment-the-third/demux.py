import argparse

def get_args(): #function to parse command line arguments
    parser = argparse.ArgumentParser(description=" ")
    parser.add_argument("-r1", "--read1", help="input file for read 1", required=True)
    parser.add_argument("-r2", "--read2", help="input file for read 2", required=True)
    parser.add_argument("-i1", "--index1", help="input file for index 1", required=True)
    parser.add_argument("-i2", "--index2", help="input file for index 2", required=True)
    return parser.parse_args() 

def revcomp(seq): #function to reverse compliment sequence   
    rev_seq = ''
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    for base in reversed(seq):
        rev_seq += complement[base]
    return rev_seq

def convert_phred(letter): #function to convert letter phred score to quality score number
    dec = ord(letter)
    phred = dec - 33
    return phred

def qual_score(phred_score): #function to return avergage number quality scores for sequence line 
    sum = 0
    for score in phred_score:
        converted_score = convert_phred(score)
        sum = sum + converted_score
    avg = sum/(len(phred_score))
    return avg
