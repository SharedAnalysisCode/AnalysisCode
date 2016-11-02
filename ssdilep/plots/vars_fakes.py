# encoding: utf-8
'''
vars_mumu.py
description:
variables for the mumu channel
'''

## modules
from var import Var


## Single muon variables
## ---------------------------------------
mutight_pt = Var(name = 'mutight_pt',
              path   = 'mutight',
              xmin   = 0.,
              xmax   = 150.,
              rebin  = 10,
              log    = False,
              )

muloose_pt = Var(name = 'muloose_pt',
              path   = 'muloose',
              xmin   = 0.,
              xmax   = 150.,
              rebin  = 10,
              log    = False,
              )

mutight_eta = Var(name = 'mutight_eta',
              path    = 'mutight',
              xmin    = -2.5,
              xmax    = 2.5,
              #rebin  = 10,
              log     = False,
              )

muloose_eta = Var(name = 'muloose_eta',
              path    = 'muloose',
              xmin    = -2.5,
              xmax    = 2.5,
              #rebin  = 10,
              log     = False,
              )

mutight_phi = Var(name = 'mutight_phi',
              path    = 'mutight',
              xmin    = -3.2,
              xmax    = 3.2,
              #rebin  = 10,
              log     = False,
              )

muloose_phi = Var(name = 'muloose_phi',
              path    = 'muloose',
              xmin    = -3.2,
              xmax    = 3.2,
              #rebin  = 10,
              log     = False,
              )

mutight_trkd0 = Var(name = 'mutight_trkd0',
              path    = 'mutight',
              xmin    = -0.4,
              xmax    = 0.4,
              #rebin  = 10,
              log     = False,
              )

muloose_trkd0 = Var(name = 'muloose_trkd0',
              path    = 'muloose',
              xmin    = -0.4,
              xmax    = 0.4,
              #rebin  = 10,
              log     = False,
              )

mutight_trkd0sig = Var(name = 'mutight_trkd0sig',
              path    = 'mutight',
              xmin    = 0.,
              xmax    = 10.,
              rebin  = 10,
              log     = False,
              )

muloose_trkd0sig = Var(name = 'muloose_trkd0sig',
              path    = 'muloose',
              xmin    = 0.,
              xmax    = 10.,
              rebin  = 10,
              log     = False,
              )

mutight_trkz0 = Var(name = 'mutight_trkz0',
              path    = 'mutight',
              xmin    = -2.0,
              xmax    = 2.0,
              rebin  = 2,
              log     = False,
              )

muloose_trkz0 = Var(name = 'muloose_trkz0',
              path    = 'muloose',
              xmin    = -2.0,
              xmax    = 2.0,
              rebin  = 2,
              log     = False,
              )

mutight_trkz0sintheta = Var(name = 'mutight_trkz0sintheta',
              path    = 'mutight',
              xmin    = -1.0,
              xmax    = 1.0,
              rebin   = 5,
              log     = False,
              )

muloose_trkz0sintheta = Var(name = 'muloose_trkz0sintheta',
              path    = 'muloose',
              xmin    = -1.0,
              xmax    = 1.0,
              rebin   = 5,
              log     = False,
              )


vars_list = []
vars_list.append(mutight_pt)
vars_list.append(muloose_pt)
vars_list.append(mutight_eta)
vars_list.append(muloose_eta)
vars_list.append(mutight_phi)
vars_list.append(muloose_phi)
vars_list.append(mutight_trkd0)
vars_list.append(muloose_trkd0)
vars_list.append(mutight_trkd0sig)
vars_list.append(muloose_trkd0sig)
vars_list.append(mutight_trkz0)
vars_list.append(muloose_trkz0)
vars_list.append(mutight_trkz0sintheta)
vars_list.append(muloose_trkz0sintheta)

vars_dict = {}
for var in vars_list: vars_dict[var.name] = var.__dict__


## EOF


