#!/bin/sh

#放電電源単価閾値
HI_LIMIT=18.2
#充電電源単価閾値
LO_LIMIT=10.8

echo $HI_LIMIT $LO_LIMIT

dir=`pwd`
$dir/bt/LooopBTSch.py $HI_LIMIT $LO_LIMIT $1 | while read hhmi cmd price
do
    echo python3 $dir/bt/BTSet.py $cmd $price | at $hhmi
done

