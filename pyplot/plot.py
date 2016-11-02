# encoding: utf-8
'''
plot.py

description:

'''
__author__    = "Will Davey"
__email__     = "will.davey@cern.ch"
__created__   = "2012-11-13"
__copyright__ = "Copyright 2012 Will Davey"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"



## modules
import ROOT
import core
import hist
import histutils
import fileio
from math import sqrt
import os

## logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)



# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class Plot():
    '''
    description of Plot
    '''
    #____________________________________________________________
    def __init__(self,
            stack_hists = None,
            free_hists = None,
            leg = None,
            xtitle = None,
            ytitle = None,
            do_log = False,
            ):
        self.stack_hists = stack_hists if stack_hists else []
        self.free_hists = free_hists if free_hists else []
        self.leg = leg if leg else MetaLegend()
        self.xtitle = xtitle
        self.ytitle = ytitle
        self.do_log = do_log

    def first_hist(self):
        for h in self.free_hists: return h
        for h in self.stack_hists: return h
        return None


    def init_leg(self):
        for h in self.stack_hists: 
            self.leg.AddEntry(h,core.hist_tlatex_name(h),'F')
        for h in self.free_hists:    
            self.leg.AddEntry(h,core.hist_tlatex_name(h),'PL')

    def plot(self):
        h = self.first_hist()
        assert h, 'no hists to plot!'

        stack = ROOT.THStack('h_stack','h_stack')
        for h in reversed(self.stack_hists): stack.Add(h)
        self.stack = stack

        xtitle = self.xtitle if self.xtitle else h.GetXaxis().GetTitle()
        ytitle = self.ytitle if self.ytitle else h.GetYaxis().GetTitle()
        xmin = h.GetXaxis().GetBinLowEdge(1)
        xmax = h.GetXaxis().GetBinUpEdge(h.GetNbinsX())
        ymax = max([h.GetMaximum() for h in [stack]+self.free_hists])
        ymin = min([h.GetMinimum() for h in [stack]+self.free_hists])
        
        if self.do_log: 
            ymax *= 10.
            ymin *= 0.1
            if ymin <= 0.: ymin = 1.e-3
        else:
            ymax *= 1.3
            ymin = 0.

        fr = ROOT.gPad.DrawFrame(xmin,ymin,xmax,ymax, ';%s;%s' % (xtitle,ytitle) )
        stack.Draw('SAME,HIST')
        for h in self.free_hists: h.Draw('SAME')

        self.init_leg()
        self.leg.Draw()


#------------------------------------------------------------
class NewPlot():
    '''
    description of NewPlot
    '''
    #____________________________________________________________
    def __init__(self,
            data = None,
            bkgs = None,
            sigs = None, 
            stack_sig = True,
            draw_blinds = False,
            tag = None,
            ):
        self.data = data
        self.sigs = sigs
        self.bkgs = bkgs
        self.stack_sig = stack_sig
        self.do_draw_blinds = draw_blinds
        self.tag = tag
        
    #____________________________________________________________
    def plot(self):
        data = [self.data] if self.data else []
        bkgs = self.bkgs if self.bkgs else []
        sigs = self.sigs if self.sigs else []
        pd = (data+bkgs+sigs)[0]
        do_log = pd.var_details.do_logy

        hstack = ROOT.THStack()
        for p in reversed(bkgs): hstack.Add(p.hist())
        if self.stack_sig: 
            for p in reversed(sigs): 
                h = p.hist()
                p.sample.style_hist(h) ## ensure fill style
                hstack.Add(p.hist())

        # make legend
        hists  = [p.hist() for p in data+bkgs+sigs]
        titles = [p.sample.tlatex for p in data+bkgs+sigs]
        opts   = ['PL']*len(data)+['F']*len(bkgs)+['L']*len(sigs)
        if self.stack_sig: 
            hists  = [p.hist() for p in data+sigs+bkgs]
            titles = [p.sample.tlatex for p in data+sigs+bkgs]
            opts   = ['PL']*len(data)+['F']*len(sigs)+['F']*len(bkgs)
        leg = make_legend(hists,titles,opts)
       
        # draw canvas 
        (xmin,ymin,xmax,ymax) = self.get_frame_boundaries()
        cname = self.get_cname()
        c = ROOT.TCanvas(cname,cname)
        fr = pd.var_details.frame(c,xmin,ymin,xmax,ymax) 
        hstack.Draw('SAME,HIST')
        if not self.stack_sig:
            for s in sigs: 
                h = s.hist()
                s.sample.style_hist_line(h)
                h.Draw('SAME,HIST')
        for d in data: d.hist().Draw('SAME')
        leg.Draw()
        self.draw_blinds(pd.var_details,xmin,ymin,xmax,ymax)
        if do_log: c.SetLogy()

        ## store new items as members to 
        ## prevent going out of scope
        self.hstack = hstack
        self.canvas = c
        c.SaveAs('%s.eps'%cname)
        return c 

    #____________________________________________________________
    def get_frame_boundaries(self):
        '''
        TODO: update to same code used in RatioPlot 
        '''
        data = [self.data] if self.data else []
        bkgs = self.bkgs if self.bkgs else []
        sigs = self.sigs if self.sigs else []
        pd = (data+bkgs+sigs)[0]
        do_log = pd.var_details.do_logy
        return histutils.get_frame_boundaries(
                [p.hist() for p in data+bkgs+sigs],
                logy = do_log,
                )


    #____________________________________________________________
    def draw_blinds(self,var_details,xmin,ymin,xmax,ymax):
        if not self.do_draw_blinds: return
        vd = var_details
        ## Draw Blinds
        if vd.blind_min != None:
            xpos = vd.blind_min
            xpostext = vd.blind_min - 0.01 * (xmax-xmin)
            line = ROOT.TLine()
            line.SetLineStyle(2)
            line.DrawLine( xpos, ymin, xpos, ymax )
            latex = ROOT.TLatex()
            latex.SetTextFont(42)
            latex.SetTextSize(20)
            latex.SetTextAngle(90.)
            latex.SetTextAlign(31)
            latex.DrawLatex( vd.blind_min, ymax, 'Blind   ' )

        if vd.blind_max != None:
            xpos = vd.blind_max
            xpostext = vd.blind_max + 0.01 * (xmax-xmin)
            line = ROOT.TLine()
            line.SetLineStyle(2)
            line.DrawLine( xpos, ymin, xpos, ymax )
            latex = ROOT.TLatex()
            latex.SetTextFont(42)
            latex.SetTextSize(0.04)
            latex.SetTextAngle(90.)
            latex.SetTextAlign(33)
            latex.DrawLatex( xpostext, ymax, 'Blind   ' )

    #____________________________________________________________
    def summary(self,win_min=None,win_max=None):
        data = [self.data] if self.data else []
        bkgs = self.bkgs if self.bkgs else []
        sigs = self.sigs if self.sigs else []
        pd = (data+bkgs+sigs)[0]
        log.info('')
        log.info('##'+'-'*80)
        log.info('Event Summary: %s'%(pd.full_name()))
        log.info('')
        log.info('Full-Range (Raw):')
        self.__print_raw_summary__() 
        log.info('')
        log.info('Full-Range:')
        self.__print_summary__() 

        if win_min!=None or win_max!=None:
            log.info('')
            log.info('Window, [%s,%s]:'%(win_min,win_max))
            self.__print_summary__(win_min,win_max)


    #____________________________________________________________
    def __print_summary__(self,win_min=None,win_max=None):
        tot_bkg = 0.
        tot_bkg_err2 = 0.
        for b in self.bkgs:
            h = b.hist()
            n, en = histutils.integral_and_error(h,win_min,win_max)
            tot_bkg += n
            tot_bkg_err2 += pow(en,2)
            log.info('%30s: %10.3f +- %10.3f'%(b.sample.name,n,en))
        log.info('_'*60)
        log.info('%30s: %10.3f +- %10.3f'%('SM Total',tot_bkg,sqrt(tot_bkg_err2)))
        if self.data:
            h = self.data.hist()
            n, en = histutils.integral_and_error(h,win_min,win_max)
            log.info('_'*60)
            log.info('%30s: %10.3f'%('Data',n))

        log.info('_'*60)
        for s in self.sigs:
            h = s.hist()
            n, en = histutils.integral_and_error(h,win_min,win_max)
            log.info('%30s: %10.3f +- %10.3f'%(s.sample.name,n,en))
        log.info('_'*60)

    #____________________________________________________________
    def __print_raw_summary__(self):
        tot_bkg = 0.
        for b in self.bkgs:
            n = hist.raw_events(b)
            log.info('%30s: %10.0f'%(b.sample.name,n))
        log.info('_'*60)
        if self.data:
            n = hist.raw_events(self.data)
            log.info('_'*60)
            log.info('%30s: %10.0f'%('Data',n))

        log.info('_'*60)
        for s in self.sigs:
            n = hist.raw_events(s)
            log.info('%30s: %10.0f'%(s.sample.name,n))
        log.info('_'*60)

    #____________________________________________________________
    def get_pd(self):
        data = [self.data] if self.data else []
        bkgs = self.bkgs if self.bkgs else []
        sigs = self.sigs if self.sigs else []
        return (data+bkgs+sigs)[0]
    
    #____________________________________________________________
    def get_cname(self):
        cname = 'c_'
        cname += '%s_'%self.tag if self.tag else 'NoTag_'
        cname += self.get_pd().canvas_name()
        return cname

    #____________________________________________________________
    def save(self,filename,dirname=None):
        # save canvas
        fileio.save_object(self.plot(),filename,dirname)
        # save hists
        data = [self.data] if self.data else []
        bkgs = self.bkgs if self.bkgs else []
        sigs = self.sigs if self.sigs else []
        if dirname: dirname += '/'
        dirname += '%s_contents' % self.canvas.GetName()
        dirname = os.path.relpath(dirname)
        for s in data+bkgs+sigs:
            h = s.hist().Clone(s.short_name())
            fileio.save_object(h,filename,dirname)


#------------------------------------------------------------
class RatioPlot(NewPlot):
    '''
    description of NewPlot
    '''
    #____________________________________________________________
    def __init__(self,
            data = None,
            bkgs = None,
            sigs = None, 
            stack_sig = True,
            x = 700, y = 700, rsplit = 0.25,
            rmin = 0.4, rmax = 1.6,
            text_scale = 0.8,
            draw_blinds = False,
            tag = None,
            ):
        NewPlot.__init__(self,
                data=data,
                bkgs=bkgs,
                sigs=sigs,
                stack_sig=stack_sig,
                draw_blinds = draw_blinds,
                tag = tag,
                )
        self.x = x
        self.y = y
        self.rsplit = rsplit
        self.rmin = rmin
        self.rmax = rmax
        self.text_scale = text_scale
      
    #____________________________________________________________
    def reset_frame_text( self, fr ):
        xaxis = fr.GetXaxis()
        yaxis = fr.GetYaxis()
        gs = ROOT.gStyle
        yaxis.SetTitleSize( gs.GetTitleSize('Y') )
        yaxis.SetLabelSize( gs.GetLabelSize('Y') )
        yaxis.SetTitleOffset( gs.GetTitleOffset('Y') )
        yaxis.SetLabelOffset( gs.GetLabelOffset('Y') )
        xaxis.SetTitleSize( gs.GetTitleSize('X') )
        xaxis.SetLabelSize( gs.GetLabelSize('X') )
        xaxis.SetTickLength( gs.GetTickLength('X') )

    #____________________________________________________________
    def scale_frame_text( self, fr, scale ):
        xaxis = fr.GetXaxis()
        yaxis = fr.GetYaxis()
        yaxis.SetTitleSize( yaxis.GetTitleSize() * scale )
        yaxis.SetLabelSize( yaxis.GetLabelSize() * scale )
        yaxis.SetTitleOffset( 1.1* yaxis.GetTitleOffset() / scale  )
        yaxis.SetLabelOffset( yaxis.GetLabelOffset() * scale )
        xaxis.SetTitleSize( xaxis.GetTitleSize() * scale )
        xaxis.SetLabelSize( xaxis.GetLabelSize() * scale )
        xaxis.SetTickLength( xaxis.GetTickLength() * scale )
        xaxis.SetTitleOffset( 2.5* xaxis.GetTitleOffset() / scale  )
        xaxis.SetLabelOffset( 2.5* xaxis.GetLabelOffset() / scale )


    #____________________________________________________________
    def fix_frame1(self, fr1):
        self.reset_frame_text(fr1)
        fr1.GetXaxis().SetTitleSize(0)
        fr1.GetXaxis().SetLabelSize(0)
        #scale = 1. 
        scale = 1./(1.-self.rsplit) 
        self.scale_frame_text( fr1, scale ) 


    #____________________________________________________________
    def fix_frame2(self, fr2):
        fr2.GetYaxis().SetNdivisions(505)
        fr2.GetXaxis().SetNdivisions(505)
        fr2.GetYaxis().SetTitle('obs. / exp.')
        self.reset_frame_text(fr2)
        #scale = 1./self.rsplit-1.
        scale = 1./self.rsplit 
        self.scale_frame_text( fr2, scale )

    #____________________________________________________________
    def plot(self):
        data = [self.data] if self.data else []
        bkgs = self.bkgs if self.bkgs else []
        sigs = self.sigs if self.sigs else []
        pd = (data+bkgs+sigs)[0]
        do_log = pd.var_details.do_logy

        ## make stack
        hstack = ROOT.THStack()
        htotal = histutils.add_hists([p.hist() for p in bkgs])
        for p in reversed(bkgs): hstack.Add(p.hist())
        if self.stack_sig: 
            for p in reversed(sigs): 
                h = p.hist()
                p.sample.style_hist(h) ## ensure fill style
                hstack.Add(p.hist())
                htotal.Add(p.hist())
        
        ## make ratio
        hbkg = histutils.add_hists([p.hist() for p in bkgs])
        hdata = None
        if data: hdata  = data[0].hist()
        hratio = None
        if hdata and hbkg:
            rname = hdata.GetName().replace(data[0].sample.tlatex,'ratio')
            hratio = hdata.Clone(rname)
            hratio.Divide(hbkg)

        # make legend
        hists  = [p.hist() for p in data+bkgs+sigs]
        titles = [p.sample.tlatex for p in data+bkgs+sigs]
        opts   = ['PL']*len(data)+['F']*len(bkgs)+['L']*len(sigs)
        if self.stack_sig: 
            hists  = [p.hist() for p in data+sigs+bkgs]
            titles = [p.sample.tlatex for p in data+sigs+bkgs]
            opts   = ['PL']*len(data)+['F']*len(sigs)+['F']*len(bkgs)
        leg = make_legend(hists,titles,opts)
       
        ## draw canvas 
        cname = self.get_cname()
        c = ROOT.TCanvas(cname,cname,self.x,self.y)
        pad1 = ROOT.TPad("pad1","top pad",0.0,self.rsplit,1.,1.)
        pad1.SetBottomMargin(0.05)
        pad1.Draw()
        pad2 = ROOT.TPad("pad2","bottom pad",0,0,1,self.rsplit)
        pad2.SetTopMargin(0.05)
        pad2.SetBottomMargin(0.40)
        pad2.Draw()


        ## top pad
        pad1.cd()
        (xmin,ymin,xmax,ymax) = self.get_frame_boundaries()
        xmin,ymin,xmax,ymax = histutils.get_frame_boundaries(
                [htotal]+[p.hist() for p in data+sigs],
                logy=do_log,
                )

        fr1 = pd.var_details.frame(pad1,xmin,ymin,xmax,ymax) 
        self.fix_frame1(fr1)
        hstack.Draw('SAME,HIST')
        if not self.stack_sig:
            for s in sigs: 
                h = s.hist()
                s.sample.style_hist_line(h)
                h.Draw('SAME,HIST')
        for d in data: d.hist().Draw('SAME')
        leg.Draw()
        if do_log: pad1.SetLogy()
        self.draw_blinds(pd.var_details,xmin,ymin,xmax,ymax)
        
        ## bottom pad
        pad2.cd()
        fr2 = pd.var_details.frame(pad2,xmin,self.rmin,xmax,self.rmax)
        self.fix_frame2(fr2)
        if hratio: hratio.Draw('SAME') 
        line = ROOT.TLine()
        line.SetLineColor(ROOT.kRed)
        line.SetLineWidth(2)
        line.DrawLine(xmin,1.,xmax,1.)

        ## store new items as members to 
        ## prevent going out of scope
        self.hstack = hstack
        self.canvas = c
        self.hratio = hratio
        self.rline = line
        c.SaveAs('%s.eps'%cname)
        return c 





#------------------------------------------------------------
class MetaLegend(ROOT.TLegend):
    """
    A better TLegend class that increases in height as you call AddEntry.
    stolen of Ryan Reece's 'metaroot' package: 
        https://svnweb.cern.ch/trac/penn/browser/PennTau/metaroot
    """ 
#______________________________________________________________________________
    def __init__(self, width=0.30, height=0.05,
            x1=None, y1=None,
            x2=None, y2=None,
            border=0, fill_color=0, fill_style=0):
#        assert (x1 == y1 == None) or (x2 == y2 == None)
#        assert (x1 != None and y1 != None) or (x2 != None and y2 != None)

        if x1 == x2 == None:
            x2 = 0.93
            x1 = x2 - width
        elif x1 == None:
            x1 = x2 - width
        elif x2 == None:
            x2 = x1 + width

        if y1 == y2 == None:
            y2 = 0.93
            y1 = y2 - width
        elif y1 == None:
            y1 = y2 - width
        elif y2 == None:
            y2 = y1 + width

        ROOT.TLegend.__init__(self, x1, y1, x2, y2)
        self.SetBorderSize(border)
        self.SetFillColor(fill_color)
        self.SetFillStyle(fill_style)
        self.width = width
        self.height = height # per entry
        self._nentries = 0
        self._has_drawn = False
#______________________________________________________________________________
    def AddEntry(self, obj, label='', option='P'):
        self._nentries += 1
        self.resize()
        ROOT.TLegend.AddEntry(self, obj, label, option)
#______________________________________________________________________________
    def Draw(self):
        self.resize()
        ROOT.TLegend.Draw(self)
        self._has_drawn = True
#______________________________________________________________________________
    def resize(self):
        if self._has_drawn:
            y2 = self.GetY2NDC()
            self.SetY1NDC(y2 - (self.height*self._nentries) - 0.01)
        else:
            y2 = self.GetY2()
            self.SetY1(y2 - (self.height*self._nentries) - 0.01)
    





# - - - - - - - - - - function defs - - - - - - - - - - - - #
#____________________________________________________________
#def my_function():
#    '''
#    description of my_function
#    '''
#    pass

#____________________________________________________________
def make_legend(hists, labels, draw_options=None,
        width=0.30, height=0.05, x1=None, y1=None, x2=None, y2=None):
    """
    Creates a legend from a list of hists (or graphs).
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if draw_options is None:
        draw_options = ['P']*len(hists)
    if not isinstance(draw_options, list):
        draw_options = [draw_options]*len(hists)
    assert len(hists) == len(labels) == len(draw_options)
    leg = MetaLegend(width=width, height=height, x1=x1, y1=y1, x2=x2, y2=y2)

    for h, lab, opt in zip(hists, labels, draw_options):
        """
        if not opt in ('P', 'F', 'L', 'PL', 'LP'):
            ## assume opt is of the same format as draw_options used with Draw
            if opt.count('P'):
                if opt.count('E'):
                    opt = 'PL'
                else:
                    opt = 'P'
            else: # '', 'HIST', etc.
                opt = 'F'
        """
        leg.AddEntry(h, label=lab, option=opt)
    return leg















## EOF
