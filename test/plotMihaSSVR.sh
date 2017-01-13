#!bin/bash

# Strings are passed to the scrieta but this is redundant!

python ../ssdilep/scripts/merge.py --var="invMass_2" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="ZbosonPt_2" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="ZbosonEta_2" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="nelectrons" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="NPV" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="met_trk_et" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"
#python ../ssdilep/scripts/merge.py --var="invMass" --reg="same-sign-CR-TL" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron2" --output="./SSVR" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="invMass" --reg="same-sign-CR-LT" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron2" --output="./SSVR" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="invMass" --reg="same-sign-CR-LL" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/ceph/grid/home/atlas/miham/AnalysisCode/CRelectron2" --output="./SSVR" --makeplot=True --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="el_lead_pt_2" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="el_sublead_pt_2" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="el_lead_eta_2" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="el_sublead_eta_2" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="el_lead_phi_2" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="el_sublead_phi_2" --reg="same-sign-CR" --lab="Same-Sign VR" --tag="OSCR" --icut="0" --input="/afs/f9.ijs.si/home/miham/SSVRele36_2" --output="./SSVR" --makeplot=True --fakest="FakeFactor"