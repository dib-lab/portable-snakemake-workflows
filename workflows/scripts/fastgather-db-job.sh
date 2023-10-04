#! /bin/bash -login

#SBATCH -p med2
#SBATCH -t 12:00:00
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH --mem=5G
#SBATCH -o ./slurm.%j.out
#SBATCH -e ./slurm.%j.err

k=$1

# activate conda
. /home/$USER/miniconda3/etc/profile.d/conda.sh

# activate sourmash env
conda activate sourmash

# make things fail on errors
set -e # exit when exit code is 0
set -o nounset
set -o errexit

cd ../dbs/

# make fastgather databases!
mkdir "gtdb-rs214-reps-k$k/"
cd "gtdb-rs214-reps-k$k/"
sourmash sig split -k $k /group/ctbrowngrp/sourmash-db/gtdb-rs214/gtdb-rs214-reps.k$k.zip -E .sig.zip
cd ..
find "gtdb-rs214-reps-k$k/" -name "*.sig.gz" -type f > "list.gtdb-rs214-reps-k$k.txt"
