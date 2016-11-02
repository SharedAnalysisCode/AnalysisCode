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
    config['tree']       = 'physics'
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

    sys_ff    = None

    if   systematic == None: pass
    elif systematic == 'FF_UP':      sys_ff    = 'up'
    elif systematic == 'FF_DN':      sys_ff    = 'dn'
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
    
    loop += ssdilep.algs.algs.VarsAlg(key_muons='muons',key_jets='jets')   

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AtLeastTwoMuons') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuPt22') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuEta247') 
    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            is_single_mu = True,
            mu_trig_level="Loose_Loose",
            mu_trig_chain="HLT_mu20_iloose_L1MU15_OR_HLT_mu50",
            key='SingleMuonTrigSF',
            scale=None,
            )
    
    ## pairs
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.PairWeights.MuPairsAllSF(
            key='MuPairsAllSF',
            scale=None,
            )
    
    ## fake-factors
    loop += ssdilep.algs.PairWeights.MuPairsFakeFactor(
            config_file=os.path.join(main_path,'ssdilep/data/g_DebugFF_ff.root'),
            mu_index=0,
            key='MuPairsLeadFF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsFakeFactor(
            config_file=os.path.join(main_path,'ssdilep/data/g_DebugFF_ff.root'),
            mu_index=1,
            key='MuPairsSubLeadFF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsFakeFactor(
            config_file=os.path.join(main_path,'ssdilep/data/g_DebugFF_ff.root'),
            mu_index=2,
            key='MuPairsLeadSubLeadFF',
            scale=None,
            )
    
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------
    
    ## VR1: signal region with coherent filter
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR1_NUM',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsTT',['MuPairsAllSF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR1_LTDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterLT',None],
              ['MuPairsLT',['MuPairsAllSF','MuPairsLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR1_TLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTL',None],
              ['MuPairsTL',['MuPairsAllSF','MuPairsSubLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR1_LLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterLL',None],
              ['MuPairsLL',['MuPairsAllSF','MuPairsLeadSubLeadFF']],
              ],
            )



    ## VR2: signal region with iso-iso filter
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR2_NUM',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsTT',['MuPairsAllSF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR2_LTDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsLT',['MuPairsAllSF','MuPairsLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR2_TLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsTL',['MuPairsAllSF','MuPairsSubLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR2_LLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsLL',['MuPairsAllSF','MuPairsLeadSubLeadFF']],
              ],
            )



    ## VR3: signal region with no filter
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR3_NUM',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsMVis15',None],
              ['MuPairsTT',['MuPairsAllSF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR3_LTDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsMVis15',None],
              ['MuPairsLT',['MuPairsAllSF','MuPairsLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR3_TLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsMVis15',None],
              ['MuPairsTL',['MuPairsAllSF','MuPairsSubLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR3_LLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsMVis15',None],
              ['MuPairsLL',['MuPairsAllSF','MuPairsLeadSubLeadFF']],
              ],
            )


    ## VR4: pairs with z0 requirement and no filter
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR4_NUM',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsTT',['MuPairsAllSF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR4_LTDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsLT',['MuPairsAllSF','MuPairsLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR4_TLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsTL',['MuPairsAllSF','MuPairsSubLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR4_LLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsLL',['MuPairsAllSF','MuPairsLeadSubLeadFF']],
              ],
            )


    ## VR5: pairs with z0 requirement and iso-iso filter
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR5_NUM',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsTT',['MuPairsAllSF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR5_LTDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsLT',['MuPairsAllSF','MuPairsLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR5_TLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsTL',['MuPairsAllSF','MuPairsSubLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR5_LLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsLL',['MuPairsAllSF','MuPairsLeadSubLeadFF']],
              ],
            )



    ## VR6: pairs with two muons, z0 requirement 
    # and iso-iso filter
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR6_NUM',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['TwoMuons',None],
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsTT',['MuPairsAllSF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR6_LTDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['TwoMuons',None],
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsLT',['MuPairsAllSF','MuPairsLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR6_TLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['TwoMuons',None],
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsTL',['MuPairsAllSF','MuPairsSubLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR6_LLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['TwoMuons',None],
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsFilterTT',None],
              ['MuPairsLL',['MuPairsAllSF','MuPairsLeadSubLeadFF']],
              ],
            )


    ## VR7: pairs with two muons, z0 requirement 
    # and no filter
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR7_NUM',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['TwoMuons',None],
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsTT',['MuPairsAllSF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR7_LTDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['TwoMuons',None],
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsLT',['MuPairsAllSF','MuPairsLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR7_TLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['TwoMuons',None],
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsTL',['MuPairsAllSF','MuPairsSubLeadFF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESVR7_LLDEN',
            plot_all  = False,
            obj_keys  = ["mu_pairs"],
            cut_flow  = [
              ['TwoMuons',None],
              ['PassSingleMuIsoChain',['SingleMuonTrigSF']],
              ['MuPairsMatchSingleMuIsoChain',None],
              ['MuPairsAreSS',None],
              ['MuPairsZ0SinThetaNot002',None],
              ['MuPairsMVis15',None],
              ['MuPairsLL',['MuPairsAllSF','MuPairsLeadSubLeadFF']],
              ],
            )
    
    
    
    loop += pyframe.algs.HistCopyAlg()

    ##-------------------------------------------------------------------------
    ## run the job
    ##-------------------------------------------------------------------------
    loop.run(chain, 0, config['events'],
            branches_on_file = config.get('branches_on_file'),
            do_var_log = config.get('do_var_log'),
            )
#______________________________________________________________________________
if __name__ == '__main__':
    pyframe.config.main(analyze)



