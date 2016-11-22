#!bin/bash

# Strings are passed to the scrieta but this is redundant!

#electron variables
#python ../ssdilep/scripts/merge.py --var="el_lead_eta" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
#python ../ssdilep/scripts/merge.py --var="el_lead_eta" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
#python ../ssdilep/scripts/merge.py --var="NPV" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""

#python ../ssdilep/scripts/merge.py --var="el_pt_eta_all" --reg="BeyondZAS" --lab="" --tag="SherpaTrueCHF" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
#python ../ssdilep/scripts/merge.py --var="el_pt_eta_chf2" --reg="BeyondZAS" --lab="" --tag="SherpaTrueCHF" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
#python ../ssdilep/scripts/merge.py --var="el_pt_eta_chf4" --reg="BeyondZAS" --lab="" --tag="SherpaTrueCHF" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""

python ../ssdilep/scripts/merge.py --var="el_pt_eta_all" --reg="BeyondZAS" --lab="" --tag="PowhegTrueCHF" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="el_pt_eta_chf2" --reg="BeyondZAS" --lab="" --tag="PowhegTrueCHF" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="el_pt_eta_chf4" --reg="BeyondZAS" --lab="" --tag="PowhegTrueCHF" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""

<<COMMENT1
python ../ssdilep/scripts/merge.py --var="el_lead_pt" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_sublead_pt" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
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
#Event variables'''
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
#python ../ssdilep/scripts/merge.py --var="actualIntPerXing" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="ZbosonPt" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="ZbosonEta" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
#python ../ssdilep/scripts/merge.py --var="actualIntPerXing" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="ZbosonPt" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="ZbosonEta" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""

python ../ssdilep/scripts/merge.py --var="chargeFlipHist" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="chargeFlipHist" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="chargeFlipHist" --reg="ZWindowSS-Sideband" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="chargeFlipHist" --reg="ZWindowOS-Sideband" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
#MET
python ../ssdilep/scripts/merge.py --var="met_trk_et" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="met_trk_et" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=True --fakest=""
COMMENT1
### truth studies
<<COMMENT2
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSBothPromp" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSCHF1" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSCHF2" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSBrem" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSFSR" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSFake" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSBothNonPromp" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSBothPromp" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSCHF1" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSCHF2" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSBrem" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSFSR" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSFake" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSBothNonPromp" --lab="" --tag="CHFTruth1" --icut="1" --input="/ceph/grid/home/atlas/miham/AnalysisCode/EXOT12" --output="./Plots" --makeplot=False --fakest=""
COMMENT2
