# encoding: utf-8
'''
hist.py

description:

'''
__author__    = "Will Davey"
__email__     = "will.davey@cern.ch"
__created__   = "2012-11-04"
__copyright__ = "Copyright 2012 Will Davey"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"



## modules
import core
import fileio
import utils 
import histutils
from math import sqrt 

## logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)



# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class HistGen():
    '''
    description of HistGen class
    generates and manages hists
    '''
    #____________________________________________________________
    def __init__(self,do_sample_checking=True,verbose=False):
       
        ## config
        self.do_sample_checking = do_sample_checking
        self.verbose = verbose
        ## hist dict (<plot details>)
        self.hists = {}
        

    #____________________________________________________________
    def hist(self,plot_details):
        s = plot_details.sample
        log.debug( 'in hist for sample: %s'%s.name )
        if plot_details.weights: log.debug( 'weights: %s' % str(plot_details.weights.weights) )
        ## check if hist exists
        h = self.retrieve_hist(plot_details)
        if h: return h

        ## loop through daughters if parent
        if s.is_parent():
            h = plot_details.new_hist(s)
            log.debug( 's: %s, duaghters: %s'%(s.name,str([d.name for d in s.daughters])) )
            for d in s.daughters:
                dau_details = plot_details.clone_daughter(sample=d)
                log.debug( 'new details: %s' % str(dau_details) )
                log.debug( 'new weights: %s' % str(dau_details.weights) )
                if dau_details.weights: log.debug( 'new weights: %s'%str(dau_details.weights.weights))
                htemp = self.hist(dau_details)
                if htemp: h.Add(htemp) 

        
        ## process if final daughter (not parent)
        else: 
            h = __gen_hist__(plot_details,verbose=self.verbose)
            if not h: 
                log.warn('histgen failed for %s'%s.name)
   
        log.debug( 'finished hist for sample %s' %s.name)
        self.store_hist(h,plot_details)
        return h 



    #____________________________________________________________
    def cutflow(self,plot_details):
        s = plot_details.sample
        log.debug( 'in hist for sample: %s'%s.name )
        if plot_details.weights: log.debug( 'weights: %s' % str(plot_details.weights.weights) )
       
        sel = plot_details.get_selector() 
        h_cf = sel.new_cutflow_hist(s)
        #h_cf_raw = sel.new_cutflow_hist(s)
        #h_cf_raw.SetName('%s_raw'%h_cf_raw.GetName())
        h_cf_raw = h_cf.Clone('%s_raw'%h_cf.GetName())

        vd = core.VarDetails('1',core.Var('1'),_nxbins=1,_xmin=0.,_xmax=1.)
        pd = plot_details.clone(var_details=vd)

        sel_temp = core.Selector('ALL',[core.Cut('1==1')])
        pd_temp = pd.clone(selector=sel_temp)
        h_temp = self.hist(pd_temp)
        n,en = histutils.full_integral_and_error(h_temp)
        h_cf.SetBinContent(1,n)
        h_cf.SetBinError(1,en)
        #h_cf_raw.SetBinContent(1,sel_temp.entries(s))
        #h_cf_raw.SetBinError(1,sqrt(sel_temp.entries(s)))
        h_cf_raw.SetBinContent(1,h_cf.GetEntries())
        h_cf_raw.SetBinError(1,sqrt(h_cf.GetEntries()))
        del(h_temp)
        
        selection = []
        for i in xrange(len(sel.cuts)):
            selection.append(sel.cuts[i])
            sel_temp = core.Selector('cut%d'%i,selection)
            pd_temp = pd.clone(selector=sel_temp)
            h_temp = self.hist(pd_temp)
            n,en = histutils.full_integral_and_error(h_temp)
            h_cf.SetBinContent(i+2,n)
            h_cf.SetBinError(i+2,en)
            #h_cf_raw.SetBinContent(i+2,sel_temp.entries(s))
            #h_cf_raw.SetBinError(i+2,sqrt(sel_temp.entries(s)))
            h_cf_raw.SetBinContent(i+2,h_cf.GetEntries())
            h_cf_raw.SetBinError(i+2,sqrt(h_cf.GetEntries()))
            del(h_temp)
 

        
        ## check if hist exists
        #h = self.retrieve_hist(plot_details)
        #if h: return h
        # implement this in future
       
        
   
        log.debug( 'finished cutflow for sample %s' %s.name)

        #self.store_hist(h,plot_details)
        # implement this later
        return h_cf, h_cf_raw


    #____________________________________________________________
    def retrieve_hist(self,plot_details):
        if self.hists.has_key(plot_details): 
            return self.hists[plot_details]
        return None

    #____________________________________________________________
    def store_hist(self,hist,plot_details):
        if self.retrieve_hist(plot_details):
            log.debug( 'overwriting hist: %s %s' % (plot_details.sample.name,plot_details.var_details.var.name) )
        self.hists[plot_details] = hist
                                

    #____________________________________________________________
    def save_hists( self, filename, plot_details = None ):
        '''
        save hists matching keys
        if a key is not specified, all matching hists will be saved
        '''
        f = fileio.new_file(filename)
        pd = plot_details

        keys = self.hists.keys()
        keys.sort()
        for key in keys:
            h = self.hists[key]
            s = key.sample
            vd = key.var_details
            sel = key.get_selector()
            w = key.get_weights()
            if pd:
                if pd.sample and not s==pd.sample: continue
                if pd.var_details and not vd==pd.var_details: continue
                if pd.get_selector() and not sel==pd.get_selector(): continue
                if pd.get_weights() and not sel==pd.get_weights(): continue

            sel_name = sel.name if sel else 'None'
            vd_name = vd.name if vd else 'None'
            w_name = 'None'
            if key and key.weights: 
                w_name = '_'.join(sorted([w.name for w in key.weights.weights]))
            dirname = 'hists/%s/%s/%s'%(sel_name,vd_name,w_name)
            log.debug( 'dirname: %s' % dirname )
            if h: h.SetName('h_%s'%key.short_name())
            fileio.save_object(h,filename,dirname)


# - - - - - - - - - - function defs - - - - - - - - - - - - #
#____________________________________________________________
def __gen_hist__(plot_details,verbose=False):
    '''
    generate single histogram
    only runs on samples with an input file defined, 
    ie. does not loop through daughters
    not really designed to be called by analysers
    '''
    log.debug( 'in get_hist for %s' % plot_details.sample.name )

    ## add the details from the sample
    #plot_details += plot_details.sample.plot_details

    s = plot_details.sample
    vd = plot_details.var_details
    sel = plot_details.get_selector()
    weights = plot_details.get_weights()
    target_lumi = plot_details.target_lumi

    if not s.is_active(): 
        log.warn('failed to gen hist %s for sample: %s' % (vd.name,s.name) )
        return None
    
    ## create hist 
    h = plot_details.new_hist(s)
    h.samples = s
                
    ## initialise sample
    s.initialise()

    ## return empty hist if no events
    if not s.tree.GetEntries(): return h
    
    s.switch_on_branches()
    
    ## selection
    event_list = sel.select(s) if sel else None
   

    ## initialise variables 
    s.prepare( plot_details )
    
    ## process events
    entries = event_list.GetN() if sel else s.tree.GetEntries()
    for i in xrange(entries):
        ientry = event_list.GetEntry(i) if sel else i
        s.tree.GetEntry(ientry)
        
        ## calculate event weight
        weight = weights.weight() if weights else 1. 

        ## fill hists
        val = vd.var.calc_vals()[0]
        
        h.Fill(val,weight)
        frac = float(i)/float(entries) if entries else 0.0
        if verbose: utils.print_progress(frac,title = '%s: '%s.name)
    if verbose: utils.clear_progress()
    #s.style_hist(h)
    if target_lumi: s.scale_hist(h,target_lumi)
    return h






#____________________________________________________________
def __raw_events__(plot_details):
    '''
    get the number of raw events passing selection
    only runs on samples with an input file defined, 
    ie. does not loop through daughters
    not really designed to be called by analysers
    '''
    log.debug( 'in raw_events for %s' % plot_details.sample.name )

    s = plot_details.sample
    sel = plot_details.get_selector()

    if not s.is_active(): 
        log.warn('failed to get raw events for sample: %s' % (s.name) )
        return 0 

    ## initialise sample
    s.initialise()
    tree_total = s.tree.GetEntries()
    if not tree_total: return 0 
    if not sel: return tree_total 
    s.switch_on_branches()
    elist = sel.select(s)
    if not elist: return 0
    return elist.GetN() 

#____________________________________________________________
def raw_events(plot_details):
    s = plot_details.sample
    log.debug( 'in raw_events for sample: %s'%s.name )
    
    total_raw_events = 0
    ## loop through daughters if parent
    if s.is_parent():
        log.debug( 's: %s, duaghters: %s'%(s.name,str([d.name for d in s.daughters])) )
        for d in s.daughters:
            dau_details = plot_details.clone_daughter(sample=d)
            total_raw_events += raw_events(dau_details)
    
    ## process if final daughter (not parent)
    else:  
        total_raw_events += __raw_events__(plot_details)

    log.debug( 'finished raw_events for sample %s' %s.name)
    return total_raw_events 



'''
#____________________________________________________________
def gen_hist(   sample, var_details, 
                selector = None,
                weights = None,
                target_lumi = None, 
                do_sample_weights = True 
                ):
    ##generate single histogram
    ##will loop over daughters an sum together
    
    log.info( 'in get_hist for %s' % sample.name )
    
    s = sample
    vd = var_details
    sel = selector

    ## loop over daughters
    if s.is_parent():
        h = vd.new_hist(sample)
        for d in s.daughters:
            htemp = gen_hist(d,vd,sel,
                target_lumi=target_lumi,
                do_sample_weights = do_sample_weights,
                )
            if htemp: 
                h.Add(htemp) 
    
    ## process if daughter
    else:
        h = __gen_hist__(   s,vd,sel,
                            weights = weights,
                            target_lumi=target_lumi,
                            do_sample_weights=do_sample_weights
                            )       
    return h 
'''



## EOF
