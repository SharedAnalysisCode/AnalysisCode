# encoding: utf-8
'''
core.py

description:
    core module of the pyplot package
'''
__author__    = "Will Davey"
__email__     = "will.davey@cern.ch"
__created__   = "2012-10-25"
__copyright__ = "Copyright 2012 Will Davey"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"



## modules
import os
import re
import ROOT
import time
import tempfile
import shutil
from array import array
import fileio

## logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class CutBase():
    '''
    base cut class. 
    The cut class should provide an implementation of the 
    'process' method
    '''
    #____________________________________________________________
    def __init__(self,name):
        self.name = name

    #____________________________________________________________
    def process( self, tree ):
        '''
        processes TTree and returns a TEventList
        should be implemented in derived class
        '''
        pass

    #____________________________________________________________
    def __hash__(self):
        return self.name.__hash__()
    
    #____________________________________________________________
    def __eq__( self, other ):
        '''
        overload == operator
        '''
        return bool(self.__hash__() == other.__hash__())


#------------------------------------------------------------
class Cut(CutBase):
    '''
    simple implementation of CutBase using TTree::Draw 
    '''
    #____________________________________________________________
    def __init__(self,cut,name=None):
        CutBase.__init__(self,name if name else cut)
        self.cut = cut
    #____________________________________________________________
    def process(self,tree):
        passed = tree.Draw('>>elist',self.cut)
        if not passed: return ROOT.TEventList()
        el = ROOT.gDirectory.FindObject('elist')
        return el.Clone(self.name)
       
    #____________________________________________________________
    def anti(self,anti=False):
        return Cut('!(%s)'%self.cut,'Not%s'%self.name)


#------------------------------------------------------------
class VarBase():
    '''
    base var class. 
    The var class should provide an implementation of the 
    'process' method
    '''
    #____________________________________________________________
    def __init__(self,name):
        self.name = name
        self.branches = []
        self.tree = None
    #____________________________________________________________
    def init_tree(self,tree):
        '''
        default initialise function
        '''
        pass

    #____________________________________________________________
    def calc_vals(self,tree):
        '''
        default calculate values function

        this should be implemented in the derived class.
        calculates the value(s) of the variable for the current event
        '''
        pass

    
    #____________________________________________________________
    def switch_on_branches(self):
        for br in self.branches: 
            self.tree.SetBranchStatus(br,1)
   
    #____________________________________________________________
    def __hash__(self):
        return self.name.__hash__()
    
    #____________________________________________________________
    def __eq__(self,other):
        '''
        overload == operator
        '''
        return bool(self.__hash__() == other.__hash__())



#------------------------------------------------------------
class Var(VarBase):
    '''
    simple implementation of VarBase using TTreeFormula (like in TTree::Draw) 
    The var class should provide an implementation of the 
    'process' method
    '''
    #____________________________________________________________
    def __init__(self,name):
        VarBase.__init__(self,name)
        self.name = name
        self.branches = []
        self.formula = None

    #____________________________________________________________
    def init_tree(self,tree):
        '''
        derived tree initialisation
        '''
        self.tree = tree
        self.formula = ROOT.TTreeFormula(self.name,self.name,self.tree)
        self.branches = [self.formula.GetLeaf(i).GetName() for i in xrange(self.formula.GetNcodes()) ]

    #____________________________________________________________
    def calc_vals(self):
        '''
        this should be implemented in the derived class.
        calculates the value(s) of the variable for the current event
        '''
        return [ self.formula.EvalInstance(i) for i in xrange(self.formula.GetNdata()) ]

    

#------------------------------------------------------------
class Sample():
    '''
    sample details class 
    '''
    #____________________________________________________________
    def __init__(self, name = None,
            tlatex = None,
            filename = None,
            treename = None,
            xsec = None,
            is_data = False,
            plot_details = None,
            cuts_filename = None,
            skim_hist_name = None,
            skim_hist_bin = None,
            daughters = None,
            fill_color=ROOT.kBlack, 
            fill_style = 1001, 
            line_color=ROOT.kBlack,
            line_style=1,
            marker_color=ROOT.kBlack, 
            marker_style=8, 
            marker_size=1.0,
            ):

        ## configurables
        self.name = name
        self.tlatex = tlatex
        self.filename = filename
        self.treename = treename
        self.xsec = xsec
        self.is_data = is_data
        self.plot_details = plot_details
        self.cuts_filename = cuts_filename
        self.skim_hist_name = skim_hist_name
        self.skim_hist_bin = skim_hist_bin

        self.daughters = None
        if daughters:
            for d in daughters: self.add_daughter(d)
        #self.parent = None

        ## plotting style options
        self.fill_color = fill_color
        self.fill_style = fill_style
        self.line_color = line_color
        self.line_style = line_style
        self.marker_color = marker_color
        self.marker_style = marker_style
        self.marker_size = marker_size


        ## memebers 
        self.cut_event_lists = {}
        self.nevents = None

        self.is_initialised = False
        self.saved_active_branches = []

    #____________________________________________________________
    def initialise(self):
        if self.is_initialised: return True
        tree = fileio.get_object(self.treename,self.filename)
        if not tree: 
            log.error('failed to initialise sample: %s' % (self.name) )
            return False
        

        ## determine total events before skim
        if self.skim_hist_name: 
            skim_hist = fileio.get_object(self.skim_hist_name,self.filename)
            if skim_hist: 
                self.nevents = skim_hist.GetBinContent(self.skim_hist_bin)
            else: 
                log.warn('couldnt get skim hist: %s for sample: %s' % (self.skim_hist_name,self.name) )


        self.tree = tree
        self.is_initialised = True
        return True


    #____________________________________________________________
    def prepare( self, plot_details, 
                 optimise = True, 
                 ):
        '''
        preparse a sample to run on a set of variables
        '''

        assert self.initialise(), 'failed to initialise %s' % self.name

        self.switch_on_branches()
        
        ## connect variables
        var_list = []
        if plot_details.var_details: 
            var_list += [plot_details.var_details.var]
        weights = plot_details.get_weights()
        if weights: var_list += weights.weights
        self.connect_vars(var_list)

        ## optimise
        if optimise:
            self.switch_off_branches()
            for v in var_list: v.switch_on_branches()



    #____________________________________________________________
    def connect_var( self, var ):
        '''
        set a var to run on this sample
        '''
        var.init_tree(self.tree)        

    #____________________________________________________________
    def connect_vars( self, vars ):
        '''
        connect multiple vars
        '''
        for v in vars: self.connect_var(v)

    #____________________________________________________________
    def connect_weights( self ):
        '''
        connect event weights
        '''
        self.connect_vars(self.weights)
    
    #____________________________________________________________
    def apply_cut( self, cut ):
       
        ## check if eventlist exists for cut
        if self.cut_event_lists.has_key(cut.name):
            log.debug('retrieved eventlist, samp: %s, cut: %s' %
                    (self.name,cut.name) )
            return self.cut_event_lists[cut.name]
       
        ## generate new eventlist
        log.debug('generating eventlist, samp: %s, cut: %s' %
                (self.name,cut.name) )
        if not self.initialise(): return None
        elist = cut.process(self.tree)
        if not elist: 
            log.warn( 'failed to get elist, samp: %s, cut: %s' %
                    (self.name,cut.name))
        else: 
            self.cut_event_lists[cut.name] = elist
        return elist


    #____________________________________________________________
    def apply_cuts( self, cuts ):
        '''
        cuts is a list of CutBase
        '''
        event_lists = []
        #print 'applying cuts: ', [c.name for c in cuts]
        for cut in cuts:
            el = self.apply_cut(cut)
            if el: event_lists.append(el) 
            
        el_merged = event_lists_intersect(event_lists)
        return el_merged

    #____________________________________________________________
    def default_cuts_filename(self):
        '''
        default cuts filename is defined as:
          <filename dir>/.<filename base>.cuts.<root suffix>
          where:
            <filename dir> is the dir containing filename
            <filename base> and <root suffix> are the 2 
            parts of filename split when the root suffix begins

            eg. 
            path_to_dir/ntuple.root -> path_to_dir/.ntuple.cuts.root

        '''
        if not self.filename: return None
        basename = os.path.basename(self.filename)
        m = re.search('(.*)\.(root.*)',basename)
        if not m: return None
        newbasename = '.%s.cuts.%s'%(m.group(1),m.group(2))
        filedir = os.path.dirname(os.path.abspath(self.filename))
        cuts_filename = '%s/%s' % (filedir,newbasename) 
        return cuts_filename

    #____________________________________________________________
    def switch_on_branches(self):
        self.tree.SetBranchStatus('*',1)

    #____________________________________________________________
    def switch_off_branches(self):
        self.tree.SetBranchStatus('*',0)

    #____________________________________________________________
    def save_branch_status(self):
        '''
        saves a list of the current active branches
        '''
        self.saved_active_branches = []
        itr = self.tree.GetListOfBranches().MakeIterator()
        while True:
            br = itr.Next()
            if not br: break
            if self.tree.GetBranchStatus(br.GetName()): 
                self.saved_active_branches.append(br.GetName())
    #____________________________________________________________
    def load_branch_status(self):
        '''
        sets branch statuses based on the saved list
        '''
        ## if no saved list, dont do anything
        if not self.saved_active_branches:
            self.warn('no saved branch status to load') 
            return

        self.switch_off_branches()
        for br in self.saved_active_branches:
            self.tree.SetBranchStatus(br,1)

    #____________________________________________________________
    def scale(self,target_lumi = None):
        if not self.xsec: return 1.
        if not target_lumi: return 1.
 
        self.initialise()
        assert self.nevents, 'cannot scale without nevents'

        scale = target_lumi * self.xsec / float(self.nevents)
        log.debug( 'scaling %s, lumi * xsec / nevents = %.1f * %.3f / %.1f = %.2f'%(self.name,target_lumi,self.xsec,float(self.nevents),scale) )
        return scale

    #____________________________________________________________
    def scale_hist(self,h,target_lumi=None):
        if target_lumi: h.Scale(self.scale(target_lumi))

    #____________________________________________________________
    def style_hist(self,h):
        h.SetFillColor(self.fill_color)
        h.SetFillStyle(self.fill_style)
        h.SetLineColor(self.line_color)
        h.SetLineStyle(self.line_style)
        h.SetMarkerColor(self.marker_color)
        h.SetMarkerStyle(self.marker_style)
        h.SetMarkerSize(self.marker_size)
        if self.tlatex: hist_set_tlatex_name(h,self.tlatex)

    #____________________________________________________________
    def style_hist_line(self,h):
        h.SetFillColor(self.fill_color)
        h.SetFillStyle(0)
        h.SetLineColor(self.line_color)
        h.SetLineStyle(self.line_style)
        h.SetMarkerColor(self.marker_color)
        h.SetMarkerStyle(self.marker_style)
        h.SetMarkerSize(self.marker_size)
        if self.tlatex: hist_set_tlatex_name(h,self.tlatex)


    #____________________________________________________________
    def is_active(self):
        return bool(self.filename!=None and self.treename!=None)


    #____________________________________________________________
    def is_parent(self):
        return bool(self.daughters) 

    '''
    #____________________________________________________________
    def is_daughter(self):
        return bool(self.parent) 
    '''

    #____________________________________________________________
    def add_daughter(self,sample):
        if not self.daughters: self.daughters = []
        self.daughters.append( sample )
        #sample.parent = self

    #____________________________________________________________
    def set_treename(self,treename):
        if self.is_parent():
            for d in self.daughters: d.set_treename(treename)
        else:
            self.treename = treename
        
    #____________________________________________________________
    def set_property_recursive(self,prop,val):
        if self.is_parent():
            for d in self.daughters: d.set_property_recursive(prop,val)
        setattr(self,prop,val)

    #____________________________________________________________
    def get_nevents(self):
        nevents = 0
        if not self.is_parent():
            if self.nevents: nevents += self.nevents
        else: 
            for d in self.daughters: nevents += d.get_nevents()
        return nevents

    #____________________________________________________________
    def get_files(self):
        '''
        get all input files from this and daughters
        '''
        files = []
        if self.is_parent():
            for d in self.daughters: 
                files += d.get_files()
        else:
            files.append(self.filename)
        return files

    #____________________________________________________________
    def stage_files(self):
        '''
        stage all input files from this and daughters locally
        '''
        if self.is_parent():
            for d in self.daughters: 
                d.stage_files()
        else:
            if self.filename:
                basename = os.path.splitext(os.path.basename(self.filename))[0]
                tmpfile = tempfile.mktemp(suffix='.root',prefix=basename,dir='.') 
                print 'staging file: %s -> %s...'%(self.filename,tmpfile)
                shutil.copyfile(self.filename,tmpfile)
                self.filename = tmpfile

    #____________________________________________________________
    def __hash__(self):
        return self.name.__hash__()


#------------------------------------------------------------
class VarDetails(object):
    '''
    description of VarDetails class
    '''
    #____________________________________________________________
    def __init__(self, 
            _name, _var, 
            _title = None, 
            _nxbins = 100, _xmin = None, _xmax = None, 
            _xbins = None,
            _xtitle = None, _xunit  = None,
            _ytitle = None,
            _mc_var = None,
            _do_logy = False,
            _blind_max = None,
            _blind_min = None,
            ):
      
        ## config 
        self.name      = _name
        self.var       = _var
        self.title     = _title
        self.nxbins    = _nxbins 
        self.xmin      = _xmin
        self.xmax      = _xmax
        self.xbins     = _xbins
        self.xtitle    = _xtitle
        self.xunit     = _xunit
        self.ytitle    = _ytitle
        self.mc_var    = _mc_var
        self.do_logy   = _do_logy
        self.blind_max = _blind_max
        self.blind_min = _blind_min

    #____________________________________________________________
    def get_xtitle(self):
        xtitle = '%s'%self.xtitle
        if self.xunit: xtitle = '%s [%s]'%(self.xtitle, self.xunit)
        return xtitle

    #____________________________________________________________
    def get_ytitle(self):
      if self.ytitle: return self.ytitle
      if self.xbins or self.xmin == None or self.xmax == None: 
        log.debug( 'plot has custom binning, cant include bin width in yaxis title' )
        return 'Events'
      bin_width = ( self.xmax - self.xmin )/float( self.nxbins )
      bin_width_str = '%.1g'%bin_width
      if bin_width >= 10: bin_width_str = '%.3g'%bin_width
      if bin_width == 1:
        if self.xunit: return 'Events / %s'%self.xunit
        return 'Events'
      elif self.xunit:
        return 'Events / %s %s'%(bin_width_str,self.xunit)
      return 'Events / %s'%bin_width_str

    #____________________________________________________________
    def new_hist(self,sample):

        ## build name h_<var name>_<parent1>_<parent2>_..._<sample>
        hname = 'h_%s' % self.name
        hname += '_%s' % sample.name
        '''
        parent_tree = [sample]
        stemp = sample
        while stemp.is_daughter():
            stemp = stemp.parent
            parent_tree.append(stemp) 
        parent_tree.reverse()
        for s in parent_tree: hname += '_%s' % s.name
        '''

        if self.xbins:
            h = ROOT.TH1F(hname,hname,len(self.xbins)-1,array('f',self.xbins))
        else: 
            xmin = self.xmin if self.xmin != None else 9999999999.
            xmax = self.xmax if self.xmax != None else -9999999999.
            h = ROOT.TH1F(hname,hname,self.nxbins,xmin,xmax)
            if self.xmin==None or self.xmax==None: 
                h.SetBit(ROOT.TH1.kCanRebin)

        h.GetXaxis().SetTitle(self.get_xtitle())
        h.GetYaxis().SetTitle(self.get_ytitle())
        h.Sumw2()
        sample.style_hist(h)
        return h

    #____________________________________________________________
    def frame(self,pad,
            xmin = None, ymin = None, 
            xmax = None, ymax = None,
            ):
        if xmin == None: 
            if self.xbins: xmin = self.xbins[0]
            else:          xmin = self.xmin
        if xmax == None:
            if self.xbins: xmax = self.xbins[-1]
            else:          xmax = self.xmax
       
        if ymin == None: ymin = 0.
        if ymax == None: ymax = 1.

        xtitle = self.get_xtitle()
        ytitle = self.get_ytitle()

        return pad.DrawFrame(xmin,ymin,xmax,ymax,';%s;%s'%(xtitle,ytitle))


    #____________________________________________________________
    def __hash__(self):
        return self.name.__hash__()

    #____________________________________________________________
    def __eq__( self, other ):
        '''
        overload == operator
        '''
        return bool(self.__hash__() == other.__hash__())



#------------------------------------------------------------
class Selector():
    '''
    description of Selector class
    '''
    #____________________________________________________________
    def __init__(self,name,cuts = []):
        self.name = name
        self.cuts = cuts

    #____________________________________________________________
    def add(self,cut):
        self.cuts.append(cut)

    #____________________________________________________________
    def select(self,sample):
        selector = self
        if sample.plot_details: selector += sample.plot_details.selector
        log.debug( "Selector '%s' processing '%s'..."%(self.name,sample.name) )
        return sample.apply_cuts(selector.cuts)
    #____________________________________________________________
    def entries(self,sample):
        el = self.select(sample)
        return el.GetN() if el else 0
    
    #____________________________________________________________
    def new_cutflow_hist(self,s):
        hname = 'h_cutflow_%s_%s' % (self.name,s.name)
        h = ROOT.TH1F(hname,';Cut;Events',len(self.cuts)+1,0.,1.)
        xaxis = h.GetXaxis()
        xaxis.SetBinLabel(1,'ALL')
        for i in xrange(len(self.cuts)):
            xaxis.SetBinLabel(i+2,self.cuts[i].name) 
        return h

    #____________________________________________________________
    def __hash__(self):
        '''
        define hash to put in hashable lists
        '''
        scuts = set(self.cuts)
        name = ''.join(sorted([n.name for n in scuts]))
        return name.__hash__()
    
    #____________________________________________________________
    def __add__(self,other):
        cuts = []
        name = self.name
        if self.cuts: cuts += self.cuts
        if other and other.cuts:
            cuts += other.cuts
            name = other.name
        return Selector(name,cuts = cuts)

    #____________________________________________________________
    def __eq__( self, other ):
        '''
        overload == operator
        '''
        return bool(self.__hash__() == other.__hash__())


    

class Weights():
    '''
    description of Weights class
    '''
    #____________________________________________________________
    def __init__(self,weights = []):
        self.weights = weights

    #____________________________________________________________
    def get_name(self):
        name = ''
        for w in self.weights: name += '%s_'%w.name
        return name.strip('_')
    #____________________________________________________________
    def add(self,w):
        self.weights.append(w)

    #____________________________________________________________
    def weight(self):
        weight = 1.
        for w in self.weights: weight *= w.calc_vals()[0]
        """
        print 'applying weights...'
        for w in self.weights: 
            val = w.calc_vals()[0]
            print '%s: %f'%(w.name,val)
            weight *= val
        print 'weight total: ', weight
        """
        return weight

    #____________________________________________________________
    def __add__(self,other):
        '''
        overload = operator
        '''
        weights = []
        if self.weights: weights += self.weights
        if other and other.weights: 
            weights += other.weights 
        return Weights(weights)
    
    #____________________________________________________________
    def __hash__(self):
        '''
        define hash to put in hashable lists
        '''
        s = ''.join(sorted([w.name for w in self.weights]))
        return s.__hash__()

    #____________________________________________________________
    def __eq__(self,other):
        '''
        overload == operator
        '''
        return bool(self.__hash__()==other.__hash__())


#------------------------------------------------------------
class PlotDetails():
    '''
    description of PlotDetails class
    '''
    #____________________________________________________________
    def __init__(   self,
                    sample = None,
                    var_details = None,
                    selector = None,
                    weights = None,
                    target_lumi = None,
                    histgen = None,
                    tag = None,
                    ):
        self.sample      = sample
        self.var_details = var_details
        self.selector    = selector
        self.weights     = weights
        self.target_lumi = target_lumi 
        self.histgen     = histgen
        self.tag         = tag 
   
    #____________________________________________________________
    def get_tag(self):
        return self.tag if self.tag else 'NoTag'
    #____________________________________________________________
    def full_name(self):
        parts = []
        parts += [self.get_tag()]
        if self.sample:      parts += [self.sample.name]
        if self.var_details: parts += [self.var_details.name]
        if self.selector:    parts += [self.selector.name]
        if self.weights:     parts += [self.weights.get_name()]
        name = '_'.join(parts)                        
        return name
    #____________________________________________________________
    def short_name(self):
        return ''+self.sample.name

    #____________________________________________________________
    def canvas_name(self):
        parts = []
        if self.var_details: parts += [self.var_details.name]
        if self.selector:    parts += [self.selector.name]
        if self.weights:     parts += [self.weights.get_name()]
        name = '_'.join(parts)                        
        return name


    #____________________________________________________________
    def new_hist(self,sample):
       h = self.var_details.new_hist(sample)
       h.SetName('h_%s'%self.full_name())
       return h

    #____________________________________________________________
    def hist(self):
        if not self.histgen:
            log.warn('histgen not set in PlotDetails - cant call hist()' )
            return None
        return self.histgen.hist(self)

    #____________________________________________________________
    def cutflow(self):
        if not self.histgen:
            log.warn('histgen not set in PlotDetails - cant call cut_flow()' )
            return None
        return self.histgen.cutflow(self)

    #____________________________________________________________
    def get_selector(self):
        sel = self.selector
        samp_sel = None
        if self.sample and self.sample.plot_details:
            samp_sel = self.sample.plot_details.selector 
       
        if samp_sel: 
            if sel: sel += samp_sel
            else:   sel = samp_sel

        return sel
            

    #____________________________________________________________
    def get_weights(self):
        weights = self.weights
        samp_weights = self.sample.plot_details.weights if self.sample and self.sample.plot_details else None 
        if not weights and not samp_weights: return None
        if weights: return weights+samp_weights
        return samp_weights

    #____________________________________________________________
    def clone(  self,
                sample = None,
                var_details = None,
                selector = None,
                weights = None, 
                target_lumi = None,
                histgen = None,
                tag = None,
                ):
        if sample == None: sample = self.sample
        if var_details == None: var_details = self.var_details
        if selector == None: selector = self.selector
        if weights == None: weights = self.weights
        if target_lumi == None: target_lumi = self.target_lumi
        if histgen == None: histgen = self.histgen
        if tag == None: tag = self.tag
        return PlotDetails(
            sample = sample,
            var_details = var_details,
            selector = selector,
            weights = weights,
            target_lumi = target_lumi,
            histgen = histgen,
            tag = tag,
            )
  
    #____________________________________________________________
    def clone_daughter(  self,
                sample = None,
                var_details = None,
                selector = None,
                weights = None, 
                target_lumi = None,
                histgen = None,
                tag = None,
                ):
        ## merge selectors
        if selector == None: selector = self.selector
        if self.sample and self.sample.plot_details:
            if selector: 
                selector += self.sample.plot_details.selector
            else: 
                selector = self.sample.plot_details.selector
        
        ## merge weights
        if weights == None: weights = self.weights
        if self.sample and self.sample.plot_details:
            if weights: 
                weights += self.sample.plot_details.weights
            else: 
                weights = self.sample.plot_details.weights

        return self.clone(  
            sample=sample,
            var_details = var_details,
            selector = selector,
            weights = weights,
            target_lumi = target_lumi,
            histgen = histgen,
            tag = tag,
            )

    #____________________________________________________________
    def __add__(self,other):
        if not other: return self.clone()
        weights = None
        selector = None
        if isinstance(other,Selector):
            selector = self.selector + other if self.selector else other
        elif isinstance(other,Weights):
            weights = self.weights + other if self.weights else other
        elif isinstance(other,PlotDetails):
            selector = self.selector
            if other.selector: 
                if selector: selector += other.selector
                else: selector = other.selector

            weights = self.weights
            if other.weights: 
                if weights: weights += other.weights
                else: weights = other.weights
        else:
            assert False, 'cannot add type %s to PlotDetails' % (other.__classname__)
        return self.clone(selector = selector, weights = weights)


    #____________________________________________________________
    def __hash__(self):
        name = '%s%s%s%s%s%s' % (self.get_tag(),
                               self.sample.__hash__(),
                               self.var_details.__hash__(),
                               self.selector.__hash__(),
                               self.weights.__hash__(),
                               self.target_lumi,
                               )
        return name.__hash__()




# - - - - - - - - - - function defs - - - - - - - - - - - - #
#____________________________________________________________
def event_lists_intersect( event_lists ):
    '''
    description goes here
    '''
    el_new = None
    for el in event_lists: 
        if not el_new:
            el_new = el.Clone()
        else:
            el_new.Intersect(el)
    return el_new


#____________________________________________________________
def setup(
        batch_mode = True,
        ):
    logging.basicConfig(
        #filename='%s.%s.%s.log' % (self.name, self.version, time.strftime('%Y-%m-%d-%Hh%M')),
        #filename='log',
        filemode='w',
        level=logging.INFO,
        format='[%(asctime)s %(name)-16s %(levelname)-7s]  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        )
    
    fileio.timestamp = time.strftime('%Y-%m-%d-%Hh%M')

    
    ROOT.gROOT.SetBatch(batch_mode)
    ## add atlas style in pyplot to macro path
    atlas_style_dir = '%s/atlasstyle' % os.path.dirname(os.path.abspath(__file__))
    ROOT.gROOT.SetMacroPath('%s:%s'%(ROOT.gROOT.GetMacroPath(),atlas_style_dir))
    ROOT.gROOT.LoadMacro("AtlasStyle.C")
    ROOT.gROOT.LoadMacro("AtlasUtils.C")
    ROOT.gROOT.LoadMacro("AtlasLabels.C")
    ROOT.SetAtlasStyle()

    ROOT.gInterpreter.GenerateDictionary('vector<vector<float> >','vector')
    ROOT.gInterpreter.GenerateDictionary('vector<vector<int> >','vector')

    '''
    other things to setup:
        - batch mode
        - atlas style -- also make it ship with a version of atlas style
        -  
    '''

#____________________________________________________________
def hist_tlatex_name(hist):
    if hasattr(hist,'tlatex'): return hist.tlatex
    return hist.GetName()

#____________________________________________________________
def hist_set_tlatex_name(hist,name):
    hist.tlatex = name






## EOF
