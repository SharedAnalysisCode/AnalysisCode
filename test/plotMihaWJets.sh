#!bin/bash

# Strings are passed to the scrieta but this is redundant!


python ../ssdilep/scripts/merge.py --var="met_trk_et_WJets" --reg="Wjets-VR" --lab="" --tag="WJets" --icut="0" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
python ../ssdilep/scripts/merge.py --var="el_eta" --reg="Wjets-VR" --lab="" --tag="WJets" --icut="0" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
python ../ssdilep/scripts/merge.py --var="el_phi" --reg="Wjets-VR" --lab="" --tag="WJets" --icut="0" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
python ../ssdilep/scripts/merge.py --var="el_pt" --reg="Wjets-VR" --lab="" --tag="WJets" --icut="0" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
python ../ssdilep/scripts/merge.py --var="met_trk_mt" --reg="Wjets-VR" --lab="" --tag="WJets" --icut="0" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
python ../ssdilep/scripts/merge.py --var="NPV" --reg="Wjets-VR" --lab="" --tag="WJets" --icut="0" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="Wjets-VR" --lab="" --tag="WJets" --icut="0" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"


python ../ssdilep/scripts/merge.py --var="met_trk_et_WJets_tight" --reg="Wjets-tight-VR" --lab="MET < 60 GeV, MT < 120 GeV" --tag="WJets" --icut="2" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
python ../ssdilep/scripts/merge.py --var="el_eta" --reg="Wjets-tight-VR" --lab="MET < 60 GeV, MT < 120 GeV" --tag="WJets" --icut="2" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
python ../ssdilep/scripts/merge.py --var="el_phi" --reg="Wjets-tight-VR" --lab="MET < 60 GeV, MT < 120 GeV" --tag="WJets" --icut="2" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
python ../ssdilep/scripts/merge.py --var="el_pt" --reg="Wjets-tight-VR" --lab="MET < 60 GeV, MT < 120 GeV" --tag="WJets" --icut="2" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
python ../ssdilep/scripts/merge.py --var="met_trk_mt_tight" --reg="Wjets-tight-VR" --lab="MET < 60 GeV, MT < 120 GeV" --tag="WJets" --icut="2" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
python ../ssdilep/scripts/merge.py --var="NPV" --reg="Wjets-tight-VR" --lab="MET < 60 GeV, MT < 120 GeV" --tag="WJets" --icut="2" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="Wjets-tight-VR" --lab="MET < 60 GeV, MT < 120 GeV" --tag="WJets" --icut="2" --input="/afs/f9.ijs.si/home/miham/WJets36_2" --output="./WJets36" --makeplot=True --fakest="FakeFactor1D"
