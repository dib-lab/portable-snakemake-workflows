# dotfiles

Configuration files for running snakemake with the `--profile` argument. This allows dynamic workflows to utilizing HPC resources in a holistic way. 

## config.yaml

This is the configuration of the `--profile`. It contains default allocations for both `sbatch` and `snakemake`.

## slurm-status.py

A script called by `config.yaml` for better cluster performance. See https://snakemake.readthedocs.io/en/stable/tutorial/additional_features.html#using-cluster-status for details.

# workflows

Snakemake files for creating retrieving, sketching, gathering, and parsing data commonly used in the Data Intensive Biology lab at the University of California, Davis. 

There is a directory housing the configuration and environment files called by the workflow. In addition, the metadata directory contains a `SraRunTable.txt` file for an example dataset from [CAMI](https://www.microbiome-cosi.org/). 

## Sourmash workflows

### 1. download-sketch
A set of fast, robust approaches to temporarily downloading sequence files from archives and sketch sourmash signatures.

### 2. extract-prefetch
An efficient approach to temporarily extract the sketches in sourmash signatures that are passed into a prefetch method for `sourmash gather` results via `picklists`.

### 3. sbt-lca-databases
**[WIP]** A workflow to take any existing sourmash database and create a Sequence Bloom Tree (SBT) index and Lowest Common Ancestor (LCA) database.

This was curated using existing scripts from the repo -> https://github.com/dib-lab/2018-ncbi-lineages