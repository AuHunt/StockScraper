#!/bin/sh

repeat=0;
while [ $repeat -lt 60 ]; do
    logname="nyse_`date +%Y_%m_%d_%H_%M`.html"
    wget -O $logname http://www.wsj.com/mdc/public/page/2_3021-activnyse-actives.html

    `python hw9.py $logname`
    
    sleep 1m
    repeat=$((repeat+1))
done
