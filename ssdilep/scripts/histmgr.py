# encoding: utf-8
'''
histmgr.py

description:

'''

## modules
from pyplot import histutils, fileio
import os 
import random
import ROOT
import copy
import math

from array import array

import logging
log = logging.getLogger(__name__)

# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class HistMgr():
    '''
    description of HistMgr 
    '''
    #____________________________________________________________
    def __init__(self,
            basedir = None,
            target_lumi = None,
            #cutflow_histname = 'BaselineSelection/h_cut_flow',
            cutflow_histname = 'MetaData_EventCount', ### IMPORTANT: verify origin of the cutflow hist!!!
            ):
        self.basedir = basedir
        self.target_lumi = target_lumi
        self.cutflow_histname = cutflow_histname

    #____________________________________________________________
    def get_file_path(self,samplename=None,sys=None,mode=None):
        '''
        construct path to file for sample+systematic
        '''
        ## get systematics path
        syspath = 'nominal'
        if sys and not sys.flat_err:
            if mode == 'up': syspath = sys.var_up
            else:            syspath = sys.var_dn

        ## get file path
        path_to_file = ''
        path_to_file = os.path.join(self.basedir,syspath)
        filename = '%s.root' % (samplename)
        path_to_file = os.path.join(path_to_file,filename)
        return path_to_file

    #____________________________________________________________
    def hist(self, # retrieve folder with longer name
            histname   = None,
            samplename = None,
            region     = None,
            icut       = None, 
            sys        = None,
            mode       = None,
            ):

        assert histname,  'must define histname'
        assert samplename,    'must define samplename'
        if sys: 
            assert mode in ['up','dn'], "mode must be either 'up' or 'dn'"

        path_to_file = self.get_file_path(samplename,sys,mode)
        f = ROOT.TFile.Open(path_to_file)
        assert f, 'Failed to open input file!'

        ## get hist path
        path_to_hist = ''
        if region != None:
           path_to_hist = os.path.join('regions',region)
           
           ## check region exists
           if not f.Get(path_to_hist):
               f.Close()
               return None
           cutflow = get_icut_path(path_to_file, path_to_hist, icut)
           
           if icut == 0: pass #cutflow = "ALL"
           if not cutflow: 
               log.debug( '%s no cut: %s'% (samplename,icut) )
               f.Close()
               return None
           path_to_hist = os.path.join(path_to_hist,cutflow)
          
        path_to_hist = os.path.join(path_to_hist,histname)
        h = f.Get(path_to_hist)

        if not h:
            f.Close()
            print 'failed retrieveing hist: %s:%s'%(path_to_file,path_to_hist)
            return None
        
        h = h.Clone()
        h.SetDirectory(0)
        f.Close()

        ## apply flat sys (if specified)
        if sys and sys.flat_err:
            if mode == 'up': h.Scale(1.+sys.flat_err)
            else:            h.Scale(1.-sys.flat_err)

        return h
          
    #____________________________________________________________
    def get_nevents(self,samplename,sys=None,mode=None):
        '''
        retrieves cutflow hist for given sample 
        and given systematic (which contains the 
        total events before skim)
        '''
        assert samplename, 'must provide samplename'
    
        nevents = None 
        path_to_file = self.get_file_path(samplename,sys,mode)
        f = ROOT.TFile.Open(path_to_file)
        if f: 
            h = f.Get(self.cutflow_histname)
            if h: nevents = h.GetBinContent(3)
            f.Close()
        
        return nevents


#------------------------------------------------------------
class BaseEstimator(object):
    '''
    TODO: put description of estimatior functionality here
    '''
    #____________________________________________________________
    def __init__(self,hm=None,sample=None):
        self.hm = hm
        self.sample = sample
        
        ## allowed systematics 
        self.allowed_systematics = []
        self.hist_store = {}

        assert self.sample, 'must provide sample to BaseEstimator'
    
    #____________________________________________________________
    def get_hist_tag(self,histname=None,region=None,icut=None,sys=None,mode=None):
      if isinstance(region,list): region = "_".join(region)
      htag = "_".join([str(s) for s in [histname,region,icut,sys,mode]])
      return htag
        
    #____________________________________________________________
    def hist(self,histname=None,region=None,icut=None,sys=None,mode=None):
        """
        Supports list of regions to be added
        """
        if not self.is_affected_by_systematic(sys): sys=mode=None
        htag = self.get_hist_tag(histname,region,icut,sys,mode)
        if not isinstance(region,list): region = [region]
        if not self.hist_store.has_key(htag):
          h_dict = {}
          for r in region:
             h_dict[r] = self.__hist__(
                     histname=histname,
                     region=r,
                     icut=icut,
                     sys=sys,
                     mode=mode,
                     )
          h = None
          if not all(v is None for v in h_dict.values()):
            h = histutils.add_hists(h_dict.values())
          if h: 
            self.sample.plotopts.configure(h)
            log.debug('%s: %s'%(self.sample.name,h.Integral()))

          self.hist_store[htag] = h
        return self.hist_store[htag]
    
    #__________________________________________________________________________
    def add_systematics(self, sys):
        if not isinstance(sys,list): sys = [sys]
        self.allowed_systematics += sys
    
    #__________________________________________________________________________
    def is_affected_by_systematic(self, sys):
        return sys in self.allowed_systematics

    #__________________________________________________________________________
    def flush_hists(self):
        for h in self.hist_store.values():
            if h: h.Delete()
        self.hist_store = {}


#------------------------------------------------------------
class Estimator(BaseEstimator):
    '''
    Standard Estimator class (for MC and data) 
    '''
    #____________________________________________________________
    def __init__(self,**kw):
        BaseEstimator.__init__(self,**kw)

        ## xsec / Ntotal, seperately for each systematic
        ## (set on first call to hist)
        self.mc_lumi_frac = {}
   

    #____________________________________________________________
    def __hist__(self,histname=None,region=None,icut=None,sys=None,mode=None):
        """
        implemenation of nominal hist getter
        """
        h = self.hm.hist(histname=histname,
                         samplename=self.sample.name,
                         region=region,
                         icut=icut,
                         sys=sys,
                         mode=mode,
                         )
        if h and self.sample.type == 'mc': 
            lumi_frac = self.get_mc_lumi_frac(sys,mode)
            h.Scale(self.hm.target_lumi * lumi_frac)

        return h    
    #____________________________________________________________
    def get_mc_lumi_frac(self,sys,mode):
        '''
        Gets the effective luminosity fraction of the mc sample. 
        This is done seperately for each sys, since the total 
        number of events can potentially be different for different 
        sys samples. Once retrieved, the value is stored for 
        further access. 
        '''
        if sys: 
            assert mode in ['up','dn'], "mode must be either 'up' or 'dn'"
        
        sysname = 'nominal'
        if sys:
            if mode == 'up': sysname = '%s_up'%(sys.name)
            else:            sysname = '%s_dn'%(sys.name)

        if not self.mc_lumi_frac.has_key(sysname): 
            xsec    = self.sample.xsec 
            feff    = self.sample.feff
            kfactor = self.sample.kfactor
            Ntotal  = self.hm.get_nevents(self.sample.name,sys,mode)
            # there seems to be no need for feff and kfactor
            self.mc_lumi_frac[sys] = (xsec * feff * kfactor) / Ntotal if Ntotal else 0.0
            #self.mc_lumi_frac[sys] = xsec / Ntotal if Ntotal else 0.0
        return self.mc_lumi_frac[sys]


#------------------------------------------------------------
class DataBkgSubEstimator(BaseEstimator):
    '''
    DataBkgSub Estimator class 
    subtracts bkgs from data for estimate
    '''
    #____________________________________________________________
    def __init__(self,data_sample,background_samples,**kw):
        BaseEstimator.__init__(self,**kw)
        self.data_sample = data_sample
        self.background_samples = background_samples
    #____________________________________________________________
    def __hist__(self,histname=None,region=None,icut=None,sys=None,mode=None):
        h = self.data_sample.hist(histname=histname,region=region,icut=icut,sys=sys,mode=mode).Clone()
        if self.background_samples: 
            for b in self.background_samples: 
                hbkg = b.hist(histname=histname,region=region,icut=icut,sys=sys,mode=mode)
                if not hbkg: 
                  print "WARNING: For sample %s, no %s in %s for %s %s found ..." % (b.name, histname, region, sys, mode)
                  continue
                h.Add(hbkg,-1)
        return h
    
    #__________________________________________________________________________
    def is_affected_by_systematic(self, sys):
        """
        Override BaseEstimator implemenation.
        Check all daughter systematics
        """
        if sys in self.allowed_systematics: return True
        for s in self.background_samples + [self.data_sample]: 
            if s.estimator.is_affected_by_systematic(sys): return True
        return False


    #__________________________________________________________________________
    def flush_hists(self):
        BaseEstimator.flush_hists(self)
        self.data_sample.estimator.flush_hists()
        for s in self.background_samples: 
            s.estimator.flush_hists()
    
    
#------------------------------------------------------------
class FakeEstimator(BaseEstimator):
    '''
    Estimator for merging different regions
    '''
    #____________________________________________________________
    def __init__(self,data_sample,mc_samples,**kw):
        BaseEstimator.__init__(self,**kw)
        self.data_sample = data_sample
        self.mc_samples = mc_samples
    #____________________________________________________________
    def __hist__(self,histname=None,region=None,icut=None,sys=None,mode=None):
        
        # ---------
        # LL REGION
        # ---------
        region_ll_den = region.replace("-noCHF","").replace("-CR","-CR-LL")

        h_ll_den = self.data_sample.hist(histname=histname,
                                region=region_ll_den,
                                icut=icut,
                                sys=sys,
                                mode=mode,
                                ).Clone()
        for s in self.mc_samples:
          hmc_ll = s.hist(histname=histname,region=region_ll_den,icut=icut,sys=sys,mode=mode)
          if not hmc_ll: 
            print "WARNING: For sample %s, no %s in %s for %s %s found ..." % (s.name, histname, region, sys, mode)
            continue
          h_ll_den.Add(hmc_ll,-1)
        if "CR-LL" in region: return h_ll_den
        
        
        # ---------
        # TL REGION 
        # ---------
        region_tl_den = region.replace("-noCHF","").replace("-CR","-CR-TL")

        h_tl_den = self.data_sample.hist(histname=histname,
                                  region=region_tl_den,
                                  icut=icut,
                                  sys=sys,
                                  mode=mode,
                                  ).Clone()
        for s in self.mc_samples:
          hmc_tl = s.hist(histname=histname,region=region_tl_den,icut=icut,sys=sys,mode=mode)
          if not hmc_tl: 
            print "WARNING: For sample %s, no %s in %s for %s %s found ..." % (s.name, histname, region, sys, mode)
            continue
          h_tl_den.Add(hmc_tl,-1)
        if "CR-TL" in region: return h_tl_den
        
        
        # ---------
        # LT REGION 
        # ---------        
        region_lt_den = region.replace("-noCHF","").replace("-CR","-CR-LT")

        h_lt_den = self.data_sample.hist(histname=histname,
                                  region=region_lt_den,
                                  icut=icut,
                                  sys=sys,
                                  mode=mode,
                                  ).Clone()
        for s in self.mc_samples:
          hmc_lt = s.hist(histname=histname,region=region_lt_den,icut=icut,sys=sys,mode=mode)
          if not hmc_lt: 
            print "WARNING: For sample %s, no %s in %s for %s %s found ..." % (s.name, histname, region, sys, mode)
            continue
          h_lt_den.Add(hmc_lt,-1)
        if "CR-LT" in region: return h_lt_den
        
        h = h_tl_den.Clone("fakes_hist")
        h.Add(h_lt_den)
        h.Add(h_ll_den)
        
        """ 
        region_den = region.replace("_NUM","_DEN")

        h = self.data_sample.hist(histname=histname,
                                  region=region_den,
                                  icut=icut,
                                  sys=sys,
                                  mode=mode,
                                  ).Clone()
        for s in self.mc_samples:
          hmc = s.hist(histname=histname,region=region_den,icut=icut,sys=sys,mode=mode)
          h.Add(hmc,-1)
        """
        return h

    #__________________________________________________________________________
    def add_systematics(self, sys):
        if not isinstance(sys,list): sys = [sys]
        self.allowed_systematics += sys
        self.data_sample.estimator.add_systematics(sys)
        for s in self.mc_samples:
          s.estimator.add_systematics(sys)

    #__________________________________________________________________________
    def is_affected_by_systematic(self, sys):
        """
        Override BaseEstimator implemenation.
        Check all daughter systematics
        """
        if sys in self.allowed_systematics: return True
        for s in self.mc_samples + [self.data_sample]: 
            if s.estimator.is_affected_by_systematic(sys): return True
        return False

    #__________________________________________________________________________
    def flush_hists(self):
        BaseEstimator.flush_hists(self)
        self.data_sample.estimator.flush_hists()
        for s in self.mc_samples:
          s.estimator.flush_hists()


#------------------------------------------------------------
class FakeEstimator1D(BaseEstimator):
    '''
    Estimator for merging different regions
    '''
    #____________________________________________________________
    def __init__(self,data_sample,mc_samples,**kw):
        BaseEstimator.__init__(self,**kw)
        self.data_sample = data_sample
        self.mc_samples = mc_samples
    #____________________________________________________________
    def __hist__(self,histname=None,region=None,icut=None,sys=None,mode=None):
        
        # ---------
        # L REGION
        # ---------
        region_l_den = region.replace("-VR","-VR-L")

        h_l_den = self.data_sample.hist(histname=histname,
                                region=region_l_den,
                                icut=icut,
                                sys=sys,
                                mode=mode,
                                ).Clone()
        for s in self.mc_samples:
          hmc_l = s.hist(histname=histname,region=region_l_den,icut=icut,sys=sys,mode=mode)
          if not hmc_l: 
            print "WARNING: For sample %s, no %s in %s for %s %s found ..." % (s.name, histname, region, sys, mode)
            continue
          h_l_den.Add(hmc_l,-1)
        if "VR-L" in region: return h_l_den
        
        
        h = h_l_den.Clone("fakes_hist")

        return h

    #__________________________________________________________________________
    def add_systematics(self, sys):
        if not isinstance(sys,list): sys = [sys]
        self.allowed_systematics += sys
        self.data_sample.estimator.add_systematics(sys)
        for s in self.mc_samples:
          s.estimator.add_systematics(sys)

    #__________________________________________________________________________
    def is_affected_by_systematic(self, sys):
        """
        Override BaseEstimator implemenation.
        Check all daughter systematics
        """
        if sys in self.allowed_systematics: return True
        for s in self.mc_samples + [self.data_sample]: 
            if s.estimator.is_affected_by_systematic(sys): return True
        return False

    #__________________________________________________________________________
    def flush_hists(self):
        BaseEstimator.flush_hists(self)
        self.data_sample.estimator.flush_hists()
        for s in self.mc_samples:
          s.estimator.flush_hists()

#------------------------------------------------------------
class FakeEstimatorGeneral(BaseEstimator):
    '''
    Estimator for merging different regions
    '''
    #____________________________________________________________
    def __init__(self,data_sample,mc_samples,**kw):
        BaseEstimator.__init__(self,**kw)
        self.data_sample = data_sample
        self.mc_samples = mc_samples
    #____________________________________________________________
    def __hist__(self,histname=None,region=None,icut=None,sys=None,mode=None):
        
        # ---------
        # L REGION
        # ---------
        region_l_den = region.replace("-CR","-CR-fakes").replace("-VR","-VR-fakes")

        h_l_den = self.data_sample.hist(histname=histname,
                                region=region_l_den,
                                icut=icut,
                                sys=sys,
                                mode=mode,
                                ).Clone()
        for s in self.mc_samples:
          hmc_l = s.hist(histname=histname,region=region_l_den,icut=icut,sys=sys,mode=mode)
          if not hmc_l: 
            print "WARNING: For sample %s, no %s in %s for %s %s found ..." % (s.name, histname, region, sys, mode)
            continue
          h_l_den.Add(hmc_l,-1)
        if "CR-fakes" in region: 
            return h_l_den
        elif "VR-fakes" in region:
            return h_l_den
        
        
        h = h_l_den.Clone("fakes_hist")

        return h

    #__________________________________________________________________________
    def add_systematics(self, sys):
        if not isinstance(sys,list): sys = [sys]
        self.allowed_systematics += sys
        self.data_sample.estimator.add_systematics(sys)
        for s in self.mc_samples:
          s.estimator.add_systematics(sys)

    #__________________________________________________________________________
    def is_affected_by_systematic(self, sys):
        """
        Override BaseEstimator implemenation.
        Check all daughter systematics
        """
        if sys in self.allowed_systematics: return True
        for s in self.mc_samples + [self.data_sample]: 
            if s.estimator.is_affected_by_systematic(sys): return True
        return False

    #__________________________________________________________________________
    def flush_hists(self):
        BaseEstimator.flush_hists(self)
        self.data_sample.estimator.flush_hists()
        for s in self.mc_samples:
          s.estimator.flush_hists()

#------------------------------------------------------------
class ChargeFlipEsimator(BaseEstimator):
    '''
    Estimator for merging different regions
    '''
    #____________________________________________________________
    def __init__(self,data_sample,mc_samples,**kw):
        BaseEstimator.__init__(self,**kw)
        self.data_sample = data_sample
        self.mc_samples = mc_samples
    #____________________________________________________________
    def __hist__(self,histname=None,region=None,icut=None,sys=None,mode=None):
        
        # ---------
        # L REGION
        # ---------
        region_l_den = region.replace("SS","OStoSS")

        h_l_den = self.data_sample.hist(histname=histname,
                                region=region_l_den,
                                icut=icut,
                                sys=sys,
                                mode=mode,
                                ).Clone()

        if "SS" in region: 
            return h_l_den
        
        h = h_l_den.Clone("chargeFlip_hist")

        return h

    #__________________________________________________________________________
    def add_systematics(self, sys):
        if not isinstance(sys,list): sys = [sys]
        self.allowed_systematics += sys
        self.data_sample.estimator.add_systematics(sys)
        for s in self.mc_samples:
          s.estimator.add_systematics(sys)

    #__________________________________________________________________________
    def is_affected_by_systematic(self, sys):
        """
        Override BaseEstimator implemenation.
        Check all daughter systematics
        """
        if sys in self.allowed_systematics: return True
        for s in self.mc_samples + [self.data_sample]: 
            if s.estimator.is_affected_by_systematic(sys): return True
        return False

    #__________________________________________________________________________
    def flush_hists(self):
        BaseEstimator.flush_hists(self)
        self.data_sample.estimator.flush_hists()
        for s in self.mc_samples:
          s.estimator.flush_hists()


#------------------------------------------------------------
class MergeEstimator(BaseEstimator):
    '''
    Merge Estimator class 
    '''
    #____________________________________________________________
    def __init__(self,samples,**kw):
        BaseEstimator.__init__(self,**kw)
        self.samples = samples
    #____________________________________________________________
    def __hist__(self,region=None,icut=None,histname=None,sys=None,mode=None):
        hists = []
        for s in self.samples: 
            h = s.hist(region=region,icut=icut,histname=histname,sys=sys,mode=mode)
            if h: hists.append(h)
        h = histutils.add_hists(hists)
        return h

    #__________________________________________________________________________
    def add_systematics(self, sys):
        '''
        Override BaseEstimator implementation.
        Pass systematics to daughters.
        '''
        for s in self.samples: 
            s.estimator.add_systematics(sys)

    #__________________________________________________________________________
    def is_affected_by_systematic(self, sys):
        """
        Override BaseEstimator implemenation.
        Check all daughter systematics
        """
        for s in self.samples: 
            if s.estimator.is_affected_by_systematic(sys): return True
        return False

    #__________________________________________________________________________
    def flush_hists(self):
        BaseEstimator.flush_hists(self)
        for s in self.samples:
            s.estimator.flush_hists()


# - - - - - - - - - - function defs - - - - - - - - - - - - #
#____________________________________________________________
def load_base_estimator(hm,input_sample):
    '''
    Sets a standard Estimator for samples of type "mc" or "data".
    If sample has daughters, sets the MergeEstimator.
    '''
    if input_sample.estimator == None:

        if input_sample.daughters: 
             input_sample.estimator = MergeEstimator(
                     input_sample.daughters,
                     sample=input_sample,
                     hm=hm,
                     )
             print 'sample %s, assigned MergeEstimator' % (input_sample.name)
             for d in input_sample.daughters:
                 load_base_estimator(hm,d)

        else: 
             #load estimators
             if input_sample.type in ["data","mc"]: 
                 input_sample.estimator = Estimator(hm=hm,sample=input_sample)
                 print 'sample %s, assigned Estimator' % (input_sample.name)


#____________________________________________________________
def dir_name_max(filename, dirpath):
    '''
    gets the longest subdirectory in dirpath
    '''
    #f = fileio.open_file( filename )
    f = ROOT.TFile.Open( filename )
    assert f, 'failed to open file %s'%(filename)

    temp = None
    dir = f.GetDirectory(dirpath)
    if not dir:  
        log.warn( '%s doesn\'t exist in %s' % (dirpath,filename) )
    else:
        list = dir.GetListOfKeys()
        next = ROOT.TIter(list)
        d = next()
        temp = ''
        while d != None:
            if len(temp) < len(d.GetName()) and d.IsFolder():
                temp = d.GetName()
            d = next()
    f.Close()  
    return temp 


#____________________________________________________________
def dir_cuts(filename, dirpath):
    '''
    split dir name into individual cuts
    '''
    name = dir_name_max(filename,dirpath)
    return name.split('_')


#____________________________________________________________
def get_ncuts(filename, dirpath):
    cuts = dir_cuts(filename,dirpath)
    return len(cuts)

#____________________________________________________________
def get_icut(filename, dirpath,i):
    cuts = dir_cuts(filename,dirpath)
    if i>= len(cuts): 
        return None
    return cuts[i]

#____________________________________________________________
def get_icut_path(filename, dirpath,i):
    cuts = dir_cuts(filename,dirpath)
    if i >= len(cuts):
      return None
    return '_'.join(cuts[:i+1])
    

## EOF
