#!/bin/sh
#
echo "Git add command"
git add results/
echo "Git commit command"
git commit -m "get new results"
echo "Git push command"
git push -u origin master