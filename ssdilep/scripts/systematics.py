# encoding: utf-8
'''
systematics.py

description:

'''
## modules

# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class Systematic(object):
    '''
    class to hold info about systematics 
    '''
    #____________________________________________________________
    def __init__(self,
            name,
            title=None,
            var_up=None,
            var_dn=None,
            flat_err=None,
            ):
        self.name = name
        if not title: title = name
        self.title = title
        self.var_up=var_up
        self.var_dn=var_dn
        self.flat_err=flat_err 
        assert (self.var_up and self.var_dn) or self.flat_err!=None, 'Must provide either up and dn vars or a flat err!'


sys_dict = {}
# Specific for categories (acceptance unc)

# SYS1 = sys_dict['SYS1'] = Systematic(
#         'SYS1',
#         var_up='SYS1_UP',
#         var_dn='SYS1_DN'
#         )
# SYS2 = sys_dict['SYS2'] = Systematic(
#         'SYS2','$\\sigma_{\\rm Diboson}$',      
#         flat_err=0.05,
#         )


#________________________________________________________________________________________
# LPX_KFACTOR_CHOICE_HERAPDF20/LPX_KFACTOR_CHOICE_NNPDF30     Systematics that cover the variation of the k-Factor due to a specific choice of a model dependent PDF.
# LPX_KFACTOR_BEAM_ENERGY     Systematic that covers the variation in the Beam Energy.
# LPX_KFACTOR_PDF_EV1-7   Seven PDF uncertainty bundles. Either use these or the PDF up/down.
# LPX_KFACTOR_PDF_1up/1down   90% C.L. eigen-vector variation uncertainty based on the nominal PDF choice (CT14nnlo).
# LPX_KFACTOR_PI_1up/1down    Systematic uncertainty of the Photon-Induced k-Factor.
# LPX_SCALE_Z_1up/1down   Scale uncertainty of the NC DY process.
# LPX_SCALE_W_1up/1down   Scale uncertainty of the CC DY process. 
#_________________________________________________________________________________________
BEAM = sys_dict['BEAM'] = Systematic(
        'BEAM',
        var_up='BEAM_UP',
        var_dn='BEAM_DN'
        )
CHOICE = sys_dict['CHOICE'] = Systematic(
        'CHOICE',
        var_up='CHOICE_UP',
        var_dn='CHOICE_DN'
        )
PDF = sys_dict['PDF'] = Systematic(
        'PDF',
        var_up='PDF_UP',
        var_dn='PDF_DN'
        )
PI = sys_dict['PI'] = Systematic(
        'PI',
        var_up='PI_UP',
        var_dn='PI_DN'
        )
SCALE_Z = sys_dict['SCALE_Z'] = Systematic(
        'SCALE_Z',
        var_up='SCALE_Z_UP',
        var_dn='SCALE_Z_DN'
        )

#_________________________________________________________________________________________
# Tree Systematics
#_________________________________________________________________________________________
#electron
#_________________________________________________________________________________________
EG_RESOLUTION_ALL = sys_dict['EG_RESOLUTION_ALL'] = Systematic(
        'EG_RESOLUTION_ALL',
        var_up='EG_RESOLUTION_ALL_UP',
        var_dn='EG_RESOLUTION_ALL_DN'
        )
EG_SCALE_ALLCORR = sys_dict['EG_SCALE_ALLCORR'] = Systematic(
        'EG_SCALE_ALLCORR',
        var_up='EG_SCALE_ALLCORR_UP',
        var_dn='EG_SCALE_ALLCORR_DN'
        )
EG_SCALE_E4SCINTILLATOR = sys_dict['EG_SCALE_E4SCINTILLATOR'] = Systematic(
        'EG_SCALE_E4SCINTILLATOR',
        var_up='EG_SCALE_E4SCINTILLATOR_UP',
        var_dn='EG_SCALE_E4SCINTILLATOR_DN'
        )
# muon
#_________________________________________________________________________________________
MUON_ID = sys_dict['MUON_ID'] = Systematic(
        'MUON_ID',
        var_up='MUON_ID_UP',
        var_dn='MUON_ID_DN'
        )
MUON_MS = sys_dict['MUON_MS'] = Systematic(
        'MUON_MS',
        var_up='MUON_MS_UP',
        var_dn='MUON_MS_DN'
        )
MUON_RESBIAS = sys_dict['MUON_RESBIAS'] = Systematic(
        'MUON_RESBIAS',
        var_up='MUON_RESBIAS_UP',
        var_dn='MUON_RESBIAS_DN'
        )
MUON_RHO = sys_dict['MUON_RHO'] = Systematic(
        'MUON_RHO',
        var_up='MUON_RHO_UP',
        var_dn='MUON_RHO_DN'
        )
MUON_SCALE = sys_dict['MUON_SCALE'] = Systematic(
        'MUON_SCALE',
        var_up='MUON_SCALE_UP',
        var_dn='MUON_SCALE_DN'
        )

# EG_SCALE_LARCALIB_EXTRA2015PRE = sys_dict['EG_SCALE_LARCALIB_EXTRA2015PRE'] = Systematic(
#         'EG_SCALE_LARCALIB_EXTRA2015PRE',
#         var_up='EG_SCALE_LARCALIB_EXTRA2015PRE_UP',
#         var_dn='EG_SCALE_LARCALIB_EXTRA2015PRE_DN'
#         )
# EG_SCALE_LARTEMPERATURE_EXTRA2015PRE = sys_dict['EG_SCALE_LARTEMPERATURE_EXTRA2015PRE'] = Systematic(
#         'EG_SCALE_LARTEMPERATURE_EXTRA2015PRE',
#         var_up='EG_SCALE_LARTEMPERATURE_EXTRA2015PRE_UP',
#         var_dn='EG_SCALE_LARTEMPERATURE_EXTRA2015PRE_DN'
#         )
# EG_SCALE_LARTEMPERATURE_EXTRA2016PRE = sys_dict['EG_SCALE_LARTEMPERATURE_EXTRA2016PRE'] = Systematic(
#         'EG_SCALE_LARTEMPERATURE_EXTRA2016PRE',
#         var_up='EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_UP',
#         var_dn='EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_DN'
#         )


FF = sys_dict['FF'] = Systematic(
        'FF',
        var_up='FF_UP',
        var_dn='FF_DN'
        )

CF = sys_dict['CF'] = Systematic(
        'CF',
        var_up='CF_UP',
        var_dn='CF_DN'
        )

TRIG = sys_dict['TRIG'] = Systematic(
        'TRIG',
        var_up='TRIG_UP',
        var_dn='TRIG_DN'
        )

ID = sys_dict['ID'] = Systematic(
        'ID',
        var_up='ID_UP',
        var_dn='ID_DN'
        )

ISO = sys_dict['ISO'] = Systematic(
        'ISO',
        var_up='ISO_UP',
        var_dn='ISO_DN'
        )

RECO = sys_dict['RECO'] = Systematic(
        'RECO',
        var_up='RECO_UP',
        var_dn='RECO_DN'
        )

# muon
#_________________________________________________________________________________________
MUFF = sys_dict['MUFF'] = Systematic(
        'MUFF',
        var_up='MUFF_UP',
        var_dn='MUFF_DN'
        )

TRIGSTAT = sys_dict['TRIGSTAT'] = Systematic(
        'TRIGSTAT',
        var_up='TRIG_UPSTAT',
        var_dn='TRIG_DNSTAT'
        )
TRIGSYS = sys_dict['TRIGSYS'] = Systematic(
        'TRIGSYS',
        var_up='TRIG_UPSYS',
        var_dn='TRIG_DNSYS'
        )
ISOSYS = sys_dict['ISOSYS'] = Systematic(
        'ISOSYS',
        var_up='ISO_UPSYS',
        var_dn='ISO_DNSYS'
        )
ISOSTAT = sys_dict['ISOSTAT'] = Systematic(
        'ISOSTAT',
        var_up='ISO_UPSTAT',
        var_dn='ISO_DNSTAT'
        )
RECOSYS = sys_dict['RECOSYS'] = Systematic(
        'RECOSYS',
        var_up='RECO_UPSYS',
        var_dn='RECO_DNSYS'
        )
RECOSTAT = sys_dict['RECOSTAT'] = Systematic(
        'RECOSTAT',
        var_up='RECO_UPSTAT',
        var_dn='RECO_DNSTAT'
        )
TTVASYS = sys_dict['TTVASYS'] = Systematic(
        'TTVASYS',
        var_up='TTVA_UPSYS',
        var_dn='TTVA_DNSYS'
        )
TTVASTAT = sys_dict['TTVASTAT'] = Systematic(
        'TTVASTAT',
        var_up='TTVA_UPSTAT',
        var_dn='TTVA_DNSTAT'
        )

## EOF
