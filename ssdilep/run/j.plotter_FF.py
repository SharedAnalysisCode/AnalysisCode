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
    
    loop += ssdilep.algs.algs.VarsAlg(key_muons='muons',key_jets='jets', key_electrons='electrons')   

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
    #loop += ssdilep.algs.EvWeights.TrigPresc(cutflow='presel',key='trigger_prescale')
    loop += ssdilep.algs.EvWeights.DataUnPresc(cutflow='presel',key='data_unprescale') 
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OneMuon') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuPt22') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuEta247') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OneJet') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='TwoMuons')
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='MuPairsMZwindow') 

    
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
    """
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'MyTestRegionZ',
            plot_all  = False,
            cut_flow  = [
              ['TwoMuons',None],
              ],
            )    
    """        

    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'ZWindow',
            plot_all = False,
            cut_flow = [
               ['TwoLooseLeptons',None],
               ['LeptonMassInZWindow',None],
               ],
            )
    
    """


    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EENoTriggerRegion',
            plot_all = False,
            cut_flow = [
               ['AtLeastTwoLooseElectrons',None],
               ['TwoSSElectrons',None],
               ['isEEEvent',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EEPassed_HLT_e60_lhmedium',
            plot_all = False,
            cut_flow = [
               ['AtLeastTwoLooseElectrons',None],
               ['TwoSSElectrons',None],
               ['isEEEvent',None],
               ['PassHLTe60lhmedium',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EEPassed_e24_lhmedium_L1EM20VH',
            plot_all = False,
            cut_flow = [
               ['AtLeastTwoLooseElectrons',None],
               ['TwoSSElectrons',None],
               ['isEEEvent',None],
               ['PassHLTe24lhmediumL1EM20VH',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EEPassed_e24_lhmedium_L1EM18VH',
            plot_all = False,
            cut_flow = [
               ['AtLeastTwoLooseElectrons',None],
               ['TwoSSElectrons',None],
               ['isEEEvent',None],
               ['PassHLTe24lhmediumL1EM18VH',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EEPassed_e120_lhloose',
            plot_all = False,
            cut_flow = [
               ['AtLeastTwoLooseElectrons',None],
               ['TwoSSElectrons',None],
               ['isEEEvent',None],
               ['PassHLTe120lhloose',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EEPassed_2e17_lhloose',
            plot_all = False,
            cut_flow = [
               ['AtLeastTwoLooseElectrons',None],
               ['TwoSSElectrons',None],
               ['isEEEvent',None],
               ['PassHLT2e17lhloose',None],
              ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'MuMuNoTriggerRegion',
            plot_all = False,
            cut_flow = [
               ['TwoSSMuons',None],
               ['isMuMuEvent',None],
               ['MuPairsMZwindow',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'MuMuPassed_mu26_imedium',
            plot_all = False,
            cut_flow = [
               ['TwoSSMuons',None],
               ['isMuMuEvent',None],
               ['MuPairsMZwindow',None],
               ['PassHLTmu26imedium',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'MuMuPassed_mu26_ivarmedium',
            plot_all = False,
            cut_flow = [
               ['TwoSSMuons',None],
               ['isMuMuEvent',None],
               ['MuPairsMZwindow',None],
               ['PassHLTmu26ivarmedium',None],
              ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'MuMuPassed_mu50',
            plot_all = False,
            cut_flow = [
               ['TwoSSMuons',None],
               ['isMuMuEvent',None],
               ['MuPairsMZwindow',None],
               ['PassHLTmu50',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'MuMuPassed_mu22_mu8noL1',
            plot_all = False,
            cut_flow = [
               ['TwoSSMuons',None],
               ['isMuMuEvent',None],
               ['MuPairsMZwindow',None],
               ['PassHLTmu22mu8noL1',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'MuMuPassed_mu26_imedium',
            plot_all = False,
            cut_flow = [
               ['TwoSSMuons',None],
               ['isMuMuEvent',None],
               ['MuPairsMZwindow',None],
               ['PassHLTmu26imedium',None],
              ],
            )


    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EMuNoTriggerRegion',
            plot_all = False,
            cut_flow = [
               ['AtLeastOneLooseElectrons',None],
               ['TwoSSEleMuon',None],
               ['isEMuEvent',None],
              ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EMuPassed_e60_lhmedium',
            plot_all = False,
            cut_flow = [
               ['AtLeastOneLooseElectrons',None],
               ['TwoSSEleMuon',None],
               ['isEMuEvent',None],
               ['PassHLTe60lhmedium',None],
               ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EMuPassed_e24_lhmedium_L1EM18VH',
            plot_all = False,
            cut_flow = [
               ['AtLeastOneLooseElectrons',None],
               ['TwoSSEleMuon',None],
               ['isEMuEvent',None],
               ['PassHLTe24lhmediumL1EM18VH',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EMuPassed_e24_lhmedium_L1EM20VH',
            plot_all = False,
            cut_flow = [
               ['AtLeastOneLooseElectrons',None],
               ['TwoSSEleMuon',None],
               ['isEMuEvent',None],
               ['PassHLTe24lhmediumL1EM20VH',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EMuPassed_e120_lhloose',
            plot_all = False,
            cut_flow = [
               ['AtLeastOneLooseElectrons',None],
               ['TwoSSEleMuon',None],
               ['isEMuEvent',None],
               ['PassHLTe120lhloose',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EMuPassed_mu26_imedium',
            plot_all = False,
            cut_flow = [
               ['AtLeastOneLooseElectrons',None],
               ['TwoSSEleMuon',None],
               ['isEMuEvent',None],
               ['PassHLTmu26imedium',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EMuPassed_mu26_ivarmedium',
            plot_all = False,
            cut_flow = [
               ['AtLeastOneLooseElectrons',None],
               ['TwoSSEleMuon',None],
               ['isEMuEvent',None],
               ['PassHLTmu26ivarmedium',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EMuPassed_mu50',
            plot_all = False,
            cut_flow = [
               ['AtLeastOneLooseElectrons',None],
               ['TwoSSEleMuon',None],
               ['isEMuEvent',None],
               ['PassHLTmu50',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EMuPassed_e17_lhloose_nod0_mu14',
            plot_all = False,
            cut_flow = [
               ['AtLeastOneLooseElectrons',None],
               ['TwoSSEleMuon',None],
               ['isEMuEvent',None],
               ['PassHLTe17lhloosenod0mu14',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'EMuPassed_e7_lhmedium_nod0_mu24',
            plot_all = False,
            cut_flow = [
               ['AtLeastOneLooseElectrons',None],
               ['TwoSSEleMuon',None],
               ['isEMuEvent',None],
               ['PassHLTe7lhmediumnod0mu24',None],
              ],
            )
    """        
    """
    ## FR1
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR1_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR1_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    
    
    ## FR2
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR2_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow30',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR2_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow30',None],
              ],
            )


    ## FR3
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR3_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow50',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR3_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow50',None],
              ],
            )




    ## FR4
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR4_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt40',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR4_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt40',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )


    ## FR5
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR5_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig2',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR5_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )



    ## FR6
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR6_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig4',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR6_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )


    ## FR7
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR7_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi28',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR7_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi28',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )


    ## FR8
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR8_NUM',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi26',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR8_DEN',
            plot_all  = False,
            cut_flow  = [
              ['OneJet',None],
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi26',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    """        
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


