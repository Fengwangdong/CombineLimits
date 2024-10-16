#!/bin/bash
cd /afs/cern.ch/user/f/fengwang/workplace/CombinedLimits/CMSSW_11_3_4/src/

eval $(scramv1 runtime -sh)

cd CombineLimitsRunII/HaaLimits/python/testCLs/

combine -M HybridNew --LHCmode LHC-limits --saveToys --saveHybridResult -m 1000  --setParameters MA=40 --freezeParameters=MA -T 200 datacards_shape/MuMuTauTau/mmmt_mm_h_parametric_unbinned_highmass_TauHadTauHad_V3_2018_MVAMedium_DG_DoubleExpo_yRange_Spline_wFakeTauScaleJEC_hm1000_amX.txt --expectedFromGrid 0.16 --clsAcc 1 -v 2
