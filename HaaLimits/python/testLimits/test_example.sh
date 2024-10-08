#!/bin/bash
cd /afs/cern.ch/user/f/fengwang/workplace/CombinedLimits/CMSSW_11_3_4/src/

eval $(scramv1 runtime -sh)

cd CombineLimitsRunII/HaaLimits/python/testLimits/

combine -M AsymptoticLimits -m 125 --setParameters MA=40 --rMin 0 --rMax 1 --freezeParameters=MA datacards_shape/MuMuTauTau/mmmt_mm_h_parametric_unbinned_highmass_TauHadTauHad_V3_2018_MVAMedium_DG_DoubleExpo_yRange_Spline_wFakeTauScaleJEC_hm1000_amX.txt -v 2 --saveToys --expectSignal=1
