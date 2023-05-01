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



#### ***Input data***
We will retrieve publicly available genomic sequence data from [NCBI](https://www.ncbi.nlm.nih.gov/) using customized
steps. The file `RVFV.combined.csv` contains a list of RVFV strains and each of the 3 genomic segment
accession numbers as well as related metadata. The first column is the name of the RVFV `strain`. Columns `2`, `3` and `4` 
are the `accessions` for the `L`, `M` and `S` genomic segments sequences.



1. We will create separate directories (for each genomic segment) to store the genomic sequences in `fasta` format retrieved from NCBI.
   ```
   cd
   mkdir -p rvfv-typing-tutorial/{S,M,L}
   cd rvfv-typing-tutorial
   ```
2. Download the `RVFV.combined.csv` file
   ```
   wget -c https://raw.githubusercontent.com/ajodeh-juma/rvfv-typing-tutorial/master/RVFV.combined.csv
   ```
3. Extract `L` segment accessions
   ```
   awk -F ',' '{if (NR==1) printf "accession\n"; else printf "%s\n", $2}' RVFV.combined.csv > L-segment-accessions.txt
   ```




