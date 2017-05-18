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

jobName = 'user.mmuskinj.testFederico127'

cmd = 'prun --exec "batch/GridScript.sh %IN %IN2 %IN3"'
cmd+= ' --inDS user.mmuskinj.SSDiLep.EX12MC.v3.sys.002.410069.MadGraphPythia8EvtGen_A14NNPDF23LO_ttZllonshell_Np0_tree.root'
cmd+= ' --secondaryDSs IN2:1:user.mmuskinj.SSDiLep.EX12MC.v3.sys.002.410069.MadGraphPythia8EvtGen_A14NNPDF23LO_ttZllonshell_Np0_metadata.root,IN3:1:user.mmuskinj.SSDiLep.EX12MC.v3.sys.002.410069.MadGraphPythia8EvtGen_A14NNPDF23LO_ttZllonshell_Np0_cutflow.root'
cmd+= ' --nFilesPerJob 1'
cmd+= ' --extFile ssdilep/data/chargeFlipRates-28-03-2017.root,ssdilep/data/fakeFactor-16-05-2017.root'
cmd+= ' --excludeFile run'
cmd+= ' --mergeOutput'
cmd+= ' --outputs out.root'
cmd+= ' --outDS ' + jobName

print cmd

m = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
print m.communicate()[0]