---
title: README.md
tags: ["RVFV", "typing", "lineage", "segment"]
---
# **Rift Valley fever lineage assignment**
---
###### ***Trainers***: [John Juma](https://github.com/ajodeh-juma), Tulio de Oliveira
---

- [Introduction](#introduction)
- [Scope](#scope)
- [Set-Up](#setup)
    - [Input data](#input-data)


## Introduction
Rift Valley fever (RVFV) is a febrile zoonotic disease with epidemic potential in sub-Saharan Africa.
RVF was first reported in the great rift valley region of Kenya in a town called Naivasha following 
an 'abortion storm' in a sheep farm.
The disease is often transmitted through bites from infected mosquitoes. The causative agent, Rift 
Valley fever virus (RVFV) can be transmitted to both livestock and animals. RVF leads to death, and is
a great concern to public and livestock health personnel. Currently, there are 15 known circulating lineages designated
A-O ([Grobelaar et al. 2011](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3311189/)).

## Scope
In this short tutorial, we will walk through the lineage assignemnt of RVFV genomic sequences using
the web application available as part of the Genome Detective suite of typing tools 
and a command line implementation in a domain specific language.


## Prerequisite

For the web application programme, no prerequisite knowledge in command line/UNIX is required
However, for the command line implementation, familiarity with basic Linux command-line is required.


### Set-Up
For RVFV typing on the web, we will access the tool via [Genome Detective](https://www.genomedetective.com/app/typingtool/rvfv/)
while for the command line, we will install the tool from the [github repository](https://github.com/ajodeh-juma/rvfvtyping).

1. Clone the [github repository](https://github.com/ajodeh-juma/rvfvtyping) as indicated below:
   ```
   cd ~/Downloads
   git clone https://github.com/ajodeh-juma/rvfvtyping.git
   cd rvfvtyping
   conda env create -n rvfvtyping-env -f environment.yml
   conda activate rvfvtyping-env
   ```


#### ***Input data***
We will retrieve publicly available genomic sequence data from [NCBI](https://www.ncbi.nlm.nih.gov/) using customized
steps. The file `RVFV.combined.csv` contains a list of RVFV strains and each of the 3 genomic segment
accession numbers as well as related metadata. The first column is the name of the RVFV `strain`. Columns `2`, `3` and `4` 
are the `accessions` for the `L`, `M` and `S` genomic segments sequences.


1. Clone the tutorial repository
   ```
   cd ~/Downloads
   git clone https://github.com/ajodeh-juma/rvfv-typing-tutorial.git
   cd rvfv-typing-tutorial
   ```
   
2. We will create separate directories (for each genomic segment) to store the genomic sequences in `fasta` format retrieved from NCBI.

    ```
    mkdir -p ./{S,M,L}
    ```

3. Extract `L` segment accessions
   ```
   awk -F ',' '{if (NR==1) printf "accession\n"; else printf "%s\n", $2}' RVFV.combined.csv > L/L-segment-accessions.txt
   ```


4. Retrieve the sequences using auxilliary python script provided 
   ```
   python scripts/accessionsToSequences.py \
        --accessions L/L-segment-accessions.txt \
        --fasta L/L-segment.fasta \
        --database nucleotide \
        --min-len 6000 \
        --max-len 6500 \
        --out_dir L/data \
        --cleanup True
   ```


5. Extract `M` segment accessions
   ```
   awk -F ',' '{if (NR==1) printf "accession\n"; else printf "%s\n", $3}' RVFV.combined.csv > M/M-segment-accessions.txt
   ```


6. Retrieve the sequences using auxilliary python script provided 
   ```
   python scripts/accessionsToSequences.py \
        --accessions M/M-segment-accessions.txt \
        --fasta M/M-segment.fasta \
        --database nucleotide \
        --min-len 3500 \
        --max-len 3900 \
        --out_dir M/data \
        --cleanup True
   ```


5. Extract `S` segment accessions
   ```
   awk -F ',' '{if (NR==1) printf "accession\n"; else printf "%s\n", $4}' RVFV.combined.csv > S/S-segment-accessions.txt
   ```


6. Retrieve the sequences using auxilliary python script provided 
   ```
   python scripts/accessionsToSequences.py \
        --accessions S/S-segment-accessions.txt \
        --fasta S/S-segment.fasta \
        --database nucleotide \
        --min-len 1500 \
        --max-len 1700 \
        --out_dir S/data \
        --cleanup True
   ```

