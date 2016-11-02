"""
metaroot.file

Module for retrieving histograms and graphs saved to ROOT files,
and will properly add them if retrieving from several files.
Also has methods from inspecting ROOT files like getting as list
of existing histograms or directories.

Part of the metaroot package.
"""

__author__ = 'Ryan Reece'
__email__ = 'ryan.reece@cern.ch'
__created__ = '2008-05-01'
__copyright__ = 'Copyright 2008-2011 Ryan Reece'
__license__ = 'GPL http://www.gnu.org/licenses/gpl.html'

#------------------------------------------------------------------------------

import os, sys
from glob import glob
import ROOT
verbosity = 0

#______________________________________________________________________________
def write(obj, filename, dir=''):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    f = ROOT.gROOT.GetListOfFiles().FindObject(filename)
    if not f:
        f = ROOT.TFile.Open(filename, 'RECREATE')
    d = f.GetDirectory(dir)
    if not d:
        d = make_root_dir(f, dir)
    d.cd()
    if verbosity >= 1:
        print 'metaroot: writing %s:%s/%s' % (filename, dir, obj.GetName())
        sys.stdout.flush()
    obj.Write()

#______________________________________________________________________________
def make_root_dir(f, dir):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    dir.rstrip('/')
    dir_split = dir.split('/')
    lead_dir = dir_split[0]
    sub_dirs = dir_split[1:]

    d = f.GetDirectory(lead_dir)
    if not d:
        d = f.mkdir(lead_dir)
    
    if sub_dirs:
        return make_root_dir(d, '/'.join(sub_dirs))
    else:
        return d

#______________________________________________________________________________
def walk(top, topdown=True):
    """
    os.path.walk like function for TDirectories.
    Return 4-tuple: (dirpath, dirnames, filenames, top)
        dirpath = '/some/path' for some file_name.root:/some/path
        dirnames = ['list', 'of' 'TDirectory', 'keys']
        filenames = ['list', 'of' 'object', 'keys']
        top = this level's TDirectory
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    assert isinstance(top, ROOT.TDirectory)
    names = [k.GetName() for k in top.GetListOfKeys()]
    dirpath = top.GetPath()
    dirnames = []
    filenames = []
    ## filter names for directories
    for k in names:
        d = top.Get(k)
        if isinstance(d, ROOT.TDirectory):
            dirnames.append(k)
        else:
            filenames.append(k)
    ## sort
    dirnames.sort()
    filenames.sort()
    ## yield
    if topdown:
        yield dirpath, dirnames, filenames, top
    for dn in dirnames:
        d = top.Get(dn)
        for x in walk(d, topdown):
            yield x
    if not topdown:
        yield dirpath, dirnames, filenames, top

#______________________________________________________________________________
def glob_list(li):
    file_names = []
    for fn in li:
        if fn.count('*'):
            file_names.extend(glob(fn))
        else:
            file_names.append(fn)
    return file_names

#------------------------------------------------------------------------------
# HistGetter Class
#------------------------------------------------------------------------------
class HistGetter(object):
    _unique_index = 0 # static class data 
#______________________________________________________________________________
    def __init__(self, files, prefix=''):
        """
        Initializes an instance of HistGetter with some input files given
        by files.  files can be a single file or a list.
        """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if not isinstance(files, list):
            files = [files]
        self.file_names = glob_list(files) # glob paths
        self.files = [ ROOT.TFile.Open(fn, 'READ') for fn in self.file_names ]
        self.dirs = self.files
        self.prefix = prefix
#______________________________________________________________________________
    def __iadd__(self, other):
        self.files += other.files
        self.dirs = self.files
        self.prefix = self.prefix or other.prefix
#______________________________________________________________________________
    def __add__(self, other):
        hg = HistGetter()
        hg += self
        hg += other
        return hg
#______________________________________________________________________________
    def __len__(self):
        return len(self.files)
#______________________________________________________________________________
    def get(self, name):
        """
        Returns a copy of the ROOT object with name.
        """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ## for absoulte paths, dont use current directory.
        ## cd to that path, then get.
        ## WARNING: this changes the cwd
        if name.startswith('/'):
            self.cd()
            name = name[1:]
        hadd = None
        for f in self.dirs:
            f.cd()  # ROOT cd(), not metaroot cd()
            hist = f.Get(name)
            if hist:
                if not isinstance(hist, ROOT.TH1):
                    print 'ERROR: HistGetter.get(name) only supports TH1'
                    return None
                hist = self.make_copy(hist)
                if not hadd:
                    hadd = self.make_copy(hist)
                else:
                    hadd.Add(hist)
            elif verbosity > 1:
                print 'WARNING: %s not found in file: %s' % (name, f.GetName())
        if not hadd and verbosity > 1:
            print 'WARNING: %s not found in any file.' % name
        ## prepend prefix to name
        if hadd and self.prefix:
            hadd.SetName( self.prefix + hadd.GetName() )

        return hadd
#______________________________________________________________________________
    def walk(self, top='/', topdown=True):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.cd(top)
        dirpath = top
        dirnames = self.lsd()
        objnames = self.ls_objects()
        if topdown:
            yield dirpath, dirnames, objnames
        for dn in dirnames:
            for x in self.walk(os.path.join(top, dn), topdown):
                yield x
        if not topdown:
            self.cd(dirpath)
            yield dirpath, dirnames, objnames
#______________________________________________________________________________
    def ls(self):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        dir = self.dirs[0]
        if dir:
            keys = [ k.GetName() for k in dir.GetListOfKeys() ]
            keys.sort()
            return keys
        else:
            return []
#______________________________________________________________________________
    def lsd(self):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return filter( lambda key: isinstance(self.dirs[0].Get(key), ROOT.TDirectory), self.ls() )
#______________________________________________________________________________
    def ls_objects(self):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return filter( lambda key: not isinstance(self.dirs[0].Get(key), ROOT.TDirectory), self.ls() )
#______________________________________________________________________________
    def ls_hists(self):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return filter( lambda key: isinstance(self.dirs[0].Get(key), ROOT.TH1) or isinstance(self.dirs[0].Get(key), ROOT.TH2), self.ls() )
#______________________________________________________________________________
    def ls_TH1(self):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return filter( lambda key: isinstance(self.dirs[0].Get(key), ROOT.TH1) and not isinstance(self.dirs[0].Get(key), ROOT.TH2), self.ls() )
#______________________________________________________________________________
    def ls_TH2(self):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return filter( lambda key: isinstance(self.dirs[0].Get(key), ROOT.TH2), self.ls() )
#______________________________________________________________________________
    def ls_graphs(self):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return filter( lambda key: isinstance(self.dirs[0].Get(key), ROOT.TGraph)
                                or isinstance(self.dirs[0].Get(key), ROOT.TGraphErrors)
                                or isinstance(self.dirs[0].Get(key), ROOT.TGraphAsymmErrors), self.ls() )
#______________________________________________________________________________
    def cd(self, path=None):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if path:
            if path.startswith('/'):
                self.dirs = self.files
                path = path[1:]
            self.dirs = [ d.GetDirectory(path) for d in self.dirs ]
        else:
            self.dirs = self.files
#______________________________________________________________________________
    def close(self):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        for f in self.files:
            f.Close()
        self.dirs = None
        self.files = None
#______________________________________________________________________________
    def make_copy(self, obj): 
        """
        A helper function to create copy of an object
        """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        newobj = obj.__class__(obj) # bug?: doesn't have unique name
        HistGetter._unique_index += 1
        return newobj
#______________________________________________________________________________
    def get_type(self, name):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if name.startswith('/'):
            self.cd()
            name = name[1:]
        dir = self.dirs[0]
        obj = dir.Get(name)
        return type(obj)


#------------------------------------------------------------------------------
# SubSample Class
#------------------------------------------------------------------------------
class SubSample(object):
    #__________________________________________________________________________
    def __init__(self, name='', files=None,
            n_events=0.0, cross_section=0.0, int_lumi=0.0):

        ## names
        self.name = name

        ## files
        if files is None:
            files = {}
        self.files = files

        self.n_events = n_events
        self.cross_section = cross_section
        self.int_lumi = int_lumi
        self.is_data = bool(int_lumi)

        self.hist_getter = None # initialized by load()

    #__________________________________________________________________________
    def copy(self):
        x = SubSample(
                name =  self.name,
                files = dict(self.files),
                n_events = self.n_events,
                cross_section = self.cross_section,
                int_lumi = self.int_lumi,
                )
        x.is_data = self.is_data
        return x

    #__________________________________________________________________________
    def load(self, key='default'):
        self.hist_getter = HistGetter(self.files[key])

    #__________________________________________________________________________
    def initialize(self):
        if not self.n_events:
            sum_n_events = 0.0
            h = self.hist_getter.get('h_n_events')
            if h:
                sum_n_events = h.GetBinContent(1)

            sum_mc_event_weights = 0.0
            if not self.is_data:
                h = self.hist_getter.get('h_n_events_weighted')
                if h:
                    sum_mc_event_weights = h.GetBinContent(1)
                    self.n_events = sum_mc_event_weights
    
                if sum_mc_event_weights == 0.0:
                    print 'WARNING you are trying to get sum_mc_event_weights the old way'
                    h = self.hist_getter.get('h_n_events')
                    if h:
                        sum_mc_event_weights = h.GetBinContent(11)
                        self.n_events = sum_mc_event_weights

            print '  - sample %s has sum_n_events = %s, sum_mc_event_weights = %s' % (self.name, sum_n_events, sum_mc_event_weights)

        if not self.int_lumi:
            # if int_lumi not given (should be a  Monte Carlo sample, data samples
            # should have a specified integrated luminosity), calculate it from
            # the cross section.
            self.int_lumi = float(self.n_events) / self.cross_section
    #__________________________________________________________________________
    def calc_scale(self, target_lumi=1.0):
        """
        Note that calc_scale makes no reference to self.int_lumi as that
        attribute should only be used for data, which isn't scaled.
        """
        assert self.n_events and self.cross_section
        int_lumi = float(self.n_events) / self.cross_section
        return target_lumi / int_lumi
    #__________________________________________________________________________
    def get(self, name, target_lumi=None):
        # get
        h = self.hist_getter.get(name)
        if h:
            # scale
            if target_lumi:
                if self.is_data:
                    scale = target_lumi / self.int_lumi
                    if scale != 1.0:
                        print 'WARNING HistGetter.Sample.get():'
                        print '  %s is a data sample.' % self.name
                        print '  target_lumi != sample lumi. scale = %s.' % scale
                else: # monte carlo
                    if not h.GetSumw2N():
                        h.Sumw2()
                    scale = self.calc_scale( target_lumi )
                    h.Scale(scale)
        else:
            pass 
            ## some regions won't have candidates, so no histogram is ok
            # print 'WARNING HistGetter.Sample.get():'
            # print '  samples %s failed to get histogram %s.' % (self.name, name)
        return h


#------------------------------------------------------------------------------
# Sample Class
#------------------------------------------------------------------------------
class Sample(object):
    #__________________________________________________________________________
    def __init__(self,
            name='', title='', latex='',
            files=None,
            n_events=0.0, cross_section=0.0, int_lumi=0.0,
            fill_color=ROOT.kBlack, fill_style = 1001,
            line_color=ROOT.kBlack, line_width = 1,
            marker_color=ROOT.kBlack, marker_style=8, marker_size=1.0,
            **kw):

        ## names
        self.name = name
        self.title = title
        self.latex = latex

        if files:
            self.sub_samples = [ SubSample(
                                    name = name,
                                    files = files,
                                    n_events = n_events,
                                    cross_section = cross_section,
                                    int_lumi = int_lumi) ]
        else:
            self.sub_samples = []

        ## plotting style options
        self.fill_color = fill_color
        self.fill_style = fill_style
        self.line_color = line_color
        self.line_width = line_width
        self.marker_color = marker_color
        self.marker_style = marker_style
        self.marker_size = marker_size

        ## set additional key-word args
        for k,v in kw.iteritems():
            setattr(self, k, v)

    #__________________________________________________________________________
    def copy(self):
        x = Sample(
                name = self.name,
                title = self.title,
                latex = self.latex,
                fill_color   = self.fill_color,
                fill_style   = self.fill_style,
                line_color   = self.line_color,
                line_width   = self.line_width,
                marker_color = self.marker_color,
                marker_style = self.marker_style,
                marker_size  = self.marker_size,
                )
        x.sub_samples = [ ss.copy() for ss in self.sub_samples ] ## deep copy
        return x

    #__________________________________________________________________________
    def __iadd__(self, other):
        self.sub_samples.extend( other.sub_samples )
        return self

    #__________________________________________________________________________
    def __add__(self, other):
        x = Sample(
                name = self.name,
                title = self.title,
                latex = self.latex,
                files = None,
                n_events = 0.0,
                cross_section = 0.0,
                int_lumi = 0.0,
                fill_color = self.fill_color,
                fill_style = self.fill_style,
                line_color = self.line_color,
                line_width = self.line_width,
                marker_color = self.marker_color,
                marker_style = self.marker_style,
                marker_size = self.marker_size )
        x += self
        x += other
        return x
    #__________________________________________________________________________
    def load(self, key='default'):
        print '  Loading sample: %s, key: %s' % (self.name, key)
        for ss in self.sub_samples:
            ss.load(key)
    #__________________________________________________________________________
    def initialize(self):
        for ss in self.sub_samples:
            ss.initialize()
    #__________________________________________________________________________
    def calc_integrated_luminosity(self):
        return sum( [ ss.int_lumi for ss in self.sub_samples ] )
    #__________________________________________________________________________
    def get(self, name, target_lumi=None):
        # get
        histograms = [ ss.get(name, target_lumi) for ss in self.sub_samples ]

        # add
        hadd = None
        for h in histograms:
            if h:
                if not hadd:
                    hadd = h
                else:
                    hadd.Add(h)

        # prepend name
        if hadd:
            hadd.SetName( '%s__%s' % (self.name, hadd.GetName()) )

        return hadd
    #__________________________________________________________________________
    def walk(self, top='/', topdown=True):
        self.cd(top)
        dirpath = top
        dirnames = self.lsd()
        objnames = self.ls_objects()
        if topdown:
            yield dirpath, dirnames, objnames
        for dn in dirnames:
            for x in self.walk(os.path.join(top, dn), topdown):
                yield x
        if not topdown:
            self.cd(dirpath)
            yield dirpath, dirnames, objnames
    #__________________________________________________________________________
    def ls(self):
        return list(set.union(*[ set( ss.hist_getter.ls() ) for ss in self.sub_samples ]))
#        return self.sub_samples[0].hist_getter.ls()
    #__________________________________________________________________________
    def lsd(self):
        return list(set.union(*[ set( ss.hist_getter.lsd() ) for ss in self.sub_samples ]))
#        return self.sub_samples[0].hist_getter.lsd()
    #__________________________________________________________________________
    def ls_objects(self):
        return list(set.union(*[ set( ss.hist_getter.ls_objects() ) for ss in self.sub_samples ]))
#        return self.sub_samples[0].hist_getter.ls_objects()
    #__________________________________________________________________________
    def ls_hists(self):
        return list(set.union(*[ set( ss.hist_getter.ls_hists() ) for ss in self.sub_samples ]))
#        return self.sub_samples[0].hist_getter.ls_hists()
    #__________________________________________________________________________
    def ls_TH1(self):
        return list(set.union(*[ set( ss.hist_getter.ls_TH1() ) for ss in self.sub_samples ]))
#        return self.sub_samples[0].hist_getter.ls_TH1()
    #__________________________________________________________________________
    def ls_TH2(self):
        return list(set.union(*[ set( ss.hist_getter.ls_TH2() ) for ss in self.sub_samples ]))
#        return self.sub_samples[0].hist_getter.ls_TH2()
    #__________________________________________________________________________
    def ls_graphs(self):
        return list(set.union(*[ set( ss.hist_getter.ls_graphs() ) for ss in self.sub_samples ]))
#        return self.sub_samples[0].hist_getter.ls_graphs()
    #__________________________________________________________________________
    def cd(self, path=None):
        for ss in self.sub_samples:
            ss.hist_getter.cd(path)
    #__________________________________________________________________________
    def close(self):
        for ss in self.sub_samples:
            ss.hist_getter.close()

#------------------------------------------------------------------------------
# Sample Class
#------------------------------------------------------------------------------
class Sample2(object):
    """
    Sample2: A class for managing datasets.

    The class is designed to handle two types of samples.
        (1) Datasets. These are data or MC, and they have associated d3pds. Data can have a list of d3pds. MC should have one d3pd.
        (2) Pseudo-datasets. These are data or MC, and they are combinations of datasets.

    ---- Example MC dataset: ZtautauNp0
                             d3pds         : [mc12_8TeV.107670.AlpgenJimmy_AUET2CTEQ6L1_ZtautauNp0.merge.NTUP_TAU...]
                             cross_section : 711.81*1.23*1.0
                             events        : 6605586
    ---- Example MC pseudo-dataset: ZtautauNpX (ie, ZtautauNp0 '+' ... '+' ZtautauNp5)
                                    No additional attributes.
    ---- Example data dataset: data12_A
                               name     : 'data12_A' # the user can override naming
                               d3pds    : [... long list of data runs ...]
                               int_lumi : 738.196
    ---- Example data pseudo-dataset: data12_AtoE
                                      name     : 'data12_AtoE'
                                      int_lumi : 13025.8

    Data (pseudo-)datasets should have an int_lumi. MC datasets should have a cross_section. MC pseudo-datasets should have neither.
                         
    D3PD format (bracketed quantities are optional): [user/group.USER/GROUP.]ProjectTag.DSID.FullName.merge.DATATYPE.ProductionTags/

    Example: mc12_8TeV.147818.Pythia8_AU2CTEQ6L1_Ztautau.merge.NTUP_TAU.e1176_s1479_s1470_r3553_r3549_p1130/
    """
    #__________________________________________________________________________
    def __init__(self,
                 name          = '',
                 cross_section = 0.0,
                 int_lumi      = 0.0,
                 d3pds         = [],
                 events        = 0,
                 **kw):

        ## Attach attributes.
        ## -------------------------------------------------------
        self.d3pds         = d3pds
        self.cross_section = cross_section
        self.int_lumi      = int_lumi
        self.is_data       = bool(int_lumi)
        self.events        = events

        ## Set name.
        ## Do this by hand for data periods and combined MC samples.
        ## Done automatically for single data runs and single MC samples.
        ## -------------------------------------------------------
        self.nameByHand = False
        if name:
            self.nameByHand = True
            self.name = self.long_name = name
        elif self.d3pds:
            self.name, self.long_name = self.getName(d3pds[0])
        else:
            self.name = self.long_name = ''
            
        ## parse d3pd for name and dsids
        ## -------------------------------------------------------
        self.dsids = [d3pd.split('.')[1] if not d3pd.startswith('user') and not d3pd.startswith('group') else d3pd.split('.')[3] for d3pd in self.d3pds]
        if len(self.d3pds) == 1:
            self.d3pd = self.d3pds[0]
            self.dsid = self.dsids[0]

        ## Require 1 or 0 d3pds if the sample is MC.
        ## -------------------------------------------------------
        if not self.is_data:
            if len(self.d3pds) in [0, 1]:
                pass
            else:
                sys.exit("""
                ERROR:
                MC samples should not have more than 1 d3pd!
                Exiting.
                --------------------------------------
                d3pds: %s
                """ % self.d3pds)

        ## set additional key-word args
        ## -------------------------------------------------------
        for k,w in kw.iteritems():
            setattr(self, k, w)

    #__________________________________________________________________________
    def copy(self):
        """ Return a new sample, with all the same attributes."""
        return Sample(**self.__dict__)
    #__________________________________________________________________________
    def search(self, topDir, dirTags=[], fileTag='*.root*'):
        """
        Return a list of strings which look in topDir for dirs with dirTags, and then look in those for fileTag.
        Eg: search('/xrootd/', ['Zee', 'skim-v00'], 'skim.root') returns ['/xrootd/*DSID*Zee*skim-v00*/skim.root']
        """
        dirTag = ''
        for _dirTag in dirTags: dirTag+='*%s' % _dirTag
        if self.nameByHand:
            return [os.path.join(topDir, '*%s%s*' % (self.name, dirTag), fileTag)]
        else:
            return [os.path.join(topDir, '*%s%s*' % (     dsid, dirTag), fileTag) for dsid in self.dsids]
    #__________________________________________________________________________
    def load(self, files):
        """ Create a hist-getter for retrieving histograms. """
        self.hist_getter = HistGetter(files)
    #__________________________________________________________________________
    def get(self, name):
        """ Retrieve histograms via hist-getter. """
        h = self.hist_getter.get(name)
        if h:
            if not h.GetSumw2N():
                h.Sumw2()
        else:
            pass ## Some samples wont pass cuts. No histogram is okay.
        return h
    #__________________________________________________________________________
    def getName(self, d3pd):
        """ Return human-readable names from a d3pd. """
        if not d3pd: return ''
        full_name = d3pd.split('.')[2] if not d3pd.startswith('user') and not d3pd.startswith('group') else d3pd.split('.')[4]
        long_name = full_name
        # tunes
        long_name = long_name.replace('Auto'         , '')
        long_name = long_name.replace('A2CTEQ6L1'    , '')
        long_name = long_name.replace('AUET2BCTEQ6L1', '')
        long_name = long_name.replace('AUET2CTEQ6L1' , '')
        long_name = long_name.replace('AUET2CT10'    , '')
        long_name = long_name.replace('AU2CTEQ6L1'   , '')
        long_name = long_name.replace('AU2MSTW2008LO', '')
        long_name = long_name.replace('AU2'          , '')
        long_name = long_name.replace('CT10'         , '')
        # physics boundaries
        long_name = long_name.replace('_LeptonFilter', '')
        long_name = long_name.replace('_pt20'        , '')
        long_name = long_name.replace('_Mll150to250' , '_150M250')
        long_name = long_name.replace('_Mll250to400' , '_250M400')
        long_name = long_name.replace('_Mll400'      , '_M400')
        # misc
        long_name = long_name.replace('jetjet'    , '')
        long_name = long_name.replace('.merge.'   , '.')
        long_name = long_name.replace('physics_'  , '')
        long_name = long_name.replace('tautaulh'  , '')
        long_name = long_name.replace('unfiltered', '')
        long_name = long_name.replace('ATau'      , '')
        # punctuation
        long_name = long_name.replace('.', '')
        long_name = long_name.replace('_', '')
        # generator names
        short_name = long_name
        short_name = short_name.replace('AcerMC' , '')
        short_name = short_name.replace('Alpgen' , '')
        short_name = short_name.replace('Herwig' , '')
        short_name = short_name.replace('Jimmy'  , '')
        short_name = short_name.replace('JIMMY'  , '')
        short_name = short_name.replace('McAtNlo', '')
        short_name = short_name.replace('PowHeg' , '')
        short_name = short_name.replace('Powheg' , '')
        short_name = short_name.replace('Pythia8', '')
        short_name = short_name.replace('Pythia6', '')
        short_name = short_name.replace('Pythia' , '')
        short_name = short_name.replace('pythia' , '')
        # return
        return short_name, long_name
    #__________________________________________________________________________
    def walk(self, top='/', topdown=True):
        """ Walk through the directories of a hist-getter. """
        self.cd(top)
        dirpath = top
        dirnames = self.lsd()
        objnames = self.ls_objects()
        if topdown:
            yield dirpath, dirnames, objnames
        for dn in dirnames:
            for x in self.walk(os.path.join(top, dn), topdown):
                yield x
        if not topdown:
            self.cd(dirpath)
            yield dirpath, dirnames, objnames
    #__________________________________________________________________________
    def ls(self):
        return self.hist_getter.ls()
    #__________________________________________________________________________
    def lsd(self):
        return self.hist_getter.lsd()
    #__________________________________________________________________________
    def ls_objects(self):
        return self.hist_getter.ls_objects()
    #__________________________________________________________________________
    def ls_hists(self):
        return self.hist_getter.ls_hists()
    #__________________________________________________________________________
    def ls_TH1(self):
        return self.hist_getter.ls_TH1()
    #__________________________________________________________________________
    def ls_TH2(self):
        return self.hist_getter.ls_TH2()
    #__________________________________________________________________________
    def ls_graphs(self):
        return self.hist_getter.ls_graphs()
    #__________________________________________________________________________
    def cd(self, path=None):
        self.hist_getter.cd(path)
    #__________________________________________________________________________
    def close(self):
        self.hist_getter.close()

# EOF
