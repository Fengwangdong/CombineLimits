#!/bin/bash
echo "Example complete command: bash submit_condor_lxplus.sh 125 tt 2018 highmass"
if [ -z $1 ] 
then
    echo "Please specify correct H mass! eg: 125, 250, 500, 750, 1000"
    exit 1
fi

export HMASS=$1
export PREFIX="mmmt_mm_h_parametric_unbinned"

export state="TauHadTauHad_V3"
if [ -z $2 ]
then
    echo "Please specify correct final state! eg: tt, mt, me, et, all"
    exit 1
elif [ $2 = "tt" ] 
then
    export state="TauHadTauHad_V3"
elif [ $2 = "mt" ] 
then
    export state="TauMuTauHad_V2"
elif [ $2 = "me" ] 
then
    export state="TauMuTauE"
elif [ $2 = "et" ] 
then
    export state="TauETauHad"
elif [ $2 = "all" ] 
then
    export state="allchs"
fi

export year="2018"
if [ -z $3 ]
then
    echo "Please specify correct data taking period(s)! eg: 2016, 2017, 2018, all"
    exit 1
elif [ $3 = "2016" ] 
then
    export year="2016"
elif [ $3 = "2017" ] 
then
    export year="2017"
elif [ $3 = "2018" ] 
then
    export year="2018"
elif [ $3 = "all" ] 
then
    export year="2016_2017_2018"
fi


export CHANNEL=$state"_"$year

export TFUNC="DG_DoubleExpo_yRange_Spline_wFakeTauScaleJEC"
if [ $state = "TauHadTauHad_V3" ] 
then
    export TFUNC="DG_DoubleExpo_yRange_Spline_wFakeTauScaleJEC"
elif [ $state = "TauMuTauHad_V2" ] 
then
    export TFUNC="DG_DoubleExpo_yRange_wFakeTauScale"
elif [ $state = "TauETauHad" ] || [ $state = "TauMuTauE" ] 
then
    export TFUNC="DG_DoubleExpo_Spline_wFakeTauScale"
else
    export TFUNC="DG_wFakeTauScaleFit"
fi


export WP="MVAMedium"
if [ $state = "TauMuTauE" ] 
then
    export WP="looseMuIso_tightEleId"
fi

if [ -z $4 ] 
then
    echo "Please specify correct data taking period(s)! eg: lowmass, upsilon, highmass, highmass2"
    exit 1
fi

export MREGION=$4
export AMASSES=`seq 3.6 0.1 8.5`

if [[ $MREGION == lowmass ]] 
then
    if [ $state = "TauETauHad" ] 
    then
        echo "NOT consider TauETauHad channel for low mass, skip!"
        exit 1
    fi

    if [ $1 = "125" ] 
    then
        export AMASSES=`seq 3.6 0.1 8.5`
    elif [ $1 = "250" ] 
    then
        export AMASSES=`seq 4.5 0.1 8.5`
    elif [ $1 = "500" ] 
    then
        export AMASSES=`seq 4 0.1 8.5`
    else
        echo "NOT consider H750 or H1000 for low mass, skip!"
        exit 1
    fi

    for m in $AMASSES
    do
	    export AMASS=$m
	    echo Arguments: $HMASS $AMASS $MREGION $CHANNEL $WP
	    condor_submit condor_lxplus.sub 
	done
fi

if [[ $MREGION == upsilon ]] 
then
    export AMASSES=`seq 8 0.1 12`

    if [ $state = "TauETauHad" ] && [ $1 = "250" ] 
    then
        export AMASSES=`seq 10 0.1 14`
    elif [ $state = "TauETauHad" ] && [ $1 = "500" ] || [ $state = "TauETauHad" ] && [ $1 = "750" ] || [ $state = "TauETauHad" ] && [ $1 = "1000" ] 
    then
        echo "NOT consider H500, H750 or H1000 for upsilon TauETauHad channel, skip!"
        exit 1
    fi

    for m in $AMASSES
    do
	    export AMASS=$m
	    echo Arguments: $HMASS $AMASS $MREGION $CHANNEL $WP
	    condor_submit condor_lxplus.sub
    done
fi


if [[ $MREGION == highmass ]] 
then
    if [ $1 = "125" ] 
    then
        export AMASSES=`seq 11 0.1 21`
    elif [ $1 = "250" ] 
    then
        export AMASSES=`seq 11 1.0 25`
    elif [ $1 = "500" ] 
    then
        export AMASSES=`seq 11 1.0 25`
        if
            [ $state = "TauETauHad" ] 
        then
            export AMASSES=`seq 14 1.0 25`
        fi
    elif [ $1 = "750" ] 
    then
        export AMASSES=`seq 12 1.0 35`
        if
            [ $state = "TauETauHad" ] 
        then
            export AMASSES=`seq 18 1.0 35`
        fi
    elif [ $1 = "1000" ] 
    then
        export AMASSES=`seq 11 1.0 30`
        if
            [ $state = "TauETauHad" ] 
        then
            export AMASSES=`seq 20 1.0 30`
        fi
    fi

    for m in $AMASSES
    do
	    export AMASS=$m
	    echo Arguments: $HMASS $AMASS $MREGION $CHANNEL $WP
	    condor_submit condor_lxplus.sub
    done
fi

if [[ $MREGION == highmass2 ]] 
then
    if [ $1 = "1000" ] 
    then
        export AMASSES=`seq 30 1.0 50`
    else
        echo "Only consider highmass2 for H1000, skip!"
        exit 1
    fi

    for m in $AMASSES
    do
	    export AMASS=$m
	    echo Arguments: $HMASS $AMASS $MREGION $CHANNEL $WP
	    condor_submit condor_lxplus.sub
    done
fi
