find .
echo $1
echo $2
echo $3

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet
lsetup root

source setup.sh

python ssdilep/run/j.plotter_ele_allR.py --input $1 --sampletype="mc" --config="min_entry:0,max_entry:-1,sys:EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_DN"
hadd out.root ntuple.root $2 $3