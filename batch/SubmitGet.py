import os
import sys
import subprocess

from pyutils.utils import recreplace, mcstrings

## list jobs output
## it wildcards around jtag!

from optparse import OptionParser

parser = OptionParser()
parser.add_option('-s', '--samp', dest='sample',
                  help='sample name',metavar='SAMP',default="")
(options, args) = parser.parse_args()



# --------------
user  = "fscutti"
samp  = options.sample

#jtag  = "HIGG3D3_v3_p2689.*%s*" % samp
jtag  = "EXOT12_v3_l3_p2689.*%s*" % samp
jtype = "SSDiLep"
sys   = None
if not sys: sys = "nominal"
# --------------


# --------------
SCRIPT     = "Get.sh"
#OUTDIR     = "/coepp/cephfs/mel/fscutti/ssdilep/HIGG3D3_v3_p2689"
OUTDIR     = "/coepp/cephfs/mel/fscutti/ssdilep/EXOT12_v3_l3_p2689"

OUTMERGED  = os.path.join(OUTDIR,"merged",sys)
OUTTREE    = os.path.join(OUTDIR,"tree",sys)
OUTMETA    = os.path.join(OUTDIR,"metadata",sys)
OUTCUTFLOW = os.path.join(OUTDIR,"cutflow",sys)
OUTLOGS    = os.path.join(OUTDIR,"log",sys)
JOB_TAG    = jtag
QUEUE      = "long"
# --------------

JOBDIR    = "/coepp/cephfs/mel/fscutti/jobdir" 

dir_list = []
dir_list.append(os.path.join(OUTDIR,"tree"))
dir_list.append(os.path.join(OUTDIR,"tree",sys))
dir_list.append(os.path.join(OUTDIR,"metadata"))
dir_list.append(os.path.join(OUTDIR,"metadata",sys))
dir_list.append(os.path.join(OUTDIR,"cutflow"))
dir_list.append(os.path.join(OUTDIR,"cutflow",sys))
dir_list.append(os.path.join(OUTDIR,"merged"))
dir_list.append(os.path.join(OUTDIR,"merged",sys))
dir_list.append(os.path.join(OUTDIR,"log"))
dir_list.append(os.path.join(OUTDIR,"log",sys))

for d in dir_list:
 if not os.path.exists(d):
   os.makedirs(d)

outjobs_tree = "%s_%s_%s_tree.txt" % (user, jtype, jtag)
outjobs_meta = "%s_%s_%s_metadata.txt" % (user, jtype, jtag)
outjobs_cutflow = "%s_%s_%s_cutflow.txt" % (user, jtype, jtag)

outjobs_tree = recreplace(outjobs_tree,[["*","X"]])
outjobs_meta = recreplace(outjobs_meta,[["*","X"]])
outjobs_cutflow = recreplace(outjobs_cutflow,[["*","X"]])


infile_tree = os.path.join(JOBDIR,outjobs_tree)
infile_meta = os.path.join(JOBDIR,outjobs_meta)
infile_cutflow = os.path.join(JOBDIR,outjobs_cutflow)

with open(infile_tree,"w") as f:
  cmd = "rucio list-dids"
  cmd += " %s.%s:" % ("user",user)
  cmd += "%s.%s.%s.*%s*tree*" % ("user",user,jtype,jtag)
  print cmd
  m = subprocess.Popen(cmd,shell=True,stdout=f)
  print m.communicate()[0]
f.close()

with open(infile_meta,"w") as f:
  cmd = "rucio list-dids"
  cmd += " %s.%s:" % ("user",user)
  cmd += "%s.%s.%s.*%s*metadata*" % ("user",user,jtype,jtag)
  print cmd
  m = subprocess.Popen(cmd,shell=True,stdout=f)
  print m.communicate()[0]
f.close()

with open(infile_cutflow,"w") as f:
  cmd = "rucio list-dids"
  cmd += " %s.%s:" % ("user",user)
  cmd += "%s.%s.%s.*%s*cutflow*" % ("user",user,jtype,jtag)
  print cmd
  m = subprocess.Popen(cmd,shell=True,stdout=f)
  print m.communicate()[0]
f.close()

outputs = {}

rep = []
rep.append([" ",""])
rep.append(["\n",""])
rep.append(["|",""])
rep.append(["CONTAINER",""])
rep.append(["user.fscutti:",""])

with open(infile_tree) as f: lines = f.readlines()
for l in lines:
  if not "CONTAINER" in l: continue
  if "duplicates" in l: continue
  key = recreplace(l.replace("_tree",""),rep)
  outputs[key] = {}
  print key
  outputs[key]["tree"] = recreplace(l,rep)
f.close()

with open(infile_cutflow) as f: lines = f.readlines()
for l in lines:
  if not "CONTAINER" in l: continue
  if "duplicates" in l: continue
  key = recreplace(l.replace("_cutflow",""),rep)
  outputs[key]["cutflow"] = recreplace(l,rep)
f.close()

with open(infile_meta) as f: lines = f.readlines()
for l in lines:
  if not "CONTAINER" in l: continue
  if "duplicates" in l: continue
  key = recreplace(l.replace("_metadata",""),rep)
  outputs[key]["metadata"] = recreplace(l,rep)
f.close()

jrep = []
jrep.append(["user",""])
jrep.append([user,""])
jrep.append([":",""])
jrep.append(["..",""])
jrep.append([".root",""])

for k,v in outputs.iteritems():
  print 'downloading %s ...' % k
  job_name = recreplace(k,jrep)
  if job_name.startswith("."): job_name = job_name[1:]
  if "physics_Main" in job_name: id = k.split(".")[5]+"_"+k.split(".")[4]
  else: id = k.split(".")[5]
  merged = recreplace(id, mcstrings)
  
  vars=[]
  vars+=["TREEFILE=%s"      % v["tree"]              ]
  vars+=["METAFILE=%s"      % v["metadata"]          ]
  vars+=["CUTFLOWFILE=%s"   % v["cutflow"]           ]
  vars+=["MERGEDTREE=%s"    % merged+"_tree.root"    ] 
  vars+=["MERGEDMETA=%s"    % merged+"_metadata.root"] 
  vars+=["MERGEDCUTFLOW=%s" % merged+"_cutflow.root" ] 
  vars+=["OUTTREE=%s"       % OUTTREE                ]
  vars+=["OUTMETA=%s"       % OUTMETA                ]
  vars+=["OUTCUTFLOW=%s"    % OUTCUTFLOW             ]
  vars+=["MERGED=%s"        % merged+".root"         ]
  vars+=["OUTMERGED=%s"     % OUTMERGED              ]

  VARS = ','.join(vars)

  cmd = 'qsub'
  cmd += ' -q %s'       % QUEUE
  cmd += ' -v "%s"'     % VARS
  cmd += ' -N j.get.%s' % job_name
  cmd += ' -j n -o %s'  % OUTLOGS
  cmd += ' -e %s'       % OUTLOGS
  cmd += ' %s'          % SCRIPT
  
  print cmd
  m = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
  print m.communicate()[0]

