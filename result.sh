#!/bin/sh

# Enable command echo
set -v

# Run experiments
echo "Get Results: Latency and Hit Ratios"
python printresults.py results.pickle > results.txt
echo "Results are saved to file results.txt"