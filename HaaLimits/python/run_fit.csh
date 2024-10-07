#!/bin/tcsh
echo "Example complete command: csh run_fit.csh 125 tt 2018 highmass"

setenv hmass 125
if ($1 == "" || "$1" != "125" && "$1" != "250" && "$1" != "500" && "$1" != "750" && "$1" != "1000") then
    echo "Please specify the correct H mass! eg. 125, 250, 500, 750, 1000"
    exit
else
    setenv hmass $1
endif

setenv channel TauMuTauHad_V2
if ($2 == "" || $2 != "me" && $2 != "mt" && $2 != "et" && $2 != "tt") then
    echo "Please indicate correct channel! eg: me, mt, et, tt"
    exit
else if ($2 == "me") then
    setenv channel TauMuTauE
else if ($2 == "mt") then
    setenv channel TauMuTauHad_V2
else if ($2 == "et") then
    setenv channel TauETauHad
else if ($2 == "tt") then
    setenv channel TauHadTauHad_V3
endif

setenv year 2018
if ($3 == "" || $3 != "2016" && $3 != "2017" && $3 != "2018") then
    echo "Please indicate correct era! eg: 2016, 2017, 2018"
    exit
else
    setenv year $3
endif

setenv region highmass
if ($4 == "" || $4 != "lowmass" && $4 != "upsilon" && $4 != "highmass" && $4 != "highmass2") then
    echo "Please indicate correct region! eg: lowmass, upsilon, highmass, highmass2"
    exit
else if ($4 == "highmass2" && $hmass != "1000") then
    echo "Only consider highmass2 for H1000, skip!"
    exit
else
    setenv region $4
endif

setenv suffix "MVAMedium_DG_DoubleExpo_Spline_wFakeTauScale"
if ($channel == "TauMuTauE")  then
    setenv suffix "looseMuIso_tightEleId_DG_DoubleExpo_Spline_wFakeTauScale"
else if ($channel == "TauMuTauHad_V2") then
    setenv suffix "MVAMedium_DG_DoubleExpo_yRange_wFakeTauScale"
else if ($channel == "TauETauHad") then
    setenv suffix "MVAMedium_DG_DoubleExpo_Spline_wFakeTauScale"
else if ($channel == "TauHadTauHad_V3") then
    setenv suffix "MVAMedium_DG_DoubleExpo_yRange_Spline_wFakeTauScaleJEC"
endif

setenv xrangeMin 3
setenv xrangeMax 8
setenv yrangeMin 80
setenv yrangeMax 1200

if ($region == "lowmass") then
   setenv xrangeMin 3
   setenv xrangeMax 8
else if ($region == "upsilon") then
   setenv xrangeMin 8
   setenv xrangeMax 12
else if ($region == "highmass") then
   setenv xrangeMin 12
   setenv xrangeMax 30
else if ($region == "highmass2") then
   setenv xrangeMin 30
   setenv xrangeMax 50
endif

if ($hmass == "125") then
    setenv yrangeMin 80
    setenv yrangeMax 150
else if ($hmass == "250") then
    setenv yrangeMin 130
    setenv yrangeMax 280
    if ($channel != "TauMuTauHad_V2" && $channel != "TauHadTauHad_V3") then
        setenv yrangeMin 80
        setenv yrangeMax 1200
    endif
else if ($hmass == "500") then
    setenv yrangeMin 250
    setenv yrangeMax 600
    if ($channel != "TauMuTauHad_V2" && $channel != "TauHadTauHad_V3") then
        setenv yrangeMin 80
        setenv yrangeMax 1200
    else if ($channel == "TauMuTauHad_V2") then
        setenv yrangeMin 150
        setenv yrangeMax 1200
    endif
else if ($hmass == "750") then
    setenv yrangeMin 350
    setenv yrangeMax 800
    if ($channel != "TauMuTauHad_V2" && $channel != "TauHadTauHad_V3") then
        setenv yrangeMin 80
        setenv yrangeMax 1200
    else if ($channel == "TauMuTauHad_V2") then
        setenv yrangeMin 150
        setenv yrangeMax 1200
    endif
else if ($hmass == "1000") then
    setenv yrangeMin 450
    setenv yrangeMax 1200
    if ($channel != "TauMuTauHad_V2" && $channel != "TauHadTauHad_V3") then
        setenv yrangeMin 80
        setenv yrangeMax 1200
    else if ($channel == "TauMuTauHad_V2") then
        setenv yrangeMin 150
        setenv yrangeMax 1200
    endif
endif

python haaLimitsDevToolsRunII.py mm h --unblind --parametric --addControl --unbinned --fitParams --higgs $hmass --xRange $xrangeMin $xrangeMax --yRange $yrangeMin $yrangeMax --tag ${region}_H${hmass}_${channel}_${year}_${suffix} --channel ${channel}_${year} --yFitFunc DG --doubleExpo >& log_${region}_${hmass}_${year}_${channel} &
