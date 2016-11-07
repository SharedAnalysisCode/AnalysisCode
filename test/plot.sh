#!bin/bash

# Strings are passed to the scrieta but this is redundant!

#electron variables
python ../ssdilep/scripts/merge.py --var="el_lead_pt" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/Analysis" --output="./Plots" --makeplot=True --fakest=""
#python ../ssdilep/scripts/merge.py --var="el_sublead_pt" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/Analysis" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_lead_eta" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/Analysis" --output="./Plots" --makeplot=True --fakest=""
#python ../ssdilep/scripts/merge.py --var="el_subead_eta" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/Analysis" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="el_lead_phi" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/Analysis" --output="./Plots" --makeplot=True --fakest=""
#python ../ssdilep/scripts/merge.py --var="el_sublead_phi" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/Analysis" --output="./Plots" --makeplot=True --fakest=""
#Event variables
python ../ssdilep/scripts/merge.py --var="invMass" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/Analysis" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="actualIntPerXing" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/Analysis" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="ZbosonPt" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/Analysis" --output="./Plots" --makeplot=True --fakest=""
python ../ssdilep/scripts/merge.py --var="ZbosonEta" --reg="ZWindowSS" --lab="" --tag="Powheg" --icut="1" --input="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/Analysis" --output="./Plots" --makeplot=True --fakest=""





