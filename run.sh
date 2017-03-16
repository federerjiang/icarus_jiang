#!/bin/sh

# Enable command echo
set -v

# Run all experiments
sh run-telstra.sh; sh run-telstra-snm.sh ; sh run-sinet-edge.sh; sh run-sinet-edge-snm.sh; sh run-geant.sh; sh run-geant-snm.sh