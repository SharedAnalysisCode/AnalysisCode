#!bin/bash

# Strings are passed to the scrieta but this is redundant!

#nominal
python ../ssdilep/scripts/merge.py --var="el_t_2D_pt_eta" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="0" --input="/ceph/grid/home/atlas/miham/AnalysisCode/FFelectron2" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="el_l_2D_pt_eta" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="0" --input="/ceph/grid/home/atlas/miham/AnalysisCode/FFelectron2" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="el_sl_2D_pt_eta" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="0" --input="/ceph/grid/home/atlas/miham/AnalysisCode/FFelectron2" --output="./Plots" --makeplot=False --fakest=""

python ../ssdilep/scripts/merge.py --var="el_t_pt" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="0" --input="/ceph/grid/home/atlas/miham/AnalysisCode/FFelectron2" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="el_l_pt" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="0" --input="/ceph/grid/home/atlas/miham/AnalysisCode/FFelectron2" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="el_sl_pt" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="0" --input="/ceph/grid/home/atlas/miham/AnalysisCode/FFelectron2" --output="./Plots" --makeplot=False --fakest=""

python ../ssdilep/scripts/merge.py --var="met_trk_et" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="0" --input="/ceph/grid/home/atlas/miham/AnalysisCode/FFelectron2" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="nelectrons" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="0" --input="/ceph/grid/home/atlas/miham/AnalysisCode/FFelectron2" --output="./Plots" --makeplot=False --fakest=""
