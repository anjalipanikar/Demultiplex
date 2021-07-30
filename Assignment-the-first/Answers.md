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
    ``` Read 1 Nucleotide Quality Score Distribution```  
    ![read1](https://user-images.githubusercontent.com/52551690/127605116-afde4c14-cac9-479e-b74d-901c19138101.jpeg)  
    
    ``` Read 2 Nucleotide Quality Score Distribution```  
    ![read2](https://user-images.githubusercontent.com/52551690/127605235-fcde86c2-de8c-4b86-9a78-c76bd29630c1.jpeg)  
    
    ``` Index 1 Nucleotide Quality Score Distribution```  
    ![index1](https://user-images.githubusercontent.com/52551690/127605279-8872b689-1860-4bd3-8e8a-621b363476e5.jpeg)  
    
    ``` Index 2 Nucleotide Quality Score Distribution```  
    ![index2](https://user-images.githubusercontent.com/52551690/127605356-ea9afaf6-6203-460b-a4c9-fb71a2cc40b3.jpeg)      
    
## Part 2
1. Define the problem

``` We are given 4 files, 2 read files and 2 index files. Some of the indexes in the index file are mismatched with the corresponding reads, as the data is index hopped. Because some indexes are potentially.   ```

3. Describe output

``` 48 index bin files for 24 different indexes for read 1 and 2, 2 files with index hopped read pairs for read 1 and 2, 2 files for undetermined quality pairs```

5. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
6. Pseudocode

open I1 I2 R1 R2

read record from both I1 and I2 

concatenate index with - 

if index 1 and 2 have N or elif Qs > cutoff 
    write to bad R1 and R2 with same index header 

elif 

index 2 is rev comp of index 1 

no need to have rev comp in set 

8. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
