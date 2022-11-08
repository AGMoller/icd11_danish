#!/bin/bash

#SBATCH --job-name=icd11_scraper    # Job name
#SBATCH --output=outputs/icd11_scraper.%j.out      # Name of output file (%j expands to jobId)
#SBATCH --cpus-per-task=16       # Schedule one core
#SBATCH --time=24:00:00          # Run time (hh:mm:ss) - run for one hour max
#SBATCH --partition=brown    # Run on either the Red or Brown queue
#SBATCH --mail-type=BEGIN,FAIL,END    # Send an email when the job finishes or fails

python src/icd11_client.py