#!/bin/sh

# Enable command echo
set -v

rm results.pickle


# Run experiments
# echo "Run experiments"
# python icarus.py --results results.pickle config/random.py
# echo "Simulation is finished"
# echo "Get Results: Latency and Hit Ratios"
# python printresults.py results.pickle > results/random-irm.txt
# echo "Results are saved to file results.txt"


echo "Run experiments"
python icarus.py --results results.pickle config/random.py
echo "Simulation is finished"
echo "Get Results: Latency and Hit Ratios"
python printresults.py results.pickle > results/random-irm.txt
echo "Results are saved to file results.txt"

# echo "Run experiments"
# python icarus.py --results results.pickle config/random2.py
# echo "Simulation is finished"
# echo "Get Results: Latency and Hit Ratios"
# python printresults.py results.pickle > results/random2-irm.txt
# echo "Results are saved to file results.txt"

# echo "Run experiments"
# python icarus.py --results results.pickle config/random3.py
# echo "Simulation is finished"
# echo "Get Results: Latency and Hit Ratios"
# python printresults.py results.pickle > results/random3-irm.txt
# echo "Results are saved to file results.txt"