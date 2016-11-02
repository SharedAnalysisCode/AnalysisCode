#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
job.more.py

This example job demonstrates more of pyframe's tools.  Note the use
of VarProxies in HelloWorld2.

Run with a line like:
./job.more.py
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
    loop = pyframe.core.EventLoop('pyframe_hello_world', version='more')

    ### build vertices
    loop += pyframe.algs.ListBuilder(
        prefixes = ['vxp_'],
        keys = ['all_vertices'],
        )   

    ### select vertices
    vxp_selector = pyframe.vxp.VxpSelector(
        min_nTracks = 3,
        )   
    loop += pyframe.selectors.SelectorAlg('VertexSelectorAlg',
                                          selector = vxp_selector,
                                          key_in='all_vertices',
                                          key_out='selected_vertices',
                                          )   

    ### require vertices
    loop += pyframe.filters.NObjectFilter(
        keys = ['selected_vertices'],
        min_count = 1,
        name = 'VertexFilter',
        )

    ### build electrons
    loop += pyframe.algs.ListBuilder(
                prefixes = ['el_'],
                keys = ['all_electrons'],
                )
    loop += pyframe.p4calc.AttachTLVs(
                keys = ['all_electrons'],
                )

    ### select electrons
    electron_selector = pyframe.egamma.ElectronSelector(
            min_pt = 20.0*GeV,
            allowed_etas = [(-2.47, -1.52), (-1.37, 1.37), (1.52, 2.47)],
            flags = ['tightWithTrack'],
            )
    loop += pyframe.selectors.SelectorAlg(
                name = 'ElectronSelectorAlg',
                selector = electron_selector,
                key_in = 'all_electrons',
                key_out = 'selected_electrons',
                )

    ### run HelloWorld algorithm
    loop += helloworld.HelloWorld(text=ops.text)

    ### run HelloWorld2 algorithm
    loop += helloworld.HelloWorld2(key='selected_electrons')

    ### make some plots
    loop += pyframe.algs.LooperAlg(
                key = 'selected_electrons',
                func = pyframe.egamma.plot_kinematics,
                prefix = 'el_',
                dir = '',
                )

    ## run the analysis
    loop.run(chain, 0, ops.max_events)

#______________________________________________________________________________
if __name__ == '__main__': main()
