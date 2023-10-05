This directory contains profile files for running snakemake across the entire HPC.

Place the downloaded files, `config.yaml` and `slurm-status.py` (which is called by the `config.yaml` file), in `.config/snakemake/slurm`. Consider using the command below immediately after `git clone`:

```
( cd portable-snakemake-workflows && mkdir -p $HOME/.config/snakemake/slurm && mv dotfiles/config.yaml $HOME/.config/snakemake/slurm && mv dotfiles/slurm-status.py $HOME/.config/snakemake/slurm && cd - )
```

Upon placement of the files, any snakefile may be run at default setting resources (in `config.yaml`) in the slurm job scheduler across the HPC with:
```
snakemake -s snakefile --profile slurm
```
