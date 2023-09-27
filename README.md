# dotfiles

Configuration files for running snakemake with the `--profile` argument. This allows dynamic workflows to utilizing HPC resources in a holistic way. 

## config.yaml

This is the configuration of the `--profile`. It contains default allocations for both `sbatch` and `snakemake`.

## slurm-status.py

A script called by `config.yaml` for better cluster performance. See https://snakemake.readthedocs.io/en/stable/tutorial/additional_features.html#using-cluster-status for details.

# workflows

Snakemake files for creating retrieving, sketching, gathering, and parsing data commonly used in the Data Intensive Biology lab at the University of California, Davis. 

## download-sketch
A set of fast, robust approaches to temporarily downloading sequence files from archives and sketch sourmash signatures.

## prefetch