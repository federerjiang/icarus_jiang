#!/bin/sh

# Enable command echo
set -v

# Run all experiments
python icarus.py --results results.pickle config/tree-edge.py; python printresults.py results.pickle > results/tree-edge-irm.txt