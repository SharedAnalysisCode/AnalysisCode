#!bin/bash

# Strings are passed to the scrieta but this is redundant!

#electron variables
# python ../ssdilep/scripts/merge.py --var="el_lead_eta" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest=""
# python ../ssdilep/scripts/merge.py --var="el_lead_eta" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest=""
# python ../ssdilep/scripts/merge.py --var="NPV" --reg="ZWindowOS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest=""

# python ../ssdilep/scripts/merge.py --var="el_pt_eta_all" --reg="BeyondZAS" --lab="" --tag="SherpaTrueCHF" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
# python ../ssdilep/scripts/merge.py --var="el_pt_eta_chf2" --reg="BeyondZAS" --lab="" --tag="SherpaTrueCHF" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
# python ../ssdilep/scripts/merge.py --var="el_pt_eta_chf4" --reg="BeyondZAS" --lab="" --tag="SherpaTrueCHF" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""

# python ../ssdilep/scripts/merge.py --var="el_pt_eta_all" --reg="BeyondZAS" --lab="" --tag="PowhegTrueCHF" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
# python ../ssdilep/scripts/merge.py --var="el_pt_eta_chf2" --reg="BeyondZAS" --lab="" --tag="PowhegTrueCHF" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
# python ../ssdilep/scripts/merge.py --var="el_pt_eta_chf4" --reg="BeyondZAS" --lab="" --tag="PowhegTrueCHF" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""

python ../ssdilep/scripts/merge.py --var="el_lead_pt" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign"
python ../ssdilep/scripts/merge.py --var="el_sublead_pt" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign"
python ../ssdilep/scripts/merge.py --var="el_lead_eta_2" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign"
python ../ssdilep/scripts/merge.py --var="el_sublead_eta_2" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign"
python ../ssdilep/scripts/merge.py --var="el_lead_phi_2" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign"
python ../ssdilep/scripts/merge.py --var="el_sublead_phi_2" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign"
python ../ssdilep/scripts/merge.py --var="invMassPeak_2" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign"
python ../ssdilep/scripts/merge.py --var="NPV" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign"
python ../ssdilep/scripts/merge.py --var="ZbosonPt" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign"
python ../ssdilep/scripts/merge.py --var="ZbosonEta" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign"


python ../ssdilep/scripts/merge.py --var="el_lead_pt" --reg="ZWindowSSchfSF" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign + chf SF"
python ../ssdilep/scripts/merge.py --var="el_sublead_pt" --reg="ZWindowSSchfSF" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign + chf SF"
python ../ssdilep/scripts/merge.py --var="el_lead_eta_2" --reg="ZWindowSSchfSF" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign + chf SF"
python ../ssdilep/scripts/merge.py --var="el_sublead_eta_2" --reg="ZWindowSSchfSF" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign + chf SF"
python ../ssdilep/scripts/merge.py --var="el_lead_phi_2" --reg="ZWindowSSchfSF" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign + chf SF"
python ../ssdilep/scripts/merge.py --var="el_sublead_phi_2" --reg="ZWindowSSchfSF" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign + chf SF"
python ../ssdilep/scripts/merge.py --var="invMassPeak_2" --reg="ZWindowSSchfSF" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign + chf SF"
python ../ssdilep/scripts/merge.py --var="NPV" --reg="ZWindowSSchfSF" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign + chf SF"
python ../ssdilep/scripts/merge.py --var="ZbosonPt" --reg="ZWindowSSchfSF" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign + chf SF"
python ../ssdilep/scripts/merge.py --var="ZbosonEta" --reg="ZWindowSSchfSF" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign + chf SF"

python ../ssdilep/scripts/merge.py --var="invMassPeak" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="any sign"
python ../ssdilep/scripts/merge.py --var="el_lead_pt" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="any sign"
python ../ssdilep/scripts/merge.py --var="el_sublead_pt" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="any sign"
python ../ssdilep/scripts/merge.py --var="el_lead_eta" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="any sign"
python ../ssdilep/scripts/merge.py --var="el_sublead_eta" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="any sign"
python ../ssdilep/scripts/merge.py --var="el_lead_phi" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="any sign"
python ../ssdilep/scripts/merge.py --var="el_sublead_phi" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="any sign"
python ../ssdilep/scripts/merge.py --var="NPV" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="any sign"
python ../ssdilep/scripts/merge.py --var="ZbosonPt" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="any sign"
python ../ssdilep/scripts/merge.py --var="ZbosonEta" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="any sign"

python ../ssdilep/scripts/merge.py --var="chargeFlipHist" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="chargeFlipHist" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="chargeFlipHist" --reg="ZWindowSS-Sideband" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="chargeFlipHist" --reg="ZWindowAS-Sideband" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
#MET
python ../ssdilep/scripts/merge.py --var="met_trk_et" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="any sign"
python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="ZWindowAS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="any sign"
python ../ssdilep/scripts/merge.py --var="met_trk_et" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign"
python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=True --fakest="" --lab="same sign"
### truth studies
<<COMMENT2
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSBothPromp" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSCHF1" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSCHF2" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSBrem" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSFSR" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSFake" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeOSBothNonPromp" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSBothPromp" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSCHF1" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSCHF2" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSBrem" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSFSR" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSFake" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZeeSSBothNonPromp" --lab="" --tag="CHFTruth1" --icut="1" --input="/afs/f9.ijs.si/home/miham/ZPeak36_4" --output="./ZPeak36" --makeplot=False --fakest=""
COMMENT2
