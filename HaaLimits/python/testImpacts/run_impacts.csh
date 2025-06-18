#!/bin/csh
cd /afs/cern.ch/user/f/fengwang/workplace/CombinedLimits/CMSSW_11_3_4/src/
eval `scramv1 runtime -csh`
cd CombineLimitsRunII/HaaLimits/python/testImpacts/

echo "Example complete command: csh run_impacts.csh 125 mt 2018 highmass"
setenv h 125
if ($1 != 125 && $1 != 250 && $1 != 500 && $1 != 750 && $1 != 1000) then
   echo "Please specify the correct H mass! eg: 125, 250, 500, 750, 1000"
   exit
else
   setenv h $1
endif

setenv channel TauHadTauHad_V3
if ($2 != tt && $2 != mt && $2 != et && $2 != me && $2 != all) then
   echo "Please specify the correct channel! eg: tt, mt, et, me, all"
   exit
else if ($2 == tt) then
   setenv channel TauHadTauHad_V3
else if ($2 == mt) then
   setenv channel TauMuTauHad_V2
else if ($2 == et) then
   setenv channel TauETauHad
else if ($2 == me) then
   setenv channel TauMuTauE
else if ($2 == all) then
   setenv channel allchs
endif

setenv year 2018
if ($3 != 2016 && $3 != 2017 && $3 != 2018 && $3 != all) then
   echo "Please specify the correction era! eg: 2016, 2017, 2018, all"
   exit
else if ($3 == all) then
   setenv year 2016_2017_2018
else
   setenv year $3
endif


setenv region highmass
if ($4 != lowmass && $4 != upsilon && $4 != highmass && $4 != highmass2) then
   echo "Please specify the correct region! eg: lowmass, upsilon, highmass, highmass2 #NOTE: highmass2 is only for H1000 (40-50GeV)"
   exit
else
   setenv region $4
endif

if ($channel == TauETauHad && $region == lowmass && ($h == 125 || $h == 250)) then
   echo "NOT consider lowmass region for TauETauHad channel for H125 and H250, Skip!"
   exit
else if ($channel == TauETauHad && ($region == lowmass || $region == upsilon) && ($h == 500 || $h == 750 || $h == 1000)) then
   echo	"Neither consider lowmass nor upsilon region for TauETauHad channel for H500, H750, H1000, Skip!"
   exit
else if ($region == highmass2 && ($h == 125 || $h == 250 || $h == 500 || $h == 750)) then
   echo "Not consider highmass2 for H125, H250, H500, H750, Skip!"
   exit
endif

   	     
setenv amass $5
if ($region == lowmass && !($amass <= 8)) then
   setenv amass 6.0
else if ($region == upsilon && !($amass >= 8 && $amass <= 12)) then
   setenv amass 10.0
else if ($region == highmass && !($amass >= 12 && $amass <= 30)) then
   setenv amass 15.0
else if ($region == highmass2 && !($amass >= 30)) then
   setenv amass 40.0
endif
      	      
if ($channel == TauMuTauHad_V2) then
   setenv channelT TauMuTauHad
   setenv Tfunc MVAMedium_DG_DoubleExpo_yRange_wFakeTauScale
   
else if ($channel == TauHadTauHad_V3) then
   setenv channelT TauHadTauHad
   setenv Tfunc MVAMedium_DG_DoubleExpo_yRange_Spline_wFakeTauScaleJEC
             
else if ($channel == TauMuTauE) then
   setenv channelT $channel
   setenv Tfunc looseMuIso_tightEleId_DG_DoubleExpo_Spline_wFakeTauScale
             
else if ($channel == TauETauHad) then
   setenv channelT TauETauHad
   setenv Tfunc MVAMedium_DG_DoubleExpo_Spline_wFakeTauScale
   
else if ($channel == allchs) then
   setenv channelT allchs
   setenv Tfunc MVAMedium_DG_wFakeTauScaleFit 

endif
            
setenv workDir Impacts_${channelT}_${region}_${year}_h${h}_a${amass}
setenv datacard mmmt_mm_h_parametric_unbinned_${region}_H${h}_${channel}_${year}_${Tfunc}_hm${h}_amX

                
rm -rf $workDir
mkdir $workDir
cd $workDir
mkdir datacards_shape
cp -r ../datacards_shape/MuMuTauTau datacards_shape
text2workspace.py -m ${h} datacards_shape/MuMuTauTau/${datacard}.txt -o ${datacard}.root
echo 'perform initial fits for' ${channelT} ${region} 'H'${h} ${year} '...'
combineTool.py -M Impacts -m ${h} --unbinned --setParameters MA=${amass} --freezeParameters MA --setParameterRanges MA=${amass},${amass} --rMin 0 --rMax 1 --robustFit 1 -d ${datacard}.root --doInitialFit
echo 'compute impacts for' ${channelT} ${region} 'H'${h} ${year} '...'
combineTool.py -M Impacts -m ${h} --unbinned --setParameters MA=${amass} --freezeParameters MA --setParameterRanges MA=${amass},${amass} --rMin 0 --rMax 1 --robustFit 1 -d ${datacard}.root --doFits --parallel 10
echo 'extract impacts for' ${channelT} ${region} 'H'${h} ${year} '...'
combineTool.py -M Impacts -m ${h} --unbinned --setParameters MA=${amass} --freezeParameters MA --setParameterRanges MA=${amass},${amass} --rMin 0 --rMax 1 --robustFit 1 -d ${datacard}.root --output impacts_${channelT}_${region}_${year}_h${h}_a${amass}.json
plotImpacts.py -i impacts_${channelT}_${region}_${year}_h${h}_a${amass}.json -o impacts_${channelT}_${region}_${year}_h${h}_a${amass}
rm -rf ${datacard}.root
rm -rf datacards_shape
cd -
