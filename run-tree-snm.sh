#!/bin/sh

# Enable command echo
set -v

# rm results.pickle


# Run experiments
echo "Run tree standard experiments"
python icarus.py --results results-standard.pickle config/snm/tree-standard.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results-standard.pickle > results/tree-snm.txt
echo "Results are saved to file results.txt"


echo "Run tree edge experiments"
python icarus.py --results results-edge.pickle config/snm/tree-edge.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results-edge.pickle >> results/tree-snm.txt
echo "Results are saved to file results.txt"

echo "Run tree coordinated edge experiments"
python icarus.py --results results-coor-edge.pickle config/snm/tree-coor-edge.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results-coor-edge.pickle >> results/tree-snm.txt
echo "Results are saved to file results.txt"
