#!bin/bash

# Strings are passed to the scrieta but this is redundant!

#electron variables
python ../ssdilep/scripts/merge.py --var="el_lead_pt" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
'''python ../ssdilep/scripts/merge.py --var="el_sublead_pt" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_lead_eta" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_subead_eta" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_lead_phi" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_sublead_phi" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_lead_pt" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_sublead_pt" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_lead_eta" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_subead_eta" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_lead_phi" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_sublead_phi" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
#Event variables
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="actualIntPerXing" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="ZbosonPt" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="ZbosonEta" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""

python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="actualIntPerXing" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="ZbosonPt" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="ZbosonEta" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""

'''