#!/bin/sh

# Enable command echo
set -v

# rm results.pickle


# Run experiments
echo "Run experiments"
python icarus.py --results results.pickle config/try.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results.pickle > results/try.txt
echo "Results are saved to file results.txt"
