#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import glob
import pyframe
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--channel"    , default=0  , help="Channel number for juggling similar analyses.")
parser.add_argument("--execfiles"  , default="" , help="Comma-separated list of files to be executed by config.")
parser.add_argument("--input"      , default="" , help="Comma-separated list of input ROOT files.")
parser.add_argument("--events"     , default=0  , help="Maximum number of events considered by EventLoop.")
parser.add_argument("--proc"       , default=0  , help="Number of parallel processes to run.")
parser.add_argument("--samplename" , default="" , help="Name of sample (eg Ztautau, Zee).")
parser.add_argument("--sampletype" , default="" , help="Type of sample (eg data12-Muons, mc12, AF2")
parser.add_argument("--tree"       , default="" , help="Name of tree.")
parser.add_argument("--version"    , default="" , help="Version of the job.")
parser.add_argument("--config"     , default="" , help="Set config entries by commandline 'KEY1:VAL1,KEY2:VAL2...'")
ops, unknown = parser.parse_known_args()

GeV = 1000.0

#______________________________________________________________________________
def fatal(message):
    sys.exit("Fatal error in %s: %s" % (__file__, message))
#_____________________________________________________________________________
def main(analyze):
    """
    This is the main function that drives a pyframe job.  Command line
    arguments are parsed and put in the config dictionary.  This
    function should be passed a single argument that is the user-defined
    analyze function, which takes the config dictionary as its only
    argument.  Any configuration needed to do the analysis should be put
    in the config dictionary, which should at least include:
        'input'   : a comma-separated list of the input files
        'tree'    : the name of the tree to be read from each file
        'version' : a human readable string describing the version of the job
    """
    stars = 80
    print "*"*10+" Config "+"*"*(stars-18)
    
    # config defaults
    config = {}
    config["channel"] = 0
    config["events"]  = -1
    config["input"]   = []
    config["proc"]    = 0
    config["tree"]    = "tau"
    config["version"] = ""

    # get config from the argument config files
    if ops.execfiles:
        for _file in ops.execfiles.split(","):
            print "* Executing config file: %s" % _file
            execfile(_file)

    # get config from the command-line
    if ops.events     : config["events"]     = int(ops.events)
    if ops.channel    : config["channel"]    = int(ops.channel)
    if ops.tree       : config["tree"]       = ops.tree
    if ops.version    : config["version"]    = ops.version
    if ops.proc       : config["proc"]       = int(ops.proc)
    if ops.samplename : config["samplename"] = ops.samplename
    if ops.sampletype : config["sampletype"] = ops.sampletype

    # retrieve command line config
    if ops.config: 
        pairs = ops.config.split(',')
        for pair in pairs: 
            (key,val) = pair.split(':')
            config[key] = val

    # retrieve command line input files
    if ops.input:
        inputs = ops.input.split(",")
        inputs = [input.strip() for input in inputs]
        config["input"] += inputs

    # overwrite input with globbed input
    inputs = []
    for input in config["input"]:
        if "*" in input:
            inputs += glob.glob(input)
        else:
            inputs += [input]
    config["input"] = inputs

    # count input files and announce
    ninput = len(config["input"])
    if ninput == 0:
        fatal("Found no input files.")
    print "* Configured to read %i input files." % ninput

    # add unknown args to config
    for argv in unknown:
        if argv.count("--") and argv.count("="):
            _argv = argv.lstrip("--")
            _arg, _val = _argv.split("=")
            if not _arg in config:
                print "* Adding unknown arg to config :: config['%s'] = %s" % (_arg, _val)
                config[_arg] = _val
        else:
            print "* Skipping unknown arg %s" % argv
    
    # do the work
    if config["proc"]:
        # set number of processes
        import multiprocessing
        ncpu = multiprocessing.cpu_count()
        if config["proc"] > ncpu:
            print "* You requested to use %s processors, but this machine only has %i." % (config["proc"], ncpu)
            print "*   Setting nproc = %i." % ncpu
            config["proc"] = ncpu
        nproc = config["proc"]

        # divide the input files
        ndiv = nproc
        if ninput < nproc:
            print "* You requested to divide the processing into %i jobs, but there are only %i files." % (ndiv, ninput)
            print "*   Setting nproc = ndiv = %i" % ninput
            nproc = ninput
            ndiv = ninput
        divided_input = divide_list(config["input"], ndiv)
        pool_configs = []
        for i, file_list in enumerate(divided_input):
            c = dict(config)
            c["input"] = file_list
            if c["version"]:
                c["version"] = "%s-proc%02i" % (c["version"], i)
            else:
                c["version"] =    "proc%02i" % (i)
            pool_configs.append(c)

        # parallelize on multiple cores with multiprocessing
        npool = nproc
        print "* Configured to use %i workers." % npool
        pool = multiprocessing.Pool(npool)
        results = pool.map(analyze, pool_configs)
        print "*"*stars
        return results
    else:
        print "*"*stars
        return analyze(config)
#______________________________________________________________________________
def divide_list(li, n):
    """ Yield successive n lists of even size. """
    start = 0
    for i in xrange(n):
        stop = start + len(li[i::n])
        yield li[start:stop]
        start = stop
#______________________________________________________________________________
def chunk_list(li, n):
    """ Yield successive n-sized chunks from l. """
    for i in xrange(0, len(li), n):
        yield li[i:i+n]


