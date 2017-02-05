#!/bin/sh

# Enable command echo
set -v

rm results.pickle


# Run experiments
echo "Run experiments"
python icarus.py --results results.pickle config/youtube/geant.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results.pickle > results/geant-youtube.txt
echo "Results are saved to file results.txt"
