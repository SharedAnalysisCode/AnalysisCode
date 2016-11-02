#!/bin/bash

## Batch

INPATH="/home/ATLAS-T3/ucchielli/SSCode/SSDiLep/ssdilep/Zmumu/nominal"

INSCRIPT="/home/ATLAS-T3/ucchielli/SSCode/SSDiLep/ssdilep/run"
SCRIPT="j.plotter_FF.py"

QUEUE=T3_BO_LOCAL

DATE=`date +%d.%h.%Y_%k:%m:%S`
mkdir $DATE
cd $DATE

for file in $(ls $INPATH)
do

 echo "Input File is $INPATH/$file"

 mkdir out_$file
 echo "Making Directory out_$file"

 cd out_$file
 echo "And getting inside $PWD"

 bsub -q $QUEUE -e err -o out python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/$file --sampletype="mc" --events=20000 #--config="sys:FF_DN"

 cd ..

done

cd ..
