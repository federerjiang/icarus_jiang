#!/bin/sh

# Enable command echo
set -v

rm results.pickle


# Run experiments
echo "Run experiments"
python icarus.py --results results.pickle config.py
echo "Simulation is finished"