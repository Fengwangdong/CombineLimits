#!/bin/bash
echo "Example complete command: bash run_plot.sh 125 tt 2018"
if [ -z $1 ] 
then
    echo "Please specify correct H mass! eg: 125, 250, 500, 750, 1000"
    exit 1
fi

export HMASS=$1

if [ -z $2 ]
then
    echo "Please specify correct final state! eg: tt, mt, me, et, all"
    exit 1
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

python plot_limit_haa_multi.py $1 $2 $year
