# SDSP Pipeline  
**Simulation, Destruction and Structure Prediction Pipeline**

## 📌 Overview
This repository contains the implementation of the SDSP pipeline, a workflow for generating RNA Alignments, destroying RNA Secondary Structure, prediction of existing RNA Secondary Strucutre and analyzing the Results.

The pipeline consists of four main steps:
1. **Simulation** of RNA sequences using SISSI  
2. **Destruction** of RNA secondary structure using SISSIz, multiperm, and aln-shuffle  
3. **Structure prediction** using tools such as SISSIz, RNAz, and PETfold  
4. **Evaluation** of prediction performance (e.g., boxplots, confusion matrices, and ROC curves)

The goal of this pipeline is to compare the performance of the individual tools.

## Tools

Most of the tools are available online and can be downloaded from their respective websites. If a tool is not publicly available, you can contact me or the tool’s creator for access.

- SISSI 0.99  
- SISSIz 3.0  
- multiperm 0.94  
- aln-shuffle  
- RNAz 2.1.1  
- PETfold 2.2

## ⚙️ Pipeline Workflow

![Pipeline Diagram](images/Pipeline.drawio.png)

The SDSP pipeline provides an overview of the complete analysis process:

1. **Positive datasets** are generated using SISSI, based on defined nucleotide frequency distributions. A total of 100,000 sequences per parameter set are created.  
2. **Negative control sequences** are generated from the positives using SISSIz, Multiperm, and aln-Shuffle. Each positive sequence yields five negative variants, preserving mono- and dinucleotide frequencies (SISSIz, Multiperm) or producing random permutations (aln-Shuffle). About 500,000 negative datasets are generated for evaluation.  
3. **Structure prediction** is performed using SISSIz, RNAz, and PETfold. Positive datasets retain secondary structure, while negative datasets exhibit disrupted structures.  
4. **Evaluation** is conducted in Python using pandas, numpy, matplotlib, seaborn, and scikit-learn. Boxplots illustrate structural disruption, and ROC curves evaluate classification performance.

This workflow allows a comprehensive assessment of sequence randomization methods and RNA structure prediction tools.

## 🚀 Usage

### 1. Clone the repository
```bash
git clone https://github.com/Faragas91/SDSP-Pipeline.git
cd SDSP-Pipeline
```
### 2. Create a Conda enviroment with python 3.8, 3.9 or 3.10

``` bash
conda create -n sdsp_pipeline python=3.9
conda activate sdsp_pipeline
```
