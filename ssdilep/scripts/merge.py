## modules
import ROOT

import histmgr
import funcs
import os

from ssdilep.samples import samples
from ssdilep.plots   import vars_mumu
from ssdilep.plots   import vars_ee
#from ssdilep.plots   import vars_fakes
from systematics     import *

from optparse import OptionParser

DO_SYS = True


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

(options, args) = parser.parse_args()

#-----------------
# Configuration
#-----------------
#lumi =  3158.13
#lumi =  18232.76
lumi =  36470.16
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

if options.samples == "wjet":
  mc_backgrounds = [
  samples.WenuPowheg,
  samples.ZeePowheg,
  samples.ttbar_inc,
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
  samples.ttbar_inc,
  samples.singletop_inc,
  samples.diboson_sherpa221,
  ]
elif options.samples == "chargeFlipData":
  mc_backgrounds = [
  ]
elif options.samples in ["ttbar","ttbarss"]:
  mc_backgrounds = [
  samples.ttbar,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  samples.singletop,
  samples.ttX,
  samples.AZNLOCTEQ6L1_DYee,
  # samples.ZtautauPowheg,
  ]
elif options.samples == "OSCR":
  mc_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  samples.ttbar,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  samples.singletop,
  samples.ttX,
  # samples.ZtautauPowheg,
  ]
elif options.samples in ["SSVR","SSVRBLIND"]:
  mc_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  samples.ttbar,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  samples.singletop,
  # samples.AZNLOCTEQ6L1_DYtautau,
  samples.ttX,
  ]
elif options.samples == "ZPeak":
  mc_backgrounds = [
  samples.Zee221,
  samples.diboson_sherpa221,
  samples.ttbar_inc,
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
  # samples.ttbar,
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
  samples.ttbar,
  ]
elif options.samples == "dibosonFit":
  mc_backgrounds = [
  samples.diboson_sherpa221,
  samples.singletop,
  samples.ttX,
  # samples.AZNLOCTEQ6L1_DYtautau,
  samples.ttbar,
  ]
elif options.samples in ["chargeflip","chargeflipTruth"]:
  mc_backgrounds = [
  samples.Zee221,
  ]
elif options.samples in ["chargeflipPowheg","chargeflipTruthPowheg"]:
  mc_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  ]


fakes_mumu = samples.fakes.copy()
chargeFlip = samples.chargeFlip.copy()
#fakes_mumu=[]
## signals
mumu_signals = []
#mumu_signals.append(samples.all_DCH)
#mumu_signals.append(samples.DCH800)

signal = [
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH300,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH350,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH400,
  # # samples.Pythia8EvtGen_A14NNPDF23LO_DCH450,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH500,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH550,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH600,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH650,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH700,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH750,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH800,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH850,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH900,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH950,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH1000,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH1050,
  # samples.Pythia8EvtGen_A14NNPDF23LO_DCH1100,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH1150,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH1200,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH1250,
  samples.Pythia8EvtGen_A14NNPDF23LO_DCH1300,
  ]

#--------------
# Estimators
#--------------
#for s in mc_backgrounds + mumu_signals + [data]: 
#for s in mc_backgrounds: 

for s in mc_backgrounds: 
    histmgr.load_base_estimator(hm,s)

for s in [data]: 
    histmgr.load_base_estimator(hm,s)

for s in signal:
  print s
  s.estimator = histmgr.EstimatorDCH( hm=hm, sample=s )

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
mc_sys = [
    SYS1, 
    SYS2,
    ]

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
    samples.ttbar_inc.estimator.add_systematics(CF)
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
  samples.ttbar_inc,
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
  samples.ttbar_inc,
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
  samples.AZNLOCTEQ6L1_DYee,
  samples.ttbar,
  samples.singletop,
  fakes_mumu,
  samples.diboson_sherpa221,
  # samples.VV_ee,
  # samples.ZtautauPowheg,
  samples.ttX,
  ]
elif options.samples == "ttbarss":
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  samples.ttbar,
  fakes_mumu,
  samples.singletop,
  samples.diboson_sherpa221,
  # samples.VV_ee,
  # samples.ZtautauPowheg,
  samples.ttX,
  ]
elif options.samples == "OSCR":
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  samples.ttbar,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  samples.singletop,
  fakes_mumu,
  samples.ttX,
  # samples.ZtautauPowheg,
  ]
elif options.samples == "ZPeak":
  mumu_backgrounds = [
  samples.Zee221,
  samples.diboson_sherpa221,
  samples.ttbar_inc,
  samples.singletop_inc,
  samples.ttX,
  samples.WenuPowheg,
  samples.WtaunuPowheg,
  # samples.ZtautauPowheg,
  ]
elif options.samples in ["SSVR","SSVRBLIND"]:
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  fakes_mumu,
  samples.ttbar,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  samples.singletop,
  # samples.AZNLOCTEQ6L1_DYtautau,
  samples.ttX,
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
  samples.ttX,
  # samples.AZNLOCTEQ6L1_DYtautau,
  samples.ttbar,
  # samples.WenuPowheg,
  ]
elif options.samples == "dibosonFit":
  mumu_backgrounds = [
  samples.diboson_sherpa221,
  fakes_mumu,
  samples.singletop,
  samples.ttX,
  # samples.AZNLOCTEQ6L1_DYtautau,
  samples.ttbar,
  ]
elif options.samples in ["chargeflip","chargeflipTruth"]:
  mumu_backgrounds = [
  samples.Zee221,
  ]
elif options.samples in ["chargeflipPowheg","chargeflipTruthPowheg"]:
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  ]


if (DO_SYS):
  fakes_mumu.estimator.add_systematics(FF)
  for sample in mumu_backgrounds:
    sample.estimator.add_systematics(CF)
    sample.estimator.add_systematics(FF)
  for sample in signal:
    sample.estimator.add_systematics(CF)
    sample.estimator.add_systematics(FF)

print options.blind

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
    log           = mumu_vdict[options.vname]['log'],
    logx          = mumu_vdict[options.vname]['logx'],
    xlabel        = options.xlabel,
    icut          = int(options.icut),
    sys_dict      = sys_dict if DO_SYS else None,
    do_ratio_plot = mumu_vdict[options.vname]['do_ratio_plot'],
    save_eps      = True,
    plotsfile     = plotsfile,
    blind         = True if options.blind=="True" else False
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
         rebinToEq   = True if options.rebinToEq=="True" else False
         )
 ## EOF



