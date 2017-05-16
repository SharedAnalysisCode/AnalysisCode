#!bin/bash

# Strings are passed to the scrieta but this is redundant!

python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_t_2D_pt_Ceta" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_l_2D_pt_Ceta" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_sl_2D_pt_Ceta" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=False --fakest=""

python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_t_2D_pt_Ceta" --reg="FakeEnrichedRegion-MET60" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_l_2D_pt_Ceta" --reg="FakeEnrichedRegion-MET60" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_sl_2D_pt_Ceta" --reg="FakeEnrichedRegion-MET60" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=False --fakest=""

python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_t_2D_pt_Ceta" --reg="FakeEnrichedRegion-ASjet" --lab="" --tag="FFnominal" --icut="2" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_l_2D_pt_Ceta" --reg="FakeEnrichedRegion-ASjet" --lab="" --tag="FFnominal" --icut="2" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_sl_2D_pt_Ceta" --reg="FakeEnrichedRegion-ASjet" --lab="" --tag="FFnominal" --icut="2" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=False --fakest=""


python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_t_pt" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_l_pt" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_sl_pt" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=True --fakest=""

python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_t_eta" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_l_eta" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --samples="FFele" --var="el_sl_eta" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=True --fakest=""

python ../ssdilep/scripts/merge.py --samples="FFele" --var="met_trk_et" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --samples="FFele" --var="nelectrons" --reg="FakeEnrichedRegion-nominal" --lab="" --tag="FFnominal" --icut="1" --input="/afs/f9.ijs.si/home/miham/FFele_v3_006" --output="./FFele_v3_006" --makeplot=True --fakest=""