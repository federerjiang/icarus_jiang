#!/bin/sh

# Enable command echo
set -v

# Run all experiments
sh run-tree.sh ; sh run-tree-snm.sh; sh run-telstra.sh; sh run-telstra-snm.sh ; sh run-sinet.sh; sh run-sinet-snm.sh; sh run-geant.sh; sh run-geant-snm.sh