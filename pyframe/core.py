#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py
"""

import os
import sys
import time
import array 

# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# ROOT
import ROOT
#loader = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loader.C")
#loader = os.path.join(os.getenv("LOADERPATH"), "loader.C")
#ROOT.gROOT.ProcessLine(".L %s+" % loader)

# pyframe
import pyframe

# pyutils
import progressbar
import fileutils
import decorators

timestamp = time.strftime("%Y-%m-%d-%Hh%M")

#-----------------------------------------------------------------------------
class EventLoop(object):
    """
    The event-loop class which can have multiple algorithms.  To use an
    EventLoop, one should += algorithms to the EventLoop instance and then
    call run().

    loop = EventLoop('myloop', 'v1')
    loop += MyAlg1()
    loop += MyAlg2(config)
    loop.run(tree)
    """
    #_________________________________________________________________________
    def __init__(self, name="loop", version="test", sampletype=None, outfile=None, quiet=False):
        self.name        = name
        self.version     = version
        self.outfile     = outfile or "%s.%s.%s.hist.root" % (name, version, timestamp)
        self.quiet       = quiet if sys.stdout.isatty() else True
        self.sampletype  = sampletype
        self._algorithms = []
        self._hists      = dict() # persists for the entire event-loop
        self._store      = dict() # cleared event-by-event
        self._weight     = 1.0
        self._progress_interval  = 100
        self._n_events_processed = 0
    #_________________________________________________________________________
    def __iadd__(self, alg):
        """
        The user should use this operator to schedule Algorithms to the
        EventLoop.
        """
        alg._parent = self # set a reference to this event loop
        self._algorithms.append(alg)
        return self
    #_________________________________________________________________________
    def run(self, chain, min_entry=0, max_entry=-1, branches_on_file=None, do_var_log=False):
        """
        This is the CPU-consuming function call that runs the event-loop.
        The user can optionally specify the event range to run over.
        
        branches_on_file:
            The name of a file assumed to contain single fnmatch patterns on
            each line, for branches that should be turned-on, leaving all other
            branches turned-off.  By default no SetBranchStatus calls are made
            on the chain.

        do_var_log:
            If True, after running the event-loop, use the TreeProxy to make
            log the branch names of the variables used in the analysis.
        """
        # parse branches_on_file
        branches_on = None
        if branches_on_file:
            branches_on = []
            f = open(branches_on_file)
            for line in f:
                line = line.split("#")[0].strip() # remove comments
                if line:
                    branches_on.append(line)
            f.close()
        # setup
        tree_proxy = TreeProxy(chain)
        self.setup(tree_proxy, branches_on=branches_on)
        n_entries = chain.GetEntries()
        if max_entry < 0:
            max_entry = n_entries
        else: 
            max_entry = min(max_entry, n_entries)
        self.min_entry = min_entry
        self.max_entry = max_entry
        log.info("EventLoop.run: %s.%s" % (self.name, self.version)) # must run setup before using log
        # initialize
        self.initialize()
        # do the event-loop
        log.debug("EventLoop.run execute-loop")
        if not self.quiet:
            progbar = progressbar.ProgressBar("black", width=20, block="=", empty=" ", min=min_entry, max=max_entry)
        progress_time = time.clock()
        for i_entry in xrange(min_entry, max_entry):
            if i_entry % self._progress_interval == 0 or i_entry == max_entry-1:
                temp_progress_time = time.clock()
                if temp_progress_time-progress_time > 0.0:
                    rate = float(self._progress_interval)/(temp_progress_time-progress_time) if self._n_events_processed else 0.0
                else:
                    rate = 0.0
                if not self.quiet:
                    minutes_remaining = float(max_entry-i_entry)/float(rate)/60.0 if rate else -1.0
                    digits = len(str(max_entry))
                    progbar.update(i_entry+1, "[ %*s / %*s ] @ %.1f Hz (time remaining: %.1fm)" % (digits, i_entry+1, digits, max_entry, rate, minutes_remaining))
                progress_time = temp_progress_time
            tree_proxy.clear_cache()
            chain.GetEntry(i_entry)
            self.execute()
        # finalize
        self.finalize()
        # log variables used
        if do_var_log:
            var_log_name = "%s.%s.vars.log" % (self.name, self.version)
            tree_proxy.log_vars_read(var_log_name)

    #-------------------------------------------------------------------------
    #  The user shouldnt need to use the member functions bellow.
    #-------------------------------------------------------------------------

    #_________________________________________________________________________
    def setup(self, tree_proxy, branches_on=None):
        """
        Setup the logging module and branch statuses, and call setup on each
        alg.  Note: this must be called before using logging.
        """
        # configure logging
        logging.basicConfig(
               filename="%s.%s.%s.log" % (self.name, self.version, timestamp),
               filemode="w",
               level=logging.INFO,
               format="[%(asctime)s %(name)-16s %(levelname)-7s]  %(message)s",
               datefmt="%Y-%m-%d %H:%M:%S",
               )
        # turn-off branches for speed
        if branches_on:
            tree_proxy.set_all_branches_off()
            tree_proxy.set_branches_on(branches_on)
    
        self.setup_algs(tree_proxy)
    #_________________________________________________________________________
    def setup_algs(self, tree_proxy):
        for alg in self._algorithms:
            alg.setup(tree_proxy, self._hists, self._store, self.sampletype)
    #_________________________________________________________________________
    def initialize(self):
        log.debug("EventLoop.initialize: %s %s" % (self.name, self.version))
        # begin timers
        self._timing = {}
        self._ncalls = {}
        # initialize algs
        for alg in self._algorithms:
            _time = time.time()
            alg.initialize()
            _time = time.time()-_time
            self._timing["initialize"+alg.name] = _time
            self._ncalls["initialize"+alg.name] = 1
            log.info("initialized %s" % alg.name)
    #_________________________________________________________________________
    def finalize(self):
        log.debug("EventLoop.finalize: %s %s" % (self.name, self.version))
        # finalize algs
        for alg in self._algorithms:
            _time = time.time()
            alg.finalize()
            _time = time.time()-_time
            self._timing["finalize"+alg.name] = _time
            self._ncalls["finalize"+alg.name] = 1
            log.info("finalized %s" % alg.name)
        # time summary
        log.info("ALGORITHM TIME SUMMARY\n" + self.get_time_summary())
        # write output histograms
        #if len(self._hists) > 0:
        ## WILL: always write these - empty file tells you that you 
        ##       ran on a sample, but there were no events etc.
        self.write_hists()
    #_________________________________________________________________________
    def execute(self):
        self._weight = 1.0 # reset the event weight
        for alg in self._algorithms:
            _time = time.time()
            result = alg.execute(weight=self._weight)
            _time = time.time()-_time
            # bookkeep runtimes
            if "execute"+alg.name in self._timing:
                self._timing["execute"+alg.name] += _time
                self._ncalls["execute"+alg.name] += 1
            else:
                self._timing["execute"+alg.name] = _time
                self._ncalls["execute"+alg.name] = 1
            # treat filter
            if alg.isfilter:
                if alg.cutflow:
                    self._hists[alg.cutflow].count_if(result, alg.name, self._weight)
                if not result:
                    self._store.clear()
                    self._n_events_processed += 1
                    return False
        self._store.clear()
        self._n_events_processed += 1
        return True
    #_________________________________________________________________________
    def write_hists(self):
        log.info("Writing histograms to %s" % self.outfile)
        root_file = ROOT.TFile(self.outfile, "RECREATE")
        root_file.cd()
        for key, h in self._hists.iteritems():
            if isinstance(h, ROOT.TObject):
                fileutils.write(h, self.outfile, os.path.dirname(key))
        root_file.Close()
    #_________________________________________________________________________
    def get_time_summary(self):
        s = "\n"
        s += "%3s %-40s %8s %8s %10s %8s\n" % ("#", "ALGORITHM", "TIME [s]", "CALLS", "RATE [Hz]", "FRACTION")

        # timing per method
        for method in ["initialize", "execute", "finalize"]:
            s += " %s %s %s\n" % ("-"*25, method, "-"*(79-25-len(method)))

            # timing method summary
            # WILL: filter out non-existent timing info (eg. for 
            #       exec funcs. when input had no events)
            algs = filter(lambda alg: self._timing.has_key(method+alg.name), self._algorithms)
            timingSum = sum([self._timing[method+alg.name] for alg in algs])
            ncalls = self.max_entry - self.min_entry if method == "execute" else 1
            rate = ncalls / timingSum if timingSum else 0.0
            s += "%3s %-40s %8.2f %8i %10.1f %8.3f\n" % ("", "Sum", timingSum, ncalls, rate, 1.00)
            if not timingSum:
                continue

            # timing per alg
            for i_alg, alg in enumerate(algs):
                if method+alg.name in self._timing:
                    timing = self._timing[method+alg.name]
                    ncalls = self._ncalls[method+alg.name]
                    rate = ncalls / timing if timing else -1
                    fraction = timing / timingSum
                    s += "%3i %-40s %8.2f %8i %10.1f %8.3f\n" % (i_alg, alg.name, timing, ncalls, rate, fraction)
                else:
                    log.debug(""" %s does not have runtime statistics. Oops!""" % (alg.name) )

        return s

#-----------------------------------------------------------------------------
class Algorithm(object):
    """
    A process to execute event-by-event in an analysis.  A user should write
    classes that inherit from Algorithm, implementing the initialize(),
    finalize(), and execute() methods as needed.
    """
    #_________________________________________________________________________
    def __init__(self, name=None, isfilter=False):
        # initialized here
        self.name = name or self.__class__
        self.isfilter = isfilter

        # initialized in setup()
        self.chain      = None
        self.hists      = None
        self.store      = None
        self.sampletype = None

        # initialized in +=
        self._parent = None             
    #_________________________________________________________________________
    def initialize(self):
        """
        Override this method in your derived class as you need.
        """
        pass
    #_________________________________________________________________________
    def finalize(self):
        """
        Override this method in your derived class as you need.
        """
        pass
    #_________________________________________________________________________
    def execute(self, weight=1.0):
        """
        Override this method in your derived class as you need.
        """
        pass
    #_________________________________________________________________________
    def hist(self, name="", decl="", dir=""):
        """
        Call this function in your algorithm to book a new histogram or
        retrieve it if it already exists.
        """
        if dir:
            name = os.path.join(dir, name)

        if not self.hists.has_key(name):
            # So that the temporary objects would be
            # created in a general memory space.
            ROOT.gROOT.cd()
                            
            # create new
            if decl.count("$"):
                decl = decl.replace("$", os.path.basename(name))
            h = eval(decl)

            h.SetDirectory(0)

            # Calculate the statistical uncertainties correctly for
            # weighted histograms:
            if isinstance(h, ROOT.TH1):
                h.Sumw2()

            self.hists[name] = h

        return self.hists[name]
    #_________________________________________________________________________
    def set_weight(self, weight=1.0):
        """
        Use this function in your algorithm to set the event weight.  Note
        that this will effect the event weight for all algorithms in this
        algorithms EventLoop.
        """
        self._parent._weight = weight
        return self._parent._weight
    #_________________________________________________________________________
    def is_data(self, cache=[]):
        """
        Use this function in your algorithm to check if you are running on
        data or Monte Carlo.
        """
        if cache:
            return cache[0]
        else:
            result = not hasattr(self.chain, "mc_event_weight")
            cache.append(result)
            return result

    #-------------------------------------------------------------------------
    #  The user shouldnt need to use the member functions below.
    #-------------------------------------------------------------------------

    #_________________________________________________________________________
    def setup(self, tree_proxy, hists, store, sampletype):
        self.chain      = tree_proxy
        self.hists      = hists
        self.store      = store
        self.sampletype = sampletype

#-----------------------------------------------------------------------------
class TreeProxy(object):
    """
    An Algorithm has access to the data in a tree through a TreeProxy instance
    that every algorithm has a handle of: self.chain.  This middleman between
    the user and the tree allows TreeProxy to warn you if you try to access a
    branch that does not exist or does not have its status turned-on.
    TreeProxy also allows you to create a log file of the variables you read
    from its tree.
    """
    #_________________________________________________________________________
    def __init__(self, tree):
        self.tree = tree
        self.branches = set()
        self.branches_read = set()
        self.branches_on = set()
        # cache the branch names
        for b in tree.GetListOfBranches():
            self.branches.add( b.GetName() )
        # turn on all branches
        self.set_all_branches_on()
        self._cache = {}
    #_________________________________________________________________________
    def __getattr__(self, name):
        """
        This function is called if name is not a normal attribute, it is
        assumed to be the name of a branch in self.tree.  The branches are
        cached after being read the first time to increase performance by
        avoiding reading the tree.  clear_cache() is called at the end of every
        event in EventLoop.run().
        """
        try:
            return self._cache[name]
        except KeyError:
            if not name in self.branches_on:
                raise AttributeError("The %s branch is not turned-on." % name)
            self.branches_read.add(name)
            val = getattr(self.tree, name)
            self._cache[name] = val
            return val
    #_________________________________________________________________________
    def set_all_branches_off(self):
        self.tree.SetBranchStatus("*", 0)
        self.branches_on = set()
    #_________________________________________________________________________
    def set_all_branches_on(self):
        self.tree.SetBranchStatus("*", 1)
        self.branches_on = set(self.branches)
    #_________________________________________________________________________
    def set_branches_off(self, branches):
        for bn in branches:
            self.tree.SetBranchStatus(bn, 0)
            self.branches_on.discard(bn)
    #_________________________________________________________________________
    def set_branches_on(self, branches):
        for bn in branches:
            self.tree.SetBranchStatus(bn, 1)
            self.branches_on.add(bn)
    #_________________________________________________________________________
    def log_vars_read(self, var_log_name):
        var_log = file(var_log_name, "w")
        vars_read_list = list(self.branches_read)
        vars_read_list.sort()
        for var_name in vars_read_list:
            var_log.write(var_name + "\n")
        var_log.close()
    #_________________________________________________________________________
    def clear_cache(self):
        self._cache.clear()

#-----------------------------------------------------------------------------
class ParticleProxy(object):
    """
    This is where the money is.
    """
    #_________________________________________________________________________
    def __init__(self, tree_proxy, index, prefix=""):
        self.tree_proxy = tree_proxy
        self.index = index
        self.prefix = prefix
    #_________________________________________________________________________
    def __getattr__(self, name):
        prefix_and_name = object.__getattribute__(self, "prefix") + name
        tree_proxy =  object.__getattribute__(self, "tree_proxy")
        if prefix_and_name in tree_proxy.branches:
            index = object.__getattribute__(self, "index")
            return getattr(tree_proxy, prefix_and_name)[index]
        return object.__getattribute__(self, name)


#-----------------------------------------------------------------------------
# free functions
#-----------------------------------------------------------------------------

#_____________________________________________________________________________
def buildParticleProxies(chain, n, prefix=""):
    """
    A function that builds a list of n ParticleProxys for a TTree/TChain chain.
    The chain is assumed to have a set of branches of type array or
    std::vector<T>, each of length n, and having names with a common prefix.

    Example:

    Given a tree with the following branches

        int                 el_n;
        std::vector<float>  el_pt;       
        std::vector<float>  el_eta;
        std::vector<float>  el_phi;

    One could could build ParticleProxys for each of the electrons and treat
    them like objects by:

        electrons = pyframe.core.buildParticleProxies(tree, tree.el_n, 'el_')
        print 'el_n =', tree.el_n
        for el in electrons:
            print '  pt, eta, phi =', el.pt, el.eta, el.phi
    """
    return [ ParticleProxy(chain, i, prefix) for i in xrange(n) ]

# EOF
