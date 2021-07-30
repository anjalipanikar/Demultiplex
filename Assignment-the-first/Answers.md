# Assignment the First

## Part 1
1. Be sure to upload your Python script.

| File name | label |
|---|---|
| 1294_S1_L008_R1_001.fastq.gz | Read 1 |
| 1294_S1_L008_R2_001.fastq.gz | Index 1 |
| 1294_S1_L008_R3_001.fastq.gz | Index 2 |
| 1294_S1_L008_R4_001.fastq.gz | Read 2 |

2. Per-base NT distribution    
   i.  
   
       Read 1 Nucleotide Quality Score Distribution  
      ![read1](https://user-images.githubusercontent.com/52551690/127605116-afde4c14-cac9-479e-b74d-901c19138101.jpeg)  
        
       Read 2 Nucleotide Quality Score Distribution 
      ![read2](https://user-images.githubusercontent.com/52551690/127605235-fcde86c2-de8c-4b86-9a78-c76bd29630c1.jpeg)  
    
       Index 1 Nucleotide Quality Score Distribution 
      ![index1](https://user-images.githubusercontent.com/52551690/127605279-8872b689-1860-4bd3-8e8a-621b363476e5.jpeg)  
    
       Index 2 Nucleotide Quality Score Distribution 
      ![index2](https://user-images.githubusercontent.com/52551690/127605356-ea9afaf6-6203-460b-a4c9-fb71a2cc40b3.jpeg)      
    
## Part 2
1. Define the problem

``` We are given 4 files, 2 read files and 2 index files. Some of the indexes in the index file are mismatched with the corresponding reads, as the data is index hopped. Because some indexes are potentially swapped, we must develop and alogorithm to seperate the index swapped reads from the matched index reads, in order to filter out the high quality data.   ```

3. Describe output

``` 48 index-pair reads bin files for 24 different indexes for read 1 and 2, 2 files with index hopped read pairs for read 1 and 2, 2 files for undetermined low quality pairs```

5. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).

   Unit Tes Files:  
   ``` - R1_unittest.fastq ```    
   ``` - R2_unittest.fastq ```  
   ``` - I1_unittest.fastq ```  
   ``` - I2_unittest.fastq ```  
   
   Output Files:
   ``` - matched_R1.fastq ```     
   ``` - matched_R2.fastq ```   
   ``` - swapped_R1.fastq ```   
   ``` - swapped_R2.fastq ```  
   ``` - bad_R1.fastq ```     
   ``` - bad_R2.fastq ```   


7. Pseudocode
   
   Make a set() of known indexes   
      Open I1, I2, R1, R2   
      While files open    
         read record from I1      
         read record from I2  
         read header from R1   
         read header from R2  
         index_header = I1 + rev comp(I2)    
         new header_R1 = header_R1 + index_header   
         new_header_R2 = header_R2 + index_header      
         if ("N" is in I1 or I2) or (Qscore < Cutoff):           
         write to bad R1 and bad R2 with new headers    
         else if I1 and I2 in Known Indexes    
            if R1 == revs_comp(R2)   
            write to matched R1 and R2   
            else: 
               write to swapped R1 and R2  
         else:    
           wite to bad R1 and R2  

8. High level functions. For each function, be sure to include:  
    1. Description/doc string      

      convert_phred(): takes a letter quality score and converts it to the number phred score   
      reverse_compliment(): takes a string sequence and returns it's reverse compliment    
      average_quality(): takes a sequence of quality scores and returns the average quality score of the sequence     

    3. Function headers (name and parameters)    

      convert_phred(letter_score)  
      reverse_compliment(sequence)  
      average_quality(qscore_line)      

    5. Test examples for individual functions        

      convert_phred():  
         Input: E  
         Output: 36    
         
      reverse_compliment():    
         Input: TGTTCCGT  
         Output: ACGGAACA               
      
      average_quality():     
         Input: #AAAFJJ<    
         Output: 30.5  
         
    7. Return statement        

         convert_phred(letter_score):    
            return Qscore
            
         reverse_compliment(sequence):    
            return rev_comp  
            
         average_quality(qscore_line):      
            return average_qual     
            
            
         
         
         
         
