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

    sys_somesys    = None

    if   systematic == None: pass
    elif systematic == 'SOMESYS_UP':      sys_somesys    = 'up'
    elif systematic == 'SOMESYS_DN':      sys_somesys    = 'dn'
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
    loop += ssdilep.algs.vars.PairsBuilder(
        obj_keys=['muons'],
        pair_key='mu_pairs',
        met_key='met_clus', 
        )
    
    loop += ssdilep.algs.algs.VarsAlg(key_muons='muons',key_jets='jets', key_electrons='electrons', require_prompt=True, use_simple_truth=False)  

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='NoFakesInMC')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BadJetVeto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AtLeastOneLooseEleLooseLLH')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='ZVetoLooseEleLooseLLH')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='DYVetoTightEleMediumLLHisolLoose')

    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++

    loop += ssdilep.algs.EvWeights.GlobalBjet(
            key='GlobalBjet',
            )

    loop += ssdilep.algs.EvWeights.GlobalJVT(
            key='GlobalJVT',
            )

    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------

    ## MyTestRegion
    ## ---------------------------------------

    loop += ssdilep.algs.algs.PlotAlgFFee(
            region   = 'FakeEnrichedRegion-nominal',
            plot_all = False,
            cut_flow = [
               ['bjetveto',["GlobalBjet","GlobalJVT"]],
               ['METtrkLow25',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgFFee(
            region   = 'FakeEnrichedRegion-MET60',
            plot_all = False,
            cut_flow = [
               ['bjetveto',["GlobalBjet","GlobalJVT"]],
               ['METtrkLow60',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgFFee(
            region   = 'FakeEnrichedRegion-MET100',
            plot_all = False,
            cut_flow = [
               ['bjetveto',["GlobalBjet","GlobalJVT"]],
               ['METtrkLow100',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgFFee(
            region   = 'FakeEnrichedRegion-TwoJets',
            plot_all = False,
            cut_flow = [
               ['bjetveto',["GlobalBjet","GlobalJVT"]],
               ['METtrkLow25',None],
               ['AtLeastTwo50GeVJets',None],
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


