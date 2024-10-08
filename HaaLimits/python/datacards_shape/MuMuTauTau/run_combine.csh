#!/bin/tcsh
echo "Example complete command: csh run_combine.csh tt"

setenv prefix mmmt_mm_h_parametric_unbinned
setenv channel TauMuTauHad_V2
setenv wp MVAMedium
setenv method DG_DoubleExpo_yRange_wFakeTauScale

if ($1 == "" || $1 != "me" && $1 != "mt" && $1 != "et" && $1 != "tt" && $1 != "all") then
    echo "Please indicate correct channel! eg: me, mt, et, tt, all"
    exit
else if ($1 == "me") then
    setenv channel TauMuTauE
    setenv wp looseMuIso_tightEleId
    setenv method DG_DoubleExpo_Spline_wFakeTauScale
else if ($1 == "mt") then
    setenv channel TauMuTauHad_V2
    setenv method DG_DoubleExpo_yRange_wFakeTauScale
else if ($1 == "et") then
    setenv channel TauETauHad
    setenv method DG_DoubleExpo_Spline_wFakeTauScale
else if ($1 == "tt") then
    setenv channel TauHadTauHad_V3
    setenv method DG_DoubleExpo_yRange_Spline_wFakeTauScaleJEC
else if ($1 == "all") then
    setenv channel allchs
    setenv method DG_wFakeTauScaleFit
endif

if ($1 != 'all') then
    foreach region (lowmass upsilon highmass highmass2)
        foreach hm (125 250 500 750 1000)
        ### combine same channel different years
            if (($region == highmass2) && ($hm == 125 || $hm == 250 || $hm == 500 || $hm == 750)) then
                continue
            endif
            combineCards.py ${prefix}_${region}_H${hm}_${channel}_2016_${wp}_${method}_hm${hm}_amX.txt ${prefix}_${region}_H${hm}_${channel}_2017_${wp}_${method}_hm${hm}_amX.txt ${prefix}_${region}_H${hm}_${channel}_2018_${wp}_${method}_hm${hm}_amX.txt > ${prefix}_${region}_H${hm}_${channel}_2016_2017_2018_${wp}_${method}_hm${hm}_amX.txt.tmp
            sed 's/ch1_//g' ${prefix}_${region}_H${hm}_${channel}_2016_2017_2018_${wp}_${method}_hm${hm}_amX.txt.tmp | sed 's/ch2_//g' | sed 's/ch3_//g' > ${prefix}_${region}_H${hm}_${channel}_2016_2017_2018_${wp}_${method}_hm${hm}_amX.txt
            rm -rf ${prefix}_${region}_H${hm}_${channel}_2016_2017_2018_${wp}_${method}_hm${hm}_amX.txt.tmp
        end
    end

else
    ### combine all channels

    combineCards.py --xc=control_2016 --xc=control_2017 --xc=control_2018 ${prefix}_${region}_H${hm}_TauMuTauE_2016_2017_2018_looseMuIso_tightEleId_DG_DoubleExpo_Spline_wFakeTauScale_hm${hm}_amX.txt ${prefix}_${region}_H${hm}_TauETauHad_2016_2017_2018_MVAMedium_DG_DoubleExpo_Spline_wFakeTauScale_hm${hm}_amX.txt ${prefix}_${region}_H${hm}_TauMuTauHad_V2_2016_2017_2018_MVAMedium_DG_DoubleExpo_yRange_wFakeTauScale_hm${hm}_amX.txt > card.tmp
    combineCards.py card.tmp ${prefix}_${region}_H${hm}_TauHadTauHad_V3_2016_2017_2018_MVAMedium_DG_DoubleExpo_yRange_Spline_wFakeTauScaleJEC_hm${hm}_amX.txt > ${prefix}_${region}_H${hm}_allchs_2016_2017_2018_MVAMedium_DG_wFakeTauScaleFit_hm${hm}_amX.txt.tmp
    sed 's/ch1_//g' ${prefix}_${region}_H${hm}_allchs_2016_2017_2018_MVAMedium_DG_wFakeTauScaleFit_hm${hm}_amX.txt.tmp | sed 's/ch2_//g' | sed 's/ch3_//g' | sed 's/ch4_//g' | sed 's/ch5_//g' > ${prefix}_${region}_H${hm}_allchs_2016_2017_2018_MVAMedium_DG_wFakeTauScaleFit_hm${hm}_amX.txt
    rm -rf ${prefix}_${region}_H${hm}_allchs_2016_2017_2018_MVAMedium_DG_wFakeTauScaleFit_hm${hm}_amX.txt.tmp
    rm -rf card.tmp
endif
