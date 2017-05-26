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

cutflow_presel = Var(name = 'cutflow_presel', log=False, path="")

## Non-equidistant bins
## ---------------------------------------
bins_pt = generateLogBins(35,30,2000)
bins_pt_2 = generateLogBins(20,30,1000)
bins_pt_SR = generateLogBins(20,30,2000)
bins_Zpt_SR = [0] + generateLogBins(20,10,3000)
bins_Zpt_SR_2 = [0,1,2,3,4,5,6,7,8,9] + generateLogBins(50,10,3000)
bins_mt = generateLogBins(50,50,2000)
bins_HT = generateLogBins(50,60,4000)
bins_invM = generateLogBins(50,130,2000)
bins_invM_fit = generateLogBins(30,130,2000)
bins_invMLong = generateLogBins(150,130,10000)
bins_invMassSR2EL = generateLogBins(10,200,900)
# bins_invMassSR2ELall = [200] + [x for x in range(225,875,50)] + [865,925,975,1025,2000]
bins_invMassSR2ELall = [200] + [x for x in range(325,1525,100)]
bins_invMassSR3EL = generateLogBins(5,200,1000)
bins_invMassSR3ELall = [200] + [x for x in range(425,2025,200)]
bins_invM_2 = generateLogBins(15,130,200)
bins_invM_3 = generateLogBins(8,130,200)
bins_invM_4 = generateLogBins(6,90,200)
bins_Zpeak = [50,70,74,77,80,82,83,84,85,86,87,88,89,90,91,92,93,94,95,97,99,102,105,110,130]
bins_Zpeak2 = [50,80,100,130]
bins_met = generateLogBins(15,1,1000)
bins_met_2 = generateLogBins(50,25,2000)

eta_cf_bins = [-2.5, -2.4, -2.3, -2.2, -2.1, -2.0, -1.9, -1.8, -1.7, -1.6, -1.52, -1.37, -1.20, -1.1, -1.0, -0.9, -0.7, -0.45, 0.0, 0.45, 0.7, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
pt_cf_bins  = [30., 34., 38., 43., 48., 55., 62., 69., 78.0, 88.0, 100., 115., 140., 200., 2000.]


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

nleptons = Var(name = 'nleptons',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
              )

nsspairs = Var(name = 'nsspairs',
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

nbjets = Var(name = 'nbjets',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
            )

HT = Var(name='HT',
              path   = 'event',
              xmin   = 60,
              xmax   = 4000,
              rebin  = 1,
              rebinVar  = bins_HT,
              #rebinVar  = bins_Zpeak2,
              log    = False,
              logx   = True
              )

HTmet = Var(name='HTmet',
              path   = 'event',
              xmin   = 60,
              xmax   = 4000,
              rebin  = 1,
              rebinVar  = bins_HT,
              #rebinVar  = bins_Zpeak2,
              log    = False,
              logx   = True
              )

mTtot = Var(name='mTtot',
              path   = 'event',
              xmin   = 30,
              xmax   = 4000,
              rebin  = 1,
              rebinVar  = [30,40,50] + bins_HT,
              #rebinVar  = bins_Zpeak2,
              log    = False,
              logx   = True
              )

DR = Var(name='DR',
              path   = 'event',
              xmin   = 0,
              xmax   = 6,
              rebin  = 1,
              log    = True,
              )

DR2 = Var(name='DR',
              path   = 'event',
              xmin   = 0,
              xmax   = 6,
              rebin  = 2,
              log    = True,
              )

DR4 = Var(name='DR',
              path   = 'event',
              xmin   = 0,
              xmax   = 6,
              rebin  = 4,
              log    = True,
              )

invMassOS1 = Var(name='invMassOS1',
              path   = 'event',
              xmin   = 0,
              xmax   = 350,
              rebin  = 20,
              #rebinVar  = bins_invM,
              #rebinVar  = bins_Zpeak2,
              log    = False,
              logx   = False
              )

invMassOS2 = Var(name='invMassOS2',
              path   = 'event',
              xmin   = 0,
              xmax   = 350,
              rebin  = 20,
              #rebinVar  = bins_invM,
              #rebinVar  = bins_Zpeak2,
              log    = False,
              logx   = False
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

invMass_fit = Var(name='invMass',
              path   = 'event',
              xmin   = 130,
              xmax   = 2000,
              rebin  = 1,
              rebinVar  = bins_invM_fit,
              #rebinVar  = bins_Zpeak2,
              log    = True,
              logx   = True
              )

invMassLong = Var(name='invMass',
              path   = 'event',
              xmin   = 130,
              xmax   = 10000,
              rebin  = 1,
              rebinVar  = bins_invMLong,
              #rebinVar  = bins_Zpeak2,
              log    = True,
              logx   = True
              )

invMassSR2EL = Var(name='invMass',
              path   = 'event',
              xmin   = 200,
              xmax   = 900,
              rebin  = 1,
              rebinVar  = bins_invMassSR2EL,
              log    = True,
              logx   = True
              )

invMassSR2ELall = Var(name='invMass',
              path   = 'event',
              xmin   = 200,
              xmax   = 975,
              rebin  = 1,
              rebinVar  = bins_invMassSR2ELall,
              log    = False,
              logx   = False
              )

invMassSR3EL = Var(name='invMass',
              path   = 'event',
              xmin   = 200,
              xmax   = 1000,
              rebin  = 1,
              rebinVar  = bins_invMassSR3EL,
              log    = False,
              logx   = True
              )

invMassSR3ELall = Var(name='invMass',
              path   = 'event',
              xmin   = 200,
              xmax   = 1825,
              rebin  = 1,
              rebinVar  = bins_invMassSR3ELall,
              log    = False,
              logx   = False
              )

invMass_2 = Var(name='invMass',
              path   = 'event',
              xmin   = 120,
              xmax   = 210,
              rebin  = 1,
              rebinVar  = bins_invM_2,
              #rebinVar  = bins_Zpeak2,
              log    = False,
              logx   = False,
              )

invMass_3 = Var(name='invMass',
              path   = 'event',
              xmin   = 120,
              xmax   = 210,
              rebin  = 1,
              rebinVar  = bins_invM_3,
              #rebinVar  = bins_Zpeak2,
              log    = False,
              logx   = False,
              )

invMass_4 = Var(name='invMass',
              path   = 'event',
              xmin   = 80,
              xmax   = 210,
              rebin  = 1,
              rebinVar  = bins_invM_4,
              log    = False,
              logx   = False,
              )

invMassPeak = Var(name='invMass',
              path   = 'event',
              xmin   = 71.5,
              xmax   = 110,
              rebin  = 10,
              #rebinVar  = bins_invM,
              #rebinVar  = bins_Zpeak2,
              log    = True,
              )

invMassPeak_2 = Var(name='invMass',
              path   = 'event',
              xmin   = 71.5,
              xmax   = 110,
              rebin  = 10,
              #rebinVar  = bins_invM,
              #rebinVar  = bins_Zpeak2,
              log    = True,
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
ZbosonPt_2 = Var(name='ZbosonPt',
              path   = 'event',
              xmin   = 30.,
              xmax   = 500.,
              rebin  = 1,
              rebinVar  = bins_pt_2,
              log    = False,
              logx   = True,
               )
ZbosonPt_SR = Var(name='ZbosonPt',
              path   = 'event',
              xmin   = 0.,
              xmax   = 3000.,
              rebin  = 1,
              rebinVar  = bins_Zpt_SR,
              log    = False,
              logx   = True,
               )
ZbosonPt_SR_2 = Var(name='ZbosonPt',
              path   = 'event',
              xmin   = 0.,
              xmax   = 3000.,
              rebin  = 1,
              rebinVar  = bins_Zpt_SR_2,
              log    = False,
              logx   = True,
               )
ZbosonEta = Var(name='ZbosonEta',
                path   = 'event',
                xmin   = -6,
                xmax   = 6,
                rebin  = 2,
                log    = False,
                )

ZbosonEta_2 = Var(name='ZbosonEta',
                path   = 'event',
                xmin   = -6,
                xmax   = 6,
                rebin  = 10,
                log    = False,
                )

chargeFlipHist = Var(name='chargeFlipHist',
                path   = 'event',
                xmin   = 0,
                xmax   = 10000,
                rebin  = 1,
                log    = False,
                )

el_lead_pt_eta = Var(name='el_lead_pt_eta',
                path   = 'leptons',
                )

el_sublead_pt_eta = Var(name='el_sublead_pt_eta',
                path   = 'leptons',
                )

el_pt_eta = Var(name='el_pt_eta',
                path   = 'leptons',
                )

el_pt_eta_all = Var(name='el_pt_eta_all',
                path   = 'leptons',
                )

el_pt_eta_chf2 = Var(name='el_pt_eta_chf2',
                path   = 'leptons',
                )

el_pt_eta_chf4 = Var(name='el_pt_eta_chf4',
                path   = 'leptons',
                )

el_t_2D_pt_Ceta = Var(name='el_t_2D_pt_Ceta',
                path   = 'leptons',
                )

el_l_2D_pt_Ceta = Var(name='el_l_2D_pt_Ceta',
                path   = 'leptons',
                )

el_sl_2D_pt_Ceta = Var(name='el_sl_2D_pt_Ceta',
                path   = 'leptons',
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

met_trk_et_WJets = Var(name='met_trk_et',
                path   = 'met',
                xmin   = 20.,
                xmax   = 2000.,
                rebin  = 1,
                rebinVar  = bins_met_2,
                log    = True,
                logx   = True,
                )

met_trk_et_WJets_tight = Var(name='met_trk_et',
                path   = 'met',
                xmin   = 20.,
                xmax   = 65.,
                rebin  = 2,
                #rebinVar  = bins_met_2,
                log    = False,
                logx   = False,
                )

met_trk_mt = Var(name='met_trk_mt',
                path   = 'met',
                xmin   = 40.,
                xmax   = 2000.,
                rebin  = 1,
                rebinVar  = bins_mt,
                log    = True,
                logx   = True,
                )

met_trk_mt_tight = Var(name='met_trk_mt',
                path   = 'met',
                xmin   = 40.,
                xmax   = 130.,
                rebin  = 2,
                #rebinVar  = bins_mt,
                log    = False,
                logx   = False,
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
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 4,
              rebinVar  = bins_pt,
              log    = True,
              logx   = True,
              do_ratio_plot = False,
              label = "tight",
              )

el_l_pt = Var(name = 'el_l_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 4,
              rebinVar  = bins_pt,
              log    = True,
              logx   = True,
              do_ratio_plot = False,
              label = "loose",
              )

el_sl_pt = Var(name = 'el_sl_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 4,
              rebinVar  = bins_pt,
              log    = True,
              logx   = True,
              do_ratio_plot = False,
              label = "strictly loose",
              )

el_lead_pt = Var(name = 'el_lead_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              rebinVar  = bins_pt,
              log    = True,
              logx   = True,
              )


el_lead_pt_2 = Var(name = 'el_lead_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 500.,
              rebin  = 1,
              rebinVar  = bins_pt_2,
              log    = False,
              logx   = True,
              )

el_pt = Var(name = 'el_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              rebinVar  = bins_pt,
              log    = True,
              logx   = True,
              )

el_random_pt = Var(name = 'el_random_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              rebinVar  = bins_pt,
              log    = True,
              logx   = True,
              )

el_pt_cf = Var(name = 'el_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              rebinVar  = pt_cf_bins,
              log    = True,
              logx   = True,
              )

el_lead_pt_cf = Var(name = 'el_lead_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              rebinVar  = pt_cf_bins,
              log    = True,
              logx   = True,
              )

el_sublead_pt_cf = Var(name = 'el_sublead_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              rebinVar  = pt_cf_bins,
              log    = True,
              logx   = True,
              )

ZbosonPt_cf = Var(name='ZbosonPt',
              path   = 'event',
              xmin   = 10,
              xmax   = 2000.,
              rebin  = 1,
              rebinVar  = pt_cf_bins,
              log    = True,
              logx   = True,
              )

el_sublead_pt = Var(name = 'el_sublead_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              rebinVar  = bins_pt,
              log    = True,
              logx   = True,
              )

el_sublead_pt_2 = Var(name = 'el_sublead_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 500.,
              rebin  = 1,
              rebinVar  = bins_pt_2,
              log    = False,
              logx   = True,
              )

el_third_pt_2 = Var(name = 'el_third_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 500.,
              rebin  = 1,
              rebinVar  = bins_pt_2,
              log    = False,
              logx   = True,
              )

el_third_pt_SR = Var(name = 'el_third_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 2000.,
              rebin  = 1,
              rebinVar  = bins_pt_SR,
              log    = False,
              logx   = True,
              )

el_lead_eta = Var(name = 'el_lead_eta',
              path    = 'leptons',
              xmin    = -2.47,
              xmax    = 2.47,
              #rebin   = 5,
              log     = False,
              )

el_lead_eta_2 = Var(name = 'el_lead_eta',
              path    = 'leptons',
              xmin    = -2.47,
              xmax    = 2.47,
              rebin   = 5,
              log     = False,
              )

el_eta = Var(name = 'el_eta',
              path    = 'leptons',
              xmin    = -2.47,
              xmax    = 2.47,
              #rebin   = 5,
              log     = False,
              )

el_eta_cf = Var(name = 'el_eta',
              path    = 'leptons',
              xmin    = -2.47,
              xmax    = 2.47,
              rebin  = 1,
              rebinVar  = eta_cf_bins,
              log     = False,
              )

el_lead_eta_cf = Var(name = 'el_lead_eta',
              path    = 'leptons',
              xmin    = -2.47,
              xmax    = 2.47,
              rebin  = 1,
              rebinVar  = eta_cf_bins,
              log     = False,
              )

el_sublead_eta_cf = Var(name = 'el_sublead_eta',
              path    = 'leptons',
              xmin    = -2.47,
              xmax    = 2.47,
              rebin  = 1,
              rebinVar  = eta_cf_bins,
              log     = False,
              )

el_t_eta = Var(name = 'el_t_eta',
              path    = 'leptons',
              xmin    = -2.47,
              xmax    = 2.47,
              #rebin   = 5,
              log     = False,
              do_ratio_plot = False,
              )

el_l_eta = Var(name = 'el_l_eta',
              path    = 'leptons',
              xmin    = -2.47,
              xmax    = 2.47,
              #rebin   = 5,
              log     = False,
              do_ratio_plot = False,
              )

el_sl_eta = Var(name = 'el_sl_eta',
              path    = 'leptons',
              xmin    = -2.47,
              xmax    = 2.47,
              #rebin   = 5,
              log     = False,
              do_ratio_plot = False,
              )

el_sublead_eta = Var(name = 'el_sublead_eta',
              path    = 'leptons',
              xmin    = -2.47,
              xmax    = 2.47,
              #rebin   = 4,
              log     = False,
              )

el_sublead_eta_2 = Var(name = 'el_sublead_eta',
              path    = 'leptons',
              xmin    = -2.47,
              xmax    = 2.47,
              rebin   = 5,
              log     = False,
              )

el_third_eta_2 = Var(name = 'el_third_eta',
              path    = 'leptons',
              xmin    = -2.47,
              xmax    = 2.47,
              rebin   = 5,
              log     = False,
              )

el_lead_phi = Var(name = 'el_lead_phi',
              path    = 'leptons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 1,
              log     = False,
              )

el_lead_phi_2 = Var(name = 'el_lead_phi',
              path    = 'leptons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

el_phi = Var(name = 'el_phi',
              path    = 'leptons',
              xmin    = -3.14,
              xmax    = 3.14,
              rebin   = 1,
              log     = False,
              )

el_sublead_phi = Var(name = 'el_sublead_phi',
              path    = 'leptons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 1,
              log     = False,
              )

el_sublead_phi_2 = Var(name = 'el_sublead_phi',
              path    = 'leptons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

el_third_phi_2 = Var(name = 'el_third_phi',
              path    = 'leptons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 8,
              log     = False,
              )

el_lead_trkd0 = Var(name = 'el_lead_trkd0',
              path    = 'leptons',
              xmin    = -0.4,
              xmax    = 0.4,
              rebin  = 2,
              log     = False,
              )

el_sublead_trkd0 = Var(name = 'el_sublead_trkd0',
              path    = 'leptons',
              xmin    = -0.4,
              xmax    = 0.4,
              rebin   = 2,
              log     = False,
              )

el_lead_trkd0sig = Var(name = 'el_lead_trkd0sig',
              path    = 'leptons',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 1,
              log     = False,
              )

el_sublead_trkd0sig = Var(name = 'el_sublead_trkd0sig',
              path    = 'leptons',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 1,
              log     = False,
              )

el_lead_trkz0 = Var(name = 'el_lead_trkz0',
              path    = 'leptons',
              xmin    = -2.0,
              xmax    = 2.0,
              rebin   = 2,
              log     = False,
              )

el_sublead_trkz0 = Var(name = 'el_sublead_trkz0',
              path    = 'leptons',
              xmin    = -2.0,
              xmax    = 2.0,
              rebin   = 2,
              log     = False,
              )

el_lead_trkz0sintheta = Var(name = 'el_lead_trkz0sintheta',
              path    = 'leptons',
              xmin    = -0.8,
              xmax    = 0.8,
              rebin   = 2,
              log     = True,
              )

el_sublead_trkz0sintheta = Var(name = 'el_sublead_trkz0sintheta',
              path    = 'leptons',
              xmin    = -0.8,
              xmax    = 0.8,
              rebin   = 2,
              log     = True,
              )

# isolation
el_lead_topoetcone20 = Var(name = 'el_lead_topoetcone20',
              path   = 'leptons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )

el_lead_topoetcone30 = Var(name = 'el_lead_topoetcone30',
              path   = 'leptons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_topoetcone40 = Var(name = 'el_lead_topoetcone40',
              path   = 'leptons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_ptvarcone20 = Var(name = 'el_lead_ptvarcone20',
              path   = 'leptons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_ptvarcone30 = Var(name = 'el_lead_ptvarcone30',
              path   = 'leptons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_ptvarcone40 = Var(name = 'el_lead_ptvarcone40',
              path   = 'leptons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_ptcone20 = Var(name = 'el_lead_ptcone20',
              path   = 'leptons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_ptcone30 = Var(name = 'el_lead_ptcone30',
              path   = 'leptons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
el_lead_ptcone40 = Var(name = 'el_lead_ptcone40',
              path   = 'leptons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )


## ---------------------------------------
## ---------------------------------------

bins_invM_mu = generateLogBins(20,20,200)


## Event variables
## ---------------------------------------

invMass_mu = Var(name='invMass',
              path   = 'event',
              xmin   = 20,
              xmax   = 220,
              rebin  = 20,
              log    = False,
              logx   = False,
              )


invMass_mu2 = Var(name='invMass',
              path   = 'event',
              xmin   = 0,
              xmax   = 240,
              rebin  = 40,
              log    = False,
              logx   = False,
              )



vars_list = []
vars_list.append(averageIntPerXing)
vars_list.append(actualIntPerXing)
vars_list.append(NPV)
vars_list.append(nleptons)
vars_list.append(njets)
vars_list.append(nbjets)
vars_list.append(invMass)
vars_list.append(invMassOS2)
vars_list.append(invMassOS1)
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
vars_list.append(el_sublead_trkz0)
vars_list.append(el_lead_trkz0sintheta)
vars_list.append(ZbosonPt)
vars_list.append(ZbosonEta)
vars_list.append(chargeFlipHist)
vars_list.append(el_random_pt)
vars_list.append(el_pt_eta_all)
vars_list.append(el_pt_eta_chf2)
vars_list.append(el_pt_eta_chf4)
vars_list.append(el_pt_eta)
vars_list.append(el_lead_pt_eta)
vars_list.append(el_sublead_pt_eta)
vars_list.append(el_sl_2D_pt_Ceta)
vars_list.append(el_t_2D_pt_Ceta)
vars_list.append(el_l_2D_pt_Ceta)
vars_list.append(el_l_pt)
vars_list.append(el_t_pt)
vars_list.append(el_sl_pt)
vars_list.append(el_sublead_trkz0sintheta)
vars_list.append(el_t_eta)
vars_list.append(el_l_eta)
vars_list.append(el_sl_eta)
vars_list.append(el_pt)
vars_list.append(el_eta)
vars_list.append(met_trk_mt)
vars_list.append(el_phi)
vars_list.append(DR)

vars_dict = {}
for var in vars_list: vars_dict[var.name] = var.__dict__

vars_dict["invMassPeak"] = invMassPeak.__dict__
vars_dict["met_trk_et_WJets"] = met_trk_et_WJets.__dict__
vars_dict["met_trk_et_WJets_tight"] = met_trk_et_WJets_tight.__dict__
vars_dict["met_trk_mt_tight"] = met_trk_mt_tight.__dict__
vars_dict["el_lead_pt_2"] = el_lead_pt_2.__dict__
vars_dict["el_sublead_pt_2"] = el_sublead_pt_2.__dict__
vars_dict["el_third_pt_2"] = el_third_pt_2.__dict__
vars_dict["el_lead_eta_2"] = el_lead_eta_2.__dict__
vars_dict["el_third_eta_2"] = el_third_eta_2.__dict__
vars_dict["el_sublead_eta_2"] = el_sublead_eta_2.__dict__
vars_dict["el_lead_phi_2"] = el_lead_phi_2.__dict__
vars_dict["el_sublead_phi_2"] = el_sublead_phi_2.__dict__
vars_dict["el_third_phi_2"] = el_third_phi_2.__dict__
vars_dict["invMassPeak_2"] = invMassPeak_2.__dict__
vars_dict["ZbosonPt_2"] = ZbosonPt_2.__dict__
vars_dict["invMass_2"] = invMass_2.__dict__
vars_dict["invMassSR2EL"] = invMassSR2EL.__dict__
vars_dict["invMassSR3EL"] = invMassSR3EL.__dict__
vars_dict["invMassSR2ELall"] = invMassSR2ELall.__dict__
vars_dict["invMassSR3ELall"] = invMassSR3ELall.__dict__
vars_dict["invMass_3"] = invMass_3.__dict__
vars_dict["ZbosonEta_2"] = ZbosonEta_2.__dict__
vars_dict["invMass_4"] = invMass_4.__dict__
vars_dict["invMassLong"] = invMassLong.__dict__
vars_dict["cutflow_presel"] = cutflow_presel.__dict__
vars_dict["el_pt_cf"] = el_pt_cf.__dict__
vars_dict["el_sublead_pt_cf"] = el_sublead_pt_cf.__dict__
vars_dict["el_lead_pt_cf"] = el_lead_pt_cf.__dict__
vars_dict["ZbosonPt_cf"] = ZbosonPt_cf.__dict__
vars_dict["el_eta_cf"] = el_eta_cf.__dict__
vars_dict["el_lead_eta_cf"] = el_lead_eta_cf.__dict__
vars_dict["el_sublead_eta_cf"] = el_sublead_eta_cf.__dict__
vars_dict["el_third_pt_SR"] = el_third_pt_SR.__dict__
vars_dict["HT"] = HT.__dict__
vars_dict["HTmet"] = HTmet.__dict__
vars_dict["mTtot"] = mTtot.__dict__
vars_dict["DR2"] = DR2.__dict__
vars_dict["DR4"] = DR4.__dict__
vars_dict["ZbosonPt_SR"] = ZbosonPt_SR.__dict__
vars_dict["ZbosonPt_SR_2"] = ZbosonPt_SR_2.__dict__
vars_dict["invMass_fit"] = invMass_fit.__dict__
vars_dict["nsspairs"] = nsspairs.__dict__
vars_dict["invMass_mu"] = invMass_mu.__dict__
vars_dict["invMass_mu2"] = invMass_mu2.__dict__

## EOF


