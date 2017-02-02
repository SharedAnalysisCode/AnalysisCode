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

DO_SYS = False


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
  samples.ttbar,
  samples.singletop,
  samples.diboson_sherpa,
  ]
elif options.samples in ["ttbar","ttbarss"]:
  mc_backgrounds = [
  samples.ttbar,
  samples.VV_ee,
  samples.singletop,
  samples.ttX,
  samples.AZNLOCTEQ6L1_DYee,
  samples.ZtautauPowheg,
  ]
elif options.samples == "OSCR":
  mc_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  samples.ttbar,
  samples.VV_ee,
  samples.singletop,
  samples.ttX,
  ]
elif options.samples == "SSVR":
  mc_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  samples.ttbar,
  samples.VV_ee,
  samples.singletop,
  samples.ZtautauPowheg,
  samples.ttX,
  ]
elif options.samples == "diboson":
  mc_backgrounds = [
  # samples.Zee221,
  # samples.ttbar,
  samples.diboson_sherpa,
  # samples.VV_ee,
  # samples.singletop,
  samples.ttX,
  samples.Higgs,
  # samples.WenuPowheg,
  ]
elif options.samples == "chargeflip":
  mc_backgrounds = [
  samples.Zee221,
  ]


fakes_mumu = samples.fakes.copy()
#fakes_mumu=[]
## signals
mumu_signals = []
#mumu_signals.append(samples.all_DCH)
#mumu_signals.append(samples.DCH800)



#--------------
# Estimators
#--------------
#for s in mc_backgrounds + mumu_signals + [data]: 
#for s in mc_backgrounds: 
for s in mc_backgrounds + [data]: 
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
  fakes_mumu.estimator.add_systematics(FF)

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
  samples.ttbar,
  samples.singletop,
  samples.diboson_sherpa,
  ]
elif options.samples == "ttbar":
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  samples.ttbar,
  samples.singletop,
  fakes_mumu,
  samples.VV_ee,
  samples.ZtautauPowheg,
  samples.ttX,
  ]
elif options.samples == "ttbarss":
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  samples.ttbar,
  fakes_mumu,
  samples.singletop,
  samples.VV_ee,
  samples.ZtautauPowheg,
  samples.ttX,
  ]
elif options.samples == "OSCR":
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  samples.ttbar,
  samples.VV_ee,
  samples.singletop,
  fakes_mumu,
  samples.ttX,
  ]
elif options.samples == "SSVR":
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  fakes_mumu,
  samples.ttbar,
  samples.VV_ee,
  samples.singletop,
  samples.ttX,
  ]
elif options.samples == "diboson":
  mumu_backgrounds = [
  # samples.Zee221,
  # samples.ttbar,
  samples.diboson_sherpa,
  # samples.VV_ee,
  fakes_mumu,
  # samples.singletop,
  samples.ttX,
  samples.Higgs,
  # samples.WenuPowheg,
  ]
elif options.samples == "chargeflip":
  mumu_backgrounds = [
  samples.Zee221,
  ]

signal =[]

if options.makeplot == "True":
 funcs.plot_hist(
    backgrounds   = mumu_backgrounds,
    signal        = signal, 
    data          = data,
    region        = options.region,
    label         = options.label if options.label else mumu_vdict[options.vname]['label'],
    histname      = os.path.join(mumu_vdict[options.vname]['path'],mumu_vdict[options.vname]['hname']),
    xmin          = mumu_vdict[options.vname]['xmin'],
    xmax          = mumu_vdict[options.vname]['xmax'],
    rebin         = mumu_vdict[options.vname]['rebin'],
    rebinVar      = mumu_vdict[options.vname]['rebinVar'],
    log           = mumu_vdict[options.vname]['log'],
    logx          = mumu_vdict[options.vname]['logx'],
    icut          = int(options.icut),
    sys_dict      = sys_dict if DO_SYS else None,
    do_ratio_plot = mumu_vdict[options.vname]['do_ratio_plot'],
    save_eps      = True,
    plotsfile     = plotsfile
    )

else:
 funcs.write_hist(
         backgrounds = mumu_backgrounds,
         #signal      = mumu_backgrounds, # This can be a list
         data        = data,
         region      = options.region,
         icut        = int(options.icut),
         histname    = os.path.join(mumu_vdict[options.vname]['path'],mumu_vdict[options.vname]['hname']),
         rebin       = mumu_vdict[options.vname]['rebin'],
         rebinVar    = mumu_vdict[options.vname]['rebinVar'],
         sys_dict    = None,
         outname     = plotsfile
         )
 ## EOF



