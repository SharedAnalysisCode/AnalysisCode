#!bin/bash

# Strings are passed to the scrieta but this is redundant!

python ../ssdilep/scripts/merge.py --var="invMass" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="ZbosonPt" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="ZbosonEta" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="nelectrons" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="NPV" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="met_trk_et" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="el_lead_pt" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="el_sublead_pt" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="el_lead_eta" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="el_sublead_eta" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="el_lead_phi" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="el_sublead_phi" --reg="opposite-sign-ttbar-CR" --lab="TTCR (OSCR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbar" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"


python ../ssdilep/scripts/merge.py --var="invMass_3" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="ZbosonPt_2" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="ZbosonEta_2" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="nelectrons" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="NPV" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="met_trk_et" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="el_lead_pt_2" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="el_sublead_pt_2" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="el_lead_eta_2" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="el_sublead_eta_2" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="el_lead_phi_2" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"
python ../ssdilep/scripts/merge.py --var="el_sublead_phi_2" --reg="same-sign-ttbar-CR" --lab="TTVR (SSVR + 1/2 b-jet)" --tag="TTBAR" --samples="ttbarss" --icut="3" --input="/afs/f9.ijs.si/home/miham/AllR_v3_001" --output="./TTBAR" --makeplot=True --fakest="FakeFactorGeneral"