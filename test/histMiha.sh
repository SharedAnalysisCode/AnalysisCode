#!/bin/bash

## Batch

INPATH="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12/merged/nominal/"
INSCRIPT="../ssdilep/run"
SCRIPT="j.plotter_CRele.py"

python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zee.root --sampletype="mc" --events=100000   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/00280231.physics_Main.root --sampletype="data" --events=100000   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/llll.root --sampletype="mc" --events=100000   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/lllvOFMinus.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/lllvOFPlus.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/lllvSFMinus.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/lllvSFPlus.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/llvv.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/WqqZll.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/ZqqZll.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
