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

    sys_FF = None
    sys_CF = None
    sys_trig = None
    sys_id = None
    sys_iso = None
    sys_reco = None
    sys_kfactor = None
    sys_beam = None
    sys_choice = None
    sys_pdf = None
    sys_pi = None
    sys_scale_z = None

    ## tree systematics
    treeSys = ""
    if systematic == 'EG_RESOLUTION_ALL_UP': treeSys = "EG_RESOLUTION_ALL__1up"
    elif systematic == 'EG_RESOLUTION_ALL_DN': treeSys = "EG_RESOLUTION_ALL__1down"
    elif systematic == 'EG_SCALE_ALLCORR_UP': treeSys = "EG_SCALE_ALLCORR__1up"
    elif systematic == 'EG_SCALE_ALLCORR_DN': treeSys = "EG_SCALE_ALLCORR__1down"
    elif systematic == 'EG_SCALE_E4SCINTILLATOR_UP': treeSys = "EG_SCALE_E4SCINTILLATOR__1up"
    elif systematic == 'EG_SCALE_E4SCINTILLATOR_DN': treeSys = "EG_SCALE_E4SCINTILLATOR__1down"
    # elif systematic == 'EG_SCALE_LARCALIB_EXTRA2015PRE_UP': treeSys = "EG_SCALE_LARCALIB_EXTRA2015PRE__1up"
    # elif systematic == 'EG_SCALE_LARCALIB_EXTRA2015PRE_DN': treeSys = "EG_SCALE_LARCALIB_EXTRA2015PRE__1down"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2015PRE_UP': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2015PRE__1up"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2015PRE_DN': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2015PRE__1down"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_UP': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2016PRE__1up"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_DN': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2016PRE__1down"
    else:
        treeSys = "nominal"
        if systematic == None: pass
        elif systematic == 'FF_UP':      sys_FF    = 'UP'
        elif systematic == 'FF_DN':      sys_FF    = 'DN'
        elif systematic == 'CF_UP':      sys_CF    = 'UP'
        elif systematic == 'CF_DN':      sys_CF    = 'DN'
        elif systematic == 'TRIG_UP':    sys_trig  = 'UP'
        elif systematic == 'TRIG_DN':    sys_trig  = 'DN'
        elif systematic == 'ID_UP':      sys_id    = 'UP'
        elif systematic == 'ID_DN':      sys_id    = 'DN'
        elif systematic == 'ISO_UP':     sys_iso   = 'UP'
        elif systematic == 'ISO_DN':     sys_iso   = 'DN'
        elif systematic == 'RECO_UP':    sys_reco  = 'UP'
        elif systematic == 'RECO_DN':    sys_reco  = 'DN'    
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
    
    loop += ssdilep.algs.algs.VarsAlg(key_muons='muons',key_jets='jets', key_electrons='electrons', require_prompt=True, use_simple_truth=False)   

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
    # loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='DCHAllElectron')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BadJetVeto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='PassHLT2e17lhloose')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AtLeastTwoLooseEleLooseLLH')
    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++

    loop += ssdilep.algs.EvWeights.OneOrTwoBjetsSF(
            key='OneOrTwoBjetsSF',
            )

    # loop += ssdilep.algs.EvWeights.TwoElectron2e17TrigWeight(
    #         key='TwoElectron2e17TrigWeight',
    #         )

    loop += ssdilep.algs.EvWeights.ThreeElectron2e17TrigWeight(
            key='ThreeElectron2e17TrigWeight',
            sys_trig = sys_trig,
            )

    loop += ssdilep.algs.EvWeights.AllTightEleSF(
            key='AllTightEleSF',
            config_file=os.path.join(main_path,'ssdilep/data/chargeFlipRates-28-03-2017.root'),
            chargeFlipSF=True,
            sys_CF = sys_CF,
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_reco = sys_reco,
            )

    loop += ssdilep.algs.EvWeights.AllTightEleSF(
            key='AllTightEleSFnoCF',
            config_file=os.path.join(main_path,'ssdilep/data/chargeFlipRates-28-03-2017.root'),
            chargeFlipSF=False,
            sys_CF = sys_CF,
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_reco = sys_reco,
            )

    loop += ssdilep.algs.EvWeights.GenericFakeFactor(
            key='GenericFakeFactor',
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-16-05-2017.root'),
            config_fileCHF=os.path.join(main_path,'ssdilep/data/chargeFlipRates-28-03-2017.root'),
            sys = sys_FF,
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_reco = sys_reco,
            )

    # TTT REGION
    # ---------------------------------------
    # ------  DBCR
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'diboson-CR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyThreeLooseEleLooseLLHSS90M200',None],
               ['ExactlyThreeLooseEleLooseLLHOSZmass',None],
               ['ExactlyThreeTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'diboson-CR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyThreeLooseEleLooseLLHSS90M200',None],
               ['ExactlyThreeLooseEleLooseLLHOSZmass',None],
               ['FailExactlyThreeTightEleMediumLLHisolLoose',["GenericFakeFactor","ThreeElectron2e17TrigWeight"]],
               ],
            )

    ## ------ DBVR
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'threeElectron-VR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyThreeLooseEleLooseLLHSS90M200',None],
               ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
               ['ExactlyThreeTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'threeElectron-VR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyThreeLooseEleLooseLLHSS90M200',None],
               ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
               ['FailExactlyThreeTightEleMediumLLHisolLoose',["GenericFakeFactor","ThreeElectron2e17TrigWeight"]],
               ],
            )

    # TT REGION
    # ---------------------------------------
    # ------ OSCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'opposite-sign-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['DCHFilter',None],
    #            ['ExactlyTwoLooseEleLooseLLHOS',None],
    #            ['Mass130GeVLooseLLH',None],
    #            ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'opposite-sign-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['DCHFilter',None],
    #            ['ExactlyTwoLooseEleLooseLLHOS',None],
    #            ['Mass130GeVLooseLLH',None],
    #            ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','ThreeElectron2e17TrigWeight']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'opposite-sign-noCF-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['DCHFilter',None],
    #            ['ExactlyTwoLooseEleLooseLLHOS',None],
    #            ['Mass130GeVLooseLLH',None],
    #            ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSFnoCF','ThreeElectron2e17TrigWeight']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'opposite-sign-noCF-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['DCHFilter',None],
    #            ['ExactlyTwoLooseEleLooseLLHOS',None],
    #            ['Mass130GeVLooseLLH',None],
    #            ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','ThreeElectron2e17TrigWeight']],
    #            ],
    #         )
    # ------ OSCR b-veto
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'opposite-sign-bveto-CR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyTwoLooseEleLooseLLHOS',None],
               ['Mass130GeVLooseLLH',None],
               ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'opposite-sign-bveto-CR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyTwoLooseEleLooseLLHOS',None],
               ['Mass130GeVLooseLLH',None],
               ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','ThreeElectron2e17TrigWeight']],
               ],
            )
    # ## ------ SSVR
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'same-sign-CR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyTwoLooseEleLooseLLHSS',None],
               ['Mass130GeV200LooseLLH',None],
               ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'same-sign-CR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyTwoLooseEleLooseLLHSS',None],
               ['Mass130GeV200LooseLLH',None],
               ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','ThreeElectron2e17TrigWeight']],
               ],
            )

    # TT REGION 2 bjet
    # ---------------------------------------
    # ------ OSCR2b
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'opposite-sign-ttbar-CR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
               ['ExactlyTwoLooseEleLooseLLHOS',None],
               ['Mass130GeVLooseLLH',None],
               ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'opposite-sign-ttbar-CR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
               ['ExactlyTwoLooseEleLooseLLHOS',None],
               ['Mass130GeVLooseLLH',None],
               ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','ThreeElectron2e17TrigWeight']],
               ],
            )
    # ## ------ SSVR2b
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'same-sign-ttbar-CR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
               ['ExactlyTwoLooseEleLooseLLHSS',None],
               ['Mass130GeV200LooseLLH',None],
               ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'same-sign-ttbar-CR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
               ['ExactlyTwoLooseEleLooseLLHSS',None],
               ['Mass130GeV200LooseLLH',None],
               ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','ThreeElectron2e17TrigWeight']],
               ],
            )
    # SIGNAL REGION
    # ---------------------------------------
    # ------ two ele
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'two-ele-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyTwoLooseEleLooseLLH',None],
               ['ExactlyTwoLooseEleLooseLLHSS',None],
               ['Mass200GeVLooseLLH',None],
               ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'two-ele-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyTwoLooseEleLooseLLH',None],
               ['ExactlyTwoLooseEleLooseLLHSS',None],
               ['Mass200GeVLooseLLH',None],
               ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','ThreeElectron2e17TrigWeight']],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgCRele(
                region   = 'two-ele-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['bjetveto',None],
                   ['ExactlyTwoLooseEleLooseLLH',None],
                   ['ExactlyTwoLooseEleLooseLLHSS',None],
                   ['Mass200GeVLooseLLH',None],
                   ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
                   ],
                )
    # ------ two ele dR only
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'two-ele-dR-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyTwoLooseEleLooseLLH',None],
               ['ExactlyTwoLooseEleLooseLLHSS',None],
               ['SameSignLooseEleDR35',None],
               ['Mass200GeVLooseLLH',None],
               ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'two-ele-dR-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyTwoLooseEleLooseLLH',None],
               ['ExactlyTwoLooseEleLooseLLHSS',None],
               ['SameSignLooseEleDR35',None],
               ['Mass200GeVLooseLLH',None],
               ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','ThreeElectron2e17TrigWeight']],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgCRele(
                region   = 'two-ele-dR-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['bjetveto',None],
                   ['ExactlyTwoLooseEleLooseLLH',None],
                   ['ExactlyTwoLooseEleLooseLLHSS',None],
                   ['SameSignLooseEleDR35',None],
                   ['Mass200GeVLooseLLH',None],
                   ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
                   ],
                )
    # ------ two ele optimized
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'two-ele-optimized-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyTwoLooseEleLooseLLH',None],
               ['ExactlyTwoLooseEleLooseLLHSS',None],
               ['Mass200GeVLooseLLH',None],
               ['SameSignLooseEleDR35',None],
               ['SameSignLooseElePtZ100',None],
               ['LooseEleHT300',None],
               ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'two-ele-optimized-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyTwoLooseEleLooseLLH',None],
               ['ExactlyTwoLooseEleLooseLLHSS',None],
               ['Mass200GeVLooseLLH',None],
               ['SameSignLooseEleDR35',None],
               ['SameSignLooseElePtZ100',None],
               ['LooseEleHT300',None],
               ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','ThreeElectron2e17TrigWeight']],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgCRele(
                region   = 'two-ele-optimized-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['bjetveto',None],
                   ['ExactlyTwoLooseEleLooseLLH',None],
                   ['ExactlyTwoLooseEleLooseLLHSS',None],
                   ['Mass200GeVLooseLLH',None],
                   ['SameSignLooseEleDR35',None],
                   ['SameSignLooseElePtZ100',None],
                   ['LooseEleHT300',None],
                   ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
                   ],
                )
    # ------ three ele
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-ele-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyThreeLooseEleLooseLLH',None],
               ['ExactlyThreeLooseEleLooseLLHSS200M',None],
               ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
               ['ExactlyThreeTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-ele-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyThreeLooseEleLooseLLH',None],
               ['ExactlyThreeLooseEleLooseLLHSS200M',None],
               ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
               ['FailExactlyThreeTightEleMediumLLHisolLoose',["GenericFakeFactor","ThreeElectron2e17TrigWeight"]],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgThreeLep(
                region   = 'three-ele-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['bjetveto',None],
                   ['ExactlyThreeLooseEleLooseLLH',None],
                   ['ExactlyThreeLooseEleLooseLLHSS200M',None],
                   ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
                   ['ExactlyThreeTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
                   ],
                )
    # ------ three ele dR only
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-ele-dR-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyThreeLooseEleLooseLLH',None],
               ['ExactlyThreeLooseEleLooseLLHSS200M',None],
               ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
               ['SameSignLooseEleDR35',None],
               ['ExactlyThreeTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-ele-dR-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyThreeLooseEleLooseLLH',None],
               ['ExactlyThreeLooseEleLooseLLHSS200M',None],
               ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
               ['SameSignLooseEleDR35',None],
               ['FailExactlyThreeTightEleMediumLLHisolLoose',["GenericFakeFactor","ThreeElectron2e17TrigWeight"]],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgThreeLep(
                region   = 'three-ele-dR-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['bjetveto',None],
                   ['ExactlyThreeLooseEleLooseLLH',None],
                   ['ExactlyThreeLooseEleLooseLLHSS200M',None],
                   ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
                   ['SameSignLooseEleDR35',None],
                   ['ExactlyThreeTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
                   ],
                )
    # ------ three ele optimized
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-ele-optimized-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyThreeLooseEleLooseLLH',None],
               ['ExactlyThreeLooseEleLooseLLHSS200M',None],
               ['SameSignLooseEleDR35',None],
               ['SameSignLooseElePtZ100',None],
               ['LooseEleHT300',None],
               ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
               ['ExactlyThreeTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-ele-optimized-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['ExactlyThreeLooseEleLooseLLH',None],
               ['ExactlyThreeLooseEleLooseLLHSS200M',None],
               ['SameSignLooseEleDR35',None],
               ['SameSignLooseElePtZ100',None],
               ['LooseEleHT300',None],
               ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
               ['FailExactlyThreeTightEleMediumLLHisolLoose',["GenericFakeFactor","ThreeElectron2e17TrigWeight"]],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgThreeLep(
                region   = 'three-ele-optimized-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['bjetveto',None],
                   ['ExactlyThreeLooseEleLooseLLH',None],
                   ['ExactlyThreeLooseEleLooseLLHSS200M',None],
                   ['SameSignLooseEleDR35',None],
                   ['SameSignLooseElePtZ100',None],
                   ['LooseEleHT300',None],
                   ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
                   ['ExactlyThreeTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
                   ],
                )
    # ------ two or three ele
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'SR1-ele-SR',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['LooseEleLooseLLHSS200M',None],
               ['SameSignLooseEleDR35',None],
               ['SameSignLooseElePtZ100',None],
               ['LooseEleHT300',None],
               ['LooseEleLooseLLHOSZVeto',None],
               ['NoStrictlyLooseEleTwoOrThreeTight',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'SR1-ele-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['DCHFilter',None],
               ['bjetveto',None],
               ['LooseEleLooseLLHSS200M',None],
               ['SameSignLooseEleDR35',None],
               ['SameSignLooseElePtZ100',None],
               ['LooseEleHT300',None],
               ['LooseEleLooseLLHOSZVeto',None],
               ['NotNoStrictlyLooseEleTwoOrThreeTight',['GenericFakeFactor','ThreeElectron2e17TrigWeight']],
               ],
            )
    for channel in ["eeee","eemm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlgThreeLep(
                region   = 'SR1-ele-SR-signal-'+channel,
                plot_all = False,
                cut_flow = [
                   ['DCHFilter'+channel,None],
                   ['bjetveto',None],
                   ['LooseEleLooseLLHSS200M',None],
                   ['SameSignLooseEleDR35',None],
                   ['SameSignLooseElePtZ100',None],
                   ['LooseEleHT300',None],
                   ['LooseEleLooseLLHOSZVeto',None],
                   ['NoStrictlyLooseEleTwoOrThreeTight',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
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


