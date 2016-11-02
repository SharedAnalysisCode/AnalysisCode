#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
met.py - For building met.
"""

import math
import os
import pyframe
import ROOT

GeV = 1000.0

import logging
log = logging.getLogger(__name__)

def fatal(message):
    sys.exit("Fatal error in %s: %s" % (__file__, message))

#-------------------------------------------------------------------------------
class MET(object):
    """
    Simple MET class.
    """
    #__________________________________________________________________________
    def __init__(self, et, phi, sumet):
        self.tlv = ROOT.TLorentzVector()
        self.tlv.SetPtEtaPhiM(et, 0.0, phi, 0.0)
        self.sumet = sumet

#-------------------------------------------------------------------------------
class METCLUS(pyframe.core.Algorithm):
    """
    Load the MET directly from the mini-ntuples
    """
    #__________________________________________________________________________
    def __init__(self, name="METCLUS", key="", prefix=""):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key    = key
        self.prefix = prefix
    #__________________________________________________________________________
    def initialize(self):
        log.info('initialized METCLUS')
    #__________________________________________________________________________
    def execute(self, weight):
        self.store[self.key] = MET(getattr(self.chain, self.prefix), getattr(self.chain, self.prefix+"Phi"), getattr(self.chain, self.prefix+"SumEt"))


#-------------------------------------------------------------------------------
class METTRK(pyframe.core.Algorithm):
    """
    Load the MET directly from the mini-ntuples
    """
    #__________________________________________________________________________
    def __init__(self, name="METTRK", key="", prefix=""):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key    = key
        self.prefix = prefix
    #__________________________________________________________________________
    def initialize(self):
        log.info('initialized METTRK')
    #__________________________________________________________________________
    def execute(self, weight):
        self.store[self.key] = MET(getattr(self.chain, self.prefix), getattr(self.chain, self.prefix+"Phi"), getattr(self.chain, self.prefix+"SumEt"))




