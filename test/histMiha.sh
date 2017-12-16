#!/bin/bash

## Batch

# INPATH="/ceph/grid/home/atlas/tadej/ntuples/v3ntuples/EXOT12skimmed/nominal"
# INPATH="/ceph/grid/home/atlas/miham/ntuples/merged/EXOT12SkimmedSys/nominal"
# INPATH="/ceph/grid/home/atlas/tadej/ntuples/v3ntuples/EXOT19and12unskimmed/nominal"


# INPATH="/ceph/grid/home/atlas/tadej/ntuples/DiLepAna/v2/EXOT19and12unskimmed"
# INPATH="/ceph/grid/home/atlas/tadej/ntuples/DiLepAna/v1/EXOT12_dilepton"
INPATH="/ceph/grid/home/atlas/tadej/ntuples/DiLepAna/v2/EXOT12"


# INPATH="/ceph/grid/home/atlas/miham/ntuples/DiLepAna/v1/HN-unskimmed"

INSCRIPT="../ssdilep/run"
# SCRIPT="j.plotter_WJets.py"
# SCRIPT="j.plotter_ZPeak.py"
# SCRIPT="j.plotter_ele_allR.py"
SCRIPT="j.plotter_HN.py"
# SCRIPT="j.plotter_HN_cutflow.py"
# SCRIPT="j.plotter_ele_allR_emu.py"
# SCRIPT="j.plotter_ele_all_SRX.py"
# SCRIPT="j.plotter_fourLep.py"
# SCRIPT="j.plotter_SSVRele.py"
# SCRIPT="j.plotter_CRele.py"
# SCRIPT="j.plotter_CReleTTBAR.py"
# SCRIPT="j.plotter_CReleDiboson.py"
# SCRIPT="j.plotter_ThreeEleVR.py"
# SCRIPT="j.plotter_FFele.py"

echo "ASD"

# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPythia8EvtGen_AZNLOCTEQ6L1_DYee_5000M.root --sampletype="mc" --config="min_entry:1000,max_entry:10000"   #--config="sys:FF_DN" 
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPythia8EvtGen_AZNLOCTEQ6L1_DYee_120M180.root --sampletype="mc" --config="min_entry:0,max_entry:10000,sys:CF_UP"   #--config="sys:FF_DN" 
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_dil.root --sampletype="mc" --config="min_entry:0,max_entry:-1"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_222_NNPDF30NNLO_llll.root --sampletype="mc" --config="min_entry:0,max_entry:10000,sys:CF_UP"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPy8EG_CT10nloME_AZNLOCTEQ6L1_ZZllll_mll4  --sampletype="mc" --config="min_entry:0,max_entry:10000,sys:RECO_DNSYS"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPythia8EvtGen_A14_ttbar_hdamp258p75_dil.root --sampletype="mc" --config="min_entry:0,max_entry:10000"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPythia8EvtGen_AZNLOCTEQ6L1_DYee_800M1000.root --sampletype="mc" --config="min_entry:0,max_entry:-1,sys:SCALE_Z_UP"
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_221_NNPDF30NNLO_lllv.root --sampletype="mc" --config="min_entry:0,max_entry:10000,sys:EG_SCALE_ALLCORR_DN"
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/PowhegPythia8EvtGen_AZNLOCTEQ6L1_Wplusenu.root --sampletype="mc" --config="min_entry:0,max_entry:5000"   #--config="sys:FF_DN" 
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_221_NNPDF30NNLO_Zee_MAXHTPTV0_70_CVetoBVeto.root --sampletype="mc" --config="min_entry:0,max_entry:1000,sys:MUR1_MUF1_PDF261100"   #--config="sys:FF_DN" 
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_222_NNPDF30NNLO_lvvv.root --sampletype="mc" --config="min_entry:0,max_entry:50,sys:MUR1_MUF1_PDF261100"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_221_NNPDF30NNLO_Ztautau_MAXHTPTV280_500_CFilterBVeto.root --sampletype="mc" --config="min_entry:0,max_entry:-1"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_CT10_lllljj_EW6.root --sampletype="mc" --config="min_entry:0,max_entry:-1"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/MadGraphPythia8EvtGen_A14NNPDF23LO_LRSM_WR3600_NR3500.root --sampletype="mc" --config="min_entry:0,max_entry:1000"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/MGPy8EG_N30NLO_Zee_Ht280_500_BFilter.root --sampletype="mc" --config="min_entry:0,max_entry:-1"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/MadGraphPythia8EvtGen_A14NNPDF23LO_LRSM_WR5000_NR2500.root --sampletype="mc" --config="min_entry:0,max_entry:-1,sys:EG_RESOLUTION_ALL_UP"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_221_NNPDF30NNLO_Zee_MAXHTPTV500_1000.root --sampletype="mc" --config="min_entry:0,max_entry:10000,sys:JET_EffectiveNP_1_UP"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_221_NNPDF30NNLO_Zmumu_MAXHTPTV500_1000.root --sampletype="mc" --config="min_entry:0,max_entry:10000"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Pythia8EvtGen_A14NNPDF23LO_DCH700.root --sampletype="mc" --config="min_entry:0,max_entry:10000,sys:EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_DN"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/MadGraphPythia8EvtGen_A14NNPDF23LO_LRSM_WR4500_NR2250.root --sampletype="mc" --config="min_entry:0,max_entry:10000"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/MadGraphPythia8EvtGen_A14NNPDF23LO_LRSM_WR1000_NR1000.root --sampletype="mc" --config="min_entry:0,max_entry:10000"   #--config="sys:FF_DN" 
 python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/MadGraphPythia8EvtGen_A14NNPDF23LO_LRSM_WR3000_NR2900.root --sampletype="mc" --config="min_entry:0,max_entry:10000"   #--config="sys:FF_DN" 
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Pythia8EvtGen_A14NNPDF23LO_DCH300.root --sampletype="mc" --config="min_entry:0,max_entry:5000"   #--config="sys:FF_DN" 
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/full_2015-2016_physics_Main.root --sampletype="data"  --config="min_entry:0,max_entry:-1"
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/00284285.physics_Main.root --sampletype="data"  --config="min_entry:0,max_entry:-1,sys:JET_JER_NP2_DN"
 # python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_CT10_llll.root --sampletype="mc" --config="min_entry:0,max_entry:20000,sys:TRIG_UPSTAT"   #--config="sys:FF_DN" 
# python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/00300800.physics_Main.root --sampletype="data" --config="min_entry:0,max_entry:20000,sys:FF_DN"
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

# python ../ssdilep/run/j.plotter_HN_cutflow.py --input ../ntuple.root --sampletype="mc" --config="min_entry:0,max_entry:-1"