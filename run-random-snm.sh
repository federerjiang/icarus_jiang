#!/bin/sh

# Enable command echo
set -v

rm results.pickle


# Run experiments
# echo "Run experiments"
# python icarus.py --results results.pickle config/snm/random.py
# echo "Simulation is finished"
# echo "Get Results: Latency and Hit Ratios"
# python printresults.py results.pickle > results/random-snm.txt
# echo "Results are saved to file results.txt"

echo "Run experiments"
python icarus.py --results results.pickle config/snm/random1.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results.pickle > results/random1-snm.txt
echo "Results are saved to file results.txt"

# echo "Run experiments"
# python icarus.py --results results.pickle config/snm/random2.py
# echo "Simulation is finished"
# echo "Get Results: Latency and Hit Ratios"
# python printresults.py results.pickle > results/random2-snm.txt
# echo "Results are saved to file results.txt"

# echo "Run experiments"
# python icarus.py --results results.pickle config/snm/random3.py
# echo "Simulation is finished"
# echo "Get Results: Latency and Hit Ratios"
# python printresults.py results.pickle > results/random3-snm.txt
# echo "Results are saved to file results.txt"
