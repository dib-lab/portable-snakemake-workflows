#! /bin/bash

# Check if the argument k_values has at least one value provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <k_values>"
    exit 1
fi

# Check provided arguments for whole, non-negative numbers
for arg in "$@"; do
    if ! [[ $arg =~ ^[0-9]+$ ]]; then
        echo "Error: '$arg' is not a valid whole, non-negative number."
        exit 1
    fi
done

# Define an array of k_values from arguments
k_values=("$@")

# Loop through the k_values and submit separate jobs for each
for k in "${k_values[@]}"; do
    echo "sbatch --job-name='create-fg-k${k}-db' fastgather-db-job.sh ${k}"
    sbatch --job-name="create-fg-k${k}-db" fastgather-db-job.sh "$k"
done
