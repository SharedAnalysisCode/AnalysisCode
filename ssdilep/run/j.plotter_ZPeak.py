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
    loop += ssdilep.algs.vars.PairsBuilder(
        obj_keys=['muons'],
        pair_key='mu_pairs',
        met_key='met_clus', 
        )
    
    loop += ssdilep.algs.algs.VarsAlg(key_muons='muons',key_jets='jets', key_electrons='electrons', require_prompt=False, use_simple_truth=False)  

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
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='ExactlyTwoLooseEleLooseLLH')

    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    """
    No trigger scale factors!!!
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            is_single_mu = True,
            mu_trig_level="Loose_Loose",
            mu_trig_chain="HLT_mu20_L1MU15",
            key='SingleMuonTrigSF',
            scale=None,
            )
    """ 
    loop += ssdilep.algs.EvWeights.ExactlyTwoTightEleSF(
            key='ExactlyTwoTightEleSF_MediumLLH_isolLoose',
            config_file=os.path.join(main_path,'ssdilep/data/chargeFlipRates-12-01-2017.root'),
            chargeFlipSF=False,
            )

    loop += ssdilep.algs.EvWeights.ExactlyTwoTightEleSF(
            key='ExactlyTwoTightEleSF_MediumLLH_isolLoose_CHFSF',
            config_file=os.path.join(main_path,'ssdilep/data/chargeFlipRates-12-01-2017.root'),
            chargeFlipSF=True,
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

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZWindowAS',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLoose',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ZMassWindowMediumLLHisolLoose',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZWindowSS',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseSS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ZMassWindowMediumLLHisolLooseSS',None],
               ],
            )

    # loop += ssdilep.algs.algs.PlotAlgZee(
    #         region   = 'ZWindowSSchfSF',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyTwoTightEleMediumLLHisolLooseSS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose_CHFSF']],
    #            ['ZMassWindowMediumLLHisolLooseSS',None],
    #            ],
    #         )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZWindowAS-Sideband',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLoose',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ZMassWindowMediumLLHisolLooseSideband',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZWindowSS-Sideband',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseSS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ZMassWindowMediumLLHisolLooseSSSideband',None],
               ],
            )

    # loop += ssdilep.algs.algs.PlotAlgZee(
    #         region   = 'ZWindowSSchfSF-Sideband',
    #         plot_all = False,
    #         cut_flow = [
    #            ['ExactlyTwoTightEleMediumLLHisolLooseSS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose_CHFSF']],
    #            ['ZMassWindowMediumLLHisolLooseSSSideband',None],
    #            ],
    #         )

    ## TruthStudies
    ## --------------------------------------- 

    ## prompt opposite-sign
    '''
    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeOSBothPromp',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseOS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLooseBothPrompt',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeOSCHF1',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseOS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLoosePromptAndCHF1',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeOSCHF2',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseOS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLoosePromptAndCHF2',None],
               ],
            )


    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeOSBrem',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseOS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLoosePromptAndBrem',None],
               ],
            )


    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeOSFSR',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseOS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLoosePromptAndFSR',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeOSFake',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseOS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLoosePromptAndFake',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeOSBothNonPromp',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseOS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLooseBothNonPrompt',None],
               ],
            )

    ## prompt same-sign (should be 0)
    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeSSBothPromp',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseSS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLooseBothPrompt',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeSSCHF1',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseSS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLoosePromptAndCHF1',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeSSCHF2',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseSS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLoosePromptAndCHF2',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeSSBrem',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseSS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLoosePromptAndBrem',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeSSFSR',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseSS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLoosePromptAndFSR',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeSSFake',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseSS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLoosePromptAndFake',None],
               ],
            )

    loop += ssdilep.algs.algs.PlotAlgZee(
            region   = 'ZeeSSBothNonPromp',
            plot_all = False,
            cut_flow = [
               ['ExactlyTwoTightEleMediumLLHisolLooseSS',['ExactlyTwoTightEleSF_MediumLLH_isolLoose']],
               ['ExactlyTwoTightEleMediumLLHisolLooseBothNonPrompt',None],
               ],
            )

    '''

    
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


