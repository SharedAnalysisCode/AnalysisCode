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

## environment variables
MAIN   = os.getenv('MAIN') # upper folder
USER   = os.getenv('USER')

## global config
# inputs
#NTUP='/coepp/cephfs/mel/fscutti/ssdilep/presc/merged' # input NTUP path
#NTUP='/coepp/cephfs/mel/fscutti/ssdilep/menu_singlemu/merged' # input NTUP path
#NTUP='/coepp/cephfs/mel/fscutti/ssdilep/HIGG3D3_p2666_p2667_v1_presc/merged' # input NTUP path
#NTUP='/ceph/grid/home/atlas/miham/ntuples/v2ntuples18ifb/mergedEXOT19and0' # input NTUP path
NTUP='/ceph/grid/home/atlas/tadej/ntuples/v2ntuples36ifb/mergedEXOT12' # input NTUP path
# NTUP='/ceph/grid/home/atlas/tadej/ntuples/v2ntuples36ifb/mergedEXOT19and0' # input NTUP path

JOBDIR = "/ceph/grid/home/atlas/%s/jobdir" % USER # Alright this is twisted...
INTARBALL = os.path.join(JOBDIR,'histtarball_%s.tar.gz' % (time.strftime("d%d_m%m_y%Y_H%H_M%M_S%S")) )

AUTOBUILD = True                # auto-build tarball using Makefile.tarball

# outputs
RUN = "SSVRele36_3"
#RUN = "ZPeak36_6"
#RUN = "TTBAR36_2"
#RUN = "CRelectron36"
#RUN = "FFelectron36_3"
# RUN = "WJets36_2"

OUTPATH="/ceph/grid/home/atlas/%s/AnalysisCode/%s"%(USER,RUN) # 
OUTFILE="ntuple.root"         # file output by pyframe job 

# running
QUEUE="long"                        # length of pbs queue (short, long, extralong )
# SCRIPT="./ssdilep/run/j.plotter_WJets.py"  # pyframe job script
#SCRIPT="./ssdilep/run/j.plotter_FFele.py"  # pyframe job script
#SCRIPT="./ssdilep/run/j.plotter_CRele.py"  # pyframe job script
#SCRIPT="./ssdilep/run/j.plotter_CReleTTBAR.py"  # pyframe job script
#SCRIPT="./ssdilep/run/j.plotter_ZPeak.py"  # pyframe job script
SCRIPT="./ssdilep/run/j.plotter_SSVRele.py"  # pyframe job script

BEXEC="HistMiha.sh"                  # exec script (probably dont change) 
DO_NOM = True                        # submit the nominal job
DO_NTUP_SYS = False                  # submit the NTUP systematics jobs
DO_PLOT_SYS = False                  # submit the plot systematics jobs
TESTMODE = False                     # submit only 1 sub-job (for testing)


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

    # all_mc = []
    # all_data = []

    #nominal = all_data + all_mc 
    nominal = all_mc 
    nominal += all_data
    
    ntup_sys = [
        ['SYS1_UP',                  all_mc],
        ['SYS1_DN',                  all_mc],
        ]    
    
    plot_sys = [
        ['FF_UP',        nominal],
        ['FF_DN',        nominal],
        ]    
    
    ## ensure output path exists
    #prepare_path(OUTPATH)
    
    ## auto-build tarball
    if AUTOBUILD:
        print 'building input tarball %s...'% (INTARBALL)
        cmd = 'cd %s; make -f Makefile.hist TARBALL=%s' % (MAIN,INTARBALL)
        m = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        print m.communicate()[0]

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

    ## construct config file
    cfg = os.path.join(JOBDIR,'ConfigHist.' + str(tag) + "." + str(os.path.basename(SCRIPT)[0:-3]) )
    f = open(cfg,'w')
    nsubjobs = 0
    jobnames = []
    maxevents = 2000000
    for s in samps:

        ## input
        sinput = input_file(s,job_sys)

        ## sample type
        stype  = s.type
 
        nlines = 1
        if os.stat(sinput).st_size>10e8:
            print sinput
            tempFile = ROOT.TFile.Open(sinput)
            tempFile.cd("physics")
            t = ROOT.gDirectory.Get("nominal")
            nevents = t.GetEntries()
            print "number of events ",nevents, " lines ",nevents//maxevents+1
            nlines = nevents//maxevents + 1

        ## config
        sconfig = {}
        sconfig.update(config)
        sconfig.update(s.config)
        sconfig_str = ",".join(["%s:%s"%(key,val) for key,val in sconfig.items()])

        for i in range(nlines) :
            line = ""
            if nlines==1 :
                line = ';'.join([s.name,sinput,stype,sconfig_str])
            elif len(sconfig_str)==0:
                line = ';'.join([s.name+".part"+str(i+1),sinput,stype,"min_entry:"+str( i*maxevents )+",max_entry:"+str( (i+1)*maxevents )])
            elif len(sconfig_str)!=0:
                line = ';'.join([s.name+".part"+str(i+1),sinput,stype,str(sconfig_str)+",min_entry:"+str( i*maxevents )+",max_entry:"+str( (i+1)*maxevents )])
            f.write('%s\n'%line)
            nsubjobs+=1
            jobname=str(os.path.basename(SCRIPT)[0:-2])+str(tag)+'.'+str(s.name)
            if nlines>1:
                jobname+='.part'+str(i+1)
            jobnames+=[jobname]

    f.close()

    abscfg     = os.path.abspath(cfg) 
    absintar   = os.path.abspath(INTARBALL)
    absoutpath = os.path.abspath(os.path.join(OUTPATH,tag))
    abslogpath = os.path.abspath(os.path.join(OUTPATH,'log_%s'%tag))
    if TESTMODE: nsubjobs = 1

    #prepare_path(absoutpath)
    #prepare_path(abslogpath)
 
    assert len(jobnames)==nsubjobs,"weird"

    for line_intiger in range(nsubjobs):

        TEMPXRSL = os.path.join(JOBDIR,'temp_'+ str(time.strftime("d%d_m%m_y%Y_H%H_M%M_S%S")) +'_PBS_ID_' + str(line_intiger+1) + '.xrsl' )
        JOBLISTF = os.path.join(JOBDIR,'joblist_%s.xml' % (time.strftime("d%d_m%m_y%Y")) )
        cmd =  'printf "'
        cmd += '&\n'
        cmd += '(executable=\\"%s\\")\n' % BEXEC
        cmd += '(jobName=\\"'+jobnames[line_intiger]+'\\")\n'
        cmd += '(memory=4000)\n'
        cmd += '(join=yes)\n'
        cmd += '(stdout="cp.out")\n'
        cmd += '(gmlog="gmlog")\n'
        cmd += '(cpuTime="300")\n'
        cmd += '(environment=(\\"CONFIG\\" \\"%s\\")\n'    % abscfg
        cmd += '             (\\"INTARBALL\\" \\"%s\\")\n' % absintar
        cmd += '             (\\"OUTFILE\\" \\"%s\\")\n'   % OUTFILE
        cmd += '             (\\"OUTPATH\\" \\"%s\\")\n'   % absoutpath
        cmd += '             (\\"SCRIPT\\" \\"%s\\")\n'    % SCRIPT
        cmd += '             (\\"PBS_ARRAYID\\" \\"%s\\"))'   % str(line_intiger+1)
        cmd += '">>' + TEMPXRSL
        cmd += ';arcsub -c pikolit.ijs.si -S org.nordugrid.gridftpjob -o '+JOBLISTF+' '+TEMPXRSL
        print cmd
        m = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        print m.communicate()[0]

def prepare_path(path):
    if not os.path.exists(path):
        print 'preparing outpath: %s'%(path)
        os.makedirs(path)

def input_file(sample,sys):
    global NTUP
    sinput = sample.name
    
    if sys!='nominal': sys='sys_'+sys
    sinput += '.root'
    sinput = os.path.join(NTUP,sys,sinput) 
    return sinput

if __name__=='__main__': main()


## EOF
