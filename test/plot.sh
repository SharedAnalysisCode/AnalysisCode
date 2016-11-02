#!bin/bash

# Strings are passed to the scrieta but this is redundant!

python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="ZWindow" --lab="numerator" --tag="Powheg" --icut="1" --input="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/Analysis" --output="./" --makeplot=False --fakest=""
#python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR1_DEN" --lab="numerator" --tag="Sherpa" --icut="8" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=True --fakest="Subtraction"

<<"COMMENT"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR2_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR2_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR3_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR3_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR4_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR4_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR5_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR5_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR6_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR6_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR7_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR7_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR8_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR8_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18SepSys" --output="./" --makeplot=False --fakest="Subtraction"
COMMENT

<<"COMMENT"
#python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR8_NUM" --lab="WjetsAllTrig" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17SepDataWeight" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR6_NUM" --lab="numerator" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17SepDataWeight" --output="./" --makeplot=True --fakest="Subtraction"

#python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR5_NUM" --lab="Wjets CR" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17SepDataWeight" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR6_NUM" --lab="high MET" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17SepDataWeight" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR7_NUM" --lab="lowpT no weights" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17SepDataWeight" --output="./" --makeplot=True --fakest="Subtraction"

#python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR4_NUM" --lab="numerator" --icut="8" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17SepDataWeight" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR4_DEN" --lab="denominator" --icut="8" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17SepDataWeight" --output="./" --makeplot=True --fakest="Subtraction"
COMMENT



