#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
job.min.py

This is a close to minimal top-level job file for running the
helloworld algorithm in pyframe.

Run with a line like:
./job.min.py
"""

## std modules
import optparse

## ROOT
import ROOT
ROOT.gROOT.SetBatch(True)

## my modules
import pyframe

## local modules
import helloworld

GeV = 1000.0


#_____________________________________________________________________________
def options():
    parser = optparse.OptionParser(description="hello_world")
    parser.add_option('-m', '--max_events', dest='max_events', type=int, default=-1)
    parser.add_option('-c', '--text', dest='text', type=str, default='a configurable option')
    return parser.parse_args()


#_____________________________________________________________________________
def main():
    ops, args = options()

    input_files = [
            'test.root',
            ]

    ## build the chain
    chain = ROOT.TChain('tauPerf')
    for fn in input_files:
        chain.Add(fn)

    ## configure the event loop
    loop = pyframe.core.EventLoop('pyframe_hello_world', version='min')
    loop += helloworld.HelloWorld(text=ops.text)

    ## run the analysis
    loop.run(chain, 0, ops.max_events)

#______________________________________________________________________________
if __name__ == '__main__': main()
