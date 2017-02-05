#!/bin/sh

# Enable command echo
set -v

# Run all experiments
python get-telstra-snm.py geant-irm.txt geant-irm-stat.txt;
python get-telstra-snm.py geant-snm.txt geant-snm-stat.txt;
python get-telstra-snm.py sinet-irm.txt sinet-irm-stat.txt;
python get-telstra-snm.py sinet-snm.txt sinet-snm-stat.txt;
python get-telstra-snm.py tree-irm.txt tree-irm-stat.txt;
python get-telstra-snm.py tree-snm.txt tree-snm-stat.txt;
python get-telstra-snm.py telstra-irm.txt telstra-irm-stat.txt;
python get-telstra-snm.py telstra-snm.txt telstra-snm-stat.txt;