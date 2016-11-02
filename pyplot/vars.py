# encoding: utf-8
'''
vars.py

description:

'''
__author__    = "Will Davey"
__email__     = "will.davey@cern.ch"
__created__   = "2012-11-14"
__copyright__ = "Copyright 2012 Will Davey"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"



## modules
import ROOT
from core import VarBase
from math import sqrt

# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class FakeFactorCplusplus(VarBase):
    '''
    simple implementation of VarBase using TTreeFormula (like in TTree::Draw) 
    The var class should provide an implementation of the 
    'process' method
    '''
    #____________________________________________________________
    def __init__(self,name,config_file,
            tau_pt = None,
            tau_numTrack = None,
            chargeP = None,
            uncertainty = 0.30,
            scale = None,
            ):
        VarBase.__init__(self,name)
        self.name = name
        self.tau_pt = tau_pt
        self.tau_numTrack = tau_numTrack
        self.chargeP = chargeP
        self.uncertainty = uncertainty
        self.scale = scale

        self.formula_tau_pt = None
        self.formula_tau_numTrack = None
        self.branches = []
        
        ROOT.gSystem.Load('libFakeWeightTool')
        self.ff_scaler = ROOT.FakeFactorScaler()
        self.ff_scaler.readGraphsFromFile(config_file)

        if chargeP: 
            assert chargeP in ['OS','SS'], "Invalid chargeP, use either 'OS' or 'SS'"

    #____________________________________________________________
    def init_tree(self,tree):
        '''
        derived tree initialisation
        '''
        self.tree = tree
        self.formula_tau_pt = ROOT.TTreeFormula(self.tau_pt,self.tau_pt,self.tree)
        self.formula_tau_numTrack = ROOT.TTreeFormula(self.tau_numTrack,self.tau_numTrack,self.tree)

        self.branches = []
        self.branches += [self.formula_tau_pt.GetLeaf(i).GetName() for i in xrange(self.formula_tau_pt.GetNcodes()) ]
        self.branches += [self.formula_tau_numTrack.GetLeaf(i).GetName() for i in xrange(self.formula_tau_numTrack.GetNcodes()) ]

    #____________________________________________________________
    def calc_vals(self):
        '''
        this should be implemented in the derived class.
        calculates the value(s) of the variable for the current event
        '''
        tau_pt = [ self.formula_tau_pt.EvalInstance(i) for i in xrange(self.formula_tau_pt.GetNdata()) ]
        tau_numTrack = [ int(self.formula_tau_numTrack.EvalInstance(i)) for i in xrange(self.formula_tau_numTrack.GetNdata()) ]
        weights = []
        if not self.chargeP: 
            weights = [ self.ff_scaler.getFactor(tau_pt[i],tau_numTrack[i]) for i in xrange(len(tau_pt)) ]
        elif self.chargeP == 'OS': 
            weights = [ self.ff_scaler.getFactorOS(tau_pt[i],tau_numTrack[i]) for i in xrange(len(tau_pt)) ]
        elif self.chargeP == 'SS': 
            weights = [ self.ff_scaler.getFactorSS(tau_pt[i],tau_numTrack[i]) for i in xrange(len(tau_pt)) ]

        if self.scale == 'up':
            weights = [w * (1.+self.uncertainty) for w in weights]
        elif self.scale == 'dn':
            weights = [w * (1.-self.uncertainty) for w in weights]


        #print 'numTrack: %d, pt: %.1f, ff: %.3f' % (
        #        tau_numTrack[0],
        #        tau_pt[0],
        #        weights[0],
        #        )
        return weights



#------------------------------------------------------------
class FakeFactor(VarBase):
    '''
    python implmentation of fake-factor tool
    '''
    #____________________________________________________________
    def __init__(self,name,config_file,
            tau_pt = None,
            tau_numTrack = None,
            chargeP = None,
            uncertainty = 0.30,
            scale = None,
            fudgefactor_1p = None,
            fudgefactor_3p = None,
            lead_tau_numTrack = None,
            ):
        VarBase.__init__(self,name)
        self.name = name
        self.tau_pt = tau_pt
        self.tau_numTrack = tau_numTrack
        self.chargeP = chargeP
        self.uncertainty = uncertainty
        self.scale = scale
        self.lead_tau_numTrack = lead_tau_numTrack
        self.fudgefactor_1p = fudgefactor_1p
        self.fudgefactor_3p = fudgefactor_3p

        self.formula_tau_pt = None
        self.formula_tau_numTrack = None
        self.formula_lead_tau_numTrack = None
        self.branches = []
        
        
        if chargeP: 
            assert chargeP in ['OS','SS'], "Invalid chargeP, use either 'OS' or 'SS'"

        
        assert config_file, 'Must provide config file!'
        f = ROOT.TFile.Open(config_file)
        assert f, "ERROR opening file: %s" % (config_file)
        g_1P = None
        g_3P = None
        if not chargeP: 
            g_1P = f.Get("fake_factor_1P_NoS")
            g_3P = f.Get("fake_factor_3P_NoS")
        elif chargeP == 'OS':
            g_1P = f.Get("fake_factor_1P_OS")
            g_3P = f.Get("fake_factor_3P_OS")
        elif chargeP == 'SS':
            g_1P = f.Get("fake_factor_1P_SS")
            g_3P = f.Get("fake_factor_3P_SS")

        assert g_1P, "ERROR loading 1P graph from file: %s" % (config_file)
        assert g_3P, "ERROR loading 3P graph from file: %s" % (config_file)
        self.g_1P = g_1P.Clone()
        self.g_3P = g_3P.Clone()


    #____________________________________________________________
    def get_ff(self,pt,numTrack,lead_tau_numTrack=None):
        ff = 0.
        if numTrack == 1: 
            ff = self.g_1P.Eval(pt/1000.)
        elif numTrack == 3: 
            ff = self.g_3P.Eval(pt/1000.)
        else:
            print 'WARNING no fake-factor available for numTrack = ', numTrack
            
        if lead_tau_numTrack == 1 and self.fudgefactor_1p: ff *= self.fudgefactor_1p
        if lead_tau_numTrack == 3 and self.fudgefactor_3p: ff *= self.fudgefactor_3p
        
        #print 'fake-factor numTrack: %d, pt: %.1f, ff: %f' % (numTrack,pt/1000.,ff)
        return ff

    #____________________________________________________________
    def init_tree(self,tree):
        '''
        derived tree initialisation
        '''
        self.tree = tree
        self.formula_tau_pt = ROOT.TTreeFormula(self.tau_pt,self.tau_pt,self.tree)
        self.formula_tau_numTrack = ROOT.TTreeFormula(self.tau_numTrack,self.tau_numTrack,self.tree)
        self.formula_lead_tau_numTrack = ROOT.TTreeFormula(self.lead_tau_numTrack,self.lead_tau_numTrack,self.tree)

        self.branches = []
        self.branches += [self.formula_tau_pt.GetLeaf(i).GetName() for i in xrange(self.formula_tau_pt.GetNcodes()) ]
        self.branches += [self.formula_tau_numTrack.GetLeaf(i).GetName() for i in xrange(self.formula_tau_numTrack.GetNcodes()) ]
        self.branches += [self.formula_lead_tau_numTrack.GetLeaf(i).GetName() for i in xrange(self.formula_lead_tau_numTrack.GetNcodes()) ]

    #____________________________________________________________
    def calc_vals(self):
        '''
        this should be implemented in the derived class.
        calculates the value(s) of the variable for the current event
        '''
        tau_pt = [ self.formula_tau_pt.EvalInstance(i) for i in xrange(self.formula_tau_pt.GetNdata()) ]
        tau_numTrack = [ int(self.formula_tau_numTrack.EvalInstance(i)) for i in xrange(self.formula_tau_numTrack.GetNdata()) ]
        lead_tau_numTrack = [ int(self.formula_lead_tau_numTrack.EvalInstance(i)) for i in xrange(self.formula_lead_tau_numTrack.GetNdata()) ]
        weights = []
        weights = [ self.get_ff(tau_pt[i],tau_numTrack[i],lead_tau_numTrack[i]) for i in xrange(len(tau_pt)) ]
        
        ## single flat rate
        #weights = [0.015]*len(tau_pt)
        
        ## 1p/3p split const values
        #for n in tau_numTrack:
        #    if   n==1: weights.append(0.07)
        #    elif n==3: weights.append(0.005)

        if self.scale == 'up':
            weights = [w * (1.+self.uncertainty) for w in weights]
        elif self.scale == 'dn':
            weights = [w * (1.-self.uncertainty) for w in weights]


        #print 'numTrack: %d, pt: %.1f, ff: %.3f' % (
        #        tau_numTrack[0],
        #        tau_pt[0],
        #        weights[0],
        #        )
        return weights


#------------------------------------------------------------
class FakeFactorHist(VarBase):
    '''
    python implmentation of fake-factor tool
    '''
    #____________________________________________________________
    def __init__(self,name,config_file,
            tau_pt = None,
            tau_numTrack = None,
            chargeP = None,
            uncertainty = 0.30,
            scale = None,
            fudgefactor_1p = None,
            fudgefactor_3p = None,
            lead_tau_numTrack = None,
            ):
        VarBase.__init__(self,name)
        self.name = name
        self.tau_pt = tau_pt
        self.tau_numTrack = tau_numTrack
        self.chargeP = chargeP
        self.uncertainty = uncertainty
        self.scale = scale
        self.lead_tau_numTrack = lead_tau_numTrack
        self.fudgefactor_1p = fudgefactor_1p
        self.fudgefactor_3p = fudgefactor_3p

        self.formula_tau_pt = None
        self.formula_tau_numTrack = None
        self.formula_lead_tau_numTrack = None
        self.branches = []
        
        
        if chargeP: 
            assert chargeP in ['OS','SS'], "Invalid chargeP, use either 'OS' or 'SS'"

        
        assert config_file, 'Must provide config file!'
        f = ROOT.TFile.Open(config_file)
        assert f, "ERROR opening file: %s" % (config_file)
        g_1P = None
        g_3P = None
        if not chargeP: 
            g_1P = f.Get("fake_factor_1P_NoS")
            g_3P = f.Get("fake_factor_3P_NoS")
        elif chargeP == 'OS':
            g_1P = f.Get("fake_factor_1P_OS")
            g_3P = f.Get("fake_factor_3P_OS")
        elif chargeP == 'SS':
            g_1P = f.Get("fake_factor_1P_SS")
            g_3P = f.Get("fake_factor_3P_SS")

        assert g_1P, "ERROR loading 1P graph from file: %s" % (config_file)
        assert g_3P, "ERROR loading 3P graph from file: %s" % (config_file)
        self.g_1P = g_1P.Clone()
        self.g_3P = g_3P.Clone()


    #____________________________________________________________
    def get_ff_and_error(self,pt,numTrack,lead_tau_numTrack=None):
        ff = 0.
        eff = 0.
        ibin = self.g_1P.GetXaxis().FindBin(pt/1000.)
        if numTrack == 1: 
            ff = self.g_1P.GetBinContent(ibin)
            eff = self.g_1P.GetBinError(ibin)
        elif numTrack == 3: 
            ff = self.g_3P.GetBinContent(ibin)
            eff = self.g_3P.GetBinError(ibin)
        else:
            print 'WARNING no fake-factor available for numTrack = ', numTrack
            
        if lead_tau_numTrack == 1 and self.fudgefactor_1p: ff *= self.fudgefactor_1p
        if lead_tau_numTrack == 3 and self.fudgefactor_3p: ff *= self.fudgefactor_3p
        
        #print 'fake-factor numTrack: %d, pt: %.1f, ff: %f' % (numTrack,pt/1000.,ff)
        return ff, eff

    #____________________________________________________________
    def init_tree(self,tree):
        '''
        derived tree initialisation
        '''
        self.tree = tree
        self.formula_tau_pt = ROOT.TTreeFormula(self.tau_pt,self.tau_pt,self.tree)
        self.formula_tau_numTrack = ROOT.TTreeFormula(self.tau_numTrack,self.tau_numTrack,self.tree)
        self.formula_lead_tau_numTrack = ROOT.TTreeFormula(self.lead_tau_numTrack,self.lead_tau_numTrack,self.tree)

        self.branches = []
        self.branches += [self.formula_tau_pt.GetLeaf(i).GetName() for i in xrange(self.formula_tau_pt.GetNcodes()) ]
        self.branches += [self.formula_tau_numTrack.GetLeaf(i).GetName() for i in xrange(self.formula_tau_numTrack.GetNcodes()) ]
        self.branches += [self.formula_lead_tau_numTrack.GetLeaf(i).GetName() for i in xrange(self.formula_lead_tau_numTrack.GetNcodes()) ]

    #____________________________________________________________
    def calc_vals(self):
        '''
        this should be implemented in the derived class.
        calculates the value(s) of the variable for the current event
        '''
        tau_pt = [ self.formula_tau_pt.EvalInstance(i) for i in xrange(self.formula_tau_pt.GetNdata()) ]
        tau_numTrack = [ int(self.formula_tau_numTrack.EvalInstance(i)) for i in xrange(self.formula_tau_numTrack.GetNdata()) ]
        lead_tau_numTrack = [ int(self.formula_lead_tau_numTrack.EvalInstance(i)) for i in xrange(self.formula_lead_tau_numTrack.GetNdata()) ]
        weights = []
        fake_factors = [ self.get_ff_and_error(tau_pt[i],tau_numTrack[i],lead_tau_numTrack[i]) for i in xrange(len(tau_pt)) ]
        ## const values
        #for n in tau_numTrack:
        #    if   n==1: weights.append(0.07)
        #    elif n==3: weights.append(0.005)
        
        weights = []
        for ff_data in fake_factors: 
            ff = ff_data[0]
            eff = ff_data[1]
            if self.scale == 'up':   ff += eff
            elif self.scale == 'dn': ff -= eff
            ff = max(0.,ff)
            weights.append(ff)

        #print 'numTrack: %d, pt: %.1f, ff: %.3f' % (
        #        tau_numTrack[0],
        #        tau_pt[0],
        #        weights[0],
        #        )
        return weights





#------------------------------------------------------------
class FakeWeight(VarBase):
    '''
    fake-weights for factorising tau id in MC
    '''
    #____________________________________________________________
    def __init__(self,name,config_file,
            tau_pt = None,
            tau_numTrack = None,
            tau_trueTauAssoc_matched = None,
            tau_id_level = None,
            has_trigger = False,
            fail_id = False,
            chargeP = None,
            uncertainty = 0.6,
            scale = None,
            ):
        VarBase.__init__(self,name)
        self.name = name
        self.tau_pt = tau_pt
        self.tau_numTrack = tau_numTrack
        self.tau_trueTauAssoc_matched = tau_trueTauAssoc_matched
        self.tau_id_level = tau_id_level
        self.has_trigger = has_trigger
        self.fail_id = fail_id
        self.chargeP = 0
        if chargeP == 'OS': self.chargeP = -1
        if chargeP == 'SS': self.chargeP = 1
        self.uncertainty = uncertainty
        self.scale = scale

        self.formula_tau_pt = None
        self.formula_tau_numTrack = None
        self.formula_tau_trueTauAssoc_matched = None
        self.branches = []
        
        ROOT.gSystem.Load('libFakeWeightTool')
        self.fw_scaler = ROOT.FakeWeightScaler()
        self.fw_scaler.readGraphsFromFile(config_file)

        self.chargeproduct = 0

    #____________________________________________________________
    def init_tree(self,tree):
        '''
        derived tree initialisation
        '''
        self.tree = tree
        self.formula_tau_pt = ROOT.TTreeFormula(self.tau_pt,self.tau_pt,self.tree)
        self.formula_tau_numTrack = ROOT.TTreeFormula(self.tau_numTrack,self.tau_numTrack,self.tree)
        self.formula_tau_trueTauAssoc_matched = ROOT.TTreeFormula(self.tau_trueTauAssoc_matched,self.tau_trueTauAssoc_matched,self.tree)

        self.branches = []
        self.branches += [self.formula_tau_pt.GetLeaf(i).GetName() for i in xrange(self.formula_tau_pt.GetNcodes()) ]
        self.branches += [self.formula_tau_numTrack.GetLeaf(i).GetName() for i in xrange(self.formula_tau_numTrack.GetNcodes()) ]
        self.branches += [self.formula_tau_trueTauAssoc_matched.GetLeaf(i).GetName() for i in xrange(self.formula_tau_trueTauAssoc_matched.GetNcodes()) ]

    #____________________________________________________________
    def calc_vals(self):
        '''
        this should be implemented in the derived class.
        calculates the value(s) of the variable for the current event
        '''
        tau_pt = [ self.formula_tau_pt.EvalInstance(i) for i in xrange(self.formula_tau_pt.GetNdata()) ]
        tau_numTrack = [ int(self.formula_tau_numTrack.EvalInstance(i)) for i in xrange(self.formula_tau_numTrack.GetNdata()) ]
        tau_trueTauAssoc_matched = [ int(self.formula_tau_trueTauAssoc_matched.EvalInstance(i)) for i in xrange(self.formula_tau_trueTauAssoc_matched.GetNdata()) ]
        weights = []
    

        for i in xrange(len(tau_pt)):
            fw = 1.
            if not tau_trueTauAssoc_matched[i]:
                fw = self.fw_scaler.getWeight(tau_pt[i],tau_numTrack[i],self.tau_id_level,self.has_trigger,self.chargeP,self.fail_id)
                if self.scale == 'up': fw *= (1.+self.uncertainty)
                if self.scale == 'dn': fw *= (1.-self.uncertainty)
            weights.append(fw)
        return weights



#------------------------------------------------------------
class TauIDSF(VarBase):
    '''
    simple implementation of VarBase using TTreeFormula (like in TTree::Draw) 
    The var class should provide an implementation of the 
    'process' method
    '''
    #____________________________________________________________
    def __init__(self,name,config_path,
            tau_pt = None,
            tau_eta = None,
            tau_numTrack = None,
            tau_trueTauAssoc_matched = None,
            scale = None,
            level = 'loose',

            ):
        VarBase.__init__(self,name)
        self.name = name
        self.tau_pt = tau_pt
        self.tau_eta = tau_eta
        self.tau_numTrack = tau_numTrack
        self.tau_trueTauAssoc_matched = tau_trueTauAssoc_matched
        self.scale = scale
        self.config_path = config_path

        self.formula_tau_pt = None
        self.formula_tau_eta = None
        self.formula_tau_numTrack = None
        self.formula_tau_trueTauAssoc_matched = None
        self.branches = []
        
        #ROOT.gSystem.Load('libTauCorrections')
        #self.tool = ROOT.TauCorrections()
        #self.tool.Initialise(self.config_path,True)
        
        ROOT.gSystem.Load('libTauCorrUncert')
        self.tool = ROOT.TauCorrUncert.TauSF(self.config_path, False)
       

        assert hasattr(ROOT.TauCorrUncert,level), 'ERROR invalid level!'
        self.level = ROOT.Long(getattr(ROOT.TauCorrUncert,level))
    #____________________________________________________________
    def init_tree(self,tree):
        '''
        derived tree initialisation
        '''
        self.tree = tree
        self.formula_tau_pt = ROOT.TTreeFormula(self.tau_pt,self.tau_pt,self.tree)
        self.formula_tau_eta = ROOT.TTreeFormula(self.tau_eta,self.tau_eta,self.tree)
        self.formula_tau_numTrack = ROOT.TTreeFormula(self.tau_numTrack,self.tau_numTrack,self.tree)
        self.formula_tau_trueTauAssoc_matched = ROOT.TTreeFormula(self.tau_trueTauAssoc_matched,self.tau_trueTauAssoc_matched,self.tree)

        self.branches = []
        self.branches += [self.formula_tau_pt.GetLeaf(i).GetName() for i in xrange(self.formula_tau_pt.GetNcodes()) ]
        self.branches += [self.formula_tau_eta.GetLeaf(i).GetName() for i in xrange(self.formula_tau_eta.GetNcodes()) ]
        self.branches += [self.formula_tau_numTrack.GetLeaf(i).GetName() for i in xrange(self.formula_tau_numTrack.GetNcodes()) ]
        self.branches += [self.formula_tau_trueTauAssoc_matched.GetLeaf(i).GetName() for i in xrange(self.formula_tau_trueTauAssoc_matched.GetNcodes()) ]

    #____________________________________________________________
    def calc_vals(self):
        '''
        this should be implemented in the derived class.
        calculates the value(s) of the variable for the current event
        '''
        tau_pt = [ self.formula_tau_pt.EvalInstance(i) for i in xrange(self.formula_tau_pt.GetNdata()) ]
        tau_eta = [ self.formula_tau_eta.EvalInstance(i) for i in xrange(self.formula_tau_eta.GetNdata()) ]
        tau_numTrack = [ int(self.formula_tau_numTrack.EvalInstance(i)) for i in xrange(self.formula_tau_numTrack.GetNdata()) ]
        tau_trueTauAssoc_matched = [ int(self.formula_tau_trueTauAssoc_matched.EvalInstance(i)) for i in xrange(self.formula_tau_trueTauAssoc_matched.GetNdata()) ]
        weights = []

        for i in xrange(len(tau_pt)): 
            SF = 1. 
            if tau_trueTauAssoc_matched[i]: 
                eta = tau_eta[i]
                numTrack = tau_numTrack[i]
                pt = tau_pt[i]
                SF = self.tool.GetIDSF(self.level,eta,numTrack,pt)
                if self.scale: 
                    stat = self.tool.GetIDStatUnc(self.level,eta,numTrack,pt)
                    sys  = self.tool.GetIDSysUnc(self.level,eta,numTrack,pt)
                    lowpt = sqrt(stat*stat+sys*sys)
                    highpt_rel = 0.
                    if pt > 100.e3: 
                        if numTrack == 1: 
                            highpt_rel = 0.00014 * (pt/1000. - 100.)
                            highpt_rel = min(highpt_rel,0.029)
                        else: 
                            highpt_rel = 0.000067 * (pt/1000. - 100.)
                            highpt_rel = min(highpt_rel,0.015)
                    highpt = highpt_rel * SF
                    unc = lowpt + highpt 

                if self.scale == 'up':   SF += unc 
                elif self.scale == 'dn': SF -= unc 
            weights.append(SF)
        return weights



#------------------------------------------------------------
class Tau3PSF(VarBase):
    '''
    simple implementation of VarBase using TTreeFormula (like in TTree::Draw) 
    The var class should provide an implementation of the 
    'process' method
    '''
    #____________________________________________________________
    def __init__(self,name,
            tau_pt = None,
            tau_numTrack = None,
            tau_trueTauAssoc_matched = None,
            scale = None,
            ):
        VarBase.__init__(self,name)
        self.name = name
        self.tau_pt = tau_pt
        self.tau_numTrack = tau_numTrack
        self.tau_trueTauAssoc_matched = tau_trueTauAssoc_matched
        self.scale = scale

        self.formula_tau_pt = None
        self.formula_tau_numTrack = None
        self.formula_tau_trueTauAssoc_matched = None
        self.branches = []
        
    #____________________________________________________________
    def init_tree(self,tree):
        '''
        derived tree initialisation
        '''
        self.tree = tree
        self.formula_tau_pt = ROOT.TTreeFormula(self.tau_pt,self.tau_pt,self.tree)
        self.formula_tau_numTrack = ROOT.TTreeFormula(self.tau_numTrack,self.tau_numTrack,self.tree)
        self.formula_tau_trueTauAssoc_matched = ROOT.TTreeFormula(self.tau_trueTauAssoc_matched,self.tau_trueTauAssoc_matched,self.tree)

        self.branches = []
        self.branches += [self.formula_tau_pt.GetLeaf(i).GetName() for i in xrange(self.formula_tau_pt.GetNcodes()) ]
        self.branches += [self.formula_tau_numTrack.GetLeaf(i).GetName() for i in xrange(self.formula_tau_numTrack.GetNcodes()) ]
        self.branches += [self.formula_tau_trueTauAssoc_matched.GetLeaf(i).GetName() for i in xrange(self.formula_tau_trueTauAssoc_matched.GetNcodes()) ]

    #____________________________________________________________
    def calc_vals(self):
        '''
        this should be implemented in the derived class.
        calculates the value(s) of the variable for the current event
        '''
        tau_pt = [ self.formula_tau_pt.EvalInstance(i) for i in xrange(self.formula_tau_pt.GetNdata()) ]
        tau_numTrack = [ int(self.formula_tau_numTrack.EvalInstance(i)) for i in xrange(self.formula_tau_numTrack.GetNdata()) ]
        tau_trueTauAssoc_matched = [ int(self.formula_tau_trueTauAssoc_matched.EvalInstance(i)) for i in xrange(self.formula_tau_trueTauAssoc_matched.GetNdata()) ]
        weights = []

        for i in xrange(len(tau_pt)): 
            SF = 1. 
            if self.scale and tau_trueTauAssoc_matched[i] and tau_numTrack[i]==3: 
                pt = tau_pt[i]
                if pt>150.e3: 
                    unc = 0.0005 * (pt/1000.-150.) 
                    if self.scale == 'up':   SF += unc 
                    elif self.scale == 'dn': SF -= unc 
            weights.append(SF)
        return weights





#------------------------------------------------------------
class kfactor(VarBase):
    '''
    QCD/EW k-factor from reweighting package
    '''
    #____________________________________________________________
    def __init__(self,name='kQCD',
            reso_mass = None,
            use_HOEW = False,
            scale = None,
            ):
        VarBase.__init__(self,name)
        self.name = name
        self.reso_mass = reso_mass
        self.scale = scale
        self.use_HOEW = use_HOEW

        self.formula_reso_mass = None
        self.branches = []
        
        ROOT.gSystem.Load('libreweighting')
        self.tool = ROOT.ZPReweighter()
    #____________________________________________________________
    def init_tree(self,tree):
        '''
        derived tree initialisation
        '''
        self.tree = tree
        self.formula_reso_mass = ROOT.TTreeFormula(self.reso_mass,self.reso_mass,self.tree)

        self.branches = []
        self.branches += [self.formula_reso_mass.GetLeaf(i).GetName() for i in xrange(self.formula_reso_mass.GetNcodes()) ]

    #____________________________________________________________
    def calc_vals(self):
        '''
        this should be implemented in the derived class.
        calculates the value(s) of the variable for the current event
        '''
        reso_mass = [ self.formula_reso_mass.EvalInstance(i) for i in xrange(self.formula_reso_mass.GetNdata()) ]
        weights = []

        for i in xrange(len(reso_mass)):
            mode = 0
            if self.scale == 'up': mode = 1
            elif self.scale == 'dn': mode = 2
            
            if self.use_HOEW: 
                kfactor = self.tool.kfactorQCDEW(reso_mass[i],mode) 
            else: 
                kfactor = self.tool.kfactorQCDonly(reso_mass[i],mode) 
            #print 'mass: %.f, kfactor: %.3f'%(reso_mass[i]/1000.,kfactor)
            weights.append(kfactor)
        return weights


#------------------------------------------------------------
class kQCDPowheg(VarBase):
    '''
    kQCD for Powheg (Z->ll) from reweighting package
    '''
    #____________________________________________________________
    def __init__(self,name='kQCD',
            reso_mass = None,
            scale = None,
            ):
        VarBase.__init__(self,name)
        self.name = name
        self.reso_mass = reso_mass
        self.scale = scale

        self.formula_reso_mass = None
        self.branches = []
        
        ROOT.gSystem.Load('libreweighting')
        self.tool = ROOT.ZPReweighter()
    #____________________________________________________________
    def init_tree(self,tree):
        '''
        derived tree initialisation
        '''
        self.tree = tree
        self.formula_reso_mass = ROOT.TTreeFormula(self.reso_mass,self.reso_mass,self.tree)

        self.branches = []
        self.branches += [self.formula_reso_mass.GetLeaf(i).GetName() for i in xrange(self.formula_reso_mass.GetNcodes()) ]

    #____________________________________________________________
    def calc_vals(self):
        '''
        this should be implemented in the derived class.
        calculates the value(s) of the variable for the current event
        '''
        reso_mass = [ self.formula_reso_mass.EvalInstance(i) for i in xrange(self.formula_reso_mass.GetNdata()) ]
        weights = []

        for i in xrange(len(reso_mass)): 
            kQCD = 1. 
            if self.scale == 'up':
                kQCD *= self.tool.kfactorQCDPowHeg(reso_mass[i],1) 
            elif self.scale == 'dn':
                kQCD *= self.tool.kfactorQCDPowHeg(reso_mass[i],2) 
            else:
                self.tool.kfactorQCDPowHeg(reso_mass[i],0) 
            weights.append(kQCD)
        return weights




#------------------------------------------------------------
class kEW(VarBase):
    '''
    kEW from reweighting package
    '''
    #____________________________________________________________
    def __init__(self,name='kEW',
            reso_mass = None,
            scale = None,
            error = 0.10,
            ):
        VarBase.__init__(self,name)
        self.name = name
        self.reso_mass = reso_mass
        self.scale = scale
        self.error = error 

        self.formula_reso_mass = None
        self.branches = []
        
        ROOT.gSystem.Load('libreweighting')
        self.tool = ROOT.ZPReweighter()
    #____________________________________________________________
    def init_tree(self,tree):
        '''
        derived tree initialisation
        '''
        self.tree = tree
        self.formula_reso_mass = ROOT.TTreeFormula(self.reso_mass,self.reso_mass,self.tree)

        self.branches = []
        self.branches += [self.formula_reso_mass.GetLeaf(i).GetName() for i in xrange(self.formula_reso_mass.GetNcodes()) ]

    #____________________________________________________________
    def calc_vals(self):
        '''
        this should be implemented in the derived class.
        calculates the value(s) of the variable for the current event
        '''
        reso_mass = [ self.formula_reso_mass.EvalInstance(i) for i in xrange(self.formula_reso_mass.GetNdata()) ]
        weights = []

        for i in xrange(len(reso_mass)): 
            kEW = self.tool.kfactorEW(reso_mass[i]) 
            if self.scale == 'up':
                kEW *= (1. + self.error )
            elif self.scale == 'dn':
                kEW *= (1. - self.error )
            weights.append(kEW)
        return weights


#------------------------------------------------------------
class ZPWeight(VarBase):
    '''
    ZP reweight from reweighting package
    '''
    #____________________________________________________________
    def __init__(self,name='ZPWeight',
            reso_mass = None,
            inflav = None,
            mass = None, ## in GeV
            interference = False,
            ):
        VarBase.__init__(self,name)
        self.name = name
        self.reso_mass = reso_mass
        self.inflav = inflav
        self.mass = mass
        self.interference = interference

        self.formula_reso_mass = None
        self.formula_inflav = None
        self.branches = []
        
        ROOT.gSystem.Load('libreweighting')
        self.tool = ROOT.ZPReweighter()
    #____________________________________________________________
    def init_tree(self,tree):
        '''
        derived tree initialisation
        '''

        assert self.mass, "ERROR - must provide resonance mass"
        self.tool.setZPmass(float(self.mass)*1000.)

        self.tree = tree
        self.formula_reso_mass = ROOT.TTreeFormula(self.reso_mass,self.reso_mass,self.tree)
        self.formula_inflav = ROOT.TTreeFormula(self.inflav,self.inflav,self.tree)

        self.branches = []
        self.branches += [self.formula_reso_mass.GetLeaf(i).GetName() for i in xrange(self.formula_reso_mass.GetNcodes()) ]
        self.branches += [self.formula_inflav.GetLeaf(i).GetName() for i in xrange(self.formula_inflav.GetNcodes()) ]

    #____________________________________________________________
    def calc_vals(self):
        '''
        this should be implemented in the derived class.
        calculates the value(s) of the variable for the current event
        '''
        reso_mass = [ self.formula_reso_mass.EvalInstance(i) for i in xrange(self.formula_reso_mass.GetNdata()) ]
        inflav = [ self.formula_inflav.EvalInstance(i) for i in xrange(self.formula_inflav.GetNdata()) ]
        weights = []

        for i in xrange(len(reso_mass)): 
            if self.interference:
                zpweight = self.tool.weightZP(pow(reso_mass[i],2),inflav[i]) 
            else:
                zpweight = self.tool.weightZPnoSM(pow(reso_mass[i],2),int(inflav[i])) 
            #print 'mass: %.1f, weight %f' % (reso_mass[i],zpweight)
            weights.append(zpweight)
        return weights











# - - - - - - - - - - function defs - - - - - - - - - - - - #
#____________________________________________________________
#def my_function():
#    '''
#    description of my_function
#    '''
#    pass






# EOF
