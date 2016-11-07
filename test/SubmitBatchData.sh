#!/bin/bash

## Batch
#echo
#export

#INLIST="/home/ATLAS-T3/ucchielli/SSCode/SSDiLep/filelists/Zee.list"
INFILES="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/Data/"
#INPATH="/home/ATLAS-T3/ucchielli/SSCode/SSDiLep/ssdilep/Zmumu/nominal"

INSCRIPT="/home/ATLAS-T3/ucchielli/AnalysisCode/ssdilep/run"
SCRIPT="j.plotter_ZPeak.py"

QUEUE=T3_BO_LOCAL

DATE=`date +%d.%h.%Y_%k_%m`
mkdir $DATE


for file in $(ls $INFILES)
do
    cd $DATE
    
    mkdir out_$file
    cd out_$file
    
    for dataset in $(ls "/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/Data/$file")
    do
	
	mkdir out_$dataset
	cd out_$dataset
	
	echo "file is $file" 
        bsub -q $QUEUE -e err -o out python ${INSCRIPT}/${SCRIPT} --input ${INFILES}/$file/$dataset --sampletype="data" #--events=20000 #--config="sys:FF_DN"
	
	cd ..

    done
    cd ..

done    

cd ..
