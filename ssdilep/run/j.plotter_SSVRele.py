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

    if   systematic == None: pass
    elif systematic == 'FF_UP':      sys_FF    = 'UP'
    elif systematic == 'FF_DN':      sys_FF    = 'DN'
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
    #loop += ssdilep.algs.EvWeights.TrigPresc(cutflow='presel',key='trigger_prescale')
    loop += ssdilep.algs.EvWeights.DataUnPresc(cutflow='presel',key='data_unprescale') 
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BadJetVeto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='PassHLT2e17lhloose')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='ExactlyTwoLooseEleLooseLLHSS')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='Mass130GeV200LooseLLH')
    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++

    loop += ssdilep.algs.EvWeights.ExactlyTwoTightEleSF(
            key='ExactlyTwoTightEleSF_MediumLLH_isolLoose',
            config_file=os.path.join(main_path,'ssdilep/data/chargeFlipRates-24-01-2017.root'),
            chargeFlipSF=True,
            )

    loop += ssdilep.algs.EvWeights.ExactlyTwoTightEleSF(
            key='ExactlyTwoTightEleSF_MediumLLH_isolLooseNOSF',
            config_file=os.path.join(main_path,'ssdilep/data/chargeFlipRates-24-01-2017.root'),
            chargeFlipSF=False,
            )

    loop += ssdilep.algs.EvWeights.ExactlyTwoLooseEleFakeFactor(
            key='ExactlyTwoLooseEleFFTL',
            typeFF="TL",
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-09-01-2017.root'),
            sys = sys_FF,
            )

    loop += ssdilep.algs.EvWeights.ExactlyTwoLooseEleFakeFactor(
            key='ExactlyTwoLooseEleFFLT',
            typeFF="LT",
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-09-01-2017.root'),
            sys = sys_FF,
            )

    loop += ssdilep.algs.EvWeights.ExactlyTwoLooseEleFakeFactor(
            key='ExactlyTwoLooseEleFFLL',
            typeFF="LL",
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-09-01-2017.root'),
            sys = sys_FF,
            )
    
    ## objects
    ## +++++++++++++++++++++++++++++++++++++++
    """
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            #mu_level="Tight",
            mu_index=0,
            key='MuLeadAllSF',
            scale=None,
            )
    """
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------

    ## MyTestRegion
    ## ---------------------------------------

    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'same-sign-CR',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLoose',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'same-sign-CR-noCHF',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLoose',['ExactlyTwoTightEleSF_MediumLLH_isolLooseNOSF']],
               ],
            )

    
    ## Fake Estimation
    ## ---------------------------------------

    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'same-sign-CR-TL',
            plot_all = False,
            loose_el = True,
            cut_flow = [
               ['ExactlyTwoLooseEleLooseLLHTL',['ExactlyTwoLooseEleFFTL']],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'same-sign-CR-LT',
            plot_all = False,
            loose_el = True,
            cut_flow = [
               ['ExactlyTwoLooseEleLooseLLHLT',['ExactlyTwoLooseEleFFLT']],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgCRele(
            region   = 'same-sign-CR-LL',
            plot_all = False,
            loose_el = True,
            cut_flow = [
               ['ExactlyTwoLooseEleLooseLLHLL',['ExactlyTwoLooseEleFFLL']],
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


