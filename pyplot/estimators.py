# encoding: utf-8
'''
estimators.py

description:

'''
__author__    = "Will Davey"
__email__     = "will.davey@cern.ch"
__created__   = "2012-11-13"
__copyright__ = "Copyright 2012 Will Davey"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"



## modules
import histutils
import core
import plot

## logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class DataBkgSub(core.PlotDetails):
    '''
    description of DataBkgSub
    '''
    #____________________________________________________________
    def __init__(self,pd,data=None,bkgs=None,sigs=None):
        '''
        load in the PlotDetails for each of the samples
            pd   - pd for the sample you will estimate
            data - data for the region
            bkgs - background to be subtracted from data
            sigs - sigs to give you an estimate of contamination
        '''
        ## there must be a better way of initialising
        ## the base-class from 'samp'
        core.PlotDetails.__init__(self,
                sample = pd.sample,
                var_details = pd.var_details,
                selector = pd.selector,
                weights = pd.weights,
                target_lumi = pd.target_lumi,
                histgen = pd.histgen,
                )
        self.data = data
        self.bkgs = bkgs if bkgs else []
        self.sigs = sigs if sigs else []
        self.plot_stored = None
    #____________________________________________________________
    def hist(self):
        assert self.sample, 'in DataBkgSub: must define sample for pd'
        if self.histgen and self.histgen.retrieve_hist(self):
            return self.histgen.retrieve_hist(self)

        assert self.var_details, 'in DataBkgSub: must define var_details for pd'
        h = self.new_hist(self.sample)
        h.Add(self.data.hist())
        for bkg in self.bkgs:
            h.Add(bkg.hist(),-1.)

        if self.histgen: 
            self.histgen.store_hist(h,self)
        
        return h

    #____________________________________________________________
    def plot(self):
        self.plot_stored = plot.NewPlot(
                data = self.data,
                bkgs = self.bkgs,
                sigs = self.sigs,
                stack_sig=False,
                )
        return self.plot_stored.plot()
    
    #____________________________________________________________
    def save(self,filename,dirname=None):
        self.plot()
        self.plot_stored.save(filename,dirname)

    #____________________________________________________________
    def summary(self):
        if not self.plot_stored: 
            self.plot_stored = plot.NewPlot(
                    data = self.data,
                    bkgs = self.bkgs,
                    sigs = self.sigs,
                    stack_sig=False,
                    )
        self.plot_stored.summary()


#------------------------------------------------------------
class ABCD(core.PlotDetails):
    '''
    description of ABCD
    '''
    #____________________________________________________________
    def __init__(self,pd,estB=None,estC=None,estD=None,rCD=None):
        '''
        load in the estimators for each of the regions
            pd - pd for the sample you will estimate
            estB/C/D - estimators in control region
                - shape taken from regB
              
        '''
        ## there must be a better way of initialising
        ## the base-class from 'pd'
        core.PlotDetails.__init__(self,
                sample = pd.sample if pd else None,
                var_details = pd.var_details if pd else None,
                selector = pd.selector if pd else None,
                weights = pd.weights if pd else None,
                target_lumi = pd.target_lumi if pd else None,
                histgen = pd.histgen if pd else None,
                )

        self.estB = estB
        self.estC = estC
        self.estD = estD
        self.rCD  = rCD

    #____________________________________________________________
    def get_rCD(self):
        if self.rCD == None:
            hC = self.estC.hist()
            hD = self.estD.hist()

            self.nC, self.enC = histutils.full_integral_and_error(hC)
            self.nD, self.enD = histutils.full_integral_and_error(hD)
            self.rCD = self.nC / self.nD if self.nD else 0.
            log.debug( 'rCD: %s' % (self.rCD) )

        return self.rCD


    #____________________________________________________________
    def hist(self):
        assert self.sample, 'in DataBkgSub: must define sample for pd'
        if self.histgen and self.histgen.retrieve_hist(self):
            return self.histgen.retrieve_hist(self)

        assert self.var_details, 'in DataBkgSub: must define var_details for pd'
        h = self.new_hist(self.sample)
        hB = self.estB.hist()
        rCD = self.get_rCD()
        h.Add(hB)
        h.Scale(rCD) 
        
        if self.histgen: 
            self.histgen.store_hist(h,self)
        
        return h


    #____________________________________________________________
    def plot(self):
        plots = [ self.estB.plot() ]
        if self.estC: plots += [self.estC.plot()]
        if self.estD: plots += [self.estD.plot()]
        return plots 

    #____________________________________________________________
    def save(self,filename,dirname=None):
        if self.estB: self.estB.save(filename,dirname) 
        if self.estC: self.estC.save(filename,dirname) 
        if self.estD: self.estD.save(filename,dirname) 

    #____________________________________________________________
    def summary(self):
        self.estB.summary()
        if self.estC: self.estC.summary()
        if self.estD: self.estD.summary()



 # - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class Merger(core.PlotDetails):
    '''
    description of Merger
    '''
    #____________________________________________________________
    def __init__(self,pd,daughters):
        '''
        load in the PlotDetails for each of the samples
            pd   - pd for the sample you will estimate
            data - data for the region
            bkgs - background to be subtracted from data
            sigs - sigs to give you an estimate of contamination
        '''
        ## there must be a better way of initialising
        ## the base-class from 'samp'
        core.PlotDetails.__init__(self,
                sample = pd.sample,
                var_details = pd.var_details,
                selector = pd.selector,
                weights = pd.weights,
                target_lumi = pd.target_lumi,
                histgen = pd.histgen,
                )
        self.daughters = daughters
    #____________________________________________________________
    def hist(self):
        assert self.sample, 'in DataBkgSub: must define sample for pd'
        if self.histgen and self.histgen.retrieve_hist(self):
            return self.histgen.retrieve_hist(self)

        assert self.var_details, 'in DataBkgSub: must define var_details for pd'
        h = self.new_hist(self.sample)
        for d in self.daughters: h.Add(d.hist())

        if self.histgen: 
            self.histgen.store_hist(h,self)
        
        return h

    #____________________________________________________________
    def plot(self):
        self.plot = plot.NewPlot(
                bkgs = self.daughters,
                stack_sig=True,
                )
        return self.plot.plot()
   
    #____________________________________________________________
    def save(self,filename,dirname=None):
        self.plot()
        self.plot_stored.save(filename,dirname)



# - - - - - - - - - - function defs - - - - - - - - - - - - #
#____________________________________________________________
#def my_function():
#    '''
#    description of my_function
#    '''
#    pass






## EOF
