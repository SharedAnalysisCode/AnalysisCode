# encoding: utf-8
'''
vars_mumu.py
description:
variables for the mumu channel
'''

## modules
from var import Var
from funcs import generateLogBins


## Cutflows
## ---------------------------------------
cutflow_weighted          = Var(name = 'cutflow_weighted_mumu',log=False)
cutflow                   = Var(name = 'cutflow_mumu',log=False)
cutflow_weighted_mu_pairs = Var(name = 'cutflow_weighted_mumu_mu_pairs',log=False)
cutflow_mu_pairs          = Var(name = 'cutflow_mumu_mu_pairs',log=False)
cutflow_ZWindowSS           = Var(name = 'cutflow_ZWindowSS',log=False)
cutflow_weighted_ZWindowSS  = Var(name = 'cutflow_weighted_ZWindowSS',log=False)
cutflow_ZWindowOS           = Var(name = 'cutflow_ZWindowOS',log=False)
cutflow_weighted_ZWindowOS  = Var(name = 'cutflow_weighted_ZWindowOS',log=False)

bins_invM_mu = generateLogBins(30,20,200)


## Event variables
## ---------------------------------------

invMass_mu = Var(name='invMass',
              path   = 'event',
              xmin   = 200,
              xmax   = 1000,
              rebin  = 1,
              rebinVar  = bins_invM_mu,
              log    = False,
              logx   = True
              )


vars_list = []
vars_list.append(invMass_mu)


vars_dict = {}
for var in vars_list: vars_dict[var.name] = var.__dict__


## EOF


