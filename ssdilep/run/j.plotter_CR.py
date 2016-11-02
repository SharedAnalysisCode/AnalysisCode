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
   

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
    loop += ssdilep.algs.EvWeights.TrigPresc(cutflow='presel',key='trigger_prescale')
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AtLeastOneMuon') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='TwoMuons') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OneMuon') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuPt20') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuPt22') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuPt20') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuPt12') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuEta247') 

    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    """
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            is_single_mu = True,
            mu_trig_level="Loose_Loose",
            mu_trig_chain="HLT_mu20_L1MU15",
            key='SingleMuonTrigSF',
            scale=None,
            )
    """ 
    """
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            is_di_mu = True,
            mu_trig_level="Loose_Loose",
            mu_trig_chain="HLT_2mu10",
            key='DiMuonTrigSF',
            scale=None,
            )
    """ 
    
    ## pairs
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.PairWeights.MuPairsAllSF(
            lead_mu_level="Tight",
            sublead_mu_level="Tight",
            key='MuPairsAllTightSF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsAllSF(
            lead_mu_level="Tight",
            sublead_mu_level="NotTight",
            key='MuPairsLeadTightSubLeadNotTightAllSF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsAllSF(
            lead_mu_level="NotTight",
            sublead_mu_level="Tight",
            key='MuPairsLeadNotTightSubLeadTightAllSF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsAllSF(
            lead_mu_level="NotTight",
            sublead_mu_level="NotTight",
            key='MuPairsLeadNotTightSubLeadNotTightAllSF',
            scale=None,
            )
    
    ## fake-factors
    """
    loop += ssdilep.algs.PairWeights.MuPairsFakeFactor(
            config_file=os.path.join(main_path,'ssdilep/data/hist_ff.root'),
            mu_index=0,
            key='MuPairsLeadFF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsFakeFactor(
            config_file=os.path.join(main_path,'ssdilep/data/hist_ff.root'),
            mu_index=1,
            key='MuPairsSubLeadFF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsFakeFactor(
            config_file=os.path.join(main_path,'ssdilep/data/hist_ff.root'),
            mu_index=2,
            key='MuPairsLeadSubLeadFF',
            scale=None,
            )
    """ 
    ## objects
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            #mu_level="Tight",
            mu_index=0,
            key='MuLeadAllSF',
            scale=None,
            )
    """
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            #mu_level="NotTight",
            mu_index=1,
            key='MuSubLeadAllSF',
            scale=None,
            )
    """
    """
    loop += ssdilep.algs.ObjWeights.MuFakeFactor(
            #config_file=os.path.join(main_path,'ssdilep/data/hist_ff.root'),
            #config_file=os.path.join(main_path,'ssdilep/data/hist_ff_merged_TueZ0.root'),
            #config_file=os.path.join(main_path,'ssdilep/data/hist_ff_merged_Tue2Mu10.root'),
            #config_file=os.path.join(main_path,'ssdilep/data/hist_ff_merged_Flip.root'),
            config_file=os.path.join(main_path,'ssdilep/data/hist_ff_merged_Try13.root'),
            mu_index=0,
            key='MuLeadFF',
            scale=None,
            )
    loop += ssdilep.algs.ObjWeights.MuFakeFactor(
            #config_file=os.path.join(main_path,'ssdilep/data/hist_ff.root'),
            #config_file=os.path.join(main_path,'ssdilep/data/hist_ff_merged_TueZ0.root'),
            #config_file=os.path.join(main_path,'ssdilep/data/hist_ff_merged_Tue2Mu10.root'),
            #config_file=os.path.join(main_path,'ssdilep/data/hist_ff_merged_Flip.root'),
            config_file=os.path.join(main_path,'ssdilep/data/hist_ff_merged_Try13.root'),
            mu_index=1,
            key='MuSubLeadFF',
            scale=None,
            )
    """
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------
    
    ## di-jet control region fakes numerator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR1_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuClose',None],
              ['METlow40',None],
              ],
            )
    ## di-jet control region fakes denominator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR1_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuFar',None],
              ['METlow40',None],
              ],
            )
    
    
    ## di-jet control region fakes numerator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR2_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuClose',None],
              ['METlow40',None],
              ],
            )
    ## di-jet control region fakes denominator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR2_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuInclFar',None],
              ['METlow40',None],
              ],
            )
    
    
    
    
    
    ## di-jet control region fakes numerator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR3_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              #['LeadMuClose',None],
              ['METlow40',None],
              ],
            )
    ## di-jet control region fakes denominator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR3_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              #['LeadMuFar',None],
              ['METlow40',None],
              ],
            )
    
    
    
    ## di-jet control region fakes numerator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR4_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuClose',None],
              #['METlow40',None],
              ],
            )
    ## di-jet control region fakes denominator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR4_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuFar',None],
              #['METlow40',None],
              ],
            )
    
    
    
    
    ## di-jet control region fakes numerator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR5_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuClose',None],
              ['METlow25',None],
              ],
            )
    ## di-jet control region fakes denominator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR5_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuFar',None],
              ['METlow25',None],
              ],
            )
    
    
    
    ## di-jet control region fakes numerator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR6_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              #['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuClose',None],
              ['METlow40',None],
              ],
            )
    ## di-jet control region fakes denominator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR6_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              #['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuFar',None],
              ['METlow40',None],
              ],
            )
    
    
    ## di-jet control region fakes numerator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR7_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuClose',None],
              ['METlow40',None],
              ],
            )
    ## di-jet control region fakes denominator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR7_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuFar',None],
              ['METlow40',None],
              ],
            )
    
    
    
    ## di-jet control region fakes numerator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR8_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoTight',None],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuClose',None],
              ['METlow40',None],
              ],
            )
    ## di-jet control region fakes denominator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR8_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoNotTight',None],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuFar',None],
              ['METlow40',None],
              ],
            )
    
    ## di-jet control region fakes numerator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR9_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              #['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuClose',None],
              ['METlow40',None],
              ],
            )
    ## di-jet control region fakes denominator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR9_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              ['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              #['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuFar',None],
              ['METlow40',None],
              ],
            )
    
    ## di-jet control region fakes numerator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR10_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              #['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuClose',None],
              ['METlow40',None],
              ],
            )
    ## di-jet control region fakes denominator
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESCR10_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MuTrigMatch',None],
              #['MuTruthFilter',None],
              ['SingleMuTrigPass',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt25',None],
              ['LeadMuFar',None],
              ['METlow40',None],
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



