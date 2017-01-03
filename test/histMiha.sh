#!/bin/bash

## Batch

INPATH="/ceph/grid/home/atlas/miham/ntuples/v2ntuples18ifb/mergedEXOT19and0/nominal/"
INSCRIPT="../ssdilep/run"
SCRIPT="j.plotter_FFele.py"

#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPythia8EvtGen_AZNLOCTEQ6L1_DYee_1750M2000.root --sampletype="mc" --config="min_entry:1000,max_entry:2000"   #--config="sys:FF_DN" 
python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/00299055.physics_Main.root --sampletype="data" --config="min_entry:0,max_entry:100000"   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/00280231.physics_Main.root --sampletype="data" --events=100000   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/llll.root --sampletype="mc" --events=100000   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/lllvOFMinus.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/lllvOFPlus.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/lllvSFMinus.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/lllvSFPlus.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/llvv.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/WqqZll.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/ZqqZll.root --sampletype="mc" --events=-1   #--config="sys:FF_DN"