#!/bin/sh

# Enable command echo
set -v

# Run experiments
echo "Run telstra standard experiments"
python icarus.py --results results-standard.pickle config/youtube/telstra-standard.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results-standard.pickle > results/results-telstra-youtube-standard.txt
echo "Results are saved to file results.txt"