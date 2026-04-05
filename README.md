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
