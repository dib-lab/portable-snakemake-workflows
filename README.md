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

#### Quickstart:
To begin, for ssh:
```
git clone git@github.com:dib-lab/portable-snakemake-workflows.git
```

For https:
```
git clone https://github.com/dib-lab/portable-snakemake-workflows.git
```

Consider using the command below immediately after `git clone` to correctly place the dotfiles for `--profile` arugments on an HPC using slurm:
```
( cd portable-snakemake-workflows && mkdir -p $HOME/.config/snakemake/slurm && mv dotfiles/config.yaml $HOME/.config/snakemake/slurm && mv dotfiles/slurm-status.py $HOME/.config/snakemake/slurm && cd - )
```

The following portable workflows will run sequentially.

### 1a. download-sketch
A set of fast, robust approaches to temporarily downloading sequence files from archives and sketch sourmash signatures.

#### Quickstart:
If the dotfiles have been properly installed, run:
```
snakemake -s download-sketch-cluster --resources allowed_jobs=100 --profile slurm
```

This will download and sketch the CAMI dataset into the `sigs` directory at scale of 1000 and kmer size of 21, 31, and 51. These values are set in the `download-sketch-config.yaml` and may be changed there at any time. 

### 2a. extract-prefetch
An efficient approach to temporarily extract the sketches in sourmash signatures that are passed into the 'preferred' prefetch method. Creating a `picklist` for rapid `sourmash gather` results.

#### Quickstart:
(While on the Farm HPC) From within the `scripts` directory, run `./fastgather-db-submit-jobs.sh` to create the proper structureed GTDB databases for `fastgather` to run.

If the dotfiles have been properly installed and `download-sketch` has been successfully ran, run:
```
snakemake -s extract-prefetch-cluster --resources allowed_jobs=100 --profile slurm
```

This will temporarily extract all k-sizes and create a `prefetch` csv file of the CAMI sketches in the `gather/prefetch` directory for the scale and k value set in the `extract-prefetch-config.yaml`. 

### 1b. sbt-lca-databases
**[WIP]** A workflow to take any existing sourmash database and create a Sequence Bloom Tree (SBT) index and Lowest Common Ancestor (LCA) database.

This was curated using existing scripts from the repo -> https://github.com/dib-lab/2018-ncbi-lineages

An additional script, `find-rank-kmers.py` was included to extract the rank-specific kmers from an LCA database.
```
usage: find-rank-kmers.py [-h] -o OUTPUT [-s SAVE_NAMES] lca_db keep_rank

positional arguments:
  lca_db
  keep_rank             Keep the rank specified (i.e. Species)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output signature containing rank-specific hash values
  -s SAVE_NAMES, --save-names SAVE_NAMES
                        save list of matching signature names from that lineage to this file
```

TODO:
1. create example dataset using `sourmash sketch fromfile` to run the workflow 
  - using a set of fasta genomes currently from [refseq plastid](https://ftp.ncbi.nih.gov/refseq/release/plastid/) 
2. combine into single cmd with ( && )
  - `mkdir dbs`
  - `cd dbs`
  - `wget -c ftp://ftp.ncbi.nih.gov/refseq/release/plastid/plastid.3.1.genomic.fna.gz -o plastid.3.1.genomic.fna.gz`
  - `sourmash sketch dna -p scaled=100,k=21,k=31,k=51 -p scaled=1000,k=21,k=31,k=51 --singleton plastid.3.1.genomic.fna.gz -o plastid.3.1.genomic.sig.gz`
  - ...
  - `cd ..`
  - `snakemake -s sbt-lca-databases -j?`