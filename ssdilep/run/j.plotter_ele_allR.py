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
    ## setup
    ##-------------------------------------------------------------------------
    config['tree']       = 'physics/nominal'
    config['do_var_log'] = True
    main_path = os.getenv('MAIN')
    
    ## build chain
    chain = ROOT.TChain(config['tree'])
    for fn in config['input']: chain.Add(fn)

    ##-------------------------------------------------------------------------
    ## systematics 
    ##-------------------------------------------------------------------------
    """
    pass systematics on the command line like this:
    python j.plotter.py --config="sys:SYS_UP"
    """
    config.setdefault('sys',None)
    systematic = config['sys']

    sys_FF    = None
    sys_CF    = None

    if   systematic == None: pass
    elif systematic == 'FF_UP':      sys_FF    = 'UP'
    elif systematic == 'FF_DN':      sys_FF    = 'DN'
    elif systematic == 'CF_UP':      sys_CF    = 'UP'
    elif systematic == 'CF_DN':      sys_CF    = 'DN'
    else: 
        assert False, "Invalid systematic %s!"%(systematic)


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
    loop += ssdilep.algs.EvWeights.LPXKfactor(cutflow='presel',key='lpx_kfactor')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='NoFakesInMC')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='DCHAllElectron')
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

    loop += ssdilep.algs.EvWeights.TwoElectron2e17TrigWeight(
            key='TwoElectron2e17TrigWeight',
            )

    loop += ssdilep.algs.EvWeights.ThreeElectron2e17TrigWeight(
            key='ThreeElectron2e17TrigWeight',
            )

    loop += ssdilep.algs.EvWeights.AllTightEleSF(
            key='AllTightEleSF',
            config_file=os.path.join(main_path,'ssdilep/data/chargeFlipRates-28-03-2017.root'),
            chargeFlipSF=True,
            sys_CF = sys_CF,
            )

    loop += ssdilep.algs.EvWeights.GenericFakeFactor(
            key='GenericFakeFactor',
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-27-03-2017.root'),
            config_fileCHF=os.path.join(main_path,'ssdilep/data/chargeFlipRates-28-03-2017.root'),
            sys = sys_FF,
            )

    ## TTT REGION
    ## ---------------------------------------
    ## ------  diboson
    # loop += ssdilep.algs.algs.PlotAlgThreeLep(
    #         region   = 'diboson-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyThreeLooseEleLooseLLHSS90M200',None],
    #            ['ExactlyThreeLooseEleLooseLLHOSZmass',None],
    #            ['ExactlyThreeTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgThreeLep(
    #         region   = 'diboson-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyThreeLooseEleLooseLLHSS90M200',None],
    #            ['ExactlyThreeLooseEleLooseLLHOSZmass',None],
    #            ['FailExactlyThreeTightEleMediumLLHisolLoose',["GenericFakeFactor","ThreeElectron2e17TrigWeight"]],
    #            ],
    #         )

    # ## ------ three electron
    # loop += ssdilep.algs.algs.PlotAlgThreeLep(
    #         region   = 'threeElectron-VR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyThreeLooseEleLooseLLHSS90M200',None],
    #            ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
    #            ['ExactlyThreeTightEleMediumLLHisolLoose',['AllTightEleSF','ThreeElectron2e17TrigWeight']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgThreeLep(
    #         region   = 'threeElectron-VR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyThreeLooseEleLooseLLHSS90M200',None],
    #            ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
    #            ['FailExactlyThreeTightEleMediumLLHisolLoose',["GenericFakeFactor","ThreeElectron2e17TrigWeight"]],
    #            ],
    #         )

    # ## TT REGION
    # ## ---------------------------------------
    # ## ------ OSCR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'opposite-sign-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyTwoLooseEleLooseLLHOS',None],
    #            ['Mass130GeVLooseLLH',None],
    #            ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','TwoElectron2e17TrigWeight']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'opposite-sign-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyTwoLooseEleLooseLLHOS',None],
    #            ['Mass130GeVLooseLLH',None],
    #            ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','TwoElectron2e17TrigWeight']],
    #            ],
    #         )
    # ## ------ SSVR
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'same-sign-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyTwoLooseEleLooseLLHSS',None],
    #            ['Mass130GeV200LooseLLH',None],
    #            ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','TwoElectron2e17TrigWeight']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'same-sign-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyTwoLooseEleLooseLLHSS',None],
    #            ['Mass130GeV200LooseLLH',None],
    #            ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','TwoElectron2e17TrigWeight']],
    #            ],
    #         )

    # ## TT REGION 2 bjet
    # ## ---------------------------------------
    # ## ------ OSCR ttbar
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'opposite-sign-ttbar-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyTwoLooseEleLooseLLHOS',None],
    #            ['Mass130GeVLooseLLH',None],
    #            ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
    #            ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','TwoElectron2e17TrigWeight']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'opposite-sign-ttbar-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyTwoLooseEleLooseLLHOS',None],
    #            ['Mass130GeVLooseLLH',None],
    #            ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
    #            ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','TwoElectron2e17TrigWeight']],
    #            ],
    #         )
    # ## ------ SSVR ttbar
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'same-sign-ttbar-CR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyTwoLooseEleLooseLLHSS',None],
    #            ['Mass130GeV200LooseLLH',None],
    #            ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
    #            ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','TwoElectron2e17TrigWeight']],
    #            ],
    #         )
    # loop += ssdilep.algs.algs.PlotAlgCRele(
    #         region   = 'same-sign-ttbar-CR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyTwoLooseEleLooseLLHSS',None],
    #            ['Mass130GeV200LooseLLH',None],
    #            ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
    #            ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','TwoElectron2e17TrigWeight']],
    #            ],
    #         )
    ## SIGNAL REGION
    ## ---------------------------------------
    ## ------ two ele
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'two-ele-SR',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoLooseEleLooseLLH',None],
               ['ExactlyTwoLooseEleLooseLLHSS',None],
               ['Mass200GeVLooseLLH',None],
               ['ExactlyTwoTightEleMediumLLHisolLoose',['AllTightEleSF','TwoElectron2e17TrigWeight']],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'two-ele-SR-fakes',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoLooseEleLooseLLH',None],
               ['ExactlyTwoLooseEleLooseLLHSS',None],
               ['Mass200GeVLooseLLH',None],
               ['NotExactlyTwoTightEleMediumLLHisolLoose',['GenericFakeFactor','TwoElectron2e17TrigWeight']],
               ],
            )
    ## ------ three ele
    loop += ssdilep.algs.algs.PlotAlgThreeLep(
            region   = 'three-ele-SR',
            plot_all = False,
            cut_flow = [
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
               ['ExactlyThreeLooseEleLooseLLH',None],
               ['ExactlyThreeLooseEleLooseLLHSS200M',None],
               ['ExactlyThreeLooseEleLooseLLHOSZVeto',None],
               ['FailExactlyThreeTightEleMediumLLHisolLoose',["GenericFakeFactor","ThreeElectron2e17TrigWeight"]],
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


