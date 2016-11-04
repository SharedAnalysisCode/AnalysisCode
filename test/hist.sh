#!/bin/bash

## Batch

#INPATH="/home/ATLAS-T3/ucchielli/SSCode/SSDiLep/ssdilep/Zmumu/nominal"
INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/MCtoRun/Sherpa_CT10_VV_llmumu_4000M5000_tree.root/"
#INPATH="/home/ATLAS-T3/ucchielli/SSCode/SSDiLep/user.gucchiel.SSDiLep.v1Ntuples.364118.Sherpa_221_NNPDF30NNLO_Zee_MAXHTPTV70_140_CFilterBVeto_tree.root"
INSCRIPT="/home/ATLAS-T3/ucchielli/AnalysisCode/ssdilep/run"
SCRIPT="j.plotter_ZPeak.py"

#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/zumu.root --sampletype="mc" #--events=2000 #--config="sys:FF_DN"
python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/user.gucchiel.9635668._000001.tree.root  --sampletype="mc" --events=2000 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00302380.root --sampletype="data" --events=200 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_NNPDF30NNLO_Zmumu_Pt500_700_BFilter.root --sampletype="mc" --events=200   #--config="sys:FF_DN" 
