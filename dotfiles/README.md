This directory contains profile files for running snakemake across the entire HPC.

Place the downloaded files, `config.yaml` and `slurm-status.py` (which is called by the `config.yaml` file), in `.config/snakemake/slurm`. Consider using:
```
(( mkdir -p .config/snakemake/slurm && wget <rawgithttps of file> ))

Upon placement, any snakefile may be run at default setting resources (in `config.yaml`) with the slurm job scheduler across the HPC with:
```
snakemake -s snakefile --profile slurm
```
