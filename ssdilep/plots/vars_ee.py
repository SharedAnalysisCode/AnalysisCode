# encoding: utf-8
'''
vars_ee.py
description:
variables for the ee channel
'''

## modules
from var import Var
from funcs import generateLogBins

## Cutflows
## ---------------------------------------
cutflow_ZWindowSS           = Var(name = 'cutflow_ZWindowSS',log=False)
cutflow_weighted_ZWindowSS  = Var(name = 'cutflow_weighted_ZWindowSS',log=False)
cutflow_ZWindowOS           = Var(name = 'cutflow_ZWindowOS',log=False)
cutflow_weighted_ZWindowOS  = Var(name = 'cutflow_weighted_ZWindowOS',log=False)

## Non-equidistant bins
## ---------------------------------------
bins_pt = generateLogBins(35,30,2000)
bins_invM = generateLogBins(50,130,2000)
bins_Zpeak = [50,70,74,77,80,82,83,84,85,86,87,88,89,90,91,92,93,94,95,97,99,102,105,110,130]
bins_Zpeak2 = [50,80,100,130]
bins_met = generateLogBins(15,1,1000)



## Event variables
## ---------------------------------------
averageIntPerXing = Var(name = 'averageIntPerXing',
              path  = 'event',
              xmin  = 0,
              xmax  = 45,
              log   = False,
              )

actualIntPerXing = Var(name = 'actualIntPerXing',
              path  = 'event',
              xmin  = 0,
              xmax  = 45,
              log   = False,
              )

NPV = Var(name = 'NPV',
              path  = 'event',
              xmin  = 0,
              xmax  = 35.,
              log   = False,
              )

nelectrons = Var(name = 'nelectrons',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
              )
njets = Var(name = 'njets',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
            )
invMass = Var(name='invMass',
              path   = 'event',
              xmin   = 130,
              xmax   = 2000,
              rebin  = 1,
              rebinVar  = bins_invM,
              #rebinVar  = bins_Zpeak2,
              log    = True,
              logx   = True
              )
ZbosonPt = Var(name='ZbosonPt',
              path   = 'event',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              rebinVar  = bins_pt,
              log    = True,
              logx   = True,
               )
ZbosonEta = Var(name='ZbosonEta',
                path   = 'event',
                xmin   = -6,
                xmax   = 6,
                rebin  = 2,
                log    = False,
                )

chargeFlipHist = Var(name='chargeFlipHist',
                path   = 'event',
                xmin   = 0,
                xmax   = 10000,
                rebin  = 1,
                log    = False,
                )

el_pt_eta_all = Var(name='el_pt_eta_all',
                path   = 'electrons',
                )

el_pt_eta_chf2 = Var(name='el_pt_eta_chf2',
                path   = 'electrons',
                )

el_pt_eta_chf4 = Var(name='el_pt_eta_chf4',
                path   = 'electrons',
                )

el_t_2D_pt_eta = Var(name='el_t_2D_pt_eta',
                path   = 'electrons',
                )

el_l_2D_pt_eta = Var(name='el_l_2D_pt_eta',
                path   = 'electrons',
                )

el_sl_2D_pt_eta = Var(name='el_sl_2D_pt_eta',
                path   = 'electrons',
                )

## MET
## ---------------------------------------

met_trk_et = Var(name='met_trk_et',
                path   = 'met',
                xmin   = 0.,
                xmax   = 1000.,
                rebin  = 1,
                rebinVar  = [0] + bins_met,
                log    = True,
                logx   = True,
                )

met_clus_et = Var(name='met_clus_et',
                path   = 'met',
                xmin   = 0.,
                xmax   = 1000.,
                rebin  = 1,
                rebinVar  = [0] + bins_met,
                log    = True,
                logx   = True,
                )

## Single muon variables
## ---------------------------------------
el_t_pt = Var(name = 'el_t_pt',
              path   = 'electrons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              #rebinVar  = bins_pt,
              log    = True,
              logx   = True,
              )

el_l_pt = Var(name = 'el_l_pt',
              path   = 'electrons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              #rebinVar  = bins_pt,
              log    = True,
              logx   = True,
              )

el_sl_pt = Var(name = 'el_sl_pt',
              path   = 'electrons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              #rebinVar  = bins_pt,
              log    = True,
              logx   = True,
              )

el_lead_pt = Var(name = 'el_lead_pt',
              path   = 'electrons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              rebinVar  = bins_pt,
              log    = True,
              logx   = True,
              )

el_sublead_pt = Var(name = 'el_sublead_pt',
              path   = 'electrons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              rebinVar  = bins_pt,
              log    = True,
              logx   = True,
              )
el_lead_eta = Var(name = 'el_lead_eta',
              path    = 'electrons',
              xmin    = -2.5,
              xmax    = 2.5,
              #rebin   = 5,
              log     = False,
              )

el_sublead_eta = Var(name = 'el_sublead_eta',
              path    = 'electrons',
              xmin    = -2.5,
              xmax    = 2.5,
              #rebin   = 4,
              log     = False,
              )

el_lead_phi = Var(name = 'el_lead_phi',
              path    = 'electrons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

el_sublead_phi = Var(name = 'el_sublead_phi',
              path    = 'electrons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

el_lead_trkd0 = Var(name = 'el_lead_trkd0',
              path    = 'electrons',
              xmin    = -0.4,
              xmax    = 0.4,
              rebin  = 2,
              log     = False,
              )

el_sublead_trkd0 = Var(name = 'el_sublead_trkd0',
              path    = 'electrons',
              xmin    = -0.4,
              xmax    = 0.4,
              rebin   = 2,
              log     = False,
              )

el_lead_trkd0sig = Var(name = 'el_lead_trkd0sig',
              path    = 'electrons',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 1,
              log     = False,
              )

el_sublead_trkd0sig = Var(name = 'el_sublead_trkd0sig',
              path    = 'electrons',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 1,
              log     = False,
              )

el_lead_trkz0 = Var(name = 'el_lead_trkz0',
              path    = 'electrons',
              xmin    = -2.0,
              xmax    = 2.0,
              rebin   = 2,
              log     = False,
              )

el_sublead_trkz0 = Var(name = 'el_sublead_trkz0',
              path    = 'electrons',
              xmin    = -2.0,
              xmax    = 2.0,
              rebin   = 2,
              log     = False,
              )

el_lead_trkz0sintheta = Var(name = 'el_lead_trkz0sintheta',
              path    = 'electrons',
              xmin    = -0.8,
              xmax    = 0.8,
              rebin   = 2,
              log     = False,
              )

el_sublead_trkz0sintheta = Var(name = 'el_sublead_trkz0sintheta',
              path    = 'electrons',
              xmin    = -0.8,
              xmax    = 0.8,
              rebin   = 2,
              log     = False,
              )

# isolation
el_lead_topoetcone20 = Var(name = 'el_lead_topoetcone20',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )

el_lead_topoetcone30 = Var(name = 'el_lead_topoetcone30',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_topoetcone40 = Var(name = 'el_lead_topoetcone40',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_ptvarcone20 = Var(name = 'el_lead_ptvarcone20',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_ptvarcone30 = Var(name = 'el_lead_ptvarcone30',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_ptvarcone40 = Var(name = 'el_lead_ptvarcone40',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_ptcone20 = Var(name = 'el_lead_ptcone20',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_ptcone30 = Var(name = 'el_lead_ptcone30',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_ptcone40 = Var(name = 'el_lead_ptcone40',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )

vars_list = []
vars_list.append(averageIntPerXing)
vars_list.append(actualIntPerXing)
vars_list.append(NPV)
vars_list.append(nelectrons)
vars_list.append(invMass)
vars_list.append(met_trk_et)
vars_list.append(met_clus_et)
vars_list.append(el_lead_pt)
vars_list.append(el_sublead_pt)
vars_list.append(el_lead_eta)
vars_list.append(el_sublead_eta)
vars_list.append(el_lead_phi)
vars_list.append(el_sublead_phi)
vars_list.append(el_lead_trkd0)
vars_list.append(el_sublead_trkd0)
vars_list.append(el_lead_trkd0sig)
vars_list.append(el_sublead_trkd0sig)
vars_list.append(el_lead_trkz0)
#vars_list.append(el_sublead_trkz0)
vars_list.append(el_lead_trkz0sintheta)
vars_list.append(ZbosonPt)
vars_list.append(ZbosonEta)
vars_list.append(chargeFlipHist)
vars_list.append(el_pt_eta_all)
vars_list.append(el_pt_eta_chf2)
vars_list.append(el_pt_eta_chf4)
vars_list.append(el_sl_2D_pt_eta)
vars_list.append(el_t_2D_pt_eta)
vars_list.append(el_l_2D_pt_eta)
vars_list.append(el_l_pt)
vars_list.append(el_t_pt)
vars_list.append(el_sl_pt)
#vars_list.append(el_sublead_trkz0sintheta)

vars_dict = {}
for var in vars_list: vars_dict[var.name] = var.__dict__

## EOF


