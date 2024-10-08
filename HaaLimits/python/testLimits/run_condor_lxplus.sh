#!/bin/bash
cd /afs/cern.ch/user/f/fengwang/workplace/CombinedLimits/CMSSW_11_3_4/src/

eval $(scramv1 runtime -sh)

cd CombineLimitsRunII/HaaLimits/python/testLimits/


echo "Arguments passed to this script are: "
echo "  for 1 (m): $1"
echo "  for 2 (MA): $2"
echo "  for 3 (datacard): $3"
echo "  for 4 (name): $4"
echo "  for 5 (output): $5"

combine -M AsymptoticLimits -m ${1} --setParameters MA=${2} --rMin 0 --rMax 1 --freezeParameters=MA ${3} -n ${4}
mkdir H${1}
mv ${5} H${1}
