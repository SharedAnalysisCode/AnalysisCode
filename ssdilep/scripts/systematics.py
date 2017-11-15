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
            onesided=None,
            envelope=None,
            constituents=None,
            ):
        self.name = name
        if not title: title = name
        self.title = title
        self.var_up=var_up
        self.var_dn=var_dn
        self.flat_err=flat_err
        self.onesided = onesided
        self.envelope = envelope
        self.constituents = constituents
        assert (self.var_up or self.var_dn) or self.flat_err!=None or (self.envelope!=None and self.constituents!=None), 'Must provide either up and dn vars or a flat err!'


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

# jet
#_________________________________________________________________________________________

                             
B_SYS = sys_dict['B_SYS'] = Systematic(
      'B_SYS',
      var_up='B_SYS_UP',
      var_dn='B_SYS_DN',
      )                             
                             
C_SYS = sys_dict['C_SYS'] = Systematic(
      'C_SYS',
      var_up='C_SYS_UP',
      var_dn='C_SYS_DN',
      )                             
                             
L_SYS = sys_dict['L_SYS'] = Systematic(
      'L_SYS',
      var_up='L_SYS_UP',
      var_dn='L_SYS_DN',
      )                             
                             
E_SYS = sys_dict['E_SYS'] = Systematic(
      'E_SYS',
      var_up='E_SYS_UP',
      var_dn='E_SYS_DN',
      )                             
                           
EFC_SYS = sys_dict['EFC_SYS'] = Systematic(
      'EFC_SYS',
      var_up='EFC_SYS_UP',
      var_dn='EFC_SYS_DN',
      )                           
                           
JVT_SYS = sys_dict['JVT_SYS'] = Systematic(
      'JVT_SYS',
      var_up='JVT_SYS_UP',
      var_dn='JVT_SYS_DN',
      )         

JET_BJES_Response = sys_dict['JET_BJES_Response'] = Systematic(
      'JET_BJES_Response',
      var_up='JET_BJES_Response_UP',
      var_dn='JET_BJES_Response_DN',
      )                 
                 
JET_EffectiveNP_1 = sys_dict['JET_EffectiveNP_1'] = Systematic(
      'JET_EffectiveNP_1',
      var_up='JET_EffectiveNP_1_UP',
      var_dn='JET_EffectiveNP_1_DN',
      )                 
                 
JET_EffectiveNP_2 = sys_dict['JET_EffectiveNP_2'] = Systematic(
      'JET_EffectiveNP_2',
      var_up='JET_EffectiveNP_2_UP',
      var_dn='JET_EffectiveNP_2_DN',
      )                 
                 
JET_EffectiveNP_3 = sys_dict['JET_EffectiveNP_3'] = Systematic(
      'JET_EffectiveNP_3',
      var_up='JET_EffectiveNP_3_UP',
      var_dn='JET_EffectiveNP_3_DN',
      )                 
                 
JET_EffectiveNP_4 = sys_dict['JET_EffectiveNP_4'] = Systematic(
      'JET_EffectiveNP_4',
      var_up='JET_EffectiveNP_4_UP',
      var_dn='JET_EffectiveNP_4_DN',
      )                 
                 
JET_EffectiveNP_5 = sys_dict['JET_EffectiveNP_5'] = Systematic(
      'JET_EffectiveNP_5',
      var_up='JET_EffectiveNP_5_UP',
      var_dn='JET_EffectiveNP_5_DN',
      )                 
                 
JET_EffectiveNP_6 = sys_dict['JET_EffectiveNP_6'] = Systematic(
      'JET_EffectiveNP_6',
      var_up='JET_EffectiveNP_6_UP',
      var_dn='JET_EffectiveNP_6_DN',
      )                 
                 
JET_EffectiveNP_7 = sys_dict['JET_EffectiveNP_7'] = Systematic(
      'JET_EffectiveNP_7',
      var_up='JET_EffectiveNP_7_UP',
      var_dn='JET_EffectiveNP_7_DN',
      )                 
                 
JET_EffectiveNP_8restTerm = sys_dict['JET_EffectiveNP_8restTerm'] = Systematic(
      'JET_EffectiveNP_8restTerm',
      var_up='JET_EffectiveNP_8restTerm_UP',
      var_dn='JET_EffectiveNP_8restTerm_DN',
      )         
         
JET_EtaIntercalibration_Modelling = sys_dict['JET_EtaIntercalibration_Modelling'] = Systematic(
      'JET_EtaIntercalibration_Modelling',
      var_up='JET_EtaIntercalibration_Modelling_UP',
      var_dn='JET_EtaIntercalibration_Modelling_DN',
      ) 
 
JET_EtaIntercalibration_NonClosure = sys_dict['JET_EtaIntercalibration_NonClosure'] = Systematic(
      'JET_EtaIntercalibration_NonClosure',
      var_up='JET_EtaIntercalibration_NonClosure_UP',
      var_dn='JET_EtaIntercalibration_NonClosure_DN',
      )

JET_EtaIntercalibration_TotalStat = sys_dict['JET_EtaIntercalibration_TotalStat'] = Systematic(
      'JET_EtaIntercalibration_TotalStat',
      var_up='JET_EtaIntercalibration_TotalStat_UP',
      var_dn='JET_EtaIntercalibration_TotalStat_DN',
      ) 
 
JET_Flavor_Composition = sys_dict['JET_Flavor_Composition'] = Systematic(
      'JET_Flavor_Composition',
      var_up='JET_Flavor_Composition_UP',
      var_dn='JET_Flavor_Composition_DN',
      )            
            
JET_Flavor_Response = sys_dict['JET_Flavor_Response'] = Systematic(
      'JET_Flavor_Response',
      var_up='JET_Flavor_Response_UP',
      var_dn='JET_Flavor_Response_DN',
      )               
               
JET_Pileup_OffsetMu = sys_dict['JET_Pileup_OffsetMu'] = Systematic(
      'JET_Pileup_OffsetMu',
      var_up='JET_Pileup_OffsetMu_UP',
      var_dn='JET_Pileup_OffsetMu_DN',
      )               
               
JET_Pileup_OffsetNPV = sys_dict['JET_Pileup_OffsetNPV'] = Systematic(
      'JET_Pileup_OffsetNPV',
      var_up='JET_Pileup_OffsetNPV_UP',
      var_dn='JET_Pileup_OffsetNPV_DN',
      )              
              
JET_Pileup_PtTerm = sys_dict['JET_Pileup_PtTerm'] = Systematic(
      'JET_Pileup_PtTerm',
      var_up='JET_Pileup_PtTerm_UP',
      var_dn='JET_Pileup_PtTerm_DN',
      )                 
                 
JET_Pileup_RhoTopology = sys_dict['JET_Pileup_RhoTopology'] = Systematic(
      'JET_Pileup_RhoTopology',
      var_up='JET_Pileup_RhoTopology_UP',
      var_dn='JET_Pileup_RhoTopology_DN',
      )            
            
JET_PunchThrough_MC15 = sys_dict['JET_PunchThrough_MC15'] = Systematic(
      'JET_PunchThrough_MC15',
      var_up='JET_PunchThrough_MC15_UP',
      var_dn='JET_PunchThrough_MC15_DN',
      )             
             
JET_SingleParticle_HighPt = sys_dict['JET_SingleParticle_HighPt'] = Systematic(
      'JET_SingleParticle_HighPt',
      var_up='JET_SingleParticle_HighPt_UP',
      var_dn='JET_SingleParticle_HighPt_DN',
      )         
         
JET_JER_CROSS_CALIB_FORWARD = sys_dict['JET_JER_CROSS_CALIB_FORWARD'] = Systematic(
      'JET_JER_CROSS_CALIB_FORWARD',
      var_up='JET_JER_CROSS_CALIB_FORWARD_UP',
      var_dn=None,
      onesided=True,
      )   

JET_JER_NOISE_FORWARD = sys_dict['JET_JER_NOISE_FORWARD'] = Systematic(
      'JET_JER_NOISE_FORWARD',
      var_up='JET_JER_NOISE_FORWARD_UP',
      var_dn=None,
      onesided=True,
      )             
                       
JET_JER_NP0 = sys_dict['JET_JER_NP0'] = Systematic(
      'JET_JER_NP0',
      var_up='JET_JER_NP0_UP',
      var_dn='JET_JER_NP0_DN',
      )                       
                       
JET_JER_NP1 = sys_dict['JET_JER_NP1'] = Systematic(
      'JET_JER_NP1',
      var_up='JET_JER_NP1_UP',
      var_dn='JET_JER_NP1_DN',
      )                       
                       
JET_JER_NP2 = sys_dict['JET_JER_NP2'] = Systematic(
      'JET_JER_NP2',
      var_up='JET_JER_NP2_UP',
      var_dn='JET_JER_NP2_DN',
      )                       
                       
JET_JER_NP3 = sys_dict['JET_JER_NP3'] = Systematic(
      'JET_JER_NP3',
      var_up='JET_JER_NP3_UP',
      var_dn='JET_JER_NP3_DN',
      )                       
                       
JET_JER_NP4 = sys_dict['JET_JER_NP4'] = Systematic(
      'JET_JER_NP4',
      var_up='JET_JER_NP4_UP',
      var_dn='JET_JER_NP4_DN',
      )                       
                       
JET_JER_NP5 = sys_dict['JET_JER_NP5'] = Systematic(
      'JET_JER_NP5',
      var_up='JET_JER_NP5_UP',
      var_dn='JET_JER_NP5_DN',
      )                       
                       
JET_JER_NP6 = sys_dict['JET_JER_NP6'] = Systematic(
      'JET_JER_NP6',
      var_up='JET_JER_NP6_UP',
      var_dn='JET_JER_NP6_DN',
      )                       
                       
JET_JER_NP7 = sys_dict['JET_JER_NP7'] = Systematic(
      'JET_JER_NP7',
      var_up='JET_JER_NP7_UP',
      var_dn='JET_JER_NP7_DN',
      )                       
                       
JET_JER_NP8 = sys_dict['JET_JER_NP8'] = Systematic(
      'JET_JER_NP8',
      var_up='JET_JER_NP8_UP',
      var_dn='JET_JER_NP8_DN',
      )                       

## Theory
# sys_list_theory = [
# ALPHA_SYS,
# PDFCHOICE_SYS,
# MUR_SYS,
# MUF_SYS,
# ]

ALPHA_SYS = sys_dict['ALPHA_SYS'] = Systematic(
        'ALPHA_SYS',
        var_up='MUR1_MUF1_PDF270000',
        var_dn='MUR1_MUF1_PDF269000',
        )

MUR_SYS = sys_dict['MUR_SYS'] = Systematic(
        'MUR_SYS',
        var_up='MUR2_MUF1_PDF261000',
        var_dn='MUR0.5_MUF1_PDF261000'
        )

MUF_SYS = sys_dict['MUF_SYS'] = Systematic(
        'MUF_SYS',
        var_up='MUR1_MUF2_PDF261000',
        var_dn='MUR1_MUF0.5_PDF261000'
        )


PDFCHOICE_SYS1 = Systematic(
        'PDFCHOICE_SYS1',
        var_up='MUR1_MUF1_PDF13000',
        var_dn=None,
        onesided=True,
        )

PDFCHOICE_SYS2 = Systematic(
        'PDFCHOICE_SYS2',
        var_up='MUR1_MUF1_PDF25300',
        var_dn=None,
        onesided=True,
        )

PDF_CHOICE = [PDFCHOICE_SYS1, PDFCHOICE_SYS2]

PDF_SYS = []
for PDFvar in range (1,101):
    PDFstr = str(PDFvar)
    while len(PDFstr) != 3:
        PDFstr = "0" + PDFstr
    # globals()['PDF261'+PDFstr+'_SYS'] = sys_dict['PDF261'+PDFstr+'_SYS'] = Systematic(
    temp = Systematic(
            'PDF261'+PDFstr+'_SYS',
            var_up='MUR1_MUF1_PDF261'+PDFstr,
            var_dn=None,
            onesided=True,
            )
    # PDF_SYS += [ sys_dict['PDF261'+PDFstr+'_SYS'] ]
    PDF_SYS += [ temp ]

QCD_SCALE = []
for qcd_var in ['MUR1_MUF2','MUR2_MUF1','MUR0.5_MUF1','MUR1_MUF0.5']:
    temp = Systematic(
            qcd_var + '_PDF261000',
            var_up=qcd_var + '_PDF261000',
            var_dn=None,
            onesided=True,
            )
    QCD_SCALE += [ temp ]

PDF_SYS_ENVELOPE = sys_dict['PDF_SYS_ENVELOPE'] = Systematic(name='PDF_SYS_ENVELOPE',
title=None,
var_up=None,
var_dn=None,
flat_err=None,
onesided=None,
envelope=True,
constituents=PDF_SYS
        )

PDF_COICE_ENVELOPE = sys_dict['PDF_COICE_ENVELOPE'] = Systematic(name='PDF_COICE_ENVELOPE',
title=None,
var_up=None,
var_dn=None,
flat_err=None,
onesided=None,
envelope=True,
constituents=PDF_CHOICE
        )

QCD_SCALE_ENVELOPE = sys_dict['QCD_SCALE_ENVELOPE'] = Systematic(name='QCD_SCALE_ENVELOPE',
title=None,
var_up=None,
var_dn=None,
flat_err=None,
onesided=None,
envelope=True,
constituents=QCD_SCALE
        )


## EOF
