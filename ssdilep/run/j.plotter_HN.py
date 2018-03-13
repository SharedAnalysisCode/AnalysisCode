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

DO_FAKE_COMPOSITION = False


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

    ## b-jet and JVT
    sys_bjet = None
    sys_JVT = None

    QCD = {
    "MUR0.5_MUF0.5":4,
    "MUR0.5_MUF1":5,
    "MUR1_MUF0.5":6,
    "MUR1_MUF1":7,
    "MUR1_MUF2":8,
    "MUR2_MUF1":9,
    "MUR2_MUF2":10,
    }
    HepMCEventWeight = None
    if not systematic == None:
        if "PDF261000" in systematic:
            for key in QCD.keys():
                if key in systematic:
                    HepMCEventWeight = QCD[key]
        else:
            PDF = re.findall('PDF(261[0-9]*)',systematic)
            if len(PDF):
                HepMCEventWeight = int(PDF[0]) - 261000 + 10
            elif "PDF269000" in systematic:
                HepMCEventWeight = 111
            elif "PDF270000" in systematic:
                HepMCEventWeight = 112
            elif "PDF25300" in systematic:
                HepMCEventWeight = 113
            elif "PDF13000" in systematic:
                HepMCEventWeight = 114
        print "HepMCEventWeight: ",HepMCEventWeight


    ## tree systematics
    # treeSys = ""
    if systematic   == 'EG_RESOLUTION_ALL_UP': treeSys = "EG_RESOLUTION_ALL__1up"
    elif systematic == 'EG_RESOLUTION_ALL_DN': treeSys = "EG_RESOLUTION_ALL__1down"
    elif systematic == 'EG_SCALE_ALLCORR_UP': treeSys = "EG_SCALE_ALLCORR__1up"
    elif systematic == 'EG_SCALE_ALLCORR_DN': treeSys = "EG_SCALE_ALLCORR__1down"
    elif systematic == 'EG_SCALE_E4SCINTILLATOR_UP': treeSys = "EG_SCALE_E4SCINTILLATOR__1up"
    elif systematic == 'EG_SCALE_E4SCINTILLATOR_DN': treeSys = "EG_SCALE_E4SCINTILLATOR__1down"
    elif systematic == 'MUON_ID_DN':treeSys= "MUON_ID__1down"
    elif systematic == 'MUON_ID_UP':treeSys= "MUON_ID__1up"
    elif systematic == 'MUON_MS_DN':treeSys= "MUON_MS__1down"
    elif systematic == 'MUON_MS_UP':treeSys= "MUON_MS__1up"
    elif systematic == 'MUON_RESBIAS_DN':treeSys= "MUON_SAGITTA_RESBIAS__1down"
    elif systematic == 'MUON_RESBIAS_UP':treeSys= "MUON_SAGITTA_RESBIAS__1up"
    elif systematic == 'MUON_RHO_DN':treeSys= "MUON_SAGITTA_RHO__1down"
    elif systematic == 'MUON_RHO_UP':treeSys= "MUON_SAGITTA_RHO__1up"
    elif systematic == 'MUON_SCALE_DN':treeSys= "MUON_SCALE__1down"
    elif systematic == 'MUON_SCALE_UP':treeSys= "MUON_SCALE__1up"
    # elif systematic == 'EG_SCALE_LARCALIB_EXTRA2015PRE_UP': treeSys = "EG_SCALE_LARCALIB_EXTRA2015PRE__1up"
    # elif systematic == 'EG_SCALE_LARCALIB_EXTRA2015PRE_DN': treeSys = "EG_SCALE_LARCALIB_EXTRA2015PRE__1down"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2015PRE_UP': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2015PRE__1up"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2015PRE_DN': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2015PRE__1down"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_UP': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2016PRE__1up"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_DN': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2016PRE__1down"
    elif systematic == 'JET_BJES_Response_UP'                 : treeSys = 'JET_BJES_Response__1up'
    elif systematic == 'JET_BJES_Response_DN'                 : treeSys = 'JET_BJES_Response__1down'
    elif systematic == 'JET_EffectiveNP_1_UP'                 : treeSys = 'JET_EffectiveNP_1__1up'
    elif systematic == 'JET_EffectiveNP_1_DN'                 : treeSys = 'JET_EffectiveNP_1__1down'
    elif systematic == 'JET_EffectiveNP_2_UP'                 : treeSys = 'JET_EffectiveNP_2__1up'
    elif systematic == 'JET_EffectiveNP_2_DN'                 : treeSys = 'JET_EffectiveNP_2__1down'
    elif systematic == 'JET_EffectiveNP_3_UP'                 : treeSys = 'JET_EffectiveNP_3__1up'
    elif systematic == 'JET_EffectiveNP_3_DN'                 : treeSys = 'JET_EffectiveNP_3__1down'
    elif systematic == 'JET_EffectiveNP_4_UP'                 : treeSys = 'JET_EffectiveNP_4__1up'
    elif systematic == 'JET_EffectiveNP_4_DN'                 : treeSys = 'JET_EffectiveNP_4__1down'
    elif systematic == 'JET_EffectiveNP_5_UP'                 : treeSys = 'JET_EffectiveNP_5__1up'
    elif systematic == 'JET_EffectiveNP_5_DN'                 : treeSys = 'JET_EffectiveNP_5__1down'
    elif systematic == 'JET_EffectiveNP_6_UP'                 : treeSys = 'JET_EffectiveNP_6__1up'
    elif systematic == 'JET_EffectiveNP_6_DN'                 : treeSys = 'JET_EffectiveNP_6__1down'
    elif systematic == 'JET_EffectiveNP_7_UP'                 : treeSys = 'JET_EffectiveNP_7__1up'
    elif systematic == 'JET_EffectiveNP_7_DN'                 : treeSys = 'JET_EffectiveNP_7__1down'
    elif systematic == 'JET_EffectiveNP_8restTerm_UP'         : treeSys = 'JET_EffectiveNP_8restTerm__1up'
    elif systematic == 'JET_EffectiveNP_8restTerm_DN'         : treeSys = 'JET_EffectiveNP_8restTerm__1down'
    elif systematic == 'JET_EtaIntercalibration_Modelling_UP' : treeSys = 'JET_EtaIntercalibration_Modelling__1up'
    elif systematic == 'JET_EtaIntercalibration_Modelling_DN' : treeSys = 'JET_EtaIntercalibration_Modelling__1down'
    elif systematic == 'JET_EtaIntercalibration_NonClosure_UP': treeSys = 'JET_EtaIntercalibration_NonClosure__1up'
    elif systematic == 'JET_EtaIntercalibration_NonClosure_DN': treeSys = 'JET_EtaIntercalibration_NonClosure__1down'
    elif systematic == 'JET_EtaIntercalibration_TotalStat_UP' : treeSys = 'JET_EtaIntercalibration_TotalStat__1up'
    elif systematic == 'JET_EtaIntercalibration_TotalStat_DN' : treeSys = 'JET_EtaIntercalibration_TotalStat__1down'
    elif systematic == 'JET_Flavor_Composition_UP'            : treeSys = 'JET_Flavor_Composition__1up'
    elif systematic == 'JET_Flavor_Composition_DN'            : treeSys = 'JET_Flavor_Composition__1down'
    elif systematic == 'JET_Flavor_Response_UP'               : treeSys = 'JET_Flavor_Response__1up'
    elif systematic == 'JET_Flavor_Response_DN'               : treeSys = 'JET_Flavor_Response__1down'
    elif systematic == 'JET_Pileup_OffsetMu_UP'               : treeSys = 'JET_Pileup_OffsetMu__1up'
    elif systematic == 'JET_Pileup_OffsetMu_DN'               : treeSys = 'JET_Pileup_OffsetMu__1down'
    elif systematic == 'JET_Pileup_OffsetNPV_UP'              : treeSys = 'JET_Pileup_OffsetNPV__1up'
    elif systematic == 'JET_Pileup_OffsetNPV_DN'              : treeSys = 'JET_Pileup_OffsetNPV__1down'
    elif systematic == 'JET_Pileup_PtTerm_UP'                 : treeSys = 'JET_Pileup_PtTerm__1up'
    elif systematic == 'JET_Pileup_PtTerm_DN'                 : treeSys = 'JET_Pileup_PtTerm__1down'
    elif systematic == 'JET_Pileup_RhoTopology_UP'            : treeSys = 'JET_Pileup_RhoTopology__1up'
    elif systematic == 'JET_Pileup_RhoTopology_DN'            : treeSys = 'JET_Pileup_RhoTopology__1down'
    elif systematic == 'JET_PunchThrough_MC15_UP'             : treeSys = 'JET_PunchThrough_MC15__1up'
    elif systematic == 'JET_PunchThrough_MC15_DN'             : treeSys = 'JET_PunchThrough_MC15__1down'
    elif systematic == 'JET_SingleParticle_HighPt_UP'         : treeSys = 'JET_SingleParticle_HighPt__1up'
    elif systematic == 'JET_SingleParticle_HighPt_DN'         : treeSys = 'JET_SingleParticle_HighPt__1down'
    elif systematic == 'JET_JER_CROSS_CALIB_FORWARD_UP'       : treeSys = 'JET_JER_CROSS_CALIB_FORWARD__1up'
    elif systematic == 'JET_JER_CROSS_CALIB_FORWARD_UP'       : treeSys = 'JET_JER_CROSS_CALIB_FORWARD__down'
    elif systematic == 'JET_JER_NOISE_FORWARD_UP'             : treeSys = 'JET_JER_NOISE_FORWARD__1up'
    elif systematic == 'JET_JER_NOISE_FORWARD_UP'             : treeSys = 'JET_JER_NOISE_FORWARD__1down'
    elif systematic == 'JET_JER_NP0_DN'                       : treeSys = 'JET_JER_NP0__1down'
    elif systematic == 'JET_JER_NP0_UP'                       : treeSys = 'JET_JER_NP0__1up'
    elif systematic == 'JET_JER_NP1_DN'                       : treeSys = 'JET_JER_NP1__1down'
    elif systematic == 'JET_JER_NP1_UP'                       : treeSys = 'JET_JER_NP1__1up'
    elif systematic == 'JET_JER_NP2_DN'                       : treeSys = 'JET_JER_NP2__1down'
    elif systematic == 'JET_JER_NP2_UP'                       : treeSys = 'JET_JER_NP2__1up'
    elif systematic == 'JET_JER_NP3_DN'                       : treeSys = 'JET_JER_NP3__1down'
    elif systematic == 'JET_JER_NP3_UP'                       : treeSys = 'JET_JER_NP3__1up'
    elif systematic == 'JET_JER_NP4_DN'                       : treeSys = 'JET_JER_NP4__1down'
    elif systematic == 'JET_JER_NP4_UP'                       : treeSys = 'JET_JER_NP4__1up'
    elif systematic == 'JET_JER_NP5_DN'                       : treeSys = 'JET_JER_NP5__1down'
    elif systematic == 'JET_JER_NP5_UP'                       : treeSys = 'JET_JER_NP5__1up'
    elif systematic == 'JET_JER_NP6_DN'                       : treeSys = 'JET_JER_NP6__1down'
    elif systematic == 'JET_JER_NP6_UP'                       : treeSys = 'JET_JER_NP6__1up'
    elif systematic == 'JET_JER_NP7_DN'                       : treeSys = 'JET_JER_NP7__1down'
    elif systematic == 'JET_JER_NP7_UP'                       : treeSys = 'JET_JER_NP7__1up'
    elif systematic == 'JET_JER_NP8_DN'                       : treeSys = 'JET_JER_NP8__1down'
    elif systematic == 'JET_JER_NP8_UP'                       : treeSys = 'JET_JER_NP8__1up'

    else:
        treeSys = "nominal"
        if systematic == None: pass
        elif systematic == 'FF_UP':      sys_FF_ele   = 'UP'
        elif systematic == 'FF_DN':      sys_FF_ele   = 'DN'
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
        elif systematic == 'RECO_UPSTAT':    sys_reco  = 'UPSTAT'
        elif systematic == 'RECO_DNSTAT':    sys_reco  = 'DNSTAT'    
        elif systematic == 'RECO_UPSYS':    sys_reco  = 'UPSYS'
        elif systematic == 'RECO_DNSYS':    sys_reco  = 'DNSYS'    
        elif systematic == 'TTVA_UPSTAT':  sys_TTVA  = 'UPSTAT'
        elif systematic == 'TTVA_DNSTAT':  sys_TTVA  = 'DNSTAT'    
        elif systematic == 'TTVA_UPSYS':  sys_TTVA  = 'UPSYS'
        elif systematic == 'TTVA_DNSYS':  sys_TTVA  = 'DNSYS'
        elif systematic == 'B_SYS_DN'   : sys_bjet = 'B_SYS_DN'    
        elif systematic == 'B_SYS_UP'   : sys_bjet = 'B_SYS_UP'   
        elif systematic == 'C_SYS_DN'   : sys_bjet = 'C_SYS_DN'   
        elif systematic == 'C_SYS_UP'   : sys_bjet = 'C_SYS_UP'   
        elif systematic == 'L_SYS_DN'   : sys_bjet = 'L_SYS_DN'   
        elif systematic == 'L_SYS_UP'   : sys_bjet = 'L_SYS_UP'   
        elif systematic == 'E_SYS_DN'   : sys_bjet = 'E_SYS_DN'   
        elif systematic == 'E_SYS_UP'   : sys_bjet = 'E_SYS_UP'   
        elif systematic == 'EFC_SYS_DN' : sys_bjet = 'EFC_SYS_DN' 
        elif systematic == 'EFC_SYS_UP' : sys_bjet = 'EFC_SYS_UP' 
        elif systematic == 'JVT_SYS_DN' : sys_JVT = 'JVT_SYS_DN' 
        elif systematic == 'JVT_SYS_UP' : sys_JVT = 'JVT_SYS_UP' 

    assert treeSys!="", "Invalid systematic %s!"%(systematic)

    print treeSys," with systematic: ",systematic

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
    
    loop += ssdilep.algs.algs.VarsAlg(key_muons='muons',key_jets='jets', key_electrons='electrons', require_prompt=False)   

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(
        cutflow='presel',
        key='weight_mc_event',
        sys=HepMCEventWeight)
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
    # loop += ssdilep.algs.EvWeights.MJJReweight(cutflow='presel',key='MJJReweight')
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    # loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='NoFakesInMC')
    # loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='NoFakeMuonsInMC')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BadJetVeto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='bjetveto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AtLeastTwo50GeVJets')
    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++


    loop += ssdilep.algs.EvWeights.SuperGenericFakeFactor(
            key='SuperGenericFakeFactor',
            do_FFweight=True,
            config_file_e=os.path.join(main_path,'ssdilep/data/fakeFactor-21-09-2017.root'),
            config_file_m=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_v11.root'),
            config_fileCHF=os.path.join(main_path,'ssdilep/data/chargeFlipRates-04-08-2017.root'),
            sys_FFe=sys_FF_ele,
            sys_FFm=sys_FF_mu,
            sys_CHF=sys_CF,
            sys_id_e = sys_id,
            sys_iso_e = sys_iso,
            sys_reco_e = sys_reco,
            sys_reco_m = sys_reco,
            sys_iso_m = sys_iso,
            sys_TTVA_m = sys_TTVA,
            )

    # loop += ssdilep.algs.EvWeights.SuperGenericFakeFactor(
    #         key='SuperGenericWeight',
    #         do_FFweight=False,
    #         config_file_e=os.path.join(main_path,'ssdilep/data/fakeFactor-03-08-2017.root'),
    #         config_file_m=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_bveto.root'),
    #         config_fileCHF=os.path.join(main_path,'ssdilep/data/chargeFlipRates-04-08-2017.root'),
    #         sys_FFe=sys_FF_ele,
    #         sys_FFm=sys_FF_mu,
    #         sys_CHF=sys_CF,
    #         sys_id_e = sys_id,
    #         sys_iso_e = sys_iso,
    #         sys_reco_e = sys_reco,
    #         sys_reco_m = sys_reco,
    #         sys_iso_m = sys_iso,
    #         sys_TTVA_m = sys_TTVA,
    #         )

    loop += ssdilep.algs.EvWeights.MuTrigSF(
            trig_list     = ["HLT_mu26_ivarmedium_OR_HLT_mu50"],
            mu_reco       = "Medium",
            mu_iso        = "FixedCutTightTrackOnly",
            key           = "MuTrigSF2016",
            sys_trig      = sys_trig,
            period        = 2016,
            )

    loop += ssdilep.algs.EvWeights.MuTrigSF(
            trig_list     = ["HLT_mu26_imedium_OR_HLT_mu50"],
            mu_reco       = "Medium",
            mu_iso        = "FixedCutTightTrackOnly",
            key           = "MuTrigSF2015",
            sys_trig      = sys_trig,
            period        = 2015,
            )

    loop += ssdilep.algs.EvWeights.ThreeElectron2e17TrigWeight(
            key='ThreeElectron2e17TrigWeight',
            sys_trig = sys_trig,
            )

    loop += ssdilep.algs.EvWeights.GlobalBjet(
            key='GlobalBjet',
            sys = sys_bjet,
            )

    loop += ssdilep.algs.EvWeights.GlobalJVT(
            key='GlobalJVT',
            sys = sys_JVT,
            )

    # Electron Channel OS
    # ---------------------------------------
    # ------ Broad Region
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-OS-Z-BROAD',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronOS',None],
    #            ['TwoEleTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass60GeV2000ele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-OS-Z-BROAD-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronOS',None],
    #            ['TwoEleTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass60GeV2000ele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ------ Z peak
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-OS-Z-PEAK',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronOS',None],
    #            ['TwoEleTwoJetHT300',None],
    #            ['Mjj110',None],
    #            ['Mass60GeV110ele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-OS-Z-PEAK-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronOS',None],
    #            ['TwoEleTwoJetHT300',None],
    #            ['Mjj110',None],
    #            ['Mass60GeV110ele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # ------ ZCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-OS-Z-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronOS',None],
    #            ['TwoEleTwoJetHT300',None],
    #            ['Mjj110',None],
    #            ['Mass110GeV300ele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-OS-Z-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronOS',None],
    #            ['TwoEleTwoJetHT300',None],
    #            ['Mjj110',None],
    #            ['Mass110GeV300ele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ---------------------------------------
    # # ------ ZVR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-OS-Z-VR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronOS',None],
    #            ['TwoEleTwoJetHT300',None],
    #            ['Mjj110',None],
    #            ['Mass300GeV400ele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-OS-Z-VR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronOS',None],
    #            ['TwoEleTwoJetHT300',None],
    #            ['Mjj110',None],
    #            ['Mass300GeV400ele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ---------------------------------------
    # # ------ ZSR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-OS-Z-SR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronOS',None],
    #            ['TwoEleTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass400GeVele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-OS-Z-SR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronOS',None],
    #            ['TwoEleTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass400GeVele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # Electron Channel SS
    # # ---------------------------------------
    # # ------ Z PEAK
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z-PEAK',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass60GeV110ele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z-PEAK-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass60GeV110ele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # ---------------------------------------
    # ------ ZCR
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'electron-SS-Z-CR',
            plot_all = False,
            cut_flow = [
               ['NoLooseFakesInMC',None],
               ['PassHLT2e17lhvloose',None],
               ['ExactlyZeroMuons',None],
               ['ExactlyTwoLooseElectronSS',None],
               # ['TwoEleTwoJetHT300',None],
               # ['Mjj110',None],
               ['Mass110GeV300ele',None],
               ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'electron-SS-Z-CR-fakes',
            plot_all = False,
            cut_flow = [
               ['NoLooseFakesInMC',None],
               ['PassHLT2e17lhvloose',None],
               ['ExactlyZeroMuons',None],
               ['ExactlyTwoLooseElectronSS',None],
               # ['TwoEleTwoJetHT300',None],
               # ['Mjj110',None],
               ['Mass110GeV300ele',None],
               ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
               ],
            )
    # ---------------------------------------
    # ------ ZCR no m(ll) cut
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'electron-SS-Z-nomll-CR',
            plot_all = False,
            cut_flow = [
               ['NoLooseFakesInMC',None],
               ['PassHLT2e17lhvloose',None],
               ['ExactlyZeroMuons',None],
               ['ExactlyTwoLooseElectronSS',None],
               # ['TwoEleTwoJetHT300',None],
               # ['Mjj110',None],
               ['Mass60GeVele',None],
               ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'electron-SS-Z-nomll-CR-fakes',
            plot_all = False,
            cut_flow = [
               ['NoLooseFakesInMC',None],
               ['PassHLT2e17lhvloose',None],
               ['ExactlyZeroMuons',None],
               ['ExactlyTwoLooseElectronSS',None],
               # ['TwoEleTwoJetHT300',None],
               # ['Mjj110',None],
               ['Mass60GeVele',None],
               ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
               ],
            )
    # ---------------------------------------
    # ------ ZCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z60-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['AtLeastTwo60GeVJets',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass110GeV300ele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z60-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['AtLeastTwo60GeVJets',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass110GeV300ele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ---------------------------------------
    # # ------ ZCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z70-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['AtLeastTwo70GeVJets',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass110GeV300ele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z70-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['AtLeastTwo70GeVJets',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass110GeV300ele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ---------------------------------------
    # # ------ ZCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z80-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['AtLeastTwo80GeVJets',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass110GeV300ele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z80-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['AtLeastTwo80GeVJets',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass110GeV300ele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ---------------------------------------
    # # ------ ZCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z90-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['AtLeastTwo90GeVJets',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass110GeV300ele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z90-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['AtLeastTwo90GeVJets',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass110GeV300ele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ---------------------------------------
    # # ------ ZCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z100-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['AtLeastTwo100GeVJets',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass110GeV300ele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z100-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['AtLeastTwo100GeVJets',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass110GeV300ele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # ---------------------------------------
    # ------ ZVR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z-VR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass300GeV400ele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z-VR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            # ['TwoEleTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass300GeV400ele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # ---------------------------------------
    # ------ ZSR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z-SR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['AtLeastTwo100GeVJets',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            ['TwoEleTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass400GeVele',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'electron-SS-Z-SR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoLooseFakesInMC',None],
    #            ['AtLeastTwo100GeVJets',None],
    #            ['PassHLT2e17lhvloose',None],
    #            ['ExactlyZeroMuons',None],
    #            ['ExactlyTwoLooseElectronSS',None],
    #            ['TwoEleTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass400GeVele',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','ThreeElectron2e17TrigWeight','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # Muon Channel OS
    # ---------------------------------------
    # ------ BROAD
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-OS-Z-BROAD',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonOS',None],
    #            ['TwoMuonTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass60GeV2000muon',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-OS-Z-BROAD-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonOS',None],
    #            ['TwoMuonTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass60GeV2000muon',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ------ ZCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-OS-Z-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonOS',None],
    #            ['TwoMuonTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass60GeV110muon',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-OS-Z-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonOS',None],
    #            ['TwoMuonTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass60GeV110muon',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ---------------------------------------
    # # ------ ZVR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-OS-Z-VR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonOS',None],
    #            ['TwoMuonTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass110GeV400muon',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-OS-Z-VR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonOS',None],
    #            ['TwoMuonTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass110GeV400muon',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # Muon Channel SS
    # ---------------------------------------
    # ------ ZCR
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'muon-SS-Z-CR',
            plot_all = False,
            cut_flow = [
               ['NoFakeMuonsInMC',None],
               ['PassORSingleLeptonTriggerMuon',None],
               ['ExactlyZeroElectrons',None],
               ['ExactlyTwoLooseMuonSS',None],
               # ['TwoMuonTwoJetHT300',None],
               # ['Mjj110',None],
               ['Mass60GeV300muon',None],
               ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'muon-SS-Z-CR-fakes',
            plot_all = False,
            cut_flow = [
               ['NoFakeMuonsInMC',None],
               ['PassORSingleLeptonTriggerMuon',None],
               ['ExactlyZeroElectrons',None],
               ['ExactlyTwoLooseMuonSS',None],
               # ['TwoMuonTwoJetHT300',None],
               # ['Mjj110',None],
               ['Mass60GeV300muon',None],
               ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
               ],
            )
    # ------ ZCR no m(ll) cut
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'muon-SS-Z-nomll-CR',
            plot_all = False,
            cut_flow = [
               ['NoFakeMuonsInMC',None],
               ['PassORSingleLeptonTriggerMuon',None],
               ['ExactlyZeroElectrons',None],
               ['ExactlyTwoLooseMuonSS',None],
               # ['TwoMuonTwoJetHT300',None],
               # ['Mjj110',None],
               ['Mass60GeVmuon',None],
               ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'muon-SS-Z-nomll-CR-fakes',
            plot_all = False,
            cut_flow = [
               ['NoFakeMuonsInMC',None],
               ['PassORSingleLeptonTriggerMuon',None],
               ['ExactlyZeroElectrons',None],
               ['ExactlyTwoLooseMuonSS',None],
               # ['TwoMuonTwoJetHT300',None],
               # ['Mjj110',None],
               ['Mass60GeVmuon',None],
               ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
               ],
            )
    # ---------------------------------------
    # ------ ZCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z60-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['AtLeastTwo60GeVJets',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            # ['TwoMuonTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass60GeV300muon',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z60-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['AtLeastTwo60GeVJets',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            # ['TwoMuonTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass60GeV300muon',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ---------------------------------------
    # # ------ ZCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z70-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['AtLeastTwo70GeVJets',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            # ['TwoMuonTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass60GeV300muon',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z70-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['AtLeastTwo70GeVJets',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            # ['TwoMuonTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass60GeV300muon',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ---------------------------------------
    # # ------ ZCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z80-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['AtLeastTwo80GeVJets',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            # ['TwoMuonTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass60GeV300muon',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z80-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['AtLeastTwo80GeVJets',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            # ['TwoMuonTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass60GeV300muon',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ---------------------------------------
    # # ------ ZCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z90-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['AtLeastTwo90GeVJets',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            # ['TwoMuonTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass60GeV300muon',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z90-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['AtLeastTwo90GeVJets',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            # ['TwoMuonTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass60GeV300muon',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ---------------------------------------
    # # ------ ZCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z100-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['AtLeastTwo100GeVJets',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            # ['TwoMuonTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass60GeV300muon',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z100-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['AtLeastTwo100GeVJets',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            # ['TwoMuonTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass60GeV300muon',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # ---------------------------------------
    # ------ ZVR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z-VR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            # ['TwoMuonTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass300GeV400muon',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z-VR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            # ['TwoMuonTwoJetHT300',None],
    #            # ['Mjj110',None],
    #            ['Mass300GeV400muon',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # # ---------------------------------------
    # # ------ ZSR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z-SR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['AtLeastTwo100GeVJets',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            ['TwoMuonTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass400GeVmuon',None],
    #            ['ExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'muon-SS-Z-SR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['NoFakeMuonsInMC',None],
    #            ['AtLeastTwo100GeVJets',None],
    #            ['PassORSingleLeptonTriggerMuon',None],
    #            ['ExactlyZeroElectrons',None],
    #            ['ExactlyTwoLooseMuonSS',None],
    #            ['TwoMuonTwoJetHT400',None],
    #            ['Mjj110',None],
    #            ['Mass400GeVmuon',None],
    #            ['NotExactlyTwoTightLeptons',['SuperGenericFakeFactor','MuTrigSF2016','MuTrigSF2015','GlobalBjet','GlobalJVT']],
    #            ],
    #         )
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


