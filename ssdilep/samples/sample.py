# encoding: utf-8
'''
sample.py

description:

simple sample class. 

'''

## modules
import metaroot

# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------------------------
# Sample Class
#------------------------------------------------------------------------------
class Sample(object):
    """
    basic sample class
    """
    #__________________________________________________________________________
    def __init__(self,
                 name          = '',
                 tlatex        = None,
                 xsec          = 0.0,
                 feff          = 1.0, 
                 kfactor       = 1.0,
                 files         = [],
                 type          = "mc",
                 config        = None,
                 daughters     = [],
                 estimator     = None,
                 **kw):

        ## Attach attributes.
        ## -------------------------------------------------------
        self.name          = name
        self.tlatex        = tlatex or name
        self.xsec          = xsec
        self.feff          = feff
        self.kfactor       = kfactor
        self.files         = files
        self.type          = type
        self.config        = config or {}
        self.daughters     = daughters
        self.estimator     = estimator
        ## for stylying histograms
        self.plotopts      = metaroot.hist.PlotOptions(**kw)

        ## set additional key-word args
        ## -------------------------------------------------------
        for k,w in kw.iteritems():
            setattr(self, k, w)

    #__________________________________________________________________________
    def copy(self):
        """ Return a new sample, with all the same attributes."""
        return Sample(**self.__dict__)

    #__________________________________________________________________________
    def get_active_samples(self):
        """
        get end samples (ie. that dont have daughters)
        """
        samples = []
        if self.daughters: 
            for d in self.daughters: samples += d.get_active_samples()
        else:
            samples.append(self)

        return samples

    #____________________________________________________________
    def hist(self,**kw): 
        assert self.estimator, "ERROR - sample %s missing estimator!" % self.name

        h = self.estimator.hist(**kw)
        return h





## EOF
