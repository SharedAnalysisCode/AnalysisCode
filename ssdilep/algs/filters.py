#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
filters.py
"""

import array
import fnmatch
import os
import sys

# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# ROOT
import ROOT
import metaroot

# pyframe
import pyframe

# pyutils

import mcutils

GeV = 1000.0


#------------------------------------------------------------------------------
class DiLepMassOverlapFilter(pyframe.core.Algorithm):
    """
    removes mass overlap (with high-mass DY samples) from low-mass samples in 
    Zee/Zmumu/Ztautau
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None):
        pyframe.core.Algorithm.__init__(self, name="DiLepMassOverlapFilter", isfilter=True)
        self.cutflow = cutflow 
    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype:
            mc_channel_number = self.chain.mc_channel_number
            if mcutils.isztautau_pythia(mc_channel_number):
                resomass = self.chain.RESOMASS
                return resomass < 180.0*GeV
            if mcutils.iszleplep_powheg(mc_channel_number):
                resomass = self.chain.RESOMASS
                return resomass < 120.0*GeV 
        return True


#------------------------------------------------------------------------------
class SherpaWJetBoostOverlapFilter(pyframe.core.Algorithm):
    """
    removes overlap of inclusive W+jets sherpa sample with high-boosted phase
    space of samples binned in W boost.  
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None):
        pyframe.core.Algorithm.__init__(self, name="DiLepMassOverlapFilter", isfilter=True)
        self.cutflow = cutflow 
    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype:
            mc_channel_number = self.chain.mc_channel_number
            if mcutils.iswjets_sherpa_inclusive(mc_channel_number):
                boson_pt = self.chain.sherpa_boson_pt
                return boson_pt < 70.0*GeV
        return True












# EOF
