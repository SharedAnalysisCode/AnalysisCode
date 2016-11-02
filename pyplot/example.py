import ROOT
import os
import re
import fileio
import logging
import core
import fileio
import hist 
import analysers

import file_config_v00_03 as samples

## logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


## setup core tools
core.setup( 
        batch_mode = True,
        )


## selection
base_selection = [
    core.Cut('tau_pt[0]>50.e3'),
    core.Cut('tau_pt[1]>50.e3'),
    core.Cut('tau_numTrack[0]==1||tau_numTrack[0]==3'),
    core.Cut('tau_numTrack[1]==1||tau_numTrack[1]==3'),
    core.Cut('TMath::Abs(tau_charge[0])==1'),
    core.Cut('TMath::Abs(tau_charge[1])==1'),
    core.Cut('TMath::ACos(TMath::Cos(tau_phi[0]-tau_phi[1]))>2.7'),
    core.Cut('EF_2tau38T_medium1'),
    ]

sel_sig = [
    core.Cut('tau_JetBDTSigMedium[0]'),
    core.Cut('tau_JetBDTSigMedium[1]'),
    core.Cut('tau_charge[0]*tau_charge[1]<0'),
    ]

sel_ss = [
    core.Cut('tau_JetBDTSigMedium[0]'),
    core.Cut('tau_JetBDTSigMedium[1]'),
    core.Cut('tau_charge[0]*tau_charge[1]>0'),
    ]


selector_sig = core.Selector('reg_sig',base_selection+sel_sig)
selector_ss = core.Selector('reg_ss',base_selection+sel_ss)



## variable details 
vd = core.VarDetails(
        'eff_trans_mass', core.Var('eff_trans_mass/1000.'), 
        _xmin=0.,_xmax=2000.,
        _xtitle='m_{T}^{tot}',_xunit='GeV'
        )


## plot details
pd = core.PlotDetails(var_details=vd,selector=selector_sig,target_lumi=10000.)



## do plotting
hg = hist.HistGen()

for s in samples.all_samples:
    h = hg.hist(pd.clone(sample=s))


'''
ana = analysers.SimpleAnalysis(
    hist_gen = hg,
    def_sel = selector_sig,
    def_vd  = details,
    )
ana.add_sig(samples.Zprime500tautau)
for s in samples.mc_bkg: ana.add_bkg(s)
ana.execute()


ana_ss = analysers.SimpleAnalysis(
    hist_gen = hg,
    def_sel = selector_ss,
    def_vd  = details,
    )
ana_ss.add_sig(samples.Zprime500tautau)
for s in samples.mc_bkg: ana_ss.add_bkg(s)
ana_ss.execute()
'''




    

#h = hg.hist(samples.others,details,selector)
#h.Draw()





hg.save_hists('test.root')




'''
pg.execute()

fout = fileio.new_file( 'test.root' )
for var, val in pg.hists.items():
    for s, h in val.items():
        fout.WriteTObject(h)
fout.Close()
'''

#h = core.gen_hist(s,details,selection)

#h = pg.hists['tau1_pt']['Zprime500tautau']
#h.Scale(s.scale(10000.))

#c = ROOT.TCanvas('c','c')
#h.Draw()
#c.SaveAs('test.eps')













