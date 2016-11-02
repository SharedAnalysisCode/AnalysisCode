#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
algs.py
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
import Counter
import rootutils

GeV = 1000.0

#------------------------------------------------------------------------------
class ListMerger(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self,
            keys_in = None,
            key_out = None,
            name = 'ListMerger',
            ):
        pyframe.core.Algorithm.__init__(self, name)
        if keys_in:
            if not isinstance(keys_in, list):
                keys_in = [keys_in]
        self.keys_in = keys_in
        self.key_out = key_out
    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        out = []
        for key in self.keys_in:
            out.extend(self.store[key])
        self.store[self.key_out] = out

#------------------------------------------------------------------------------
class ListBuilder(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self, name='ListBuilder', prefixes=None, keys=None):
        pyframe.core.Algorithm.__init__(self, name)
        if not len(keys) == len(prefixes) : fatal("Need equal number of keys and prefixes in ListBuilder")
        if not isinstance(keys, list)     : fatal("Need keys to be list in ListBuilder")
        if not isinstance(prefixes, list) : fatal("Need prefixes to be list in ListBuilder")
        self.keys     = keys
        self.prefixes = prefixes
    #__________________________________________________________________________
    def execute(self, weight):
        for prefix, key in zip(self.prefixes, self.keys):
            #parts = pyframe.core.buildParticleProxies(self.chain, getattr(self.chain, prefix+'n'), prefix)
            nparts = "" 
            if "jet" in prefix: nparts = "njets"      # added!!!
            else: nparts = "n"+prefix.replace("_","") # added!!!
            parts = pyframe.core.buildParticleProxies(self.chain, getattr(self.chain, nparts), prefix) # changed!!!
            self.store[key] = parts

#------------------------------------------------------------------------------
class HistCopyAlg(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self, name='HistCopyAlg'):
        pyframe.core.Algorithm.__init__(self, name)
        pass
    #__________________________________________________________________________
    def finalize(self):
        log.info('Saving histograms from input files.')
        file_names = [ x.GetTitle() for x in self.chain.tree.GetListOfFiles() ]
        hg = metaroot.file.HistGetter(file_names)
        for dirpath, dirnames, objnames in hg.walk():
            for name in hg.ls_hists():
                hist_path = os.path.join(dirpath, name)
                log.info('  %s' % hist_path)
                self.hists[hist_path] = hg.get(hist_path)

#------------------------------------------------------------------------------
class TreeWriterAlg(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self,
            name = 'TreeWriterAlg',
            out_file_name = 'TreeWriterAlg.root',
            tree_name = None,
            branch_names_key    = None,
            branch_contents_key = None,
            branch_types_key    = None,
            do_clone            = False,
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.out_file_name = out_file_name
        self.tree_name = tree_name
        self.branch_names_key    = branch_names_key
        self.branch_contents_key = branch_contents_key
        self.branch_types_key    = branch_types_key
        self.do_clone            = do_clone
        # requirements
        assert tree_name, 'Need name for new TTree.'
        assert branch_names_key,    'Need key to find branch names in store.'
        assert branch_contents_key, 'Need key to find branch contents in store.'
        assert branch_types_key,    'Need key to find branch types in store.'
        # set in initialize
        self.out_file = None
        self.tree = None
        self._n_events = 0
        self._n_events_tree = 0
    #__________________________________________________________________________
    def initialize(self):
        # start new file and tree
        fn = self.out_file_name
        tn = self.tree_name
        self.out_file = ROOT.TFile.Open(fn, 'RECREATE')
        if self.do_clone: self.tree = self.chain.tree.CloneTree(0)
        else: self.tree = ROOT.TTree(tn, tn)
        # make persistent lists of branch info
        self.branch_names    = []
        self.branch_contents = []
        self.branch_types    = []
    #__________________________________________________________________________
    def execute(self, weight):
        """
        C++ will fuck your day up.

        TODO: Write a coherent docstring.
        """
        # fill tree if write_to_tree flag is set
        if self.store.get('write_to_tree', False):
            if self._n_events_tree == 0:
                self.initialize_branches()
            else:
                self.update_branches()
            self.tree.Fill()
            self._n_events_tree += 1
        else:
            pass
        self._n_events += 1
    #__________________________________________________________________________
    def finalize(self):
        log.info('Saving output tree.')
        # write file
        self.tree.GetCurrentFile().Write()
        # copy histgrams from memory to file
        for histpath in self.hists:
            hist = self.hists[histpath]
            if not isinstance(hist, ROOT.TH1): continue
            histdir = os.path.dirname(histpath.lstrip("/"))
            metaroot.file.write(hist, self.out_file, histdir)
        # close file, bookkeep
        self.tree.GetCurrentFile().Close()
        log.info('number of events (raw)     = %i' % self._n_events)
        log.info('number of events (written) = %i' % self._n_events_tree)
    #__________________________________________________________________________
    def initialize_branches(self):
        # retrieve branch info from the store
        branch_names        = self.store[self.branch_names_key   ]
        branch_contents_raw = self.store[self.branch_contents_key]
        branch_types        = self.store[self.branch_types_key   ]
        assert len(branch_names) > 0, 'Received no branches to write to tree.'
        assert len(branch_names) == len(branch_contents_raw) == len(branch_types), 'Please give equal numbers of branch names, contents, and types.'

        # rootify branch contents
        branch_contents = self.rootify(branch_names, branch_contents_raw, branch_types)

        # add branches and fill persistent lists
        for bn, bc, bt in zip(branch_names, branch_contents, branch_types):
            self.add_branch(bn, bc, bt)
            self.branch_names.append(bn)
            self.branch_contents.append(bc)
            self.branch_types.append(bt)
    #__________________________________________________________________________
    def add_branch(self, name, content, type):
        """
        Thanks Will!

        ftp://root.cern.ch/root/doc/19PythonRuby.pdf
        """
        # Warning, info, debug
        if not self.tree:
            log.warning('Trying to add branch %s but self.tree does not exist.' % name)
            return
        log.info('Adding branch: %s' % name)
        if self.tree.GetBranch(name):
            log.warning('Trying to add branch %s which already exists.' % name)
            return

        # ints, floats
        if type in ['I', 'F']:
            # construct TLeaf name (eg. "RunNumber/I")
            leafname = '%s/%s' % (name, type)
            self.tree.Branch(name, content, leafname)
        # vectors
        else:
            self.tree.Branch(name, content)

    #__________________________________________________________________________
    def update_branches(self):
        # get branch names and contents from store
        branch_names        = self.store[self.branch_names_key   ]
        branch_contents_raw = self.store[self.branch_contents_key]
        branch_types        = self.store[self.branch_types_key   ]
        assert len(branch_names) > 0, 'Received no branches to write to tree.'
        assert len(branch_names) == len(branch_contents_raw) == len(branch_types), 'Please give equal numbers of branch names, contents, and types.'

        # rootify branch contents
        branch_contents = self.rootify(branch_names, branch_contents_raw, branch_types)

        # requirements
        assert branch_names == self.branch_names, 'Branch names in store not equal to names in TreeWriterAlg.'
        assert branch_types == self.branch_types, 'Branch types in store not equal to types in TreeWriterAlg.'

        # update branch contents
        for i, bc in enumerate(branch_contents):
            # floats, ints
            if self.branch_types[i] in ['I', 'F']:
                self.branch_contents[i][0] = bc[0]
            # vectors
            else:
                self.branch_contents[i].clear()
                for var in bc:
                    self.branch_contents[i].push_back(var)

    #__________________________________________________________________________
    def rootify(self, names, items_raw, types):
        """
        Transform everyday python objects into tree-compatible objects. For
        vectors, this means using rootutils.rootify to transform python lists
        into ROOT vectors. For ints (floats), this means making an array.array
        of ints (floats) of unit length, filled with the int (float) of interest.
        
        Names of the objects are kept for debugging purposes.
        """
        assert len(items_raw) == len(types)
        items = []
        for name, item_raw, type in zip(names, items_raw, types):
            if type == 'I':
                items.append(array.array('i', [item_raw]))
            elif type == 'F':
                items.append(array.array('f', [item_raw]))
            else:
                items.append(rootutils.rootify(item_raw, type))
        return items

#------------------------------------------------------------------------------
#class CutFlowAlg(pyframe.core.Algorithm):
#    #__________________________________________________________________________
#    def __init__(self, name="", key="main", *args, **kw):
#        name = name or "CutFlowAlg."+key
#        pyframe.core.Algorithm.__init__(self, name)
#        self.key = key
#        self._cutflow = Counter.CutFlow()
#    #_________________________________________________________________________
#    def initialize(self):
#        # save cut flow in the hists dict so other algorithms can retrieve it
#        self.hists[self.key] = self._cutflow
#    #__________________________________________________________________________
#    def execute(self, weight):
#        pyframe.core.Algorithm.execute(self, weight)
#        self._cutflow.count("all", weight)
#    #_________________________________________________________________________
#    def finalize(self):
#        log.info("CUTFLOW: %s\n%s" % (self.key, self._cutflow))
#        h_cutflow = self._cutflow.make_hist("cutflow_weighted_" + self.key)
#        self.hists[h_cutflow.GetName()] = h_cutflow
#        h_cutflow_raw = self._cutflow.make_hist_raw("cutflow_" + self.key)
#        self.hists[h_cutflow_raw.GetName()] = h_cutflow_raw

#------------------------------------------------------------------------------
class CutFlowAlg(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self, name="", key="main", obj_keys=[], *args, **kw):
        name = name or "CutFlowAlg."+key
        pyframe.core.Algorithm.__init__(self, name)
        self.key      = key
        self._cutflow = Counter.CutFlow()
        self.obj_keys = obj_keys 
        
        if self.obj_keys:
          for k in self.obj_keys:
            setattr(self,"_objcutflow_%s"%k, Counter.CutFlow())

    #_________________________________________________________________________
    def initialize(self):
        # save cut flow in the hists dict so other algorithms can retrieve it
        self.hists[self.key] = self._cutflow
        if self.obj_keys:
          for k in self.obj_keys:
            self.hists["_".join([self.key,k])] = getattr(self,"_objcutflow_%s"%k)
    
    #__________________________________________________________________________
    def execute(self, weight, list_weights=None, list_cuts=None):
        pyframe.core.Algorithm.execute(self, weight)
        self._cutflow.count("all", weight)
        if self.obj_keys: 
          for k in self.obj_keys:
           for o in self.store[k]:
             if hasattr(o,"wdict"): 
               obj_weight = 1.0
               obj_passed = True
               if list_weights:
                 for w in list_weights:
                   obj_weight *= o.GetWeight(w)
               getattr(self,"_objcutflow_%s"%k).count("all", obj_weight * weight)

    #_________________________________________________________________________
    def finalize(self):
        log.info("CUTFLOW: %s\n%s" % (self.key, self._cutflow))
        h_cutflow = self._cutflow.make_hist("cutflow_weighted_" + self.key)
        self.hists[h_cutflow.GetName()] = h_cutflow
        h_cutflow_raw = self._cutflow.make_hist_raw("cutflow_" + self.key)
        self.hists[h_cutflow_raw.GetName()] = h_cutflow_raw

        if self.obj_keys:
          for k in self.obj_keys:
            log.info("CUTFLOW %s: %s\n%s" % (k, self.key, getattr(self,"_objcutflow_%s"%k)))
            h_objcutflow = getattr(self,"_objcutflow_%s"%k).make_hist("cutflow_weighted_%s_%s" % (self.key,k))
            self.hists[h_objcutflow.GetName()] = h_objcutflow
            h_objcutflow_raw = getattr(self,"_objcutflow_%s"%k).make_hist_raw("cutflow_%s_%s" % (self.key,k))
            self.hists[h_objcutflow_raw.GetName()] = h_objcutflow_raw


#------------------------------------------------------------------------------
class SelectorAlg(pyframe.core.Algorithm):
    """
    An algorithm for filtering a list of objects and storing the filtered list.

    NB: Requirements should be a list of strings where the object in question is
    referred to as 'part'. For example:

    requirements = ['part.tlv.Pt() > 20*GeV',
                    'abs(part.tlv.Eta()) < 2.5',
                    'part.JetBDTSigMedium == 1',
                    ]
    """
    #__________________________________________________________________________
    def __init__(self, name='', key_in='', key_out='', requirements=[]):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_in  = key_in
        self.key_out = key_out
        self.requirements = requirements
        if not self.key_in       : fatal("Need to provide input key (key_in) to %s"     % name)
        if not self.key_out      : fatal("Need to provide output key (key_out) to %s"   % name)
        if not self.requirements : fatal("Need to provide selection requirements to %s" % name)
    #__________________________________________________________________________
    def execute(self, weight):
        """
        Example in words: save selected taus as the list of preselected taus which pass all requirements.
        """
        self.store[self.key_out] = filter(lambda part: all([eval(req) for req in self.requirements]), self.store[self.key_in])

#------------------------------------------------------------------------------
class AttachTLVs(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self, keys=None, obj=None, name='AttachTLVs'):
        pyframe.core.Algorithm.__init__(self, name)
        self.keys = keys        
        self.obj  = obj
        for key in self.keys:
            if "L1" in key and ("tau" in key or "electron" in key) and not self.obj in ["EM", "tau"]:
                fatal("Need obj=EM or obj=tau when building L1_emtau TLVs.")
    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        for key in self.keys:
            vec = self.store[key]
            for p in vec:
                p.tlv = ROOT.TLorentzVector()
                if p.prefix.startswith('muon_'):
                    p.tlv.SetPtEtaPhiM(p.pt, p.eta, p.phi, p.m)
                elif p.prefix.startswith('el_'):
                    p.tlv.SetPtEtaPhiM(p.pt, p.eta, p.phi, 0.0)
                elif p.prefix.startswith('ph_'):
                    p.tlv.SetPtEtaPhiM(p.pt, p.etas2, p.phi, 0.0)
                elif p.prefix.startswith('jet_'):
                    p.tlv.SetPtEtaPhiM(p.pt, p.eta, p.phi, p.m)
                elif p.prefix.startswith('tau_'):
                    p.tlv.SetPtEtaPhiM(p.pt, p.eta, p.phi, p.m)
                #elif p.prefix.startswith('trig_EF_tau_'):
                #    p.tlv.SetPtEtaPhiM(p.pt, p.eta, p.phi, p.m)
                #elif p.prefix.startswith('trig_L2_tau_'):
                #    p.tlv.SetPtEtaPhiM(p.pt, p.eta, p.phi, 0.0)
                #elif p.prefix.startswith('trig_L1_emtau_') and self.obj == "tau":
                #    p.tlv.SetPtEtaPhiM(p.tauClus, p.eta, p.phi, 0.0)
                #elif p.prefix.startswith('trig_L1_emtau_') and self.obj == "EM":
                #    p.tlv.SetPtEtaPhiM(p.EMClus, p.eta, p.phi, 0.0)
                #elif p.prefix.startswith('trig_L1_jet_'):
                #    p.tlv.SetPtEtaPhiM(p.et8x8 if hasattr(p, "et8x8") else 1.0, p.eta, p.phi, 0.0)
                #elif p.prefix.startswith('trig_L1_mu_'):
                #    p.tlv.SetPtEtaPhiM(p.pt, p.eta, p.phi, 0.0)
                #elif p.prefix.startswith('trueTau_'):
                #    p.tlv.SetPtEtaPhiM(et_to_pt(p.vis_Et,p.vis_eta,p.vis_m), p.vis_eta, p.vis_phi, p.vis_m)
                #elif p.prefix.startswith('jet_antikt4truth_'):
                #    p.tlv.SetPtEtaPhiM(p.pt, p.eta, p.phi, p.m)
                #elif p.prefix.startswith('trk_'):
                #    p.tlv.SetPtEtaPhiM(p.pt, p.eta, p.phi, 139.6)
                else:
                    log.error('attach_tlv: unrecognized prefix = %s' % p.prefix)

#------------------------------------------------------------------------------
class PtSort(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self, keys=None, name="PtSort"):
        pyframe.core.Algorithm.__init__(self, name)
        self.keys = keys
    #__________________________________________________________________________
    def execute(self, weight):
        for key in self.keys:
            vec = self.store[key]
            vec.sort(lambda x, y: cmp(x.tlv.Pt(), y.tlv.Pt()), reverse=True) # pt sort

#------------------------------------------------------------------------------
class OverlapRemoval(pyframe.core.Algorithm):
    """
    OverlapRemoval - An alg to remove objects which overlap with other objects.

    Example in words: Make a new list called 'olr_taus' out of preselected taus
    which do not overlap with preselected muons.

    key_in = 'preselected_taus', key_out = 'olr_taus', key_olr = 'preselected_muons'
    """
    #__________________________________________________________________________
    def __init__(self, name='OverlapRemoval', key_in=None, key_out=None, key_olr=None, dr=0.2):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_in  = key_in
        self.key_out = key_out
        self.key_olr = key_olr
        self.dr      = dr
    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        self.store[self.key_out] = filter(lambda part: not any([part.tlv.DeltaR(part2.tlv) < self.dr for part2 in self.store[self.key_olr]]), self.store[self.key_in])

#------------------------------------------------------------------------------
class PyGRLFilter(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self, xml=None, cutflow=None):
        pyframe.core.Algorithm.__init__(self, name="PyGRLFilter", isfilter=True)
        self.xml     = xml
        self.cutflow = cutflow 
    #__________________________________________________________________________
    def initialize(self):
        import goodruns
        self.grl = goodruns.GRL(self.xml)
        log.info("Using GRL: %s" % self.xml)        
    #__________________________________________________________________________
    def execute(self, weight):
        if "data" in self.sampletype or "embedding" in self.sampletype:
            passed = (self.chain.RunNumber, self.chain.lbn) in self.grl
        else:
            passed = True 
        return passed

#------------------------------------------------------------------------------
class MCEventWeight(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self, cutflow=None,key=None):
        pyframe.core.Algorithm.__init__(self, name="MCEventWeight", isfilter=True)
        self.cutflow = cutflow
        self.key=key
    #_________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype:
            if self.chain.mc_channel_number in [129921, 129922, 129923,
                                                129915, 129916, 129917]: # sherpa
                mc_event_weight = self.chain.mcevt_weight[0][0]
            else:
                mc_event_weight = self.chain.mc_event_weight
            self.set_weight(mc_event_weight*weight)
            if self.key: self.store[self.key] = mc_event_weight
        else:
            pass

        return True

#______________________________________________________________________________
def fatal(message):
    sys.exit("Fatal error in %s: %s" % (__file__, message))

# EOF
