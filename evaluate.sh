#!/bin/bash
#SBATCH --job-name=rlcard
#SBATCH --time=300:00:00
#SBATCH --mem=96G
#SBATCH --cpus-per-task=4
#SBATCH --exclude=linux41,linux42,linux43,linux44,linux45
#SBATCH --partition=compsci

source /home/users/shuai/venv/rlcard/bin/activate
hostname

## ai vs human
python3 evaluate_human.py --ai_agent dmc --model_path results/dmc_swy_1.0/bailongmen/model.tar

## ai vs random baseline
# python3 evaluate.py --ai_agent dmc --model_path results/dmc_swy_1.0/bailongmen/model.tar --baseline_agent random

## ai vs rule-based baseline
# python3 evaluate.py --ai_agent dmc --model_path results/dmc_swy_1.0/bailongmen/model.tar --baseline_agent rule-based
