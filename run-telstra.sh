#!/bin/sh

# Enable command echo
set -v

# rm results.pickle


# Run experiments
echo "Run telstra standard experiments"
python icarus.py --results results-standard.pickle config/telstra-standard.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results-standard.pickle > results/telstra-irm.txt
echo "Results are saved to file results.txt"


echo "Run telstra edge experiments"
python icarus.py --results results-edge.pickle config/telstra-edge.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results-edge.pickle >> results/telstra-irm.txt
echo "Results are saved to file results.txt"

echo "Run telstra coordinated edge experiments"
python icarus.py --results results-coor-edge.pickle config/telstra-coor-edge.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results-coor-edge.pickle >> results/telstra-irm.txt
echo "Results are saved to file results.txt"
