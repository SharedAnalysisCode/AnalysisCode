#!/usr/bin/env python
"""
This is a test script for exercising most of the functionality provided by the
metaroot Python module. Since it shows many examples of what metaroot can do,
this script could also be used as somewhat of a tutorial.
"""


import ROOT, rootlogon
from array import array
import metaroot
from metaroot.tree import TreeMaker
from metaroot.file import HistGetter

# run in batch mode to avoid displaying graphics
ROOT.gROOT.SetBatch(True)

# set statistics display options
ROOT.gStyle.SetOptStat('iourme')

# make output directory
import os
dir = 'test'
if not os.path.exists(dir):
    os.mkdir(dir)
os.chdir(dir)


#------------------------------------------------------------------------------
# TreeMaker
#------------------------------------------------------------------------------
#
# This shows the use of the TreeMaker class to create a TTree filled with
# random pseudo data to be used in the following tests. This is just to
# generate some data for the following test plots. To see how to use the
# histogram formatting tools, you can skip down.

# distributions to draw random test tree from
f_w = ROOT.TF1('f_w', 'gaus', 0.0, 200.0)
f_w.SetParameters(1.0, 54.0, 7.0)
f_x = ROOT.TF1('f_x', 'TMath::CauchyDist(x, [0], [1])', 0.0, 200.0)
f_x.SetParameters(91.0, 3.5)
f_y = ROOT.TF1('f_y', 'expo', 0.0, 200.0)
f_y.SetParameters(0.0, -1.0/150.0)
f_z = ROOT.TF1('f_z', 'pol0', 0.0, 200.0)
f_z.SetParameter(0, 1.0)
f_n = ROOT.TF1('f_n', 'TMath::Poisson(x, [0])', 0 , 20)
f_n.SetParameter(0, 3)
f_a = ROOT.TF1('f_a', 'gaus', 0.0, 200.0)
f_a.SetParameters(1.0, 40.0, 15.0)
f_t = ROOT.TF1('f_t', '0.5*[0]*(1.0+TMath::Erf((x-[1])/[2]))', 0.0, 200.0)
f_t.SetParameters(0.9, 20.0, 6.0)

ROOT.gRandom.SetSeed(0)
nentries = 10000

# make tree
tm = TreeMaker(
        name = 'tree',
        vars =  ['w', 'x', 'y', 'z', 'a[10]', 'n', 'v[n]', 'p[n]'],
        types = ['f', 'f', 'f', 'f', 'f',     'i', 'f',    'i'],
        root_file_name = 'test.root')
for i in xrange(nentries):
    w = f_w.GetRandom()
    x = f_x.GetRandom()
    y = f_y.GetRandom()
    z = f_z.GetRandom()
    a = [f_a.GetRandom() for j in xrange(10)]
    n = int(f_n.GetRandom())
    v = []; p = []
    for j in xrange(n):
        v.append(f_y.GetRandom())
        if ROOT.gRandom.Uniform() < f_t.Eval(v[-1]):
            p.append(1)
        else:
            p.append(0)
    tm.fill([w, x, y, z, a, n, v, p])
tm.write()

# make some histograms
tfile = ROOT.TFile('test.root', 'UPDATE')
tree = tfile.Get('tree')
branches = [ b.GetName() for b in tree.GetListOfBranches() ]
for b in branches:
    hist_name = 'h_%s' % b
    if b in ('n'):
        h = ROOT.TH1F(hist_name, ';variable  [unit];', 21, -0.5, 20.5)
    elif b in ('p'):
        h = ROOT.TH1F(hist_name, ';variable  [unit];', 4, -1.5, 2.5)
    else:
        h = ROOT.TH1F(hist_name, ';variable  [unit];', 40, 0.0, 200.0)
    tree.Draw('%s>>%s' % (b, hist_name))
    h.Write()

h_numer = ROOT.TH1F('h_numer', ';variable  [unit];', 40, 0.0, 200.0)
tree.Draw('%s>>%s' % ('v', 'h_numer'), 'p')
h_numer.Write()

h_denom = ROOT.TH1F('h_denom', ';variable  [unit];', 40, 0.0, 200.0)
tree.Draw('%s>>%s' % ('v', 'h_denom'))
h_denom.Write()

del h_numer, h_denom
tfile.Close()


#------------------------------------------------------------------------------
# metaroot.hist  - the hist formatter
#------------------------------------------------------------------------------

hg = HistGetter('test.root')
h_x = hg.get('h_x')
h_y = hg.get('h_y')
h_z = hg.get('h_z')

plot_options = [
        metaroot.hist.PlotOptions(
            line_color = ROOT.kGray+1,
            fill_color = ROOT.kGray+1, # stat box uses fill color
            fill_style = 0, # hollow
            norm = 1.0 ),
        metaroot.hist.PlotOptions(
            line_color = ROOT.kRed+1,
            fill_color = ROOT.kRed+1,
            fill_style = 0,
            norm = 1.0 ),
        metaroot.hist.PlotOptions(
            line_color = ROOT.kBlue+1,
            fill_color = ROOT.kBlue+1,
            fill_style = 0,
            norm = 1.0 ),
        ]

plot = metaroot.hist.pile_hists(
        hists = [h_x, h_y, h_z],
        name = 'pile_hists',
        plot_options = plot_options,
        draw_options = ['HIST', 'HIST', 'HIST'],
        show_stats = True)
plot['canvas'].cd()
leg = metaroot.hist.make_legend(
        hists = [h_x, h_y, h_z],
        labels = ['x', 'y', 'z'],
        draw_options = ['F', 'F', 'F'],
        x2 = 0.85, y2 = 0.90 )
leg.Draw()
plot['canvas'].SaveAs('plot_hists.eps')
ROOT.gStyle.SetOptStat(0)

#------------------------------------------------------------------------------
h_x = hg.get('h_x')
h_y = hg.get('h_y')
h_z = hg.get('h_z')

for h, s in [(h_x, 1.0), (h_y, 20.0), (h_z, 3.0)]:
    h.Scale(s)

plot_options = [
        metaroot.hist.PlotOptions(
                fill_color = ROOT.kBlue+1,
                fill_style = 1001 ),
        metaroot.hist.PlotOptions(
                fill_color = ROOT.kRed+1,
                fill_style = 1001 ),
        metaroot.hist.PlotOptions(
                fill_color = ROOT.kGray+1,
                fill_style = 1001 ),
        ]

plot = metaroot.hist.stack_hists(
        hists = [h_x, h_y, h_z],
        name = 'stack_hists',
        plot_options = plot_options,
        show_stats = False)
plot['canvas'].cd()
leg = metaroot.hist.make_legend(
        hists = [h_x, h_y, h_z],
        labels = ['x', 'y', 'z'],
        draw_options = ['F', 'F', 'F'],
        x2 = 0.90, y2 = 0.90 )
leg.Draw()
plot['canvas'].SaveAs('stack_hists.eps')


#------------------------------------------------------------------------------
h_n = hg.get('h_n')
h_np = metaroot.plot.prune_empty_bins(h_n)
plot = metaroot.plot.plot_pie(
        name = 'plot_pie',
        counts = h_np )
plot['canvas'].SaveAs('plot_pie.eps')

#------------------------------------------------------------------------------
h_numer = hg.get('h_numer')
h_denom = hg.get('h_denom')
plot1 = metaroot.plot.plot_eff(
        numers = h_numer,
        denoms = h_denom,
        name = 'plot_eff',
        min = 0.0, max = 1.0 )
f_t.SetLineColor(ROOT.kAzure+2)
plot1['hists'][0].Fit(f_t, '', '', 0.0, 200.0)
text = ROOT.TPaveText(0.55, 0.45, 0.88, 0.25, 'NDC')
text.SetFillStyle(0)
text.SetBorderSize(0)
text.AddText('Plateau = %.3g #pm %.2g' % (f_t.GetParameter(0), f_t.GetParError(0)))
text.AddText('Edge = %.3g #pm %.2g' %  (f_t.GetParameter(1), f_t.GetParError(1)))
text.AddText('Width = %.3g #pm %.2g' %  (f_t.GetParameter(2), f_t.GetParError(2)))
text.AddText('#chi^{2} / NDF = %.3g / %i = %.3g' % (f_t.GetChisquare(), f_t.GetNDF(), f_t.GetChisquare()/f_t.GetNDF()))
text.Draw()
plot1['canvas'].SaveAs('plot_eff.eps')

#------------------------------------------------------------------------------
plot2 = metaroot.plot.plot_ratio(
        numers = h_numer,
        denoms = h_denom,
        name = 'plot_ratio',
        min = 0.0, max = 1.0 )
plot2['canvas'].SaveAs('plot_ratio.eps')

#------------------------------------------------------------------------------
plot = metaroot.plot.plot_graph_errors(
        name = 'plot_graph_errors',
        title = ';x;y',
        x =  [   1,   2,   3,   4,   5,    6,    7,    8,    9 ],
        y =  [ 1.0, 5.4, 6.2, 7.2, 9.8, 11.1, 12.3, 14.5, 15.7 ],
        ex = [   0,   0,   0,   0,   0,    0,    0,    0,    0 ],
        ey = [ 0.6, 0.6, 0.6, 0.3, 0.4,  0.7,  0.5,  0.4,  0.4 ] )
plot['canvas'].SaveAs('plot_graph_errors.eps')

#------------------------------------------------------------------------------
plot = metaroot.plot.plot_shared_axis(
        plot1['canvas'],
        plot2['canvas'],
        name = 'shared_axis',
        split = 0.4)
ROOT.gROOT.ForceStyle()
plot['canvas'].SaveAs('plot_shared_axis.eps')
plot['canvas'].SaveAs('plot_shared_axis.png')


hg.close()

