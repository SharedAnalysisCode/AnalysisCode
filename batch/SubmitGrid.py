# encoding: utf-8
'''
SubmitHist.py
'''
import ROOT

## modules
import os
import re
import subprocess
import time
from   ssdilep.samples import samples

# SCRIPT="./ssdilep/run/j.plotter_WJets.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_CReleDiboson.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_ThreeEleVR.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_FFele.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_CRele.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_CReleTTBAR.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_ZPeak.py"  # pyframe job script
SCRIPT="./ssdilep/run/j.plotter_ele_allR.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_SSVRele.py"  # pyframe job script

JOBNAME = "test1"

DO_NTUP_SYS = False                  # submit the NTUP systematics jobs
TESTMODE = False                     # submit only 1 sub-job (for testing)


DO_NOM = False                        # submit the nominal job

DO_PLOT_SYS = True                  # submit the plot systematics jobs

CF_SYS = True
FF_SYS = False

BEAM_SYS = True
CHOICE_SYS = True
PDF_SYS = True
PI_SYS = True
SCALE_Z_SYS = True

EG_RESOLUTION_ALL_SYS = True
EG_SCALE_ALLCORR_SYS = True
EG_SCALE_E4SCINTILLATOR_SYS = True

TRIG_SYS = True
ID_SYS = True
ISO_SYS = True
RECO_SYS = True


def main():
  """
  * configure the samples (input->output)
  * configure which samples to run for each systematic
  * prepare outdirs and build intarball
  * launch the jobs
  """
  global MAIN
  global USER
  global NTUP
  global INTARBALL
  global AUTOBUILD
  global RUN
  global OUTPATH
  global OUTFILE
  global QUEUE
  global SCRIPT
  global BEXEC
  global DO_NOM
  global DO_NTUP_SYS
  global DO_PLOT_SYS
  global TESTMODE

  ## get lists of samples
  all_mc   = samples.all_mc
  all_data = samples.all_data

  nominal = all_mc 
  # nominal += all_data
  
  ntup_sys = [
      ['SYS1_UP',                  all_mc],
      ['SYS1_DN',                  all_mc],
      ]    
  
  plot_sys = []
  if CF_SYS:
      plot_sys += [
          ['CF_UP',        nominal],
          ['CF_DN',        nominal],
          ]  
  if FF_SYS:
      plot_sys += [
          ['FF_UP',        nominal],
          ['FF_DN',        nominal],
          ]  
  if BEAM_SYS:
      plot_sys += [
          ['BEAM_UP',        nominal],
          ['BEAM_DN',        nominal],
          ]  
  if CHOICE_SYS:
      plot_sys += [
          ['CHOICE_UP',        nominal],
          ['CHOICE_DN',        nominal],
          ]  
  if PDF_SYS:
      plot_sys += [
          ['PDF_UP',        nominal],
          ['PDF_DN',        nominal],
          ]  
  if PI_SYS:
      plot_sys += [
          ['PI_UP',        nominal],
          ['PI_DN',        nominal],
          ]  
  if SCALE_Z_SYS:
      plot_sys += [
          ['SCALE_Z_UP',        nominal],
          ['SCALE_Z_DN',        nominal],
          ]  
  if EG_RESOLUTION_ALL_SYS:
      plot_sys += [
          ['EG_RESOLUTION_ALL_UP',        nominal],
          ['EG_RESOLUTION_ALL_DN',        nominal],
          ]  
  if EG_SCALE_ALLCORR_SYS:
      plot_sys += [
          ['EG_SCALE_ALLCORR_UP',        nominal],
          ['EG_SCALE_ALLCORR_DN',        nominal],
          ]  
  if EG_SCALE_E4SCINTILLATOR_SYS:
      plot_sys += [
          ['EG_SCALE_E4SCINTILLATOR_UP',        nominal],
          ['EG_SCALE_E4SCINTILLATOR_DN',        nominal],
          ]  
  if TRIG_SYS:
      plot_sys += [
          ['TRIG_UP',        nominal],
          ['TRIG_DN',        nominal],
          ]  
  if ID_SYS:
      plot_sys += [
          ['ID_UP',        nominal],
          ['ID_DN',        nominal],
          ]  
  if ISO_SYS:
      plot_sys += [
          ['ISO_UP',        nominal],
          ['ISO_DN',        nominal],
          ]  
  if RECO_SYS:
      plot_sys += [
          ['RECO_UP',        nominal],
          ['RECO_DN',        nominal],
          ]  

  if DO_NOM: submit('nominal','nominal',nominal)
  if DO_NTUP_SYS: 
    for sys,samps in ntup_sys:
          submit(sys,sys,samps)
  if DO_PLOT_SYS:  
    for sys,samps in plot_sys:
          submit(sys,'nominal',samps,config={'sys':sys})


def submit(tag,job_sys,samps,config={}):
  """
  * construct config file 
  * prepare variable list to pass to job
  * submit job
  """
  global MAIN
  global USER
  global NTUP
  global INTARBALL
  global AUTOBUILD
  global RUN
  global OUTPATH
  global OUTFILE
  global QUEUE
  global SCRIPT
  global BEXEC
  global DO_NOM
  global DO_NTUP_SYS
  global DO_PLOT_SYS
  global TESTMODE
  global JOBNAME

  sample_list = ""
  sample_file = 'filelists/v3ntuples_fullSys.txt'
  with open(sample_file, 'r') as f:
    sample_list = f.read()
  f.closed

  for s in samps:
    if len(config) > 0:
      ## skip signal and alt samples
      if s in samples.diboson_powheg_alt.daughters:
        continue
      elif s in samples.ttbar_Py8_alt.daughters:
        continue
      elif s in [samples.Pythia8EvtGen_A14NNPDF23LO_DCH450, samples.Pythia8EvtGen_A14NNPDF23LO_DCH1100]:
        continue
      elif s in samples.all_DCH.daughters and config['sys'] in ['CF_UP','CF_DN','FF_DN','FF_UP']:
        continue
      elif s in samples.all_data and config['sys'] not in ['FF_UP','FF_DN']:
        continue
      elif s not in samples.AZNLOCTEQ6L1_DYee_DYtautau.daughters and config['sys'] in ["BEAM_UP","CHOICE_UP","PDF_UP","BEAM_UP","PI_UP","SCALE_Z_UP","BEAM_DN","CHOICE_DN","PDF_DN","BEAM_DN","PI_DN","SCALE_Z_DN"]:
        continue

    jobName = "user.mmuskinj." + JOBNAME + "." + s.name + "." + (config['sys'] if len(config) > 0 else "nominal")

    assert len(re.findall(".*" + s.name + ".*",sample_list)) == 1, "WARNING!! sample " + s.name + " not found or has multiple entries in " + sample_file
    dataset = re.findall(".*" + s.name + ".*",sample_list)[0]

    datasetType = "data" if s in samples.all_data else "mc"

    cmd = ""
    if len(config) == 0:
      cmd+= 'prun --exec "batch/GridScript.sh %IN %IN2 %IN3 ' + SCRIPT + ' ' + datasetType + '"'
    elif len(config) > 0:
      cmd+= 'prun --exec "batch/GridScript.sh %IN %IN2 %IN3 ' + SCRIPT + ' ' + datasetType + ' ' + config['sys'] + '"'
    cmd+= ' --inDS ' + dataset+'_tree.root'
    cmd+= ' --secondaryDSs IN2:1:' + dataset+'_metadata.root' + ',IN3:1:' + dataset+'_cutflow.root'
    cmd+= ' --nFilesPerJob 1'
    cmd+= ' --extFile ssdilep/data/chargeFlipRates-28-03-2017.root,ssdilep/data/fakeFactor-16-05-2017.root'
    cmd+= ' --excludeFile run/'
    cmd+= ' --mergeOutput'
    cmd+= ' --rootVer=6.04/14 --cmtConfig=x86_64-slc6-gcc49-opt'
    cmd+= ' --outputs out.root'
    cmd+= ' --outDS ' + jobName
    print cmd
    m = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    print m.communicate()[0]

if __name__=='__main__': main()