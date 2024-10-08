#!/bin/bash
echo "Example complete command: bash run_plot.sh 125 tt 2018"
if [ -z $1 ] 
then
    echo "Please specify correct H mass! eg: 125, 250, 500, 750, 1000"
    exit 1
fi

export h=$1
if [ -z $2 ]
then
    echo "Please specify correct final state! eg: tt, mt, me, et"
    exit 1
fi

export year="2018"
if [ -z $3 ]
then
    echo "Please specify correct data taking period(s)! eg: 2016, 2017, 2018"
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
fi


for s in 'lowmass' 'upsilon' 'highmass' 'highmass2';
do
    if [[ $s = 'highmass2' && $h != 1000 ]]; then
        continue
    elif [[ $s = 'lowmass' && ($h = 750 || $h = 1000) ]]; then
        continue
    fi

    if [ $2 = "tt" ]; then
        python2 plot_postfit_thth.py $s $year $h
    elif [ $2 = "mt" ]; then
        python2 plot_postfit_tmth.py $s $year $h
    elif [ $2 = "et" ]; then
        python2 plot_postfit_teth.py $s $year $h
    elif [ $2 = "me" ]; then
        python2 plot_postfit_tmte.py $s $year $h
    fi
done
