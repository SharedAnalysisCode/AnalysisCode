#!bin/bash

# Strings are passed to the scrieta but this is redundant!

python ../ssdilep/scripts/merge.py --var="invMass" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="ZbosonPt" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="ZbosonEta" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="nelectrons" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="NPV" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="met_trk_et" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
#python ../ssdilep/scripts/merge.py --var="invMass" --reg="opposite-sign-CR-TL" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron2" --output="./Plots" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="invMass" --reg="opposite-sign-CR-LT" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron2" --output="./Plots" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="invMass" --reg="opposite-sign-CR-LL" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron2" --output="./Plots" --makeplot=True --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="el_lead_pt" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="el_sublead_pt" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="el_lead_eta" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="el_sublead_eta" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="el_lead_trkd0sig" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="el_sublead_trkd0sig" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="el_lead_trkz0sintheta" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="el_sublead_trkz0sintheta" --reg="opposite-sign-CR" --lab="" --tag="OSCR" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron3" --output="./Plots" --makeplot=True --fakest="FakeFactor"
