# python ../ssdilep/scripts/merge.py -y "False" --varName="obs_Mjj" --rebinToEq="True" --elesys="True" --musys="True" --var="Mjj5" --reg="electron-SS-Z-CR" --lab="SS ZCR ee" --tag="SSZCRee" --samples="nothing" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_CR_test" --output="./HN_v2_CR_test" --makeplot=False --fakest="FakeFactorGeneral" -S True
# python ../ssdilep/scripts/merge.py -y "False" --varName="obs_Mjj" --rebinToEq="True" --elesys="True" --musys="True" --var="Mjj6"  --tag="SSZCRmm" --reg="muon-SS-Z-CR" --lab="SS ZCR #mu#mu" --tag="SSZCRmm" --samples="nothing" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_CR_test" --output="./HN_v2_CR_test" --makeplot=False --fakest="FakeFactorGeneral" -S True

# python ../ssdilep/scripts/merge.py -y "False" --elesys="True" --musys="True" --var="invMassSignalHN" --reg="electron-SS-Z-nomll-CR" --lab="SS ZCR ee" --tag="SSZCRee" --samples="nothing" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_CR_test_02" --output="./HN_v2_CR_test_02" --makeplot=False --fakest="FakeFactorGeneral" -S True
# python ../ssdilep/scripts/merge.py -y "False" --elesys="True" --musys="True" --var="invMassSignalHN"  --tag="SSZCRmm" --reg="muon-SS-Z-nomll-CR" --lab="SS ZCR #mu#mu" --tag="SSZCRmm" --samples="nothing" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_CR_test_02" --output="./HN_v2_CR_test_02" --makeplot=False --fakest="FakeFactorGeneral" -S True

# python ../ssdilep/scripts/merge.py -y "False" --elesys="True" --musys="True" --var="HTlljj" --reg="electron-SS-Z-nomll-CR" --lab="SS ZCR ee" --tag="SSZCRee" --samples="nothing" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_CR_test_02" --output="./HN_v2_CR_test_02" --makeplot=False --fakest="FakeFactorGeneral" -S True
# python ../ssdilep/scripts/merge.py -y "False" --elesys="True" --musys="True" --var="HTlljj"  --tag="SSZCRmm" --reg="muon-SS-Z-nomll-CR" --lab="SS ZCR #mu#mu" --tag="SSZCRmm" --samples="nothing" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_CR_test_02" --output="./HN_v2_CR_test_02" --makeplot=False --fakest="FakeFactorGeneral" -S True

# python ../ssdilep/scripts/merge.py -y "False" --elesys="True" --musys="True" --var="Mjj0" --reg="electron-SS-Z-nomll-CR" --lab="SS ZCR ee" --tag="SSZCRee" --samples="nothing" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_CR_test_02" --output="./HN_v2_CR_test_02" --makeplot=False --fakest="FakeFactorGeneral" -S True
# python ../ssdilep/scripts/merge.py -y "False" --elesys="True" --musys="True" --var="Mjj0"  --tag="SSZCRmm" --reg="muon-SS-Z-nomll-CR" --lab="SS ZCR #mu#mu" --tag="SSZCRmm" --samples="nothing" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_CR_test_02" --output="./HN_v2_CR_test_02" --makeplot=False --fakest="FakeFactorGeneral" -S True

# python ../ssdilep/scripts/merge.py -y "False" --elesys="True" --musys="True" --var="Mlljj0" --reg="electron-SS-Z-nomll-CR" --lab="SS ZCR ee" --tag="SSZCRee" --samples="nothing" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_CR_test_02" --output="./HN_v2_CR_test_02" --makeplot=False --fakest="FakeFactorGeneral" -S True
# python ../ssdilep/scripts/merge.py -y "False" --elesys="True" --musys="True" --var="Mlljj0"  --tag="SSZCRmm" --reg="muon-SS-Z-nomll-CR" --lab="SS ZCR #mu#mu" --tag="SSZCRmm" --samples="nothing" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_CR_test_02" --output="./HN_v2_CR_test_02" --makeplot=False --fakest="FakeFactorGeneral" -S True

#### SR
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="invMassSignalHN" --reg="electron-SS-Z-inclusive-SR" --lab="SS ee" --lab2="m(ee)>110, m(eejj)>400" --tag="SSZCRee" --samples="HNeeFitNoPt0_70_CVetoBVeto" --icut="7" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="invMassSignalHN" --reg="muon-SS-Z-inclusive-SR" --lab="SS #mu#mu" --lab2="m(#mu#mu)>110, m(#mu#mujj)>400" --tag="SSZCRmm" --samples="HNeeFit" --icut="7" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="Mlljj0" --reg="electron-SS-Z-inclusive-SR" --lab="SS ee" --lab2="m(ee)>110, m(eejj)>400" --tag="SSZCRee" --samples="HNeeFitNoPt0_70_CVetoBVeto" --icut="7" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="Mlljj0" --reg="muon-SS-Z-inclusive-SR" --lab="SS #mu#mu" --lab2="m(#mu#mu)>110, m(#mu#mujj)>400" --tag="SSZCRmm" --samples="HNeeFit" --icut="7" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="HTlljj" --reg="electron-SS-Z-inclusive-SR" --lab="SS ee" --lab2="m(ee)>110, m(eejj)>400" --tag="SSZCRee" --samples="HNeeFitNoPt0_70_CVetoBVeto" --icut="7" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="HTlljj" --reg="muon-SS-Z-inclusive-SR" --lab="SS #mu#mu" --lab2="m(#mu#mu)>110, m(#mu#mujj)>400" --tag="SSZCRmm" --samples="HNeeFit" --icut="7" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="Mjj0" --reg="electron-SS-Z-inclusive-SR" --lab="SS ee" --lab2="m(ee)>110, m(eejj)>400" --tag="SSZCRee" --samples="HNeeFitNoPt0_70_CVetoBVeto" --icut="7" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="Mjj0" --reg="muon-SS-Z-inclusive-SR" --lab="SS #mu#mu" --lab2="m(#mu#mu)>110, m(#mu#mujj)>400" --tag="SSZCRmm" --samples="HNeeFit" --icut="7" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True

#### CR
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="invMassSignalHN2" --reg="electron-SS-Z-inclusive-CR" --lab="SS ee" --lab2="m(ee)>110, m(eejj)<400" --tag="SSZCRee" --samples="HNeeFit" --icut="6" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="invMassSignalHN2" --reg="muon-SS-Z-inclusive-CR" --lab="SS #mu#mu" --lab2="m(#mu#mu)>110, m(#mu#mujj)<400" --tag="SSZCRmm" --samples="HNeeFit" --icut="6" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="Mlljj1" --reg="electron-SS-Z-inclusive-CR" --lab="SS ee" --lab2="m(ee)>110, m(eejj)<400" --tag="SSZCRee" --samples="HNeeFit" --icut="6" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="Mlljj1" --reg="muon-SS-Z-inclusive-CR" --lab="SS #mu#mu" --lab2="m(#mu#mu)>110, m(#mu#mujj)<400" --tag="SSZCRmm" --samples="HNeeFit" --icut="6" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="HTlljj1" --reg="electron-SS-Z-inclusive-CR" --lab="SS ee" --lab2="m(ee)>110, m(eejj)<400" --tag="SSZCRee" --samples="HNeeFit" --icut="6" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="HTlljj1" --reg="muon-SS-Z-inclusive-CR" --lab="SS #mu#mu" --lab2="m(#mu#mu)>110, m(#mu#mujj)<400" --tag="SSZCRmm" --samples="HNeeFit" --icut="6" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="Mjj1" --reg="electron-SS-Z-inclusive-CR" --lab="SS ee" --lab2="m(ee)>110, m(eejj)<400" --tag="SSZCRee" --samples="HNeeFit" --icut="6" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="Mjj1" --reg="muon-SS-Z-inclusive-CR" --lab="SS #mu#mu" --lab2="m(#mu#mu)>110, m(#mu#mujj)<400" --tag="SSZCRmm" --samples="HNeeFit" --icut="6" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True


#### VR
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="invMassSignalHN3" --reg="electron-SS-Z-inclusive-VR" --lab="SS ee" --lab2="60<m(ee)<110" --tag="SSZCRee" --samples="HNeeFit" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="Mlljj0" --reg="electron-SS-Z-inclusive-VR" --lab="SS ee" --lab2="60<m(ee)<110" --tag="SSZCRee" --samples="HNeeFit" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="HTlljj" --reg="electron-SS-Z-inclusive-VR" --lab="SS ee" --lab2="60<m(ee)<110" --tag="SSZCRee" --samples="HNeeFit" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True
python ../ssdilep/scripts/merge.py --logy="False" --makeplot=True -y "False" --elesys="True" --musys="True" --var="Mjj0" --reg="electron-SS-Z-inclusive-VR" --lab="SS ee" --lab2="60<m(ee)<110" --tag="SSZCRee" --samples="HNeeFit" --icut="5" --input="/ceph/grid/home/atlas/miham/AnalysisCode/HN_v2_inclusive_SR_01" --output="./HN_v2_inclusive_SR_01" --fakest="FakeFactorGeneral" -S True



