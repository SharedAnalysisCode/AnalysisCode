#!/usr/bin/env python                                                                                                                                                            
# -*- coding: utf-8 -*-                                                                                                                                                          

"""                                                                                                                                                                              
algs.py                                                                                                                                                                          
                                                                                                                                                                                 
This module contains a set of analysis specific algs                                                                                                                             
for calculating variables, applying selection and                                                                                                                                
plotting.                                                                                                                                                                        
"""

## std modules                                                                                                                                                                   
import itertools
import os
import math
import ROOT

## logging                                                                                                                                                                       
import logging
log = logging.getLogger(__name__)

## python                                                                                                                                                                        
from itertools import combinations
from copy import copy

## pyframe                                                                                                                                                                       
import pyframe

import mcutils
import algs

GeV = 1000.0

#------------------------------------------------------------------------------                                                                                                  
class CutAlg(pyframe.core.Algorithm):
    """                                                                                                                                                                          
    Filtering alg for applying a single cut.  The predefined cuts must be                                                                                                        
    implemeneted as a function with the prefix "cut_". One can then specify the                                                                                                  
    cut to be applied by passing the cut=<cut name> in the constructor, which                                                                                                    
    will execture the cut_<cut name>() function.                                                                                                                                 
    """
    #__________________________________________________________________________    
    def __init__(self,
                 name     = None,
                 cut      = None,
                 cutflow  = None,
                 isfilter = True,
                 ):
        pyframe.core.Algorithm.__init__(self, name if name else cut,isfilter=isfilter)
        self.cutflow = cutflow

    #__________________________________________________________________________                                                                                                  
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)

        return self.apply_cut(self.name)

    #__________________________________________________________________________                                                                                                  
    def apply_cut(self,cutname):
        if self.store.has_key(cutname): return self.store[cutname]
        cut_function = 'cut_%s'%cutname
        assert hasattr(self,cut_function),"cut %s doesnt exist!'"%(cutname)
        self.store[cutname] = result = getattr(self,cut_function)()
        return result

    #__________________________________________________________________________   

    def cut_AtLeastOneLooseElectrons(self):
        return self.chain.nel > 0

    #__________________________________________________________________________                                                                                                  
    def cut_AtLeastTwoLooseElectrons(self):
      return self.chain.nel > 1

    #__________________________________________________________________________                                                                                                  
    def cut_OneLooseElectron(self):
        return self.chain.nel == 1

    #__________________________________________________________________________                                                                                                  
    def cut_TwoLooseElectrons(self):
        return self.chain.nel == 2

    #__________________________________________________________________________                                                                                                  
    def cut_LeadElectronIsLoose(self):
        cname = "LeadElectronIsLoose"
        electrons  = self.store['electrons']
        if electrons[0].tlv.Pt()>30*GeV and electrons[0].isLHLoose and electrons[0].tlv.Eta()<2.47 and not(1.37<electrons[0].tlv.Eta()<1.52) and electrons[0].trkd0sig<5 and electrons[0].trkz0sintheta<0.5 : return True;
         
        return False;    

    #__________________________________________________________________________                                                                                                  
    def cut_SubLeadElectronIsLoose(self):
        cname = "SubLeadElectronIsLoose"
        electrons  = self.store['electrons']
        if electrons[1].tlv.Pt()>30*GeV and electrons[1].isLHLoose and electrons[1].tlv.Eta()<2.47 and not(1.37<electrons[1].tlv.Eta()<1.52) and electrons[1].trkd0sig<5 and electrons[1].trkz0sintheta<0.5 : return True;
        
        return False;    

    #__________________________________________________________________________                                                                                                  
    def cut_LeadElectronIsTight(self):
        cname = "LeadElectronIsTight"
        electrons  = self.store['electrons']
        if electrons[0].tlv.Pt()>30*GeV and electrons[0].isLHMedium and electrons[0].tlv.Eta()<2.47 and not(1.37<electrons[0].tlv.Eta()<1.52) and electrons[0].trkd0sig<5 and electrons[0].trkz0sintheta<0.5 and electrons[0].isIsolated_Loose : return True;

        return False;

    #__________________________________________________________________________ 

    def cut_SubLeadElectronIsTight(self):
        cname = "SubLeadElectronIsTight"
        electrons  = self.store['electrons']
        if electrons[1].tlv.Pt()>30*GeV and electrons[1].isLHMedium and electrons[1].tlv.Eta()<2.47 and not(1.37<electrons[1].tlv.Eta()<1.52) and electrons[1].trkd0sig<5 and electrons[1].trkz0sintheta<0.5 and electrons[1].isIsolated_Loose : return True;

        return False;

    #__________________________________________________________________________                                                                                               
    def cut_TwoOSElectrons(self):
      electrons  = self.store['electrons']
      if len(electrons)==2:
        if electrons[0].trkcharge * electrons[1].trkcharge < 0.0:
          return True
      return False

    #__________________________________________________________________________                                                                                                  
    def cut_TwoSSElectrons(self):
      electrons  = self.store['electrons']
      if len(electrons)==2:
        if electrons[0].trkcharge * electrons[1].trkcharge > 0.0:
          return True
      return False

    #__________________________________________________________________________                                                                                                  
    def cut_PASS(self):
      return True
#------------------------------------------------------------------------------
class PlotAlg(pyframe.algs_EE.CutFlowAlg,CutAlg):
    """

    For making a set of standard plots after each cut in a cutflow.  PlotAlg
    inherets from CutAlg so all the functionality from CutAlg is available for
    applying selection. In addition you can apply weights at different points
    in the selection.

    The selection should be configured by specifying 'cut_flow' in the
    constructor as such:

    cut_flow = [
        ['Cut1', ['Weight1a','Weight1b'],
        ['Cut2', ['Weight2']],
        ['Cut3', None],
        ...
        ]

    The weights must be available in the store.

    'region' will set the name of the dir where the plots are saved

    Inhereting from CutFlowAlg provides the functionality to produce cutflow
    histograms that will be named 'cutflow_<region>' and 'cutflow_raw_<region>'

    """
    #__________________________________________________________________________
    def __init__(self,
                 name     = 'PlotAlg',
                 region   = '',
                 obj_keys = [], # make cutflow hist for just this objects
                 cut_flow = None,
                 plot_all = True,
                 ):
        pyframe.algs_EE.CutFlowAlg.__init__(self,key=region,obj_keys=obj_keys)
        CutAlg.__init__(self,name,isfilter=False)
        self.cut_flow = cut_flow
        self.region   = region
        self.plot_all = plot_all
        self.obj_keys = obj_keys
    
    #_________________________________________________________________________
    def initialize(self):
        pyframe.algs_EE.CutFlowAlg.initialize(self)
    #_________________________________________________________________________
    def execute(self, weight):
   
        # next line fills in the cutflow hists
        # the first bin of the cutflow does not
        # take into account object weights
        pyframe.algs_EE.CutFlowAlg.execute(self, weight)

        list_cuts = []
        for cut, list_weights in self.cut_flow:
            ## apply weights for this cut
            if list_weights:
              for w in list_weights: weight *= self.store[w]

            list_cuts.append(cut)
            passed = self.check_region(list_cuts)
            self.hists[self.region].count_if(passed, cut, weight)

            ## if plot_all is True, plot after each cut, 
            ## else only plot after full selection
            
            # obj cutflow is computed at the end of the cutflow
            #if len(list_cuts)==len(self.cut_flow):
            if self.obj_keys:
             for k in self.obj_keys:
              for o in self.store[k]:
               if hasattr(o,"cdict") and hasattr(o,"wdict"):
                obj_passed = True
                obj_weight = 1.0
                if list_weights:
                 for w in list_weights:
                  if w.startswith("MuPairs"):
                   obj_weight *= o.GetWeight(w) 
                for c in list_cuts:
                 if c.startswith("MuPairs"):
                  obj_passed = o.HasPassedCut(c) and obj_passed
                self.hists[self.region+"_"+k].count_if(obj_passed and passed, c, obj_weight * weight)
            
            if (self.plot_all or len(list_cuts)==len(self.cut_flow)):
               region_name = os.path.join(self.region,'_'.join(list_cuts))
               region_name = region_name.replace('!', 'N')
               region = os.path.join('/regions/', region_name)
               
               #if passed:             
               self.plot(region, passed, list_cuts, cut, list_weights=list_weights, weight=weight)

        return True

    #__________________________________________________________________________
    def finalize(self):
        pyframe.algs_EE.CutFlowAlg.finalize(self)

    #__________________________________________________________________________
    def plot(self, region, passed, list_cuts, cut, list_weights=None, weight=1.0):
        
        # should probably make this configurable
        ## get event candidate
        electrons  = self.store['electrons']
        el_lead    = electrons[0]
        el_sublead = electrons[1]
        
        ELECTRONS = os.path.join(region,'electrons')
        
        # -----------------
        # Create histograms
        # -----------------
        ## muon plots
        # leading
        self.h_ellead_pt = self.hist('h_ellead_pt', "ROOT.TH1F('$', ';p_{T}(#mu_{lead}) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_ellead_eta = self.hist('h_ellead_eta', "ROOT.TH1F('$', ';#eta(#mu_{lead});Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_ellead_phi = self.hist('h_ellead_phi', "ROOT.TH1F('$', ';#phi(#mu_{lead});Events / (0.1)', 64, -3.2, 3.2)", dir=ELECTRONS)
        self.h_ellead_trkd0 = self.hist('h_ellead_trkd0', "ROOT.TH1F('$', ';d^{trk}_{0}(#mu_{lead}) [mm];Events / (0.01)', 80, -0.4, 0.4)", dir=ELECTRONS)
        self.h_ellead_trkd0sig = self.hist('h_ellead_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(#mu_{lead});Events / (0.1)', 100, 0., 10.)", dir=ELECTRONS)
        self.h_ellead_trkz0 = self.hist('h_ellead_trkz0', "ROOT.TH1F('$', ';z^{trk}_{0}(#mu_{lead}) [mm];Events / (0.1)', 40, -2, 2)", dir=ELECTRONS)
        self.h_ellead_trkz0sintheta = self.hist('h_ellead_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(#mu_{lead}) [mm];Events / (0.01)', 200, -1, 1)", dir=ELECTRONS)
              
        self.h_ellead_topoetcone20 = self.hist('h_ellead_topoetcone20', "ROOT.TH1F('$', ';topoetcone20/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_topoetcone30 = self.hist('h_ellead_topoetcone30', "ROOT.TH1F('$', ';topoetcone30/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_topoetcone40 = self.hist('h_ellead_topoetcone40', "ROOT.TH1F('$', ';topoetcone40/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_ptvarcone20 = self.hist('h_ellead_ptvarcone20', "ROOT.TH1F('$', ';ptvarcone20/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_ptvarcone30 = self.hist('h_ellead_ptvarcone30', "ROOT.TH1F('$', ';ptvarcone30/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_ptvarcone40 = self.hist('h_ellead_ptvarcone40', "ROOT.TH1F('$', ';ptvarcone40/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
              
        self.h_ellead_ptcone20 = self.hist('h_ellead_ptcone20', "ROOT.TH1F('$', ';ptcone20/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_ptcone30 = self.hist('h_ellead_ptcone30', "ROOT.TH1F('$', ';ptcone30/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_ptcone40 = self.hist('h_ellead_ptcone40', "ROOT.TH1F('$', ';ptcone40/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        
        
        # subleading
        """
        self.h_musublead_pt = self.hist('h_musublead_pt', "ROOT.TH1F('$', ';p_{T}(#mu_{sublead}) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MUONS)
        self.h_musublead_eta = self.hist('h_musublead_eta', "ROOT.TH1F('$', ';#eta(#mu_{sublead});Events / (0.1)', 50, -2.5, 2.5)", dir=MUONS)
        self.h_musublead_phi = self.hist('h_musublead_phi', "ROOT.TH1F('$', ';#phi(#mu_{sublead});Events / (0.1)', 64, -3.2, 3.2)", dir=MUONS)
        self.h_musublead_trkd0 = self.hist('h_musublead_trkd0', "ROOT.TH1F('$', ';d^{trk}_{0}(#mu_{sublead}) [mm];Events / (0.01)', 80, -0.4, 0.4)", dir=MUONS)
        self.h_musublead_trkd0sig = self.hist('h_musublead_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(#mu_{sublead});Events / (0.1)', 100, 0., 10.)", dir=MUONS)
        self.h_musublead_trkz0 = self.hist('h_musublead_trkz0', "ROOT.TH1F('$', ';z^{trk}_{0}(#mu_{sublead}) [mm];Events / (0.1)', 40, -2, 2)", dir=MUONS)
        self.h_musublead_trkz0sintheta = self.hist('h_musublead_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(#mu_{sublead}) [mm];Events / (0.01)', 200, -1, 1)", dir=MUONS)
              
        self.h_musublead_topoetcone20 = self.hist('h_musublead_topoetcone20', "ROOT.TH1F('$', ';topoetcone20/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_topoetcone30 = self.hist('h_musublead_topoetcone30', "ROOT.TH1F('$', ';topoetcone30/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_topoetcone40 = self.hist('h_musublead_topoetcone40', "ROOT.TH1F('$', ';topoetcone40/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptvarcone20 = self.hist('h_musublead_ptvarcone20', "ROOT.TH1F('$', ';ptvarcone20/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptvarcone30 = self.hist('h_musublead_ptvarcone30', "ROOT.TH1F('$', ';ptvarcone30/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptvarcone40 = self.hist('h_musublead_ptvarcone40', "ROOT.TH1F('$', ';ptvarcone40/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
              
        self.h_musublead_ptcone20 = self.hist('h_musublead_ptcone20', "ROOT.TH1F('$', ';ptcone20/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptcone30 = self.hist('h_musublead_ptcone30', "ROOT.TH1F('$', ';ptcone30/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptcone40 = self.hist('h_musublead_ptcone40', "ROOT.TH1F('$', ';ptcone40/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        """



        # ---------------
        # Fill histograms
        # ---------------
        if passed:
          ## muon plots
          # leading
          self.h_ellead_pt.Fill(el_lead.tlv.Pt()/GeV, weight)
          self.h_ellead_eta.Fill(el_lead.tlv.Eta(), weight)
          self.h_ellead_phi.Fill(el_lead.tlv.Phi(), weight)
          self.h_ellead_trkd0.Fill(el_lead.trkd0, weight)
          self.h_ellead_trkd0sig.Fill(el_lead.trkd0sig, weight)
          self.h_ellead_trkz0.Fill(el_lead.trkz0, weight)
          self.h_ellead_trkz0sintheta.Fill(el_lead.trkz0sintheta, weight)
         
          self.h_ellead_topoetcone20.Fill(el_lead.topoetcone20/el_lead.tlv.Pt(), weight)
          self.h_ellead_topoetcone30.Fill(el_lead.topoetcone30/el_lead.tlv.Pt(), weight)
          self.h_ellead_topoetcone40.Fill(el_lead.topoetcone40/el_lead.tlv.Pt(), weight)
          self.h_ellead_ptvarcone20.Fill(el_lead.ptvarcone20/el_lead.tlv.Pt(), weight)
          self.h_ellead_ptvarcone30.Fill(el_lead.ptvarcone30/el_lead.tlv.Pt(), weight)
          self.h_ellead_ptvarcone40.Fill(el_lead.ptvarcone40/el_lead.tlv.Pt(), weight)
         
          self.h_ellead_ptcone20.Fill(el_lead.ptcone20/el_lead.tlv.Pt(), weight)
          self.h_ellead_ptcone30.Fill(el_lead.ptcone30/el_lead.tlv.Pt(), weight)
          self.h_ellead_ptcone40.Fill(el_lead.ptcone40/el_lead.tlv.Pt(), weight)
         
         
          # subleading
          """
          self.h_elsublead_pt.Fill(mu_sublead.tlv.Pt()/GeV, weight)
          self.h_elsublead_eta.Fill(mu_sublead.tlv.Eta(), weight)
          self.h_musublead_phi.Fill(mu_sublead.tlv.Phi(), weight)
          self.h_musublead_trkd0.Fill(mu_sublead.trkd0, weight)
          self.h_musublead_trkd0sig.Fill(mu_sublead.trkd0sig, weight)
          self.h_musublead_trkz0.Fill(mu_sublead.trkz0, weight)
          self.h_musublead_trkz0sintheta.Fill(mu_sublead.trkz0sintheta, weight)
          
          self.h_musublead_topoetcone20.Fill(mu_sublead.topoetcone20/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_topoetcone30.Fill(mu_sublead.topoetcone30/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_topoetcone40.Fill(mu_sublead.topoetcone40/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptvarcone20.Fill(mu_sublead.ptvarcone20/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptvarcone30.Fill(mu_sublead.ptvarcone30/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptvarcone40.Fill(mu_sublead.ptvarcone40/mu_sublead.tlv.Pt(), weight)
          
          self.h_musublead_ptcone20.Fill(mu_sublead.ptcone20/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptcone30.Fill(mu_sublead.ptcone30/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptcone40.Fill(mu_sublead.ptcone40/mu_sublead.tlv.Pt(), weight)
          """ 
              
    #__________________________________________________________________________
    def check_region(self,cutnames):
        cut_passed = True
        for cn in cutnames:
            ## could use this to fail when cuts not available
            #if not cuts.has_key(cn): return False
    
            ## pass if None
            if cn == 'ALL': continue
            #if cn.startswith("MuPairs"): continue

            if cn.startswith('!'):
                cut_passed = not self.apply_cut(cn[1:])
            else:
                cut_passed = self.apply_cut(cn) and cut_passed
            #if not cut_passed:
            #    return False
        return cut_passed
    
       
    #__________________________________________________________________________
    def check_region(self,cutnames):
        cut_passed = True
        for cn in cutnames:
            ## could use this to fail when cuts not available
            #if not cuts.has_key(cn): return False
    
            ## pass if None
            if cn == 'ALL': continue
            #if cn.startswith("MuPairs"): continue

            if cn.startswith('!'):
                cut_passed = not self.apply_cut(cn[1:])
            else:
                cut_passed = self.apply_cut(cn) and cut_passed
            #if not cut_passed:
            #    return False
        return cut_passed
    
    
#__________________________________________________________________________
def log_bins(nbins,xmin,xmax):
    xmin_log = math.log(xmin)
    xmax_log = math.log(xmax)
    log_bins = [ float(i)/float(nbins)*(xmax_log-xmin_log) + xmin_log for i in xrange(nbins+1)]
    bins = [ math.exp(x) for x in log_bins ]
    return bins

#__________________________________________________________________________
def log_bins_str(nbins,xmin,xmax):
    bins = log_bins(nbins,xmin,xmax)
    bins_str = "%d, array.array('f',%s)" % (len(bins)-1, str(bins))
    return bins_str 
 
