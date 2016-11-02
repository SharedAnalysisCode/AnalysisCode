#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
job.more_config.py

This demonstrates the utility of the config module for passing configuration
through command-line options and/or configuration files.  Note that the
main() function is actually handled by the config module.  Also, note that
one of the configuration options is to use the multiprocessing standard
module for parallelizing your job on several cores.

Run with a line like:
./job.more_config.py input.py

To use multiprocessing to run on two cores:
./job.more_config.py -p 2 input.py
"""


## ROOT
import ROOT
ROOT.gROOT.SetBatch(True)

## my modules
import pyframe

## local modules
import helloworld

GeV = 1000.0


#_____________________________________________________________________________
def analyze(config):

    ## build the chain
    chain = ROOT.TChain('tauPerf')
    for fn in config['input_files']:
        chain.Add(fn)

    ## configure the event loop
    loop = pyframe.core.EventLoop('pyframe_hello_world', version=config['version'])
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
    loop += helloworld.HelloWorld(text=config['text'])

    ### run HelloWorld2 algorithm
    loop += helloworld.HelloWorld2(key='selected_electrons')

    ### make some plots
    loop += pyframe.algs.LooperAlg(
                key = 'selected_electrons',
                func = pyframe.egamma.plot_kinematics,
                prefix = 'el_',
                dir = '',
                )

    ## run the job
    loop.run(chain, 0, config['max_events'],
            branches_on_file = config.get('branches_on_file'),
            do_var_log = config.get('do_var_log'),
            )

#______________________________________________________________________________
## Note that the actual main function is handled by the config module.
if __name__ == '__main__':
    pyframe.config.main(analyze)
