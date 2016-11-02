#!/usr/bin/python

import os
import subprocess
import time
from ssdilep import plots

def make_tag(cat,var):
  return '_'.join([cat,var])

#---------------------
# Set environment
#---------------------
# Environment variables defined in batchsetup.sh

ana      = 'ssdilep'

indir    = 'Hist18SepSys'
outdir   = 'Plots18SepSys'

USER    = os.getenv('USER')
MAIN    = os.getenv('MAIN')

inpath  = os.path.join("/coepp/cephfs/mel",USER,ana)
INDIR   = os.path.join(inpath,indir)  
OUTDIR  = os.path.join(inpath,outdir)

if not os.path.isdir(OUTDIR): os.makedirs(OUTDIR)
if not os.path.isdir(OUTDIR+"/"+"log"): os.makedirs(OUTDIR+"/"+"log")

#---------------------
# Batch jobs options
#---------------------
AUTOBUILD = True
QUEUE     = 'short'
BEXEC     = 'Plots.sh'
JOBDIR    = "/coepp/cephfs/mel/%s/jobdir" % USER

#---------------------
# Batch jobs variables
#---------------------
INTARBALL = os.path.join(JOBDIR,'plotstarball_%s.tar.gz' % (time.strftime("d%d_m%m_y%Y_H%H_M%M_S%S")) )
SCRIPT    = os.path.join("./",ana,"scripts",'merge.py')

job_vars={}
job_vars['INTARBALL'] = INTARBALL
job_vars['OUTDIR']    = OUTDIR
job_vars['INDIR']     = INDIR
job_vars['SCRIPT']    = SCRIPT

#fake_estimate = "FakeFactor"
fake_estimate = "Subtraction"

regions = {}
# use it as such:
#regions["FOLDERNAME"]     = [icut, "plot label"]
"""
regions["FAKESVR1_NUM"]   = [5,  "VR1 numerator"]
regions["FAKESVR1_LTDEN"] = [5,"VR1 loose+tight"]
regions["FAKESVR1_TLDEN"] = [5,"VR1 tight+loose"]
regions["FAKESVR1_LLDEN"] = [5,"VR1 loose+loose"]

regions["FAKESVR2_NUM"]   = [5,  "VR2 numerator"]
regions["FAKESVR2_LTDEN"] = [5,"VR2 loose+tight"]
regions["FAKESVR2_TLDEN"] = [5,"VR2 tight+loose"]
regions["FAKESVR2_LLDEN"] = [5,"VR2 loose+loose"]

regions["FAKESVR3_NUM"]   = [4,  "VR3 numerator"]
regions["FAKESVR3_LTDEN"] = [4,"VR3 loose+tight"]
regions["FAKESVR3_TLDEN"] = [4,"VR3 tight+loose"]
regions["FAKESVR3_LLDEN"] = [4,"VR3 loose+loose"]

regions["FAKESVR4_NUM"]   = [5,  "VR4 numerator"]
regions["FAKESVR4_LTDEN"] = [5,"VR4 loose+tight"]
regions["FAKESVR4_TLDEN"] = [5,"VR4 tight+loose"]
regions["FAKESVR4_LLDEN"] = [5,"VR4 loose+loose"]

regions["FAKESVR5_NUM"]   = [6,  "VR5 numerator"]
regions["FAKESVR5_LTDEN"] = [6,"VR5 loose+tight"]
regions["FAKESVR5_TLDEN"] = [6,"VR5 tight+loose"]
regions["FAKESVR5_LLDEN"] = [6,"VR5 loose+loose"]

regions["FAKESVR6_NUM"]   = [7,  "VR6 numerator"]
regions["FAKESVR6_LTDEN"] = [7,"VR6 loose+tight"]
regions["FAKESVR6_TLDEN"] = [7,"VR6 tight+loose"]
regions["FAKESVR6_LLDEN"] = [7,"VR6 loose+loose"]

regions["FAKESVR7_NUM"]   = [6,  "VR7 numerator"]
regions["FAKESVR7_LTDEN"] = [6,"VR7 loose+tight"]
regions["FAKESVR7_TLDEN"] = [6,"VR7 tight+loose"]
regions["FAKESVR7_LLDEN"] = [6,"VR7 loose+loose"]
"""


regions["FAKESFR1_NUM"]   = [8,  "di-jet numerator", "Sherpa"]
#regions["FAKESFR1_DEN"]   = [8,  "di-jet denominator", "Sherpa"]

"""
regions["FAKESFR2_NUM"]   = [9,  "di-jet numerator", "Sherpa"]
regions["FAKESFR2_DEN"]   = [9,  "di-jet denominator", "Sherpa"]


regions["FAKESFR3_NUM"]   = [9,  "di-jet numerator", "Sherpa"]
regions["FAKESFR3_DEN"]   = [9,  "di-jet denominator", "Sherpa"]

regions["FAKESFR4_NUM"]   = [9,  "di-jet numerator", "Sherpa"]
regions["FAKESFR4_DEN"]   = [9,  "di-jet denominator", "Sherpa"]

regions["FAKESFR5_NUM"]   = [9,  "di-jet numerator", "Sherpa"]
regions["FAKESFR5_DEN"]   = [9,  "di-jet denominator", "Sherpa"]

regions["FAKESFR6_NUM"]   = [9,  "di-jet numerator", "Sherpa"]
regions["FAKESFR6_DEN"]   = [9,  "di-jet denominator", "Sherpa"]

regions["FAKESFR7_NUM"]   = [9,  "di-jet numerator", "Sherpa"]
regions["FAKESFR7_DEN"]   = [9,  "di-jet denominator", "Sherpa"]

regions["FAKESFR8_NUM"]   = [9,  "di-jet numerator", "Sherpa"]
regions["FAKESFR8_DEN"]   = [9,  "di-jet denominator", "Sherpa"]
"""

#---------------------
# Make input tarball
#---------------------
if os.path.exists(os.path.join(INTARBALL)):
  print 'removing existing tarball %s...'% (INTARBALL)
  cmd = 'rm %s' % (INTARBALL)
  m = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
  m.communicate()[0]

print 'building input tarball %s...'% (INTARBALL)
cmd = 'cd %s; make -f Makefile.plots TARBALL=%s' % (MAIN,INTARBALL)
m = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
m.communicate()[0]


for REG,OPT in regions.iteritems():
  vars_list = plots.vars_mumu.vars_list
  #vars_list = plots.vars_fakes.vars_list

  for var in vars_list:

    job_vars['VAR']      = var.name
    job_vars['REG']      = REG
    job_vars['ICUT']     = OPT[0]
    job_vars['LAB']      = OPT[1]
    job_vars['TAG']      = OPT[2]
    job_vars['MAKEPLOT'] = True
    job_vars['FAKEST']   = fake_estimate
    
    VARS = []
    
    for vname in job_vars.keys(): VARS += ['%s=%s' % (vname,job_vars[vname])]
    
    cmd = 'qsub'
    cmd += " -q %s" % QUEUE
    cmd += ' -v "%s"' % (','.join(VARS))
    cmd += ' -N j.plots.%s' % (make_tag(REG,job_vars['VAR']))
    cmd += ' -o %s/log' % (OUTDIR)
    cmd += ' -e %s/log' % (OUTDIR)
    cmd += ' %s' % BEXEC
    print cmd
    m = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    print m.communicate()[0]
 
 
## EOF

