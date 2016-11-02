# encoding: utf-8
'''
analysers.py

description:

'''
__author__    = "Will Davey"
__email__     = "will.davey@cern.ch"
__created__   = "2012-11-04"
__copyright__ = "Copyright 2012 Will Davey"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"



## modules
import hist

## logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)



# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class SimpleAnalysis():
    '''
    description of SimpleAnalysis
    '''
    #____________________________________________________________
    def __init__(self,
        hist_gen = None,
        def_vd = None,    # default var details
        def_sel = None,   # default selector
        ):

        ## config
        self.hist_gen = hist_gen if hist_gen else hist.HistGen()
        self.def_vd = def_vd
        self.def_sel = def_sel

        ## members
        self.sig = []
        self.bkg = []
        self.data = None
    
        self.hsig = []
        self.hbkg = []
        self.hdata = None

    #____________________________________________________________
    def add_sig(self,sample,var_details=None,selector=None):
        if var_details == None: var_details = self.def_vd
        if selector == None: selector = self.def_sel
        self.sig.append([sample,var_details,selector])

    #____________________________________________________________
    def add_bkg(self,sample,var_details=None,selector=None):
        if var_details == None: var_details = self.def_vd
        if selector == None: selector = self.def_sel
        self.sig.append([sample,var_details,selector])

    #____________________________________________________________
    def set_data(self,sample,var_details=None,selector=None):
        if var_details == None: var_details = self.def_vd
        if selector == None: selector = self.def_sel
        self.data = [sample,var_details,selector]


    #____________________________________________________________
    def execute(self):
        
        ## gen sig hists
        for s in self.sig: 
            self.hsig.append(self.hist_gen.hist(s[0],s[1],s[2]))
        ## gen bkg hists
        for s in self.bkg: 
            self.hbkg.append(self.hist_gen.hist(s[0],s[1],s[2]))
        ## gen data hists
        if self.data:
            s = self.data
            self.hbkg = self.hist_gen.hist(s[0],s[1],s[2])

        
    


# - - - - - - - - - - function defs - - - - - - - - - - - - #






## EOF
