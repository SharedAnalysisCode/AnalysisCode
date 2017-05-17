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

#arcproxy -S gen.vo.sling.si
#arcproxy -S atlas:/atlas/si

## global config
# inputs
#NTUP='/coepp/cephfs/mel/fscutti/ssdilep/presc/merged' # input NTUP path
#NTUP='/coepp/cephfs/mel/fscutti/ssdilep/menu_singlemu/merged' # input NTUP path
#NTUP='/coepp/cephfs/mel/fscutti/ssdilep/HIGG3D3_p2666_p2667_v1_presc/merged' # input NTUP path
#NTUP='/ceph/grid/home/atlas/miham/ntuples/v2ntuples18ifb/mergedEXOT19and0' # input NTUP path
# NTUP='/ceph/grid/home/atlas/tadej/ntuples/v2ntuples36ifb/mergedEXOT12' # input NTUP path
# NTUP='/ceph/grid/home/atlas/tadej/ntuples/v2ntuples36ifb/mergedEXOT19and0' # input NTUP path

# NTUP='/ceph/grid/home/atlas/tadej/ntuples/v3ntuples/EXOT12skimmed'
NTUP='/ceph/grid/home/atlas/miham/ntuples/merged/EXOT12SkimmedSys'
# NTUP='/ceph/grid/home/atlas/tadej/ntuples/v3ntuples/EXOT19and12unskimmed'

JOBDIR = "/ceph/grid/home/atlas/%s/jobdir" % USER # Alright this is twisted...
INTARBALL = os.path.join(JOBDIR,'histtarball_%s.tar.gz' % (time.strftime("d%d_m%m_y%Y_H%H_M%M_S%S")) )

AUTOBUILD = True                # auto-build tarball using Makefile.tarball

# outputs
# RUN = "SSVRele36_7"
# RUN = "ZPeak_v3_003"
RUN = "AllR_v3_020"
# RUN = "WJets_v3_004"
# RUN = "FFele_v3_006"

OUTPATH="/ceph/grid/home/atlas/%s/AnalysisCode/%s"%(USER,RUN) # 
OUTFILE="ntuple.root"         # file output by pyframe job 

# running
QUEUE="long"                        # length of pbs queue (short, long, extralong )
# SCRIPT="./ssdilep/run/j.plotter_WJets.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_CReleDiboson.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_ThreeEleVR.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_FFele.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_CRele.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_CReleTTBAR.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_ZPeak.py"  # pyframe job script
SCRIPT="./ssdilep/run/j.plotter_ele_allR.py"  # pyframe job script
# SCRIPT="./ssdilep/run/j.plotter_SSVRele.py"  # pyframe job script

BEXEC="HistMiha.sh"                  # exec script (probably dont change) 
DO_NOM = True                        # submit the nominal job
DO_NTUP_SYS = False                  # submit the NTUP systematics jobs
TESTMODE = False                     # submit only 1 sub-job (for testing)

DO_PLOT_SYS = True                  # submit the plot systematics jobs

CF_SYS = True
FF_SYS = True

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

    # all_mc = []
    # all_data = []

    nominal = all_mc 
    nominal += all_data
    
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
    cfg = os.path.join(JOBDIR,'ConfigHist.' + str(time.strftime("d%d_m%m_y%Y_H%H_M%M_S%S")) + "." + str(tag) + "." + str(os.path.basename(SCRIPT)[0:-3]) )
    f = open(cfg,'w')
    nsubjobs = 0
    jobnames = []
    maxevents = 1000000
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


        ## input
        sinput = input_file(s,job_sys)

        ## sample type
        stype  = s.type
 
        nlines = 1
        if os.stat(sinput).st_size>5e8:
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
