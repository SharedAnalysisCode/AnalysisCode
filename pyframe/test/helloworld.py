#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
helloworld.py
"""

## std modules

## logging
import logging
log = logging.getLogger(__name__)

## ROOT

## my modules
import pyframe

## local modules

GeV = 1000.0

#------------------------------------------------------------------------------
class HelloWorld(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self,
            text = '',
            name = 'HelloWorld',
            ):
        pyframe.core.Algorithm.__init__(self, name)
        self.text = text

    #__________________________________________________________________________
    def initialize(self):
        pyframe.core.Algorithm.initialize(self)
        log.info('config text = %s' % self.text)
        log.info('This algorithm reads data directly from the tree.')

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        ch = self.chain
        log.info('el_n = %s' % ch.el_n)
        log.info('el_pt = %s' % [ ch.el_pt[i]/GeV for i in xrange(ch.el_n) ])


#------------------------------------------------------------------------------
class HelloWorld2(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self,
            key = 'selected_electrons',
            name = 'HelloWorld2',
            ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key = key

    #__________________________________________________________________________
    def initialize(self):
        pyframe.core.Algorithm.initialize(self)
        log.info('This algorithm reads data via VarProxy instances.')

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        selected = self.store[self.key]
        n = len(selected)
        log.info('len(%s) = %s' % (self.key, n))
        log.info('tlv.Pt() = %s' % [ p.tlv.Pt() for p in selected ])
        log.info('tlv.Eta() = %s' % [ p.tlv.Eta() for p in selected ])


