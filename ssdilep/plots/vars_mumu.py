# encoding: utf-8
'''
vars_mumu.py
description:
variables for the mumu channel
'''

## modules
from var import Var

## Cutflows
## ---------------------------------------
cutflow_weighted          = Var(name = 'cutflow_weighted_mumu',log=False)
cutflow                   = Var(name = 'cutflow_mumu',log=False)
cutflow_weighted_mu_pairs = Var(name = 'cutflow_weighted_mumu_mu_pairs',log=False)
cutflow_mu_pairs          = Var(name = 'cutflow_mumu_mu_pairs',log=False)



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

nmuons = Var(name = 'nmuons',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
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

nmuonpairs = Var(name = 'nmuonpairs',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
              )

mujet_dphi = Var(name = 'mujet_dphi',
              path    = 'event',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 2,
              log     = False,
              )

scdphi = Var(name     = 'scdphi',
              path    = 'event',
              xmin    = -2.,
              xmax    = 2.,
              rebin   = 2,
              log     = False,
              )

muons_mVis = Var(name     = 'muons_mVis',
              path    = 'event',
              xmin    = 0.,
              xmax    = 500.,
              rebin   = 40,
              log     = False,
              )

muons_mTtot = Var(name     = 'muons_mTtot',
              path    = 'event',
              xmin    = 0.,
              xmax    = 500.,
              rebin   = 40,
              log     = False,
              )

muons_dphi = Var(name = 'muons_dphi',
              path    = 'event',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 2,
              log     = False,
              )

muons_deta = Var(name = 'muons_deta',
              path    = 'event',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin  = 2,
              log     = False,
              )

muons_chargeprod = Var(name = 'muons_chargeprod',
              path    = 'event',
              xmin    = -2,
              xmax    = 2,
              #rebin  = 10,
              log     = False,
              )


## Single muon variables
## ---------------------------------------
mulead_pt = Var(name = 'mulead_pt',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 400.,
              rebin  = 20,
              log    = True,
              )

musublead_pt = Var(name = 'musublead_pt',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 400.,
              rebin  = 20,
              log    = True,
              )

mulead_eta = Var(name = 'mulead_eta',
              path    = 'muons',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin   = 4,
              log     = False,
              )

musublead_eta = Var(name = 'musublead_eta',
              path    = 'muons',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin   = 4,
              log     = False,
              )

mulead_phi = Var(name = 'mulead_phi',
              path    = 'muons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

musublead_phi = Var(name = 'musublead_phi',
              path    = 'muons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

mulead_trkd0 = Var(name = 'mulead_trkd0',
              path    = 'muons',
              xmin    = -0.4,
              xmax    = 0.4,
              rebin  = 2,
              log     = False,
              )

musublead_trkd0 = Var(name = 'musublead_trkd0',
              path    = 'muons',
              xmin    = -0.4,
              xmax    = 0.4,
              rebin   = 2,
              log     = False,
              )

mulead_trkd0sig = Var(name = 'mulead_trkd0sig',
              path    = 'muons',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 3,
              log     = False,
              )

musublead_trkd0sig = Var(name = 'musublead_trkd0sig',
              path    = 'muons',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 3,
              log     = False,
              )

mulead_trkz0 = Var(name = 'mulead_trkz0',
              path    = 'muons',
              xmin    = -2.0,
              xmax    = 2.0,
              rebin   = 2,
              log     = False,
              )

musublead_trkz0 = Var(name = 'musublead_trkz0',
              path    = 'muons',
              xmin    = -2.0,
              xmax    = 2.0,
              rebin   = 2,
              log     = False,
              )

mulead_trkz0sintheta = Var(name = 'mulead_trkz0sintheta',
              path    = 'muons',
              xmin    = -0.8,
              xmax    = 0.8,
              rebin   = 2,
              log     = False,
              )

musublead_trkz0sintheta = Var(name = 'musublead_trkz0sintheta',
              path    = 'muons',
              xmin    = -0.8,
              xmax    = 0.8,
              rebin   = 2,
              log     = False,
              )

# isolation
mulead_topoetcone20 = Var(name = 'mulead_topoetcone20',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )

mulead_topoetcone30 = Var(name = 'mulead_topoetcone30',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
mulead_topoetcone40 = Var(name = 'mulead_topoetcone40',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
mulead_ptvarcone20 = Var(name = 'mulead_ptvarcone20',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
mulead_ptvarcone30 = Var(name = 'mulead_ptvarcone30',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
mulead_ptvarcone40 = Var(name = 'mulead_ptvarcone40',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
mulead_ptcone20 = Var(name = 'mulead_ptcone20',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
mulead_ptcone30 = Var(name = 'mulead_ptcone30',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )
mulead_ptcone40 = Var(name = 'mulead_ptcone40',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 3.5,
              rebin  = 100,
              log    = False,
              )

# jets
jetlead_pt = Var(name = 'jetlead_pt',
              path    = 'jets',
              xmin    = 0.,
              xmax    = 200.,
              rebin   = 5,
              log     = False,
              )


## MET variables
## ---------------------------------------
met_clus_et = Var(name = 'met_clus_et',
              path    = 'met',
              xmin    = 0.,
              xmax    = 200.,
              rebin   = 10,
              log     = False,
              )

met_clus_phi = Var(name = 'met_clus_phi',
              path    = 'met',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 2,
              log     = False,
              )

met_trk_et = Var(name = 'met_trk_et',
              path    = 'met',
              xmin    = 0.,
              xmax    = 200.,
              rebin   = 10,
              log     = False,
              )

met_trk_phi = Var(name = 'met_trk_phi',
              path    = 'met',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 2,
              log     = False,
              )

met_clus_sumet = Var(name = 'met_clus_sumet',
              path    = 'met',
              xmin    = 0.,
              xmax    = 1000.,
              rebin   = 50,
              log     = False,
              )

met_trk_sumet = Var(name = 'met_trk_sumet',
              path    = 'met',
              xmin    = 0.,
              xmax    = 1000.,
              rebin   = 50,
              log     = False,
              )


## Di-muon variables
## ---------------------------------------
mumu_mulead_pt = Var(name = 'mumu_mulead_pt',
              path   = 'pairs',
              xmin   = 0.,
              xmax   = 500.,
              rebin  = 20,
              log    = False,
              )

mumu_musublead_pt = Var(name = 'mumu_musublead_pt',
              path   = 'pairs',
              xmin   = 0.,
              xmax   = 500.,
              rebin  = 20,
              log    = False,
              )

mumu_mulead_eta = Var(name = 'mumu_mulead_eta',
              path    = 'pairs',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin  = 5,
              log     = False,
              )

mumu_musublead_eta = Var(name = 'mumu_musublead_eta',
              path    = 'pairs',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin  = 5,
              log     = False,
              )

mumu_mulead_phi = Var(name = 'mumu_mulead_phi',
              path    = 'pairs',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin  = 5,
              log     = False,
              )

mumu_musublead_phi = Var(name = 'mumu_musublead_phi',
              path    = 'pairs',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin  = 5,
              log     = False,
              )

mumu_sumcosdphi = Var(name = 'mumu_sumcosdphi',
              path    = 'pairs',
              xmin    = -2.,
              xmax    = 2.,
              rebin   = 5,
              log     = False,
              )

mumu_mVis = Var(name = 'mumu_mVis',
              path    = 'pairs',
              xmin    = 0.,
              xmax    = 500.,
              rebin   = 20,
              log     = False,
              )

mumu_mTtot = Var(name = 'mumu_mTtot',
              path    = 'pairs',
              xmin    = 0.,
              xmax    = 500.,
              rebin   = 20,
              log     = False,
              )

mumu_angle = Var(name = 'mumu_angle',
              path    = 'pairs',
              xmin    = 0.,
              xmax    = 3.2,
              rebin   = 20,
              log     = False,
              )


vars_list = []
vars_list.append(averageIntPerXing)
vars_list.append(actualIntPerXing)
vars_list.append(NPV)
vars_list.append(nmuons)
vars_list.append(nelectrons)
vars_list.append(njets)
vars_list.append(nmuonpairs)
vars_list.append(mujet_dphi)
#vars_list.append(scdphi)
#vars_list.append(muons_dphi)
#vars_list.append(muons_deta)
#vars_list.append(muons_mTtot)
#vars_list.append(muons_mVis)
#vars_list.append(muons_chargeprod)

vars_list.append(mulead_pt)
#vars_list.append(musublead_pt)
vars_list.append(mulead_eta)
#vars_list.append(musublead_eta)
vars_list.append(mulead_phi)
#vars_list.append(musublead_phi)
vars_list.append(mulead_trkd0)
#vars_list.append(musublead_trkd0)
vars_list.append(mulead_trkd0sig)
#vars_list.append(musublead_trkd0sig)
vars_list.append(mulead_trkz0)
#vars_list.append(musublead_trkz0)
vars_list.append(mulead_trkz0sintheta)
#vars_list.append(musublead_trkz0sintheta)

#vars_list.append(jetlead_pt)

#vars_list.append(mulead_topoetcone20)
#vars_list.append(mulead_topoetcone30)
#vars_list.append(mulead_topoetcone40)
#vars_list.append(mulead_ptvarcone20)
#vars_list.append(mulead_ptvarcone30)
#vars_list.append(mulead_ptvarcone40)
#vars_list.append(mulead_ptcone20)
#vars_list.append(mulead_ptcone30)
#vars_list.append(mulead_ptcone40)


vars_list.append(met_clus_et)
vars_list.append(met_clus_phi)
vars_list.append(met_clus_sumet)
vars_list.append(met_trk_et)
vars_list.append(met_trk_phi)
vars_list.append(met_trk_sumet)
"""
vars_list.append(mumu_mulead_pt)
vars_list.append(mumu_musublead_pt)
vars_list.append(mumu_mulead_eta)
vars_list.append(mumu_musublead_eta)
vars_list.append(mumu_mulead_phi)
vars_list.append(mumu_musublead_phi)
vars_list.append(mumu_mVis)
vars_list.append(mumu_mTtot)
vars_list.append(mumu_sumcosdphi)
vars_list.append(mumu_angle)
"""

vars_dict = {}
for var in vars_list: vars_dict[var.name] = var.__dict__


## EOF


