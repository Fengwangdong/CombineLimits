#!/bin/bash
cd /afs/cern.ch/user/f/fengwang/workplace/CombinedLimits/CMSSW_11_3_4/src/
eval $(scramv1 runtime -sh)
cd /afs/cern.ch/user/f/fengwang/workplace/CombinedLimits/CMSSW_11_3_4/src/CombineLimitsRunII/HaaLimits/python/testCLs/

combine -M HybridNew -v -1 --LHCmode LHC-limits --saveToys --saveHybridResult -m ${1} --setParameters MA=${2} --freezeParameters=MA -T 200 ${3} -n ${4} --expectedFromGrid 0.975 --clsAcc 1
mkdir H${1}
mv ${5}.123456.quant0.975.root H${1}
