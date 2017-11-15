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

    sys_FF_ele    = None

    if   systematic == None: pass
    elif systematic == 'FF_UP':      sys_FF_ele    = 'UP'
    elif systematic == 'FF_DN':      sys_FF_ele    = 'DN'
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
    loop += ssdilep.algs.met.METTRK(
        prefix='metFinalTrk',
        key = 'met_trk',
        )
    
    
    loop += ssdilep.algs.algs.VarsAlg(key_muons='muons',key_jets='jets', key_electrons='electrons', require_prompt=False, use_simple_truth=False)  

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
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='bjetveto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='ExactlyOneLooseEleLooseLLH')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='ExactlyZeroMuons')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='METhigher25')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='MThigher50')

    
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

    loop += ssdilep.algs.EvWeights.SuperGenericFakeFactor(
            key='SuperGenericFakeFactor',
            do_FFweight=True,
            config_file_e=os.path.join(main_path,'ssdilep/data/fakeFactor-21-09-2017.root'),
            config_file_m=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_bveto.root'),
            config_fileCHF=os.path.join(main_path,'ssdilep/data/chargeFlipRates-04-08-2017.root'),
            sys_FFe=sys_FF_ele,
            # sys_FFm=sys_FF_mu,
            # sys_CHF=sys_CF,
            # sys_id_e = sys_id,
            # sys_iso_e = sys_iso,
            # sys_reco_e = sys_reco,
            # sys_reco_m = sys_reco,
            # sys_iso_m = sys_iso,
            # sys_TTVA_m = sys_TTVA,
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

    ## WJets nominal
    ## ---------------------------------------
    # loop += ssdilep.algs.algs.PlotAlgWJets(
    #         region   = 'Wjets-VR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyOneTightEleMediumLLHisolLoose',["SuperGenericFakeFactor","GlobalBjet","GlobalJVT"]],
    #            ],
    #         )

    # loop += ssdilep.algs.algs.PlotAlgWJets(
    #         region   = 'Wjets-VR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyZeroTightEleMediumLLHisolLoose',["SuperGenericFakeFactor","GlobalBjet","GlobalJVT"]],
    #            ],
    #         )

    ## WJets 2 jets
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlgWJets(
            region   = 'Wjets-TwoJets-VR',
            plot_all = False,
            cut_flow = [
               ['ExactlyOneTightEleMediumLLHisolLoose',["SuperGenericFakeFactor","GlobalBjet","GlobalJVT"]],
               ['AtLeastTwo50GeVJets',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgWJets(
            region   = 'Wjets-TwoJets-VR-fakes',
            plot_all = False,
            cut_flow = [
               ['ExactlyZeroTightEleMediumLLHisolLoose',["SuperGenericFakeFactor","GlobalBjet","GlobalJVT"]],
               ['AtLeastTwo50GeVJets',None],
               ],
            )

    ## WJets tight
    ## ---------------------------------------
    # loop += ssdilep.algs.algs.PlotAlgWJets(
    #         region   = 'Wjets-tight-VR',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyOneTightEleMediumLLHisolLoose',["SuperGenericFakeFactor","GlobalBjet","GlobalJVT"]],
    #            ['METtrkLow60',None],
    #            ['MTlow120',None],
    #            ],
    #         )

    # loop += ssdilep.algs.algs.PlotAlgWJets(
    #         region   = 'Wjets-tight-VR-fakes',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyZeroTightEleMediumLLHisolLoose',["SuperGenericFakeFactor","GlobalBjet","GlobalJVT"]],
    #            ['METtrkLow60',None],
    #            ['MTlow120',None],
    #            ],
    #         )

    ## WJets tight 2 jets
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlgWJets(
            region   = 'Wjets-tight-TwoJets-VR',
            plot_all = False,
            cut_flow = [
               ['ExactlyOneTightEleMediumLLHisolLoose',["SuperGenericFakeFactor","GlobalBjet","GlobalJVT"]],
               ['METtrkLow60',None],
               ['MTlow120',None],
               ['AtLeastTwo50GeVJets',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgWJets(
            region   = 'Wjets-tight-TwoJets-VR-fakes',
            plot_all = False,
            cut_flow = [
               ['ExactlyZeroTightEleMediumLLHisolLoose',["SuperGenericFakeFactor","GlobalBjet","GlobalJVT"]],
               ['METtrkLow60',None],
               ['MTlow120',None],
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


