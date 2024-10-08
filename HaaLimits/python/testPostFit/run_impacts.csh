#!/bin/tcsh
echo "Example complete command: csh run_impacts.csh 125 mt highmass 2018"
setenv h 125
if ($1 != 125 && $1 != 250 && $1 != 500 && $1 != 750 && $1 != 1000) then
   echo "Please specify the correct H mass! eg: 125, 250, 500, 750, 1000"
   exit
else
   setenv h $1
endif

setenv channel TauHadTauHad_V3
if ($2 != tt && $2 != mt && $2 != et && $2 != me) then
   echo "Please specify the correct channel! eg: tt, mt, et, me"
   exit
else if ($2 == tt) then
   setenv channel TauHadTauHad_V3
else if ($2 == mt) then
   setenv channel TauMuTauHad_V2
else if ($2 == et) then
   setenv channel TauETauHad
else if ($2 == me) then
   setenv channel TauMuTauE
endif


setenv region highmass
if ($3 != lowmass && $3 != upsilon && $3 != highmass && $3 != highmass2) then
   echo "Please specify the correct region! eg: lowmass, upsilon, highmass, highmass2 #NOTE: highmass2 is only for H1000 (30-50GeV)"
   exit
else
   setenv region $3
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

setenv year 2018
if ($4 != 2016 && $4 != 2017 && $4 != 2018) then
   echo "Please specify the correction era! eg: 2016, 2017, 2018"
   exit
else
   setenv year $4
endif
   	     
setenv amass 5.0
if ($region == lowmass) then
   setenv amass 5.0
else if ($region == upsilon) then
   setenv amass 11.0
else if ($region == highmass) then
   setenv amass 20.0
else
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
   
endif
            
setenv workDir Impacts_${channelT}_${region}_${year}_h${h}
setenv datacard mmmt_mm_h_parametric_unbinned_${region}_H${h}_${channel}_${year}_${Tfunc}_hm${h}_amX

                
rm -rf $workDir
mkdir $workDir
text2workspace.py -m ${h} datacards_shape/MuMuTauTau/${datacard}.txt
mv datacards_shape/MuMuTauTau/${datacard}.root .
cd $workDir
echo 'compute impacts for' ${channelT} ${region} 'H'${h} ${year} '...'
combineTool.py -M Impacts -m ${h} --unbinned --setParameters MA=${amass} --freezeParameters MA --setParameterRanges MA=${amass},${amass} --rMin -1 --rMax 1 --robustFit 1 -d ../${datacard}.root --doInitialFit -v 2 > fit.log
cd -
