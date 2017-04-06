#!/bin/sh

# Enable command echo
set -v

# Run all experiments
python icarus.py --results results.pickle config/random.py; python printresults.py results.pickle > results/random-test-irm.txt