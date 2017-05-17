find .
echo $IN
echo $IN2
echo $IN3

python ssdilep/run/j.plotter_ele_allR.py --input $IN --sampletype="mc" --config="min_entry:0,max_entry:-1,sys:EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_DN"
hadd out.root ntuple.root $IN2 $IN3