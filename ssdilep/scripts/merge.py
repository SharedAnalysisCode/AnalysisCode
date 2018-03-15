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
ELE_SYS = True
MU_SYS = True


JET_SYS = True
THEORY_SYS = True

BRee = 0.
BRem = 0.
BRmm = 0.


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
parser.add_option('-E', '--elesys', dest='elesys',
                  help='elesys',metavar='ELESYS',default=None)
parser.add_option('-M', '--musys', dest='musys',
                  help='musys',metavar='MUSYS',default=None)
parser.add_option('', '--BRee', dest='BRee',
                  help='BRee',metavar='BREE',default=None)
parser.add_option('', '--BRem', dest='BRem',
                  help='BRem',metavar='BREM',default=None)
parser.add_option('', '--BRmm', dest='BRmm',
                  help='BRmm',metavar='BRMM',default=None)
parser.add_option('', '--ymin', dest='ymin',
                  help='ymin',metavar='ymin',default=None)
parser.add_option('', '--noNorm', dest='noNorm',
                  help='noNorm',metavar='noNorm',default=None)

(options, args) = parser.parse_args()

if options.sys == "False":
  DO_SYS = False

if options.elesys == "True":
  print "set ele sys to true"
  ELE_SYS = True

if options.musys == "True":
  MU_SYS = True

if options.BRee:
  BRee = options.BRee

if options.BRem:
  BRem = options.BRem

if options.BRmm:
  BRmm = options.BRmm

print "BRee: ", BRee
print "BRem: ", BRem
print "BRmm: ", BRmm

print "ELE_SYS: ", ELE_SYS


#-----------------
# Configuration
#-----------------
#lumi =  3158.13
#lumi =  18232.76
lumi =  36097.56
#lumi =  18232.8
#lumi = 5000

# Control regions
plotsfile = []
if options.makeplot == "False":
  plotsfile.append("hists")
plotsfile.append(options.vname)
plotsfile.append(options.region)
plotsfile.append(options.tag)

print plotsfile

plotsfile = "_".join(plotsfile)+".root"
plotsfile = os.path.join(options.outdir,plotsfile)

ROOT.gROOT.SetBatch(True)
hm = histmgr.HistMgr(basedir=options.indir,target_lumi=lumi)

#-----------------
# Samples        
#-----------------

## data
if options.samples in ["FFele","wjet"]:
  data = samples.dataEXOT19
elif options.samples ==  "ZPeak":
  data = samples.EXOT12_data
elif options.samples in  ["HNee","HNmumu","HNeeFit","HNmumuFit"]:
  data = samples.dataEXOT12
else:
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
  samples.Wenu221,
  samples.Zee221,
  samples.ttbar_inc,
  samples.diboson_sherpa221_all,
  samples.singletop_inc,
  samples.Wtaunu221,
  samples.Ztautau221,
  ]
elif options.samples == "FFele":
  mc_backgrounds = [
  samples.Wenu221,
  samples.Zee221,
  samples.diboson_sherpa221_all,
  samples.ttbar_inc,
  samples.singletop_inc,
  samples.Wtaunu221,
  samples.Ztautau221,
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
  samples.top_physics_noSC,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  # samples.singletop,
  # samples.ttX,
  # samples.AZNLOCTEQ6L1_DYtautau,
  ]
elif options.samples in ["SSVR","SSVRBLIND"]:
  mc_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  samples.top_physics_noSC,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  # samples.singletop,
  # samples.ttX,
  ]
elif options.samples in ["SSVR_emu"]:
  mc_backgrounds = [
  samples.diboson_sherpa221,
  samples.top_physics_noSC,
  # samples.VV_ee,
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  # samples.singletop,
  # samples.ttX,
  ]
elif options.samples in ["SSVR_mu","SSVRBLIND"]:
  mc_backgrounds = [
  # samples.AZNLOCTEQ6L1_DYee_DYtautau,
  samples.top_physics_noSC,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  # samples.singletop,
  # samples.ttX,
  ]
elif options.samples == "ZPeak":
  mc_backgrounds = [
  samples.ZeeSherpa221,
  samples.diboson_sherpa222_all,
  samples.top_physics_all,
  samples.WenuPowheg,
  samples.WtaunuPowheg,
  samples.Rare,
  # samples.Higgs,
  ]
elif options.samples == "HNee":
  mc_backgrounds = [
  samples.ZeeSherpa221,
  # samples.MGPy8Zee,
  # samples.diboson_sherpa222,
  samples.diboson_sherpa222_llll,
  samples.diboson_sherpa222_jj,
  samples.diboson_sherpa222_lllv,
  samples.diboson_sherpa222_gg,
  samples.diboson_sherpa222_xxll,
  samples.top_physics,
  # samples.Rare,
  ]
elif options.samples == "HNmumu":
  mc_backgrounds = [
  # samples.ZmmSherpa221,
  # samples.diboson_sherpa222,
  samples.diboson_sherpa222_llll,
  samples.diboson_sherpa222_jj,
  samples.diboson_sherpa222_lllv,
  samples.diboson_sherpa222_gg,
  samples.diboson_sherpa222_xxll,
  samples.top_physics,
  # samples.Rare,
  ]
elif options.samples == "HNeeFit":
  mc_backgrounds = [
  samples.ZeeSherpa221,
  # samples.MGPy8Zee,
  samples.diboson_sherpa222,
  samples.top_physics,
  # samples.Rare,
  ]
elif options.samples == "HNmumuFit":
  mc_backgrounds = [
  # samples.ZmmSherpa221,
  samples.diboson_sherpa222,
  samples.top_physics,
  # samples.Rare,
  ]
elif options.samples == "totalSM":
  mc_backgrounds = [
  samples.AllSM,
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
  samples.top_physics_noSC,
  # samples.Rare,
  ]
elif options.samples == "dibosonFit":
  mc_backgrounds = [
  samples.diboson_sherpa221,
  # samples.ttX,
  # samples.singletop,
  samples.top_physics_noSC,
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  ]
elif options.samples == "dibosonFit_mu":
  mc_backgrounds = [
  samples.diboson_sherpa221,
  # samples.ttX,
  # samples.singletop,
  samples.top_physics_noSC,
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
  samples.dibosonSherpaEE,
  samples.dibosonSysSample,
  samples.top_physics_noSC,
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
  samples.dibosonSherpaMM,
  samples.dibosonSysSample,
  samples.top_physics_noSC,
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
elif options.samples == "allSamples_emu":
  mc_backgrounds = [
  # samples.AZNLOCTEQ6L1_DYee,
  samples.dibosonSherpaEM,
  samples.dibosonSysSample,
  samples.top_physics_noSC,
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
elif options.samples == "signalEigenVectors":
  mc_backgrounds = samples.list_DCH
elif options.samples == "nothing":
  mc_backgrounds = []


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

# xsecL = [82.677, 34.825, 16.704, 8.7528, 4.9001, 2.882, 1.7631, 1.10919, 0.72042, 0.476508, 0.32154, 0.21991, 0.15288, 0.107411, 0.076403, 0.0547825, 0.039656, 0.0288885, 0.021202, 0.0156347, 0.011632, 0.00874109, 0.0065092]
# masses = [200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300]
xsecL = [82.677, 34.825, 16.704, 8.7528, 4.9001, 2.882, 1.7631, 1.10919, 0.72042, 0.476508, 0.32154, 0.21991, 0.15288, 0.107411, 0.076403, 0.0547825, 0.039656, 0.0288885, 0.021202, 0.0156347, 0.011632, 0.00874109]
masses = [200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250]


#--------------
# Estimators
#--------------

signalMassToPlots = [500,600,700]
BRsToPlot = [100]

signal = []

if options.signal == "True":
  if float(BRee) > 0 and float(BRmm)+float(BRem)==0:

    print "ee"

    for br in [10,50,100]:
      signal_samples += [[]]
      intiger = 1
      for mass,xsec in zip(masses,xsecL):
        if options.makeplot == "True":
          if mass not in signalMassToPlots or br not in BRsToPlot: continue
        name = "Pythia8EvtGen_A14NNPDF23LO_DCH%d" % mass
        print "tlatex: ", "DCH%d Br(ee)=%d" % (mass,br)
        globals()[name+"ee"+str(br)+"mm"+str(100-br)] = sample.Sample(
          name = name,
          tlatex = ("DCH%d Br(ee)=%d" % (mass,br)),
          line_color = intiger,
          marker_color = intiger,
          fill_color = intiger,
          line_width  = 3,
          line_style = 1,
          fill_style = 3004,
          xsec       = xsec/1000.,
          )
        signal_samples[len(signal_samples)-1] += [ globals()[name+"ee"+str(br)+"mm"+str(100-br)] ]
        intiger += 1

  elif float(BRem) > 0 and float(BRmm)+float(BRee)==0:

    print "em"

    for br in [10,50,100]:
      signal_samples += [[]]
      intiger = 1
      for mass,xsec in zip(masses,xsecL):
        if options.makeplot == "True":
          if mass not in signalMassToPlots or br not in BRsToPlot: continue
        name = "Pythia8EvtGen_A14NNPDF23LO_DCH%d" % mass
        print "tlatex: ", "DCH%d Br(e#mu)=%d" % (mass,br)
        globals()[name+"em"+str(br)+"mm"+str(100-br)] = sample.Sample(
          name = name,
          tlatex = ("DCH%d Br(e#mu)=%d" % (mass,br)),
          line_color = intiger,
          marker_color = intiger,
          fill_color = intiger,
          line_width  = 3,
          line_style = 1,
          fill_style = 3004,
          xsec       = xsec/1000.,
          )
        signal_samples[len(signal_samples)-1] += [ globals()[name+"em"+str(br)+"mm"+str(100-br)] ]
        intiger += 1

  elif float(BRmm) > 0 and float(BRee)+float(BRem)==0:

    print "mm"

    for br in [10,50,100]:
      signal_samples += [[]]
      intiger = 1
      for mass,xsec in zip(masses,xsecL):
        if options.makeplot == "True":
          if mass not in signalMassToPlots or br not in BRsToPlot: continue
        name = "Pythia8EvtGen_A14NNPDF23LO_DCH%d" % mass
        print "tlatex: ", "DCH%d Br(#mu#mu)=%d" % (mass,br)
        globals()[name+"ee"+str(100-br)+"mm"+str(br)] = sample.Sample(
          name = name,
          tlatex = ("DCH%d Br(#mu#mu)=%d" % (mass,br)),
          line_color = intiger,
          marker_color = intiger,
          fill_color = intiger,
          line_width  = 3,
          line_style = 1,
          fill_style = 3004,
          xsec       = xsec/1000.,
          )
        signal_samples[len(signal_samples)-1] += [ globals()[name+"ee"+str(100-br)+"mm"+str(br)] ]
        intiger += 1

  elif options.signal and float(BRmm)+float(BRee)+float(BRem)==0:
    pass


for samps in signal_samples:
  for s in samps:
    if float(BRee) > 0 and float(BRmm)+float(BRem)==0:
      br = re.findall("Br\([e#mu]*\)\=([0-9]*)",s.tlatex)[0]
      print "ee"
      s.estimator = histmgr.EstimatorDCH( hm=hm, ee=float(br)/100., mm=(1-float(br)/100.), em=0., sample=s )
      s.nameSuffix = "ee"+br+"mm"+str(int(100-float(br)))
    elif float(BRem) > 0 and float(BRmm)+float(BRee)==0:
      br = re.findall("Br\([e#mu]*\)\=([0-9]*)",s.tlatex)[0]
      print "em"
      s.estimator = histmgr.EstimatorDCH( hm=hm, em=float(br)/100., mm=(1-float(br)/100.), ee=0., sample=s )
      s.nameSuffix = "em"+br+"mm"+str(int(100-float(br)))
    elif float(BRmm) > 0 and float(BRee)+float(BRem)==0:
      br = re.findall("Br\([e#mu]*\)\=([0-9]*)",s.tlatex)[0]
      print "mm"
      s.estimator = histmgr.EstimatorDCH( hm=hm, em=0., mm=float(br)/100., ee=(1-float(br)/100.), sample=s )
      s.nameSuffix = "ee"+str(int(100-float(br)))+"mm"+br
    elif options.signal and float(BRmm)+float(BRee)+float(BRem)==0:
      pass
    # print float(br)
    # print s.nameSuffix
    signal += [s]


signal = samples.list_HN


for s in [data] + mc_backgrounds + signal:
    histmgr.load_base_estimator(hm,s)
    if options.samples == "signalEigenVectors":
      s.nameSuffix = re.findall(".*signal-([em]*)",options.region)[0]
      print s.name
      print s.nameSuffix


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

elif options.fakest == "MCFakes":
  fakes_mumu.estimator = histmgr.MCFakes(
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

mumu_vdict  = vars_ee.vars_dict
#fakes_vdict = vars_fakes.vars_dict

#-----------------
# Plotting 
#-----------------
mumu_backgrounds = []

if options.samples == "wjet":
  mumu_backgrounds = [
  samples.Wenu221,
  fakes_mumu,
  samples.Zee221,
  samples.ttbar_inc,
  samples.diboson_sherpa221_all,
  samples.singletop_inc,
  samples.Wtaunu221,
  samples.Ztautau221,
  ]
elif options.samples == "FFele":
  mumu_backgrounds = [
  samples.Wenu221,
  samples.Zee221,
  samples.diboson_sherpa221_all,
  samples.ttbar_inc,
  samples.singletop_inc,
  samples.Wtaunu221,
  samples.Ztautau221,
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
  samples.top_physics_noSC,
  samples.diboson_sherpa221,
  # samples.singletop,
  fakes_mumu,
  # samples.AZNLOCTEQ6L1_DYtautau,
  ]
elif options.samples == "ZPeak":
  mumu_backgrounds = [
  samples.ZeeSherpa221,
  samples.diboson_sherpa222_all,
  samples.top_physics_all,
  # samples.ttbar_Py8,
  # samples.singletop_inc,
  # samples.ttX,
  # samples.WenuPowheg,
  # samples.WtaunuPowheg,
  # samples.Ztautau221,
  samples.WenuPowheg,
  samples.WtaunuPowheg,
  samples.Rare,
  # samples.Higgs,
  ]
elif options.samples == "totalSM":
  mumu_backgrounds = [
  samples.AllSM,
  ]
elif options.samples in ["SSVR","SSVRBLIND"]:
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  fakes_mumu,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  samples.top_physics_noSC,
  # samples.singletop,
  # samples.ttX,
  ]
elif options.samples in ["SSVR_emu"]:
  mumu_backgrounds = [
  samples.diboson_sherpa221,
  fakes_mumu,
  samples.top_physics_noSC,
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  # samples.VV_ee,
  # samples.singletop,
  # samples.ttX,
  ]
elif options.samples in ["SSVR_mu"]:
  mumu_backgrounds = [
  # samples.AZNLOCTEQ6L1_DYee_DYtautau,
  fakes_mumu,
  # samples.VV_ee,
  samples.diboson_sherpa221,
  samples.top_physics_noSC,
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
  samples.top_physics_noSC,
  # samples.Rare,
  # samples.WenuPowheg,
  ]
elif options.samples == "dibosonFit":
  mumu_backgrounds = [
  samples.diboson_sherpa221,
  fakes_mumu,
  # samples.ttX,
  # samples.singletop,
  samples.top_physics_noSC,
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  ]
elif options.samples == "dibosonFit_mu":
  mumu_backgrounds = [
  samples.diboson_sherpa221,
  fakes_mumu,
  # samples.ttX,
  # samples.singletop,
  samples.top_physics_noSC,
  ]
elif options.samples in ["chargeflip","chargeflipTruth"]:
  mumu_backgrounds = [
  samples.Zee221,
  ]
elif options.samples == "HNee":
  mumu_backgrounds = [
  samples.ZeeSherpa221,
  # samples.MGPy8Zee,
  # samples.diboson_sherpa222,
  samples.diboson_sherpa222_llll,
  samples.diboson_sherpa222_jj,
  samples.diboson_sherpa222_lllv,
  samples.diboson_sherpa222_gg,
  samples.diboson_sherpa222_xxll,
  samples.top_physics,
  # samples.Rare,
  fakes_mumu,
  ]
elif options.samples == "HNmumu":
  mumu_backgrounds = [
  # samples.ZmmSherpa221,
  # samples.diboson_sherpa222,
  samples.diboson_sherpa222_llll,
  samples.diboson_sherpa222_jj,
  samples.diboson_sherpa222_lllv,
  samples.diboson_sherpa222_gg,
  samples.diboson_sherpa222_xxll,
  samples.top_physics,
  # samples.Rare,
  fakes_mumu,
  ]
elif options.samples == "HNeeFit":
  mumu_backgrounds = [
  samples.ZeeSherpa221,
  # samples.MGPy8Zee,
  samples.diboson_sherpa222,
  samples.top_physics,
  # samples.Rare,
  fakes_mumu,
  ]
elif options.samples == "HNmumuFit":
  mumu_backgrounds = [
  # samples.ZmmSherpa221,
  samples.diboson_sherpa222,
  samples.top_physics,
  # samples.Rare,
  fakes_mumu,
  ]
elif options.samples in ["chargeflipPowheg","chargeflipTruthPowheg"]:
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee,
  ]
elif options.samples == "allSamples":
  mumu_backgrounds = [
  samples.AZNLOCTEQ6L1_DYee_DYtautau,
  samples.dibosonSherpaEE,
  samples.dibosonSysSample,
  samples.top_physics_noSC,
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
  samples.dibosonSherpaMM,
  samples.dibosonSysSample,
  samples.top_physics_noSC,
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
elif options.samples == "allSamples_emu":
  mumu_backgrounds = [
  # samples.AZNLOCTEQ6L1_DYee,
  samples.dibosonSherpaEM,
  samples.dibosonSysSample,
  samples.top_physics_noSC,
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
elif options.samples == "signalEigenVectors":
  mumu_backgrounds = samples.list_DCH
elif options.samples == "nothing":
  mumu_backgrounds = []


sys_list_ele = [
EG_RESOLUTION_ALL,
EG_SCALE_ALLCORR,
EG_SCALE_E4SCINTILLATOR,
CF,
TRIG,
ID,
ISO,
RECO,
]

sys_list_muon = [
MUON_ID,
MUON_MS,
MUON_RESBIAS,
MUON_RHO,
MUON_SCALE,
TRIGSTAT,
TRIGSYS,
ISOSYS,
ISOSTAT,
RECOSYS,
RECOSTAT,
TTVASYS,
TTVASTAT,
]

sys_list_jet = [
B_SYS,
C_SYS,
L_SYS,
E_SYS,
EFC_SYS,
JVT_SYS,
JET_BJES_Response,
JET_EffectiveNP_1,
JET_EffectiveNP_2,
JET_EffectiveNP_3,
JET_EffectiveNP_4,
JET_EffectiveNP_5,
JET_EffectiveNP_6,
JET_EffectiveNP_7,
JET_EffectiveNP_8restTerm,
JET_EtaIntercalibration_Modelling,
JET_EtaIntercalibration_NonClosure,
JET_EtaIntercalibration_TotalStat,
JET_Flavor_Composition,
JET_Flavor_Response,
JET_Pileup_OffsetMu,
JET_Pileup_OffsetNPV,
JET_Pileup_PtTerm,
JET_Pileup_RhoTopology,
JET_PunchThrough_MC15,
JET_SingleParticle_HighPt,
JET_JER_CROSS_CALIB_FORWARD,
JET_JER_NOISE_FORWARD,
JET_JER_NP0,
JET_JER_NP1,
JET_JER_NP2,
JET_JER_NP3,
JET_JER_NP4,
JET_JER_NP5,
JET_JER_NP6,
JET_JER_NP7,
JET_JER_NP8,
]

sys_list_theory = [
ALPHA_SYS,
QCD_SCALE_ENVELOPE,
PDF_COICE_ENVELOPE,
PDF_SYS_ENVELOPE,
]

print "MU SYS, ",MU_SYS

if (DO_SYS):
  if options.fakest!="" and ELE_SYS:
    print "Fake Factor Sys"
    fakes_mumu.estimator.add_systematics(FF)
  if MU_SYS:
    fakes_mumu.estimator.add_systematics(MUFF)
  for sample in mumu_backgrounds:
    if sample in [samples.dibosonSysSample,samples.ttbar_Py8_up,samples.ttbar_Py8_do,samples.ttbar_Herwig,samples.ttbar_Py8_aMcAtNlo,samples.ttbar_Py8_CF]:
      print "skip sys MC samples in other systematics"
      continue
    if THEORY_SYS:
      for sys in sys_list_theory:
        sample.estimator.add_systematics(sys)  
    if JET_SYS:
      for sys in sys_list_jet:
        sample.estimator.add_systematics(sys)
    if ELE_SYS:
      for sys in sys_list_ele:
        sample.estimator.add_systematics(sys)
    if MU_SYS:
      for sys in sys_list_muon:
        sample.estimator.add_systematics(sys)
  for sample in signal:
    if JET_SYS:
      for sys in sys_list_jet:
        sample.estimator.add_systematics(sys)
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

tempNoNorm = None
if options.noNorm=="True":
  tempNoNorm = True
elif options.noNorm=="False":
  tempNoNorm = False

HNsignal1 = samples.Sample( name = "MadGraphPythia8EvtGen_A14NNPDF23LO_LRSM_WR600_NR500",
          tlatex = "WR600 NR500",
          line_color = ROOT.kRed-4,
          fill_color = ROOT.kRed-2,
          line_width  = 3,
          line_style = 1,
          fill_style = 0,
          xsec       = 8.7848,
          )
histmgr.load_base_estimator(hm,HNsignal1)

HNsignal2 = samples.Sample( name = "MadGraphPythia8EvtGen_A14NNPDF23LO_LRSM_WR1000_NR700",
          tlatex = "WR1000 NR700",
          line_color = ROOT.kGreen-7,
          fill_color = ROOT.kGreen-5,
          line_width  = 3,
          line_style = 1,
          fill_style = 0,
          xsec       = 2.7778,
          )
histmgr.load_base_estimator(hm,HNsignal2)

HNsignal3 = samples.Sample( name = "MadGraphPythia8EvtGen_A14NNPDF23LO_LRSM_WR1200_NR600",
          tlatex = "WR1200 NR600",
          line_color = ROOT.kBlue-7,
          fill_color = ROOT.kBlue-5,
          line_width  = 3,
          line_style = 1,
          fill_style = 0,
          xsec       = 2.3153,
          )
histmgr.load_base_estimator(hm,HNsignal3)


if options.rebinToEq!="True":
  signal = [HNsignal1,HNsignal2,HNsignal3]

if options.makeplot == "True":
 funcs.plot_hist(
    backgrounds   = mumu_backgrounds,
    signal        = signal if options.signal=="True" else None, 
    data          = data if options.samples not in ["chargeflipTruth","chargeflipTruthPowheg","nothing"] else None,
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
    Ymin          = float(options.ymin) if options.ymin else 1e-2,
    )

else:
 funcs.write_hist(
         backgrounds = mumu_backgrounds,
         signal      = signal if options.signal=="True" else None, 
         data        = data if options.samples not in ["chargeflipTruth","chargeflipTruthPowheg","signalEigenVectors","nothing"] else None,
         region      = options.region,
         icut        = int(options.icut),
         histname    = os.path.join(mumu_vdict[options.vname]['path'],mumu_vdict[options.vname]['hname']),
         rebin       = mumu_vdict[options.vname]['rebin'],
         rebinVar    = mumu_vdict[options.vname]['rebinVar'],
         sys_dict    = sys_dict if DO_SYS else None,
         outname     = plotsfile,
         regName     = options.tag,
         rebinToEq   = True if options.rebinToEq=="True" else False,
         varName     = str(options.varName),
         noNorm      = tempNoNorm
         )
 ## EOF



