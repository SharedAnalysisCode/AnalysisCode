#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
met.py - For building met.
"""

import math
import os
from itertools import combinations
from copy import copy, deepcopy
from types import MethodType

import pyframe
import ROOT

GeV = 1000.0

import logging
log = logging.getLogger(__name__)

def fatal(message):
    sys.exit("Fatal error in %s: %s" % (__file__, message))

#-------------------------------------------------------------------------------
class PairVars(object):
    """
    Variables attibuted to the pair
    """
    #__________________________________________________________________________
    def __init__(self, pair, met, wdict={"InitWeight":1.0}, cdict={"InitCut":True}, **kwargs):
      self.pair = pair
      self.met  = met
      
      self.lead    = self.pair[0]
      self.sublead = self.pair[1]
      if self.lead.tlv.Pt() < self.sublead.tlv.Pt():
        self.lead    = self.pair[1]
        self.sublead = self.pair[0]
      
      # charge product 
      # ---------------------
      self.charge_product = self.lead.trkcharge * self.sublead.trkcharge 

      # visible mass
      # ---------------------
      self.m_vis = (self.lead.tlv + self.sublead.tlv).M()
      
      # total transverse mass
      # ---------------------
      leadT    = ROOT.TLorentzVector()
      subleadT = ROOT.TLorentzVector()

      leadT.SetPtEtaPhiM( self.lead.tlv.Pt(), 0., self.lead.tlv.Phi(), self.lead.tlv.M() )
      subleadT.SetPtEtaPhiM( self.sublead.tlv.Pt(), 0., self.sublead.tlv.Phi(), self.sublead.tlv.M() )
      self.mt_tot = (leadT + subleadT + self.met.tlv ).M()

      # sumCosDphi
      # ---------------------
      scdphi = 0.0
      scdphi += ROOT.TMath.Cos(self.met.tlv.Phi() - self.lead.tlv.Phi())
      scdphi += ROOT.TMath.Cos(self.met.tlv.Phi() - self.sublead.tlv.Phi())
      self.SumCosDphi = scdphi

      # Angle between two particles
      # ---------------------
      self.angle = self.lead.tlv.Angle(self.sublead.tlv.Vect())
      
      # Delta pt between two particles
      # ---------------------
      self.deltapt = abs(self.lead.tlv.Pt() - self.sublead.tlv.Pt())
      self.reldeltapt = abs(self.lead.tlv.Pt() - self.sublead.tlv.Pt()) / self.lead.tlv.Pt()

      # weights and cuts
      # ---------------------
      self.wdict   = wdict
      self.cdict   = cdict
    #__________________________________________________________________________
    def ResetCuts(self):
      self.cdict = {"InitCut":True}
      return 
    #__________________________________________________________________________
    def ResetWeights(self):
      self.wdict = {"InitWeight":1.0}
      return 
    #__________________________________________________________________________
    def HasPassedCut(self,c):
      return self.cdict[c]
    #__________________________________________________________________________
    def GetWeight(self,w):
      return self.wdict[w]
    #__________________________________________________________________________
    def HasPassedAllCuts(self):
      passed = True
      for c in self.cdict.values():
        passed = passed and c
      return passed
    #__________________________________________________________________________
    def GetTotalWeight(self):
      tot_weight = 1.0
      for w in self.wdict.values():
        tot_weight *= w
      return tot_weight 
    #__________________________________________________________________________
    def StoreWeight(self,w,v):
        self.wdict[w] = v
        return 
    #__________________________________________________________________________
    def StoreCut(self,c,v):
        self.cdict[c] = v
        return 
    #__________________________________________________________________________
    #def isMatchedToTrigChain(self,chain):
    #    if self.lead.isTrigMatched and self.sublead.isTrigMatched:
    #      if self.lead.isTrigMatchedToChain.at(0)==1 and self.lead.listTrigChains==chain:
    #        if self.sublead.isTrigMatchedToChain.at(0)==1 and self.sublead.listTrigChains==chain:
    #          return True
    #    return False

    #__________________________________________________________________________
    def isMatchedToTrigChain(self):
      return self.lead.isTrigMatched and self.sublead.isTrigMatched
    
    #https://svnweb.cern.ch/trac/atlasoff/browser/PhysicsAnalysis/MCTruthClassifier/tags/MCTruthClassifier-00-00-26/MCTruthClassifier/MCTruthClassifierDefs.h
    #__________________________________________________________________________
    def isTrueNonIsoPair(self):
      matchtype_lead = self.lead.truthType in [5,7,8]
      matchtype_sublead = self.sublead.truthType in [5,7,8]
      return self.lead.isTruthMatchedToMuon and self.sublead.isTruthMatchedToMuon and matchtype_lead and matchtype_sublead
    #__________________________________________________________________________
    def isTrueIsoPair(self):
      matchtype_lead = self.lead.truthType in [6]
      matchtype_sublead = self.sublead.truthType in [6]
      return self.lead.isTruthMatchedToMuon and self.sublead.isTruthMatchedToMuon and matchtype_lead and matchtype_sublead


class PairsBuilder(pyframe.core.Algorithm):
    """
    Creates pairs of objects in the store
    """
    #__________________________________________________________________________
    def __init__(self, name="Pairs", obj_keys=[], pair_key="", met_key=""):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.obj_keys = obj_keys
        self.pair_key = pair_key
        self.met_key  = met_key
    #__________________________________________________________________________
    def initialize(self):
        log.info('initialize pairs for %s ...' % self.pair_key)
    #__________________________________________________________________________
    def execute(self,weight):
        objects = [] 
        for k in self.obj_keys:
          objects += self.store[k] 
        met = self.store[self.met_key]
    
        self.store[self.pair_key] = [PairVars(copy(p),met) for p in combinations(objects,2)]


#-------------------------------------------------------------------------------
class Particle(pyframe.core.ParticleProxy):
    """
    Variables added to the particle
    """
    #__________________________________________________________________________
    def __init__(self, particle, wdict={"InitWeight":1.0}, cdict={"InitCut":True} , **kwargs):
        pyframe.core.ParticleProxy.__init__(self, 
             tree_proxy = particle.tree_proxy,
             index      = particle.index,
             prefix     = particle.prefix)   
        self.particle = particle
        self.wdict    = wdict
        self.cdict    = cdict
        self.__dict__ = particle.__dict__.copy() 
    
    """    
    #_________________________________________________________________________
    def __getattr__(self, name):
        prefix_and_name = object.__getattribute__(self.particle, "prefix") + name
        tree_proxy =  object.__getattribute__(self.particle, "tree_proxy")
        if prefix_and_name in tree_proxy.branches:
            index = object.__getattribute__(self.particle, "index")
            return getattr(tree_proxy, prefix_and_name)[index]
        return object.__getattribute__(self.particle, name)
    """
    #__________________________________________________________________________
    def ResetCuts(self):
      self.cdict = {"InitCut":True}
      return 
    #__________________________________________________________________________
    def ResetWeights(self):
      self.wdict = {"InitWeight":1.0}
      return 
    #__________________________________________________________________________
    def HasPassedCut(self,c):
      return self.cdict[c]
    #__________________________________________________________________________
    def GetWeight(self,w):
      return self.wdict[w]
    #__________________________________________________________________________
    def HasPassedAllCuts(self):
      passed = True
      for c in self.cdict.values():
        passed = passed and c
      return passed
    #__________________________________________________________________________
    def GetTotalWeight(self):
      tot_weight = 1.0
      for w in self.wdict.values():
        tot_weight *= w
      return tot_weight 
    #__________________________________________________________________________
    def StoreWeight(self,w,v):
        self.wdict[w] = v
        return 
    #__________________________________________________________________________
    def StoreCut(self,c,v):
        self.cdict[c] = v
        return 
    #__________________________________________________________________________
    def isMatchedToTrigChain(self):
      return self.isTrigMatched

    #https://svnweb.cern.ch/trac/atlasoff/browser/PhysicsAnalysis/MCTruthClassifier/tags/MCTruthClassifier-00-00-26/MCTruthClassifier/MCTruthClassifierDefs.h
    #__________________________________________________________________________
    def isTrueNonIsoMuon(self):
      matchtype = self.truthType in [5,7,8]
      return self.isTruthMatchedToMuon and matchtype
    #__________________________________________________________________________
    def isTrueIsoMuon(self):
      matchtype = self.truthType in [6]
      return self.isTruthMatchedToMuon and matchtype


class ParticlesBuilder(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self, name="ParticlesBuilder", key=""):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key  = key
    #__________________________________________________________________________
    def initialize(self):
        log.info('initialize single particles for %s ...' % self.key)
    #__________________________________________________________________________
    def execute(self,weight):
        self.store[self.key] = [Particle(copy(l)) for l in self.store[self.key]]

# EOF 








