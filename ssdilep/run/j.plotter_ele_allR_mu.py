#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
j.postprocessor.py
"""

## std modules
import os,re

## ROOT
import ROOT
ROOT.gROOT.SetBatch(True)

## my modules
import pyframe

## local modules
import ssdilep

GeV = 1000.0


#_____________________________________________________________________________
def analyze(config):
  
    ##-------------------------------------------------------------------------
    ## eval systematics
    ##-------------------------------------------------------------------------
    """
    pass systematics on the command line like this:
    python j.plotter.py --config="sys:SYS_UP"
    """
    config.setdefault('sys',None)
    systematic = config['sys']

    sys_FF_ele   = None
    sys_FF_mu   = None
    sys_trig = None
    sys_id   = None
    sys_iso  = None
    sys_reco = None
    sys_TTVA = None
    sys_CF = None
    sys_kfactor = None
    sys_beam = None
    sys_choice = None
    sys_pdf = None
    sys_pi = None
    sys_scale_z = None

    ## tree systematics
    # treeSys = ""
    if systematic == 'EG_RESOLUTION_ALL_UP': treeSys = "EG_RESOLUTION_ALL__1up"
    elif systematic == 'EG_RESOLUTION_ALL_DN': treeSys = "EG_RESOLUTION_ALL__1down"
    elif systematic == 'EG_SCALE_ALLCORR_UP': treeSys = "EG_SCALE_ALLCORR__1up"
    elif systematic == 'EG_SCALE_ALLCORR_DN': treeSys = "EG_SCALE_ALLCORR__1down"
    elif systematic == 'EG_SCALE_E4SCINTILLATOR_UP': treeSys = "EG_SCALE_E4SCINTILLATOR__1up"
    elif systematic == 'EG_SCALE_E4SCINTILLATOR_DN': treeSys = "EG_SCALE_E4SCINTILLATOR__1down"
    elif systematic == 'MUON_ID_DN':treeSys= "MUON_ID___1down"
    elif systematic == 'MUON_ID_UP':treeSys= "MUON_ID___1up"
    elif systematic == 'MUON_MS_DN':treeSys= "MUON_MS___1down"
    elif systematic == 'MUON_MS_UP':treeSys= "MUON_MS___1up"
    elif systematic == 'MUON_RESBIAS_DN':treeSys= "MUON_SAGITTA_RESBIAS___1down"
    elif systematic == 'MUON_RESBIAS_UP':treeSys= "MUON_SAGITTA_RESBIAS___1up"
    elif systematic == 'MUON_RHO_DN':treeSys= "MUON_SAGITTA_RHO___1down"
    elif systematic == 'MUON_RHO_UP':treeSys= "MUON_SAGITTA_RHO___1up"
    elif systematic == 'MUON_SCALE_DN':treeSys= "MUON_SCALE___1down"
    elif systematic == 'MUON_SCALE_UP':treeSys= "MUON_SCALE___1up"
    # elif systematic == 'EG_SCALE_LARCALIB_EXTRA2015PRE_UP': treeSys = "EG_SCALE_LARCALIB_EXTRA2015PRE__1up"
    # elif systematic == 'EG_SCALE_LARCALIB_EXTRA2015PRE_DN': treeSys = "EG_SCALE_LARCALIB_EXTRA2015PRE__1down"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2015PRE_UP': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2015PRE__1up"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2015PRE_DN': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2015PRE__1down"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_UP': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2016PRE__1up"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_DN': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2016PRE__1down"
    else:
        treeSys = "nominal"
        if systematic == None: pass
        elif systematic == 'ELEFF_UP':      sys_FF_ele   = 'UP'
        elif systematic == 'ELEFF_DN':      sys_FF_ele   = 'DN'
        elif systematic == 'MUFF_UP':      sys_FF_mu   = 'UP'
        elif systematic == 'MUFF_DN':      sys_FF_mu   = 'DN'
        elif systematic == 'CF_UP':      sys_CF   = 'UP'
        elif systematic == 'CF_DN':      sys_CF   = 'DN'
        elif systematic == 'TRIG_UP':    sys_trig = 'UP'
        elif systematic == 'TRIG_DN':    sys_trig = 'DN'
        elif systematic == 'TRIG_UPSTAT': sys_trig= 'UPSTAT'
        elif systematic == 'TRIG_UPSYS':  sys_trig= 'UPSYS'
        elif systematic == 'TRIG_DNSTAT': sys_trig= 'DNSTAT'
        elif systematic == 'TRIG_DNSYS':  sys_trig= 'DNSYS'
        elif systematic == 'ID_UP':      sys_id   = 'UP'
        elif systematic == 'ID_DN':      sys_id   = 'DN'
        elif systematic == 'ID_UPSTAT': sys_id    = 'UPSTAT'
        elif systematic == 'ID_DNSTAT': sys_id    = 'DNSTAT'
        elif systematic == 'ID_UPSYS':  sys_id    = 'UPSYS'
        elif systematic == 'ID_DNSYS':  sys_id    = 'DNSYS'
        elif systematic == 'ISO_UP':    sys_iso   = 'UP'
        elif systematic == 'ISO_DN':    sys_iso   = 'DN'
        elif systematic == 'ISO_UPSTAT':     sys_iso   = 'UPSTAT'
        elif systematic == 'ISO_DNSTAT':     sys_iso   = 'DNSTAT'
        elif systematic == 'ISO_UPSYS':     sys_iso   = 'UPSYS'
        elif systematic == 'ISO_DNSYS':     sys_iso   = 'DNSYS'
        elif systematic == 'RECO_UP':    sys_reco  = 'UP'
        elif systematic == 'RECO_DN':    sys_reco  = 'DN'    
        elif systematic == 'RECO_UPSTAT':  sys_reco  = 'UPSTAT'
        elif systematic == 'RECO_DNSTAT':  sys_reco  = 'DNSTAT'    
        elif systematic == 'RECO_UPSYS':  sys_reco  = 'UPSYS'
        elif systematic == 'RECO_DNSYS':  sys_reco  = 'DNSYS'    
        elif systematic == 'TTVA_UPSTAT':  sys_TTVA  = 'UPSTAT'
        elif systematic == 'TTVA_DNSTAT':  sys_TTVA  = 'DNSTAT'    
        elif systematic == 'TTVA_UPSYS':  sys_TTVA  = 'UPSYS'
        elif systematic == 'TTVA_DNSYS':  sys_TTVA  = 'DNSYS'    
        elif systematic == 'BEAM_UP':    sys_beam  = 'UP'
        elif systematic == 'BEAM_DN':    sys_beam  = 'DN'    
        elif systematic == 'CHOICE_UP':  sys_choice  = 'UP'
        elif systematic == 'CHOICE_DN':  sys_choice  = 'DN'    
        elif systematic == 'PDF_UP':     sys_pdf  = 'UP'
        elif systematic == 'PDF_DN':     sys_pdf  = 'DN'    
        elif systematic == 'PI_UP':      sys_pi  = 'UP'
        elif systematic == 'PI_DN':      sys_pi  = 'DN'
        elif systematic == 'SCALE_Z_UP': sys_scale_z  = 'UP'
        elif systematic == 'SCALE_Z_DN': sys_scale_z  = 'DN'

    assert treeSys!="", "Invalid systematic %s!"%(systematic)

    ##-------------------------------------------------------------------------
    ## setup
    ##-------------------------------------------------------------------------
    config['tree']       = 'physics/' + treeSys
    config['do_var_log'] = True
    main_path = os.getenv('MAIN')
    
    ## build chain
    chain = ROOT.TChain(config['tree'])
    for fn in config['input']: chain.Add(fn)

    ##-------------------------------------------------------------------------
    ## event loop
    ##-------------------------------------------------------------------------
    loop = pyframe.core.EventLoop(name='ssdilep',
                                  sampletype=config['sampletype'],
                                  outfile='ntuple.root',
                                  quiet=False,
                                  )
    
    ## build and pt-sort objects
    ## ---------------------------------------
    loop += pyframe.algs.ListBuilder(
        prefixes = ['muon_','el_','jet_'],
        keys = ['muons','electrons','jets'],
        )
    loop += pyframe.algs.AttachTLVs(
        keys = ['muons','electrons','jets'],
        )
    # just a decoration of particles ...
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='muons',
        )
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='electrons',
        )


    ## build MET
    ## ---------------------------------------
    loop += ssdilep.algs.met.METCLUS(
        prefix='metFinalClus',
        key = 'met_clus',
        )
    loop += ssdilep.algs.met.METTRK(
        prefix='metFinalTrk',
        key = 'met_trk',
        )
    
    
    ## initialize and/or decorate objects
    ## ---------------------------------------
    #loop += ssdilep.algs.vars.PairsBuilder(
    #    obj_keys=['muons'],
    #    pair_key='mu_pairs',
    #    met_key='met_clus', 
    #    )
    
    loop += ssdilep.algs.algs.VarsAlg(key_muons='muons',key_jets='jets', key_electrons='electrons', require_prompt=True, use_simple_truth=False, remove_signal_electrons=True)   

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    loop += ssdilep.algs.EvWeights.LPXKfactor(
            cutflow='presel',
            key='lpx_kfactor',
            sys_beam = sys_beam,
            sys_choice = sys_choice,
            sys_pdf = sys_pdf,
            sys_pi = sys_pi,
            sys_scale_z = sys_scale_z,
            doAssert = True,
            nominalTree = True if treeSys == "nominal" else False
            )
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='NoFakesInMC')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='ExactlyZeroElectrons')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BadJetVeto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='bjetveto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='PassORSingleLeptonTriggerMuon')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AtLeastTwoLooseMuons')
    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++


    loop += ssdilep.algs.EvWeights.GenericFakeFactorMu(
            key='GenericFakeFactorMu',
            config_file=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_bveto.root'),
            sys=sys_FF_mu,
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_TTVA = sys_TTVA,
            )

    loop += ssdilep.algs.EvWeights.MuTrigSF(
            trig_list     = ["HLT_mu26_ivarmedium_OR_HLT_mu50"],
            mu_reco       = "Medium",
            mu_iso        = "FixedCutTightTrackOnly",
            key           = "MuTrigSF",
            sys_trig      = sys_trig,
            )

    # TTT REGION
    # ---------------------------------------
    # ------  DBCR
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'diboson-CR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyThreeLeptonsSS60M200',None],
               ['ExactlyThreeLooseLepOSZmass',None],
               ['ExactlyThreeTightLep',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'diboson-CR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyThreeLeptonsSS60M200',None],
               ['ExactlyThreeLooseLepOSZmass',None],
               ['FailExactlyThreeTightLep',["GenericFakeFactorMu","MuTrigSF"]],
               ],
            )

    ## ------ DBVR
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'threeLep-VR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyThreeLeptonsSS60M200',None],
               ['ZVeto',None],
               ['ExactlyThreeTightLep',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'threeLep-VR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyThreeLeptonsSS60M200',None],
               ['ZVeto',None],
               ['FailExactlyThreeTightLep',["GenericFakeFactorMu","MuTrigSF"]],
               ],
            )

    # TT REGION
    # ---------------------------------------
    # ------ SSVR
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'same-sign-CR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyTwoLooseMuonSS',None],
               ['Mass60GeV200Leptons',None],
               ['ExactlyTwoTightLeptons',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'same-sign-CR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyTwoLooseMuonSS',None],
               ['Mass60GeV200Leptons',None],
               ['NotExactlyTwoTightLeptons',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )

    # # SIGNAL REGION
    # # ---------------------------------------
    # # ------ two muon
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'two-muon-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyTwoLooseMuonSS',None],
               ['Mass200GeVLooseLep',None],
               ['ExactlyTwoTightLeptons',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'two-muon-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyTwoLooseMuonSS',None],
               ['Mass200GeVLooseLep',None],
               ['NotExactlyTwoTightLeptons',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgThreeLep(
                region   = 'two-muon-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['ExactlyTwoLooseMuonSS',None],
                   ['Mass200GeVLooseLep',None],
                   ['ExactlyTwoTightLeptons',['GenericFakeFactorMu','MuTrigSF']],
                   ],
                )
    # # ------ two muon dR only
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'two-muon-dR-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyTwoLooseMuonSS',None],
               ['SameSignLooseLepDR35',None],
               ['Mass200GeVLooseLep',None],
               ['ExactlyTwoTightLeptons',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'two-muon-dR-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyTwoLooseMuonSS',None],
               ['SameSignLooseLepDR35',None],
               ['Mass200GeVLooseLep',None],
               ['NotExactlyTwoTightLeptons',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgThreeLep(
                region   = 'two-muon-dR-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['ExactlyTwoLooseMuonSS',None],
                   ['SameSignLooseLepDR35',None],
                   ['Mass200GeVLooseLep',None],
                   ['ExactlyTwoTightLeptons',['GenericFakeFactorMu','MuTrigSF']],
                   ],
                )
    # ------ two muon optimized
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'two-muon-optimized-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyTwoLooseMuonSS',None],
               ['Mass200GeVLooseLep',None],
               ['SameSignLooseLepDR35',None],
               ['SameSignLooseLepPtZ100',None],
               ['LooseLepHT300',None],
               ['ExactlyTwoTightLeptons',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'two-muon-optimized-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyTwoLooseMuonSS',None],
               ['Mass200GeVLooseLep',None],
               ['SameSignLooseLepDR35',None],
               ['SameSignLooseLepPtZ100',None],
               ['LooseLepHT300',None],
               ['NotExactlyTwoTightLeptons',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgThreeLep(
                region   = 'two-muon-optimized-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['ExactlyTwoLooseMuonSS',None],
                   ['Mass200GeVLooseLep',None],
                   ['SameSignLooseLepDR35',None],
                   ['SameSignLooseLepPtZ100',None],
                   ['LooseLepHT300',None],
                   ['ExactlyTwoTightLeptons',['GenericFakeFactorMu','MuTrigSF']],
                   ],
                )
    # # ------ three ele
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-muon-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyThreeLooseLep',None],
               ['ExactlyThreeLooseLepSS200M',None],
               ['ZVeto',None],
               ['ExactlyThreeTightLep',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-muon-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyThreeLooseLep',None],
               ['ExactlyThreeLooseLepSS200M',None],
               ['ZVeto',None],
               ['FailExactlyThreeTightLep',["GenericFakeFactorMu","MuTrigSF"]],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgThreeLep(
                region   = 'three-muon-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['ExactlyThreeLooseLep',None],
                   ['ExactlyThreeLooseLepSS200M',None],
                   ['ZVeto',None],
                   ['ExactlyThreeTightLep',['GenericFakeFactorMu','MuTrigSF']],
                   ],
                )
    # # ------ three ele dR only
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-muon-dR-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyThreeLooseLep',None],
               ['ExactlyThreeLooseLepSS200M',None],
               ['ZVeto',None],
               ['SameSignLooseLepDR35',None],
               ['ExactlyThreeTightLep',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-muon-dR-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyThreeLooseLep',None],
               ['ExactlyThreeLooseLepSS200M',None],
               ['ZVeto',None],
               ['SameSignLooseLepDR35',None],
               ['FailExactlyThreeTightLep',["GenericFakeFactorMu","MuTrigSF"]],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgThreeLep(
                region   = 'three-muon-dR-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['ExactlyThreeLooseLep',None],
                   ['ExactlyThreeLooseLepSS200M',None],
                   ['ZVeto',None],
                   ['SameSignLooseLepDR35',None],
                   ['ExactlyThreeTightLep',['GenericFakeFactorMu','MuTrigSF']],
                   ],
                )
    # # ------ three ele optimized
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-muon-optimized-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyThreeLooseLep',None],
               ['ExactlyThreeLooseLepSS200M',None],
               ['SameSignLooseLepDR35',None],
               ['SameSignLooseLepPtZ100',None],
               ['LooseLepHT300',None],
               ['ZVeto',None],
               ['ExactlyThreeTightLep',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-muon-optimized-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['ExactlyThreeLooseLep',None],
               ['ExactlyThreeLooseLepSS200M',None],
               ['SameSignLooseLepDR35',None],
               ['SameSignLooseLepPtZ100',None],
               ['LooseLepHT300',None],
               ['ZVeto',None],
               ['FailExactlyThreeTightLep',["GenericFakeFactorMu","MuTrigSF"]],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgThreeLep(
                region   = 'three-muon-optimized-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['ExactlyThreeLooseLep',None],
                   ['ExactlyThreeLooseLepSS200M',None],
                   ['SameSignLooseLepDR35',None],
                   ['SameSignLooseLepPtZ100',None],
                   ['LooseLepHT300',None],
                   ['ZVeto',None],
                   ['ExactlyThreeTightLep',['GenericFakeFactorMu','MuTrigSF']],
                   ],
                )
    # # ------ two or three or four ele
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'SR-muon-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['LooseLepSS200M',None],
               ['SameSignLooseLepDR35',None],
               ['SameSignLooseLepPtZ100',None],
               ['LooseLepHT300',None],
               ['ZVeto',None],
               ['NoStrictlyLooseLep',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'SR-muon-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['LooseLepSS200M',None],
               ['SameSignLooseLepDR35',None],
               ['SameSignLooseLepPtZ100',None],
               ['LooseLepHT300',None],
               ['ZVeto',None],
               ['NotNoStrictlyLooseLep',['GenericFakeFactorMu','MuTrigSF']],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgThreeLep(
                region   = 'SR-muon-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['LooseLepSS200M',None],
                   ['SameSignLooseLepDR35',None],
                   ['SameSignLooseLepPtZ100',None],
                   ['LooseLepHT300',None],
                   ['ZVeto',None],
                   ['NoStrictlyLooseLep',['GenericFakeFactorMu','MuTrigSF']],
                   ],
                )
    
    loop += pyframe.algs.HistCopyAlg()

    ##-------------------------------------------------------------------------
    ## run the job
    ##-------------------------------------------------------------------------
    min_entry = int(config.get('min_entry') if ('min_entry' in config.keys()) else  0)
    max_entry = int(config.get('max_entry') if ('max_entry' in config.keys()) else -1)
    print min_entry," ",max_entry
    loop.run(chain, 
            min_entry = min_entry,
            max_entry = max_entry,
            branches_on_file = config.get('branches_on_file'),
            do_var_log = config.get('do_var_log'),
            )
#______________________________________________________________________________
if __name__ == '__main__':
    pyframe.config.main(analyze)


