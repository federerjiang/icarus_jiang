#!/bin/sh

# Enable command echo
set -v

# rm results.pickle


# Run experiments
echo "Run tree standard experiments"
python icarus.py --results results-standard.pickle config/tree-standard.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results-standard.pickle > results/results-tree.txt
echo "Results are saved to file results.txt"


echo "Run tree edge experiments"
python icarus.py --results results-edge.pickle config/tree-edge.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results-edge.pickle >> results/results-tree.txt
echo "Results are saved to file results.txt"

echo "Run tree coordinated edge experiments"
python icarus.py --results results-coor-edge.pickle config/tree-coor-edge.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results-coor-edge.pickle >> results/results-tree.txt
echo "Results are saved to file results.txt"
