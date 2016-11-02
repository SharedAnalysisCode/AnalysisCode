"""
metaroot.plot

Module for making various special kinds of ROOT plots.
This module should be creating/modifying plots, not formatting.
metaroot.hist should be used to format and style existing
plots.

Part of the metaroot package.
"""

__author__ = 'Ryan D. Reece'
__email__ = 'ryan.reece@cern.ch'
__created__ = '2008-05-01'
__copyright__ = 'Copyright 2008-2010 Ryan D. Reece'
__license__ = 'GPL http://www.gnu.org/licenses/gpl.html'

#------------------------------------------------------------------------------

from array import array
import math
import re
import os

import ROOT
import metaroot

_alternating_grays_2 = [ROOT.kGray, ROOT.kGray+2]*10
_alternating_grays_3 = [ROOT.kGray, ROOT.kGray+2, ROOT.kBlack]*7

#______________________________________________________________________________
def prune_empty_bins(hist, do_sort=False, descending=True):
    """
    Please write a docstring.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    axis = hist.GetXaxis()
    nbins = axis.GetNbins()
    counts = []
    labels = []
    errors = []
    has_errors = (hist.GetSumw2N() > 0)
    for i in xrange(1, nbins+1):
        count = hist.GetBinContent(i)
        if count:
            counts.append(count)
            labels.append(str(int(round(axis.GetBinCenter(i)))))
            if has_errors:
                errors.append(hist.GetBinError(i))
            else:
                errors.append(None)
    if do_sort:
        zipped = zip(counts, errors, labels)
        zipped.sort()
        if descending:
            zipped.reverse()
        counts, errors, labels = map(list, zip(*zipped))
    hist_pruned = hist.__class__('%s_pruned' % hist.GetName(),
            '%s;%s;%s' % (hist.GetTitle(), hist.GetXaxis().GetTitle(), hist.GetYaxis().GetTitle()),
            len(counts), 1, len(counts)+1)
    axis_pruned = hist_pruned.GetXaxis()
    for i, c, e, a in zip(range(1, len(counts)+1), counts, errors, labels):
        hist_pruned.SetBinContent(i, c)
        axis_pruned.SetBinLabel(i, a)
        if not e is None:
            hist_pruned.SetBinError(i, e)
    return hist_pruned


#______________________________________________________________________________
def plot_pie( 
        name='pie', title='',
        counts=None, labels=None,
        colors=metaroot.default,
        min_percent=2.0,
        label_format='%txt (%perc)',
        radius=0.25,
        text_size=0.04,
        labels_offset=0.02,
        draw_options='', # 'R', 
        canvas_options=metaroot.default,
        log='',
        do_sort=True):
    """
    Please write a docstring.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if isinstance(counts, ROOT.TH1):
        hist = counts
        axis = hist.GetXaxis()
        nbins = axis.GetNbins()
        counts = []
        labels = []
        for i in xrange(1, nbins+1):
            count = hist.GetBinContent(i)
            if count:
                counts.append(count)
                bin_label = axis.GetBinLabel(i)
                if bin_label:
                    labels.append(bin_label)
                else:
                    labels.append(str(axis.GetBinCenter(i)))
        if not title:
            title = axis.GetTitle()
    else:
        # don't disturb lists passed as parameters
        counts = list(counts)
        if labels:
            labels = list(labels)
    # sort
    if do_sort:
        if labels:
            counts_and_labels = zip(counts, labels)
            counts_and_labels.sort()
            counts_and_labels.reverse()
            counts, labels = map(list, zip(*counts_and_labels))
        else:
            counts.sort()
            counts.reverse()
    # group small counts into others slice
    if min_percent:
        integral = sum(counts)
        len_counts = len(counts)
        other_index = len_counts
        for ci, c in enumerate(counts):
            if c < min_percent*integral/100.0:
                other_index = ci 
                break
        other_sum = sum(counts[other_index:])
        pie_counts = counts[:other_index]
        if labels:
            pie_labels = labels[:other_index]
        if other_sum:
            pie_counts.append(other_sum)
            pie_labels.append('other')
    # create TPie
    if colors is metaroot.default:
        colors = metaroot.hist.my_colors[:len(counts)]
    pie = None
    if colors:
        pie = ROOT.TPie(name, title, len(pie_counts), array('f', pie_counts), array('i', colors))
    else:
        pie = ROOT.TPie(name, title, len(pie_counts), array('f', pie_counts))
    pie.SetRadius(radius)
    pie.SetTextSize(text_size)
    # label slices
    if labels:
        pie.SetLabelsOffset(labels_offset)
        pie.SetLabelFormat(label_format)
        # n = p.GetEntries() # new to ROOT 5.20
        for Li, L in enumerate(pie_labels):
            pie.SetEntryLabel(Li, L)
    # Draw
    if canvas_options is metaroot.default:
        canvas_options = metaroot.hist.CanvasOptions(width=500, height=500, grid_x=0, grid_y=0)
    canvas = canvas_options.create('%s_canvas' % name)
    pie.Draw(draw_options)
    # log complete counts and labels
    if log:
        out_lines = ['%3s %10s %10s  %s\n' % ('i', 'count', '%', 'label'), '\n']
        for i in xrange(len(counts)):
            out_lines.append( '%3i %10.3g %10.3g  %s\n' \
                    % (i, counts[i], 100.0*counts[i]/integral, labels[i]) )
        out_lines.append('\n')
        out_lines.append('sum = %s\n' % integral)
        f = open(log, 'w')
        f.writelines(out_lines)
        f.close()
    return {'pie':pie, 'canvas':canvas}

#______________________________________________________________________________
def plot_ratio( numers, denoms, name, divide_option='', **kw ):
    """
    Please write a docstring.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if not isinstance(numers, list): numers = [numers]
    if not isinstance(denoms, list): denoms = [denoms]
    assert len(numers) == len(denoms)
    for h in numers + denoms:
        if not h.GetSumw2N(): h.Sumw2()
    hists = [ n.Clone('%s_ratio_temporary' % n.GetName()) for n in numers ] # make copies
    for h, n, d in zip(hists, numers, denoms):
        h.Divide(n, d, 1.0, 1.0, divide_option)
    return metaroot.hist.pile_hists(hists=hists, name=name, **kw)

#______________________________________________________________________________
def plot_ratio_band(numer, denom, name,
        band_plot_options = metaroot.default,
        ratio_plot_options = metaroot.default,
        **kw):
    """
    Please write a docstring.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if band_plot_options is metaroot.default:
        band_plot_options = metaroot.hist.PlotOptions(fill_color=ROOT.kAzure-9, line_width=0, marker_size=0.0)
    if ratio_plot_options is metaroot.default:
        ratio_plot_options = metaroot.hist.PlotOptions()
    h_ratio = numer.Clone('%s_ratio_tmp' % numer.GetName())
    h_band = denom.Clone('%s_band_tmp' % numer.GetName())
    assert numer.GetNbinsX() == denom.GetNbinsX()
    nbins = numer.GetNbinsX()
    for i in xrange(nbins+2):
        nc = numer.GetBinContent(i)
        ne = numer.GetBinError(i)
        dc = denom.GetBinContent(i)
        de = denom.GetBinError(i)
        h_band.SetBinContent(i, 1.0)
        h_band.SetBinError(i, de/dc if dc else 0.0)
        h_ratio.SetBinContent(i, nc/dc if dc else 0.0)
        h_ratio.SetBinError(i, ne/dc if dc else 0.0)
    hists = [h_ratio, h_band]
    kw['draw_options'] = ['PE', 'E4']
    kw['plot_options'] = [ratio_plot_options, band_plot_options]
    kw['include_y'] = [1.0]
    plot = metaroot.hist.pile_hists(hists=hists, name=name, **kw)
    legend = metaroot.hist.make_legend(
            hists=hists,
            labels = ['data stat. uncert.', 'model stat. uncert.'],
            draw_options = kw['draw_options'],
            width = 0.20,
            height = 0.06,
            x1 = 0.17,
            y2 = 0.95 )
    legend.Draw()
    plot['legend'] = legend
    return plot

#______________________________________________________________________________
def plot_eff( numers, denoms, name, divide_option='w', draw_options='PZ', **kw):
    """
    Please write a docstring.
    http://root.cern.ch/root/html522/TGraphAsymmErrors.html#TGraphAsymmErrors:BayesDivide
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if not isinstance(numers, list): numers = [numers]
    if not isinstance(denoms, list): denoms = [denoms]
    assert len(numers) == len(denoms)
    graphs = [ ROOT.TGraphAsymmErrors(n, d, divide_option) for n, d in zip(numers, denoms) ]
    for i, g in enumerate(graphs):
#        g.SetName('%s_%s' % (name, i))
        g.SetName('%s.eff' % numers[i])
        x_min = numers[i].GetXaxis().GetXmin()
        x_max = numers[i].GetXaxis().GetXmax()
        g.GetXaxis().SetLimits(x_min, x_max)
        g.GetXaxis().SetRangeUser(x_min, x_max)
    return metaroot.hist.pile_hists(hists=graphs, name=name, draw_options=draw_options, **kw)


#______________________________________________________________________________
def remove_imprecise_graph_points( graph,
        max_rel_error = 4.0,
        max_abs_error = None,
        remove_zeros = True):
    """
    Please write a docstring.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    i = 0
    while i <  graph.GetN():
        x = ROOT.Double()
        y = ROOT.Double()
        graph.GetPoint(i, x, y)
        if isinstance(graph, ROOT.TGraphAsymmErrors):
            ex = (graph.GetErrorXhigh(i) + graph.GetErrorXlow(i))/2.0
            ey = (graph.GetErrorYhigh(i) + graph.GetErrorYlow(i))/2.0
        else:
            ex = graph.GetErrorX(i)
            ey = graph.GetErrorY(i)
        if remove_zeros and y==0:
            i = graph.RemovePoint(i)
            continue
        if max_rel_error and y and ey/y > max_rel_error:
            i = graph.RemovePoint(i)
            continue
        if max_abs_error and ey > max_abs_error:
            i = graph.RemovePoint(i)
            continue
        i += 1


#______________________________________________________________________________
def plot_poisson_sampling( hists, name, title=''):
    """
    Please write a docstring.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    nbins = hists[0].GetNbinsX()
    axis = hists[0].GetXaxis()
    fake_data_hist = ROOT.TH1F(name, title, nbins, axis.GetXmin(), axis.GetXmax())
    rand = ROOT.TRandom()
    for i in xrange(nbins):
        y = 0.0
        for h in hists:
            y += h.GetBinContent(i+1)
        fake_data_hist.Fill(hists[0].GetBinCenter(i+1), rand.Poisson(y))
    return fake_data_hist


#______________________________________________________________________________
def plot_graph( name,
        x, y,
        title='',
        min=metaroot.default, max=metaroot.default,
        options=metaroot.default,
        draw_options='AP',
        canvas_options=metaroot.default):
    """
    Basic function for plotting a graph of the data in the lists x and y.
    Returns a dictionary with 'graph' and 'canvas' keys.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    assert len(x) == len(y)
    if not isinstance(x, array):
        x = array('f', x)
    if not isinstance(y, array):
        y = array('f', y)
    g = ROOT.TGraph(len(x), x, y)
    g.SetName(name)
    g.SetTitle(title)
    if not min is metaroot.default:
        g.SetMinimum(min)
    if not max is metaroot.default:
        g.SetMaximum(max)
    if options is metaroot.default:
        options = metaroot.hist.PlotOptions()
    options.configure(g)
    if canvas_options is metaroot.default:
        canvas_options = metaroot.hist.CanvasOptions()
    c = canvas_options.create(name)
    g.Draw(draw_options)
    return {'graph':g, 'canvas':c}


#______________________________________________________________________________
def plot_graph_errors( name,
        x, y, ex, ey,
        title='',
        min=metaroot.default, max=metaroot.default,
        options=metaroot.default,
        draw_options='APZ',
        canvas_options=metaroot.default):
    """
    Basic function for plotting a graph of the data in the lists x and y,
    with error bars in the lists ex and ey. Returns a dictionary with 'graph'
    and 'canvas' keys.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    assert len(x) == len(y) == len(ex) == len(ey)
    if not isinstance(x, array):
        x = array('f', x)
    if not isinstance(y, array):
        y = array('f', y)
    if not isinstance(ex, array):
        ex = array('f', ex)
    if not isinstance(ey, array):
        ey = array('f', ey)
    g = ROOT.TGraphErrors(len(x), x, y, ex, ey)
    g.SetName(name)
    g.SetTitle(title)
    if not min is metaroot.default:
        g.SetMinimum(min)
    if not max is metaroot.default:
        g.SetMaximum(max)
    if options is metaroot.default:
        options = metaroot.hist.PlotOptions()
    options.configure(g)
    if canvas_options is metaroot.default:
        canvas_options = metaroot.hist.CanvasOptions()
    c = canvas_options.create(name)
    g.Draw(draw_options)
    return {'graph':g, 'canvas':c}

#______________________________________________________________________________
def plot_graph_asymm_errors( name,
        x, y, exl, exh, eyl, eyh,
        title='',
        min=metaroot.default, max=metaroot.default,
        options=metaroot.default,
        draw_options='APZ',
        canvas_options=metaroot.default):
    """
    Basic function for plotting a graph of the data in the lists x and y,
    with asymmetric error bars in the lists exl, exh, eyl, and eyh. Returns
    a dictionary with 'graph' and 'canvas' keys.
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    assert len(x) == len(y) == len(exl) == len(exh) == len(eyl) == len(eyh)
    if not isinstance(x, array):
        x = array('f', x)
    if not isinstance(y, array):
        y = array('f', y)
    if not isinstance(exl, array):
        exl = array('f', exl)
    if not isinstance(exh, array):
        exh = array('f', exh)
    if not isinstance(eyl, array):
        eyl = array('f', eyl)
    if not isinstance(eyh, array):
        eyh = array('f', eyh)
    g = ROOT.TGraphAsymmErrors(len(x), x, y, exl, exh, eyl, eyh)
    g.SetName(name)
    g.SetTitle(title)
    if not min is metaroot.default:
        g.SetMinimum(min)
    if not max is metaroot.default:
        g.SetMaximum(max)
    if options is metaroot.default:
        options = metaroot.hist.PlotOptions()
    options.configure(g)
    if canvas_options is metaroot.default:
        canvas_options = metaroot.hist.CanvasOptions()
    c = canvas_options.create(name)
    g.Draw(draw_options)
    return {'graph':g, 'canvas':c}


#______________________________________________________________________________
def plot_profx(name, hists,
        title_y=None, title_x=None,
        min=None, max=metaroot.default,
        plot_options=metaroot.default,
        draw_options=metaroot.default,
        canvas_options=metaroot.default,
        plot_mode=False):
    """Please write a docstring"""
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    assert 1 <= len(hists) <= 2

    ## make profiles
    profs = [ h.ProfileX('%s_%i_profx' % (name, i)) for i, h in enumerate(hists) ]
    profs_rms = []
    for p in profs:
        p_rms = p.Clone(p.GetName() + '_rms')
        p_rms.SetErrorOption('s') # RMS error bars
        profs_rms.append(p_rms)

    if plot_mode:
        pass # TODO: plot mode instead of mean
    # RMS band should centered on the mean (possibly median?)

    ## set titles
    if title_x is None:
        title_x = hists[0].GetXaxis().GetTitle()
    if title_y is None:
        title_y = hists[0].GetYaxis().GetTitle()
        if title_y.count('#scale'): # hack
            reo = re.match(r'([^\[\]]*#scale\[\d*\.?\d*\][^\[\]]*)(\[\w+\])?', title_y)
        else:
            reo = re.match(r'([^\[\]]+)(\[\w+\])?', title_y)
        if reo:
            rest, unit = reo.groups()
            if rest: rest = rest.strip()
            if unit: unit = unit.strip()
            title_y = '#LT%s#GT' % rest
            if unit: # add unit back to y-axis title
                title_y += '  %s' % unit

    ## set default options
    if plot_options is metaroot.default:
        if len(hists) == 1:
            plot_options = [
                    metaroot.hist.PlotOptions(line_color = ROOT.kBlue+1,
                                   marker_color = ROOT.kBlue+1,
                                   marker_style = 20 ),
                    metaroot.hist.PlotOptions(line_color = ROOT.kBlue+1,
                                   marker_size = 0,
                                   line_width = 2,
                                   fill_color = ROOT.kAzure-2,
                                   fill_style = 1001),
                    ]
        elif len(hists) == 2:
            plot_options = [
                    metaroot.hist.PlotOptions(line_color = ROOT.kBlue+1,
                                   marker_color = ROOT.kBlue+1,
                                   marker_style = 20 ),
                    metaroot.hist.PlotOptions(line_color = ROOT.kRed+1,
                                   marker_color = ROOT.kRed+1,
                                   marker_style = 24 ),
                    metaroot.hist.PlotOptions(line_color = ROOT.kBlue+1,
                                   marker_size = 0,
                                   line_width = 2,
                                   fill_color = ROOT.kAzure-2,
                                   fill_style = 3004),
                    metaroot.hist.PlotOptions(line_color = ROOT.kRed+1,
                                   marker_size = 0,
                                   line_width = 2,
                                   fill_color = ROOT.kRed-6,
                                   fill_style = 1001),
                    ]
    if draw_options is metaroot.default:
        if len(hists) == 1:
            draw_options = ['EP', 'E4']
        elif len(hists) == 2:
            draw_options = ['EP', 'EP', 'E4', 'E4']

    ## draw
    return metaroot.hist.pile_hists(
            hists = profs + profs_rms,
            name = name + '_profx',
            title = ';%s;%s' % (title_x, title_y),
            min = min, max = max,
            plot_options = plot_options,
            draw_options = draw_options,
            canvas_options = canvas_options)


#______________________________________________________________________________
def plot_profx_cb(name, hists,
        title_y=None, title_x=None,
        min=None, max=None,
        plot_options=metaroot.default,
        draw_options=metaroot.default,
        canvas_options=metaroot.default):
    """Please write a docstring"""
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    assert 1 <= len(hists) <= 2

    ## crystal ball function http://en.wikipedia.org/wiki/Crystal_Ball_function
    f_cb = ROOT.TF1('f_cb', '[0]*(((x-[1])/[2] < [3])*exp(-pow((x-[1]),2)/(2*pow([2],2))) + ((x-[1])/[2] >= [3])*((pow([4]/abs([3]),[4])*exp(-[3]*[3]/2))*(([4]/abs([3])-abs([3]))+(x-[1])/[2])**(-[4])))', 0.0, 20.0)
    f_cb.SetParameters(100.0, 2.0, 0.7, 0.5, 5.0)
    f_cb.SetLineWidth(3)
    f_cb.SetLineColor(ROOT.kAzure)

    ## make profiles
    profs = []
    profs_rms = []
    projy_canvases = []
    for i, h in enumerate(hists):
        x_axis = h.GetXaxis()
        prof = ROOT.TH1F('%s_%i_profx' % (h.GetName(), i), '', x_axis.GetNbins(), x_axis.GetXmin(), x_axis.GetXmax())
        prof_rms = prof.Clone('%s_%i_prof_rms' % (h.GetName(), i))
        for i_bin in xrange(1, h.GetNbinsX()+1):
            p = h.ProjectionY('%s_%i_projy' % (h.GetName(), i_bin), i_bin, i_bin, 'e')
            mode = p.GetBinCenter(p.GetMaximumBin())
            max = p.GetBinContent(p.GetMaximumBin())
            integral = p.Integral()
            
            f_cb.SetParameter(0, max)
            f_cb.SetParLimits(0, max*0.5, max*1.5)
            f_cb.SetParameter(1, mode)
            f_cb.SetParLimits(1, mode*0.5, mode*1.5)
            f_cb.SetParameter(2, 1)
            f_cb.SetParLimits(2, 0.0, 20.0)
            f_cb.SetParameter(3, 0.5)
            f_cb.SetParLimits(3, 0.0, 5.0)
            f_cb.SetParameter(4, 100)
            f_cb.SetParLimits(4, 0, 1000)

            p.Fit(f_cb, '0')
            c = ROOT.TCanvas('c_' + p.GetName(), '', 700, 500)
            p.Draw('PE')
            f_cb.Draw('same')

            fit_mode = f_cb.GetParameter(1)
            fit_sigma = f_cb.GetParameter(1)
            fit_mode_error = f_cb.GetParError(1)        

            ## fudge the error
            # fit_error = fit_sigma / math.sqrt(integral)

            prof.SetBinContent(i_bin, fit_mode)
            prof.SetBinError(i_bin, fit_mode_error)

            prof_rms.SetBinContent(i_bin, fit_mode)
            prof_rms.SetBinError(i_bin, fit_sigma)
            
            if not os.path.isdir('projy'):
                os.system('mkdir projy')
            c.SaveAs('projy/%s.eps' % p.GetName())
            

        profs.append(prof)
        profs_rms.append(prof_rms)

    ## set titles
    if title_x is None:
        title_x = hists[0].GetXaxis().GetTitle()
    if title_y is None:
        title_y_split = hists[0].GetYaxis().GetTitle().split('[')
        title_y = '#LT%s#GT' % title_y_split[0].strip()
        if len(title_y_split) > 1: # add unit back to y-axis title
            title_y += '  [%s' % title_y_split[1]

    ## set default options
    if plot_options is metaroot.default:
        if len(hists) == 1:
            plot_options = [
                    metaroot.hist.PlotOptions(line_color = ROOT.kBlue+1,
                                   marker_color = ROOT.kBlue+1,
                                   marker_style = 20 ),
                    metaroot.hist.PlotOptions(line_color = ROOT.kBlue+1,
                                   marker_size = 0,
                                   line_width = 2,
                                   fill_color = ROOT.kAzure-2,
                                   fill_style = 3003),
                    ]
        elif len(hists) == 2:
            plot_options = [
                    metaroot.hist.PlotOptions(line_color = ROOT.kBlue+1,
                                   marker_color = ROOT.kBlue+1,
                                   marker_style = 20 ),
                    metaroot.hist.PlotOptions(line_color = ROOT.kRed+1,
                                   marker_color = ROOT.kRed+1,
                                   marker_style = 24 ),
                    metaroot.hist.PlotOptions(line_color = ROOT.kBlue+1,
                                   marker_size = 0,
                                   line_width = 2,
                                   fill_color = ROOT.kAzure-2,
                                   fill_style = 3003),
                    metaroot.hist.PlotOptions(line_color = ROOT.kRed+1,
                                   marker_size = 0,
                                   line_width = 2,
                                   fill_color = ROOT.kRed-6,
                                   fill_style = 1001),
                    ]
    if draw_options is metaroot.default:
        if len(hists) == 1:
            draw_options = ['EP', 'E4']
        elif len(hists) == 2:
            draw_options = ['EP', 'EP', 'E4', 'E4']

    ## draw
    plot = metaroot.hist.pile_hists(
            hists = profs + profs_rms,
            name = name + '_profx',
            title = ';%s;%s' % (title_x, title_y),
            min = min, max = max,
            plot_options = plot_options,
            draw_options = draw_options,
            canvas_options = canvas_options)

    return plot

#______________________________________________________________________________
def plot_shared_axis(top_canvas, bottom_canvas,name='',split=0.5,
                     canvas_options=metaroot.default,**kw):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # options with defaults
    axissep       = kw.get('axissep'       ,0.0)
    ndivs         = kw.get('ndivs'           ,[503,503])

    if not name:
        name = top_canvas.GetName() + '_shared_axis'
    if canvas_options is metaroot.default:
        canvas_options = metaroot.hist.CanvasOptions(width=600, height=600, grid_x=0, grid_y=0)
    canvas = canvas_options.create(name)

    canvas.cd()
    top_pad = ROOT.TPad(canvas.GetName() + '_top_pad', '',  0, split, 1, 1, 0, 0, 0)
    top_pad.Draw()

    bottom_pad = ROOT.TPad(canvas.GetName() + '_bottom_pad', '',  0, 0, 1, split, 0, 0, 0)
    bottom_pad.Draw()

    top_pad.cd()
    top_canvas.DrawClonePad()
    bottom_pad.cd()
    bottom_canvas.DrawClonePad()

    top_pad.SetTopMargin(canvas.GetTopMargin()*1.0/(1.0-split))
    top_pad.SetBottomMargin(axissep)
    top_pad.SetRightMargin(canvas.GetRightMargin())
    top_pad.SetLeftMargin(canvas.GetLeftMargin());
    top_pad.SetFillStyle(0) # transparent
    top_pad.SetBorderSize(0)

    bottom_pad.SetTopMargin(axissep)
    bottom_pad.SetBottomMargin(canvas.GetBottomMargin()*1.0/split)
    bottom_pad.SetRightMargin(canvas.GetRightMargin())
    bottom_pad.SetLeftMargin(canvas.GetLeftMargin());
    bottom_pad.SetFillStyle(0) # transparent
    bottom_pad.SetBorderSize(0)

    pads = [top_pad, bottom_pad]
    factors = [0.8/(1.0-split), 0.8/split]
    for i_pad, pad in enumerate(pads):
        factor = factors[i_pad]
        ndiv = ndivs[i_pad]
        prims = [ p.GetName() for p in pad.GetListOfPrimitives() ]
        for name in prims:
            h = pad.GetPrimitive(name)
            if isinstance(h, ROOT.TH1) or isinstance(h, ROOT.THStack) or isinstance(h, ROOT.TGraph) or isinstance(h, ROOT.TGraphErrors) or isinstance(h, ROOT.TGraphAsymmErrors):
                if isinstance(h, ROOT.TGraph) or isinstance(h, ROOT.THStack) or isinstance(h, ROOT.TGraphErrors) or isinstance(h, ROOT.TGraphAsymmErrors):
                    h = h.GetHistogram()
                h.SetLabelSize(h.GetLabelSize('Y')*factor, 'Y')
                h.SetTitleSize(h.GetTitleSize('X')*factor, 'X')
                h.SetTitleSize(h.GetTitleSize('Y')*factor, 'Y')
                h.SetTitleOffset(h.GetTitleOffset('Y')/factor, 'Y')
                h.GetYaxis().SetNdivisions(ndiv)
                h.GetXaxis().SetNdivisions()                
                if i_pad == 0:
                    h.SetLabelSize(0.0, 'X')
                    h.GetXaxis().SetTitle("")
                else:
                    h.SetLabelSize(h.GetLabelSize('X')*factor, 'X')
                    ## Trying to remove overlapping y-axis labels.  Doesn't work.
                    # h.GetYaxis().Set(4, h.GetYaxis().GetXmin(), h.GetYaxis().GetXmax()) 
                    # h.GetYaxis().SetBinLabel( h.GetYaxis().GetLast(), '')

    # crash in ROOT::delete_TPad ()
    # see: http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=13392
    ROOT.SetOwnership(top_canvas, False)
    ROOT.SetOwnership(bottom_canvas, False)
    ROOT.SetOwnership(canvas, False)
    
    return {'canvas':canvas, 'top_pad':top_pad, 'bottom_pad':bottom_pad, 'top_canvas':top_canvas, 'bottom_canvas':bottom_canvas}
       
#______________________________________________________________________________
def set_min_max_ratio(histlist, sigreq, top_buffer=0.1, bottom_buffer=0.1):
    sigminv=1e10
    sigmaxv=-1e10
    minv=1e10
    maxv=-1e10

#    # find min and max for bins with at least significance of sigreq
#    for hist in histlist:
#        for b in range(1,hist.GetNbinsX()+1):
#            
#            if hist.GetBinError(b)==0:
#                continue
#
#            issig=(-1*(hist.GetBinContent(b)-1)/hist.GetBinError(b) > sigreq)
#            minv=min(minv,hist.GetBinContent(b)-hist.GetBinError(b))
#            if issig:
#                sigminv=min(sigminv,hist.GetBinContent(b)-hist.GetBinError(b))
#
#            issig=((hist.GetBinContent(b)-1)/hist.GetBinError(b) > sigreq)
#            maxv=max(maxv,hist.GetBinContent(b)+hist.GetBinError(b))
#            if issig:
#                sigmaxv=max(sigmaxv,hist.GetBinContent(b)+hist.GetBinError(b))
#
#    if sigminv<1e10:
#        minv=sigminv
#    else:
#        minv=0.0
#    if minv > 1.0:
#        minv = 1.0
#
#    if sigmaxv>-1e10:
#        maxv=sigmaxv
#    else:
#        maxv=2.0
#    if maxv < 1.0:
#        maxv = 1.0
#

    highvals=[]
    lowvals=[]
    for hist in histlist:
        for b in range(1,hist.GetNbinsX()+1):
            if (hist.GetBinContent(b)-1.0)<1e-10:
                continue
            highvals.append(hist.GetBinContent(b)-1+hist.GetBinError(b))
            lowvals.append(abs(hist.GetBinContent(b)-1-hist.GetBinError(b)))
    
    highvals=sorted(highvals)
    lowvals=sorted(lowvals)

    highpercentile=highvals[int(0.7*len(highvals))]
    lowpercentile=lowvals[int(0.7*len(lowvals))]

    maxv = max(int(10*(1+2*highpercentile))/10.0,2)
    minv = min(int(10*(1-2*lowpercentile))/10.0,0)
    
    # set the min and max in the histograms
    for hist in histlist:
        hist.SetMaximum(maxv+top_buffer)
        hist.SetMinimum(minv-bottom_buffer)


# ------------------------------------------------------------
#   Make a stack plot with a ratio below
# ------------------------------------------------------------
def stack_with_data_and_ratio(data, mc, name,**kw):
    canvas_options= kw.get('canvas_options', metaroot.default)

    # make stack
    stack = metaroot.hist.stack_with_data(data, mc, name,**kw)

    # make ratio
    data=stack['data']
    ratio=data.Clone(data.GetName()+"_ratio")
    ratio.Divide(stack['sum'])
    ratio_plot_options = metaroot.hist.PlotOptions()
    ratio_plot_options.configure(ratio)
    ratio.GetYaxis().SetTitle("Data/MC")
    ratio.GetYaxis().SetNdivisions(507)
    #    set_min_max_ratio([ratio],2.0)
    rMin = kw.get("rMin",metaroot.default)
    rMax = kw.get("rMax",metaroot.default)
    metaroot.hist.set_min([ratio],  rMin, log_y=canvas_options.log_y)
    metaroot.hist.set_max([ratio],  rMax, log_y=canvas_options.log_y)
    stack['ratio']=ratio
    
    # draw ratio

    canvas_options.log_y=False
    ratio_canvas  = canvas_options.create(name+"_ratio")
    ratio.Draw("PE")
    line=ROOT.TLine()
    a=ratio.GetXaxis()
    line.DrawLine(a.GetXmin(),1.0,a.GetXmax(),1.0)

    shared=plot_shared_axis(stack['canvas'],ratio_canvas,name+"_with_ratio",split=0.3,axissep=0.04,ndivs=[505,503])
    #stack['top_canvas']=stack['canvas']
    #stack['bottom_canvas']=ratio_canvas
    stack['top_pad']=shared['top_pad']
    stack['bottom_pad']=shared['bottom_pad']
    stack['canvas']=shared['canvas']
    
    return stack


# ------------------------------------------------------------
#   Do variable rebinning for a stack plot
# ------------------------------------------------------------
def make_variable_binning(stacklist,threshold=3):

    # sum stack list
    sum = stacklist[0].Clone('sum')
    sum.Reset()
    for h in stacklist:
        sum.Add(h)

    # make binning
    bins=[]
    axis=sum.GetXaxis()
    bins.append(axis.GetXmin())
    count=0
    for b in range(1, sum.GetNbinsX()+1):
        # this special case is to not extend the first 
        # filled bin to the edge of the histogram
        if sum.GetBinContent(b)>0 and count==0 and len(bins)==1:
            bins.append(axis.GetBinLowEdge(b))
        count+=sum.GetBinContent(b)
        if count>threshold:
            bins.append(axis.GetBinUpEdge(b))
            count=0
    if count!=0:
        bins.append(axis.GetXmax())
    print bins,count
    return bins

# ------------------------------------------------------------
#   Do variable rebinning for a stack plot
# ------------------------------------------------------------
def do_variable_rebinning(hist,bins):
    newhist=ROOT.TH1F(hist.GetName()+"_rebin",
                      hist.GetTitle()+";"+hist.GetXaxis().GetTitle()+";"+hist.GetYaxis().GetTitle(),
                      len(bins)-1,
                      array('d',bins))
    a=hist.GetXaxis()
    newa=newhist.GetXaxis()
    for b in range(1, hist.GetNbinsX()+1):
        newb=newa.FindBin(a.GetBinCenter(b))
        val=newhist.GetBinContent(newb)
        err=newhist.GetBinError(newb)
        ratio_bin_widths=newa.GetBinWidth(newb)/a.GetBinWidth(b)
        val=val+hist.GetBinContent(b)/ratio_bin_widths
        err=math.sqrt(err*err+hist.GetBinError(b)/ratio_bin_widths*hist.GetBinError(b)/ratio_bin_widths)
        newhist.SetBinContent(newb,val)
        newhist.SetBinError(newb,err)

    return newhist
            
