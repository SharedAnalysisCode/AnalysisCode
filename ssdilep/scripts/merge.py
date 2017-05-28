## modules
import ROOT

import histmgr
import funcs
import os
import re

from ssdilep.samples import samples
from ssdilep.samples import sample
from ssdilep.plots   import vars_mumu
from ssdilep.plots   import vars_ee
#from ssdilep.plots   import vars_fakes
from systematics     import *

from optparse import OptionParser
import copy

DO_SYS = True
ELE_SYS = False
MU_SYS = False


#-----------------
# input
#-----------------
parser = OptionParser()
parser.add_option('-v', '--var', dest='vname',
                  help='varable name',metavar='VAR',default=None)
parser.add_option('-r', '--reg', dest='region',
                  help='region name',metavar='REG',default=None)
parser.add_option('-l', '--lab', dest='label',
                  help='region label',metavar='LAB',default=None)
parser.add_option('-c', '--icut', dest='icut',
                  help='number of cuts',metavar='ICUT',default=None)
parser.add_option('-p', '--makeplot', dest='makeplot',
                  help='make plot',metavar='MAKEPLOT',default=None)
parser.add_option('-i', '--input', dest='indir',
                  help='input directory',metavar='INDIR',default=None)
parser.add_option('-o', '--output', dest='outdir',
                  help='output directory',metavar='OUTDIR',default=None)
parser.add_option('-f', '--fakest', dest='fakest',
                  help='choose fake estimate',metavar='FAKEST',default=None)
parser.add_option('-t', '--tag', dest='tag',
                  help='outfile tag',metavar='TAG',default=None)
parser.add_option('-s', '--samples', dest='samples',
                  help='samples',metavar='SAMPLES',default=None)
parser.add_option('-x', '--xlabel', dest='xlabel',
                  help='xlabel',metavar='XLABEL',default=None)
parser.add_option('-b', '--blind', dest='blind',
                  help='blind',metavar='BLIND',default=None)
parser.add_option('-S', '--signal', dest='signal',
                  help='signal',metavar='SIGNAL',default=None)
parser.add_option('-R', '--rebinToEq', dest='rebinToEq',
                  help='rebinToEq',metavar='REBINTOEQ',default=None)
parser.add_option('-V', '--varName', dest='varName',
                  help='varName',metavar='VARNAME',default=None)
parser.add_option('-L', '--logy', dest='logy',
                  help='logy',metavar='LOGY',default=None)
parser.add_option('-y', '--sys', dest='sys',
                  help='sys',metavar='SYS',default=None)
parser.add_option('-B', '--branching', dest='branching',
                  help='branching',metavar='BRANCHING',default=None)
parser.add_option('-E', '--elesys', dest='elesys',
                  help='elesys',metavar='ELESYS',default=None)
parser.add_option('-M', '--musys', dest='musys',
                  help='musys',metavar='MUSYS',default=None)

(options, args) = parser.parse_args()

if options.sys == "False":
  DO_SYS = False

if options.elesys == "True":
  ELE_SYS = True

if options.musys == "True":
  MU_SYS = True

#-----------------
# Configuration
#-----------------
#lumi =  3158.13
#lumi =  18232.76
lumi =  36074.56
#lumi =  18232.8
#lumi = 5000

# Control regions
plotsfile = []
if options.makeplot == "False":
  plotsfile.append("hists")
plotsfile.append(options.vname)
plotsfile.append(options.region)
plotsfile.append(options.tag)

plotsfile = "_".join(plotsfile)+".root"
plotsfile = os.path.join(options.outdir,plotsfile)

ROOT.gROOT.SetBatch(True)
hm = histmgr.HistMgr(basedir=options.indir,target_lumi=lumi)

#-----------------
# Samples        
#-----------------

## data
data = samples.data
mc_backgrounds = []
## backgrounds 


# ttbar_Py8_up
# ttbar_Py8_do
# ttbar_Py8
# ttbar_Py8_aMcAtNlo
# ttbar_Py8_CF

if options.samples == "wjet":
  mc_backgrounds = [
  samples.WenuPowheg,
  samples.ZeePowheg,
  samples.ttbar_Py8,
  samples.singletop_inc,
  samples.diboson_sherpa221,
  samples.WtaunuPowheg,
  # samples.ZtautauPowheg,
  ]
elif options.samples == "FFele":
  mc_backgrounds = [
  samples.WenuPowheg,
  samples.WtaunuPowheg,
  samples.ZeePowheg,
  samples.ZtautauPowheg,
  samples.ttbar_Py8,
  samples.singletop_inc,
  samples.diboson_sherpa221,
  ]
elif options.samples == "chargeFlipData":
  mc_backgrounds = [
  ]
elif options.samples in ["ttbar","ttbarss"]:
  mc_backgrounds = [
  samples.ttbar_Py8,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  samples.singletop,
  samples.ttX,
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  ]
elif options.samples == "OSCR":
  mc_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  samples.top_physics,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  # samples.singletop,
  # samples.ttX,
  # samples.AZNLOCTEQ6L1_DYtautau,
  ]
elif options.samples in ["SSVR","SSVRBLIND"]:
  mc_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  samples.top_physics,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  # samples.singletop,
  # samples.ttX,
  ]
elif options.samples in ["SSVR_mu","SSVRBLIND"]:
  mc_backgrounds = [
  # samples.AZNLOCTEQ6L1_DYee_DYtautau,
  samples.top_physics,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  # samples.singletop,
  # samples.ttX,
  ]
elif options.samples == "ZPeak":
  mc_backgrounds = [
  samples.Zee221,
  samples.diboson_sherpa221,
  samples.ttbar_Py8,
  samples.singletop_inc,
  samples.ttX,
  samples.WenuPowheg,
  samples.WtaunuPowheg,
  # samples.ZtautauPowheg,
  # samples.Higgs,
  ]
elif options.samples == "diboson":
  mc_backgrounds = [
  # samples.Zee221,
  # samples.ttbar_Py8,
  # samples.diboson_sherpa,
  samples.diboson_sherpa221_llll,
  samples.diboson_sherpa221_lllv,
  samples.diboson_sherpa221_ggllll,
  samples.diboson_sherpa221_lllvjj,
  samples.diboson_sherpa221_lllljj,
  # samples.vgamma,
  # samples.VV_ee,
  # samples.singletop,
  samples.ttX,
  # samples.AZNLOCTEQ6L1_DYtautau,
  samples.top_physics,
  ]
elif options.samples == "dibosonFit":
  mc_backgrounds = [
  samples.diboson_sherpa221,
  # samples.ttX,
  # samples.singletop,
  samples.top_physics,
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  ]
elif options.samples == "dibosonFit_mu":
  mc_backgrounds = [
  samples.diboson_sherpa221,
  # samples.ttX,
  # samples.singletop,
  samples.top_physics,
  ]
elif options.samples in ["chargeflip","chargeflipTruth"]:
  mc_backgrounds = [
  samples.Zee221,
  ]
elif options.samples in ["chargeflipPowheg","chargeflipTruthPowheg"]:
  mc_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  ]
elif options.samples == "allSamples":
  mc_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  samples.diboson_sherpa221,
  samples.dibosonSysSample,
  samples.top_physics,
  # samples.ttbar_Py8,
  # samples.singletop,
  # samples.ttX,
  # samples.ttX_singletop,
  # samples.ttbar_Py8_up,
  # samples.ttbar_Py8_do,
  # samples.ttbar_Herwig,
  # samples.ttbar_Py8_aMcAtNlo,
  # samples.ttbar_Py8_CF,
  ]
elif options.samples == "allSamples_mu":
  mc_backgrounds = [
  samples.diboson_sherpa221,
  samples.dibosonSysSample,
  samples.top_physics,
  # samples.ttbar_Py8,
  # samples.singletop,
  # samples.ttX,
  # samples.ttX_singletop,
  # samples.ttbar_Py8_up,
  # samples.ttbar_Py8_do,
  # samples.ttbar_Herwig,
  # samples.ttbar_Py8_aMcAtNlo,
  # samples.ttbar_Py8_CF,
  ]


fakes_mumu = samples.fakes.copy()
chargeFlip = samples.chargeFlip.copy()
#fakes_mumu=[]
## signals
mumu_signals = []
#mumu_signals.append(samples.all_DCH)
#mumu_signals.append(samples.DCH800)

signal_ee100mm0 = []
signal_ee50mm50 = []

signal_samples = []

xsecL = [82.677, 34.825, 16.704, 8.7528, 4.9001, 2.882, 1.7631, 1.10919, 0.72042, 0.476508, 0.32154, 0.21991, 0.15288, 0.107411, 0.076403, 0.0547825, 0.039656, 0.0288885, 0.021202, 0.0156347, 0.011632, 0.00874109, 0.0065092]
masses = [200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300]

# for br in range(10,110,10):
for br in [0,50,100]:
  signal_samples += [[]]
  intiger = 1
  for mass,xsec in zip(masses,xsecL):
    if options.makeplot == "True":
      if mass not in [500,600,700] or br not in ([float(options.branching)] if options.branching else []): continue
    name = "Pythia8EvtGen_A14NNPDF23LO_DCH%d" % mass
    print "tlatex: ", ("DCH%d Br(ee)=%d" % (mass,br)) if options.elesys=="True" else ("DCH%d Br(#mu#mu)=%d" % (mass,100-br))
    globals()[name+"ee"+str(br)+"mm"+str(100-br)] = sample.Sample(
      name = name,
      tlatex = ("DCH%d Br(ee)=%d" % (mass,br)) if options.elesys=="True" else ("DCH%d Br(#mu#mu)=%d" % (mass,100-br)),
      line_color = intiger,
      marker_color = intiger,
      fill_color = intiger,
      line_width  = 3,
      line_style = 1,
      fill_style = 3004,
      xsec       = xsec/1000.,
      )
    signal_samples[len(signal_samples)-1] += [ globals()[name+"ee"+str(br)+"mm"+str(100-br)] ]
    # signal_ee100mm0 += [globals()[name+"ee100mm0"]]
    # globals()[name+"ee50mm50"] = sample.Sample(
    #   name = name,
    #   tlatex = "DCH%d Br(ee)=Br(#mu#mu)=0.5" % (mass),
    #   line_color = ROOT.kOrange-intiger,
    #   marker_color = ROOT.kOrange-intiger,
    #   fill_color = ROOT.kOrange-intiger,
    #   line_width  = 3,
    #   line_style = 1,
    #   fill_style = 3004,
    #   xsec       = xsec/1000.,
    #   )
    # signal_ee50mm50 += [globals()[name+"ee50mm50"]]
    intiger += 1


# signal = [
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH300,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH350,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH400,
#   # # samples.Pythia8EvtGen_A14NNPDF23LO_DCH450,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH500,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH550,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH600,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH650,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH700,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH750,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH800,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH850,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH900,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH950,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH1000,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH1050,
#   # samples.Pythia8EvtGen_A14NNPDF23LO_DCH1100,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH1150,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH1200,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH1250,
#   samples.Pythia8EvtGen_A14NNPDF23LO_DCH1300,
#   ]


#--------------
# Estimators
#--------------
#for s in mc_backgrounds + mumu_signals + [data]: 
#for s in mc_backgrounds:


for s in mc_backgrounds: 
    histmgr.load_base_estimator(hm,s)

for s in signal_ee100mm0:
  s.estimator = histmgr.EstimatorDCH( hm=hm, ee=1.0, mm=0.0, sample=s )
  s.nameSuffix = "ee100mm0"

for s in signal_ee50mm50:
  s.estimator = histmgr.EstimatorDCH( hm=hm, ee=0.5, mm=0.5, sample=s )
  s.nameSuffix = "ee50mm50"

signal = []
for samps in signal_samples:
  for s in samps:
    br = re.findall("Br\(ee\)\=([0-9]*)",s.tlatex)[0] if options.elesys=="True" else re.findall("Br\(#mu#mu\)\=([0-9]*)",s.tlatex)[0]
    print "asdasd ", br
    if not options.elesys=="True":
      print br
      br = str(100-float(br))
      print "Br(H->ee)= ", br
      print "ee= ", float(br)/100.
      print "mm= ", (1-float(br)/100.)
    s.estimator = histmgr.EstimatorDCH( hm=hm, ee=float(br)/100., mm=(1-float(br)/100.), sample=s )
    s.nameSuffix = "ee"+br+"mm"+str(int(100-float(br)))
    # print s.tlatex
    # print float(br)
    # print s.nameSuffix
    signal += [s]



# signal = signal_ee100mm0 + signal_ee50mm50
# signal = [x for x in signal_samples]
# signal = signal_ee100mm0 
# signal = signal_ee50mm50

for s in [data]: 
    histmgr.load_base_estimator(hm,s)


if options.fakest == "FakeFactor":
  fakes_mumu.estimator = histmgr.FakeEstimator(
      hm=hm, 
      sample=fakes_mumu,
      data_sample = data,
      mc_samples = mc_backgrounds )

elif options.fakest == "FakeFactor1D":
  fakes_mumu.estimator = histmgr.FakeEstimator1D(
      hm=hm, 
      sample=fakes_mumu,
      data_sample = data,
      mc_samples = mc_backgrounds )

elif options.fakest == "FakeFactorGeneral":
  fakes_mumu.estimator = histmgr.FakeEstimatorGeneral(
      hm=hm, 
      sample=fakes_mumu,
      data_sample = data,
      mc_samples = mc_backgrounds )

elif options.fakest == "ChargeFlip":
  chargeFlip.estimator = histmgr.ChargeFlipEsimator(
      hm=hm, 
      sample=chargeFlip,
      data_sample = data,
      mc_samples = mc_backgrounds
      )
elif options.fakest == "Subtraction":
  fakes_mumu.estimator = histmgr.DataBkgSubEstimator(
      hm=hm,
      sample=fakes_mumu,
      data_sample=data,
      background_samples=mc_backgrounds,
      )

else:
  print "WARNING: no estimator for fake bkg!!!"


#-----------------
# Systematics       
#-----------------
# just an example ...

## set mc systematics
#for s in mc_backgrounds + mumu_signals:
#    s.estimator.add_systematics(mc_sys)

if (DO_SYS):
  # fakes_mumu.estimator.add_systematics(FF)
  if options.fakest == "ChargeFlip":
    chargeFlip.estimator.add_systematics(CF)
  if options.samples == "chargeflip":
    samples.Zee221.estimator.add_systematics(CF)
  if options.samples == "ZPeak":
    samples.Zee221.estimator.add_systematics(CF)
    samples.diboson_sherpa221.estimator.add_systematics(CF)
    samples.ttbar_Py8.estimator.add_systematics(CF)
    samples.singletop_inc.estimator.add_systematics(CF)
    samples.ttX.estimator.add_systematics(CF)
    samples.WenuPowheg.estimator.add_systematics(CF)
    samples.WtaunuPowheg.estimator.add_systematics(CF)
    # samples.ZtautauPowheg.estimator.add_systematics(CF)

mumu_vdict  = vars_ee.vars_dict
#fakes_vdict = vars_fakes.vars_dict

#-----------------
# Plotting 
#-----------------
mumu_backgrounds = []

if options.samples == "wjet":
  mumu_backgrounds = [
  samples.WenuPowheg,
  fakes_mumu,
  samples.ZeePowheg,
  samples.ttbar_Py8,
  samples.diboson_sherpa221,
  samples.singletop_inc,
  samples.WtaunuPowheg,
  # samples.ZtautauPowheg,
  ]
elif options.samples == "FFele":
  mumu_backgrounds = [
  samples.WenuPowheg,
  samples.ZeePowheg,
  samples.diboson_sherpa221,
  samples.WtaunuPowheg,
  samples.ZtautauPowheg,
  samples.ttbar_Py8,
  samples.singletop_inc,
  ]
elif options.samples == "chargeFlipData":
  if options.fakest == "ChargeFlip":
    mumu_backgrounds = [
    chargeFlip,
    ]
  else: mumu_backgrounds = []
elif options.samples == "ttbar":
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  samples.ttbar_Py8,
  samples.singletop,
  fakes_mumu,
  samples.diboson_sherpa221,
  # samples.VV_ee,
  samples.ttX,
  ]
elif options.samples == "ttbarss":
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  samples.ttbar_Py8,
  fakes_mumu,
  samples.singletop,
  samples.diboson_sherpa221,
  # samples.VV_ee,
  samples.ttX,
  ]
elif options.samples == "OSCR":
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  # samples.VV_ee,
  samples.top_physics,
  samples.diboson_sherpa221,
  # samples.singletop,
  fakes_mumu,
  samples.ttX,
  # samples.AZNLOCTEQ6L1_DYtautau,
  ]
elif options.samples == "ZPeak":
  mumu_backgrounds = [
  samples.Zee221,
  samples.diboson_sherpa221,
  samples.ttbar_Py8,
  samples.singletop_inc,
  samples.ttX,
  samples.WenuPowheg,
  samples.WtaunuPowheg,
  # samples.ZtautauPowheg,
  ]
elif options.samples in ["SSVR","SSVRBLIND"]:
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  fakes_mumu,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  samples.top_physics,
  # samples.singletop,
  # samples.ttX,
  ]
elif options.samples in ["SSVR_mu"]:
  mumu_backgrounds = [
  # samples.AZNLOCTEQ6L1_DYee_DYtautau,
  fakes_mumu,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  samples.top_physics,
  # samples.singletop,
  # samples.ttX,
  ]
elif options.samples == "diboson":
  mumu_backgrounds = [
  # samples.Zee221,
  # samples.diboson_sherpa,
  samples.diboson_sherpa221_lllv,
  samples.diboson_sherpa221_llll,
  samples.diboson_sherpa221_ggllll,
  samples.diboson_sherpa221_lllvjj,
  samples.diboson_sherpa221_lllljj,
  # samples.vgamma,
  # samples.VV_ee,
  fakes_mumu,
  # samples.singletop,
  # samples.ttX,
  # samples.AZNLOCTEQ6L1_DYtautau,
  samples.top_physics,
  # samples.WenuPowheg,
  ]
elif options.samples == "dibosonFit":
  mumu_backgrounds = [
  samples.diboson_sherpa221,
  fakes_mumu,
  # samples.ttX,
  # samples.singletop,
  samples.top_physics,
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  ]
elif options.samples == "dibosonFit_mu":
  mumu_backgrounds = [
  samples.diboson_sherpa221,
  fakes_mumu,
  # samples.ttX,
  # samples.singletop,
  samples.top_physics,
  ]
elif options.samples in ["chargeflip","chargeflipTruth"]:
  mumu_backgrounds = [
  samples.Zee221,
  ]
elif options.samples in ["chargeflipPowheg","chargeflipTruthPowheg"]:
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  ]
elif options.samples == "allSamples":
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  samples.diboson_sherpa221,
  samples.dibosonSysSample,
  samples.top_physics,
  # samples.ttbar_Py8,
  # samples.singletop,
  # samples.ttX,
  # samples.ttX_singletop,
  # samples.ttbar_Py8_up,
  # samples.ttbar_Py8_do,
  # samples.ttbar_Herwig,
  # samples.ttbar_Py8_aMcAtNlo,
  # samples.ttbar_Py8_CF,
  fakes_mumu,
  ]
elif options.samples == "allSamples_mu":
  mumu_backgrounds = [
  samples.diboson_sherpa221,
  samples.dibosonSysSample,
  samples.top_physics,
  # samples.ttbar_Py8,
  # samples.singletop,
  # samples.ttX,
  # samples.ttX_singletop,
  # samples.ttbar_Py8_up,
  # samples.ttbar_Py8_do,
  # samples.ttbar_Herwig,
  # samples.ttbar_Py8_aMcAtNlo,
  # samples.ttbar_Py8_CF,
  fakes_mumu,
  ]

sys_list_ele = [BEAM, CHOICE, PDF, PI, SCALE_Z, EG_RESOLUTION_ALL, EG_SCALE_ALLCORR, EG_SCALE_E4SCINTILLATOR, FF, CF, TRIG, ID, ISO, RECO]
sys_list_muon = [MUON_ID, MUON_MS, MUON_RESBIAS, MUON_RHO, MUON_SCALE, TRIGSTAT, TRIGSYS, ISOSYS, ISOSTAT, RECOSYS, RECOSTAT, TTVASYS, TTVASTAT]

if (DO_SYS):
  if ELE_SYS:
    fakes_mumu.estimator.add_systematics(FF)
  if MU_SYS:
    fakes_mumu.estimator.add_systematics(MUFF)
  for sample in mumu_backgrounds:
    if sample in [samples.dibosonSysSample,samples.ttbar_Py8_up,samples.ttbar_Py8_do,samples.ttbar_Herwig,samples.ttbar_Py8_aMcAtNlo,samples.ttbar_Py8_CF]:
      print "skip sys MC samples in other systematics"
      continue
    if ELE_SYS:
      for sys in sys_list_ele:
        sample.estimator.add_systematics(sys)
    if MU_SYS:
      for sys in sys_list_muon:
        sample.estimator.add_systematics(sys)
  for sample in signal:
    if ELE_SYS:
      for sys in sys_list_ele:
        sample.estimator.add_systematics(sys)
    if MU_SYS:
      for sys in sys_list_muon:
        sample.estimator.add_systematics(sys)

print options.blind

tempLogy = None
if options.logy=="True":
  tempLogy = True
elif options.logy=="False":
  tempLogy = False

if options.makeplot == "True":
 funcs.plot_hist(
    backgrounds   = mumu_backgrounds,
    signal        = signal if options.signal=="True" else None, 
    data          = data if options.samples not in ["chargeflipTruth","chargeflipTruthPowheg"] else None,
    region        = options.region,
    label         = options.label if options.label else mumu_vdict[options.vname]['label'],
    histname      = os.path.join(mumu_vdict[options.vname]['path'],mumu_vdict[options.vname]['hname']),
    xmin          = mumu_vdict[options.vname]['xmin'],
    xmax          = mumu_vdict[options.vname]['xmax'],
    rebin         = mumu_vdict[options.vname]['rebin'],
    rebinVar      = mumu_vdict[options.vname]['rebinVar'],
    log           = tempLogy if tempLogy!=None else mumu_vdict[options.vname]['log'],
    logx          = mumu_vdict[options.vname]['logx'],
    xlabel        = options.xlabel,
    icut          = int(options.icut),
    sys_dict      = sys_dict if DO_SYS else None,
    do_ratio_plot = mumu_vdict[options.vname]['do_ratio_plot'],
    save_eps      = True,
    plotsfile     = plotsfile,
    blind         = int(options.blind) if options.blind else None,
    )

else:
 funcs.write_hist(
         backgrounds = mumu_backgrounds,
         signal      = signal if options.signal=="True" else None, 
         data        = data if options.samples not in ["chargeflipTruth","chargeflipTruthPowheg"] else None,
         region      = options.region,
         icut        = int(options.icut),
         histname    = os.path.join(mumu_vdict[options.vname]['path'],mumu_vdict[options.vname]['hname']),
         rebin       = mumu_vdict[options.vname]['rebin'],
         rebinVar    = mumu_vdict[options.vname]['rebinVar'],
         sys_dict    = sys_dict if DO_SYS else None,
         outname     = plotsfile,
         regName     = options.tag,
         rebinToEq   = True if options.rebinToEq=="True" else False,
         varName     = str(options.varName)
         )
 ## EOF



