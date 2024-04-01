#!/bin/sh

#放電電源単価閾値
HI_LIMIT=18.10
#充電電源単価閾値
LO_LIMIT=11.51
#充電コマ数(30分×n)
LENGTH=6

echo $HI_LIMIT $LO_LIMIT >&2
dir=`dirname $0`

if [ $# -lt 1 ]; then
    echo "usage: $0 [sch|chg|all]" >&2
    $dir/bt/LooopBTSch.py $HI_LIMIT $LO_LIMIT $LENGTH
    exit
fi

$dir/bt/LooopBTSch.py $HI_LIMIT $LO_LIMIT $LENGTH $1 | while read hhmi cmd price
do
    echo $hhmi $cmd $price
    echo $dir/bt/BTSet.py $cmd $price | at $hhmi
done

