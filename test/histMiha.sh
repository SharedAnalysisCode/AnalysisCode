#!/bin/bash

## Batch

INPATH="/ceph/grid/home/atlas/tadej/ntuples/v3ntuples/EXOT12skimmed/nominal"
# INPATH="/ceph/grid/home/atlas/tadej/ntuples/v3ntuples/EXOT19and12unskimmed/nominal"
INSCRIPT="../ssdilep/run"
#SCRIPT="j.plotter_WJets.py"
SCRIPT="j.plotter_ZPeak.py"
# SCRIPT="j.plotter_SSVRele.py"
# SCRIPT="j.plotter_CRele.py"
# SCRIPT="j.plotter_CReleTTBAR.py"
# SCRIPT="j.plotter_CReleDiboson.py"
# SCRIPT="j.plotter_ThreeEleVR.py"
# SCRIPT="j.plotter_FFele.py"

# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPythia8EvtGen_AZNLOCTEQ6L1_DYee_5000M.root --sampletype="mc" --config="min_entry:1000,max_entry:10000"   #--config="sys:FF_DN" 
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPythia8EvtGen_AZNLOCTEQ6L1_DYee_120M180.root --sampletype="mc" --config="min_entry:0,max_entry:-1"   #--config="sys:FF_DN" 
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_dil.root --sampletype="mc" --config="min_entry:0,max_entry:-1"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_221_NNPDF30NNLO_llll.root --sampletype="mc" --config="min_entry:0,max_entry:5000"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPythia8EvtGen_AZNLOCTEQ6L1_Wplustaunu.root --sampletype="mc" --config="min_entry:0,max_entry:5000"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_NNPDF30NNLO_Zee_Pt0_70_CVetoBVeto.root --sampletype="mc" --config="min_entry:0,max_entry:5000"   #--config="sys:FF_DN" 
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/00306269.physics_Main.root --sampletype="data"  --config="min_entry:0,max_entry:-1,sys:CF_DN"
python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/00284285.physics_Main.root --sampletype="data"  --config="min_entry:0,max_entry:-1"
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_CT10_llll.root --sampletype="mc" --config="min_entry:0,max_entry:20000,sys:CF_DN"   #--config="sys:FF_DN" 
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/00300800.physics_Main.root --sampletype="data" --config="min_entry:0,max_entry:20000"
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_CT10_VV_lvee_50M150.root --sampletype="mc" --config="min_entry:0,max_entry:-1"
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/00280231.physics_Main.root --sampletype="data"  #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/llll.root --sampletype="mc" --events=100000   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/lllvOFMinus.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/lllvOFPlus.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/lllvSFMinus.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/lllvSFPlus.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/llvv.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/WqqZll.root --sampletype="mc" --events=-1   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/ZqqZll.root --sampletype="mc" --events=-1   #--config="sys:FF_DN"