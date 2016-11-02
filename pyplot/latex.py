# encoding: utf-8
'''
latex.py

description:

'''
__author__    = "Will Davey"
__email__     = "will.davey@cern.ch"
__created__   = "2012-12-06"
__copyright__ = "Copyright 2012 Will Davey"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"



## modules
import os
import subprocess


# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class LatexDocument(object):
    '''
    class for creating latex docuements 
    '''
    #____________________________________________________________
    def __init__(self,
            _tex_filename,
            _doc_class = 'article'
            ):
        self.tex_filename = _tex_filename
        self.doc_class = _doc_class


        self.tex_file = open( self.tex_filename, 'w' )
        self.tex_name = self.tex_filename.replace( '.tex','')


    #____________________________________________________________
    def addLine( self, text = '' ):
        self.tex_file.write( '%s\n'%text )

    #____________________________________________________________
    def constructHeader( self ):
        self.addLine( '\\documentclass[]{%s}'%self.doc_class )
        self.addLine( '\\usepackage{graphicx}' )
        self.addLine( '\\usepackage[margin=0.5in]{geometry}' )
        self.addLine()
        self.addLine( '\\begin{document}' )
        self.addLine()

    #____________________________________________________________
    def constructFooter( self ):
        self.addLine()
        self.addLine( '\\end{document}' )

    
    #____________________________________________________________
    def calcFloatWidth( self, nx ):
        return 1. / nx * 0.95

    #____________________________________________________________
    def getTextWidthStringForN( self, nx ):
        return 'width=%f\\textwidth'%self.calcFloatWidth(nx)

    #____________________________________________________________
    def getTextWidthString( self, width ):
        return 'width=%f\\textwidth'%width

    #____________________________________________________________
    def addImage( self, epsfile, width ):
        width_str = self.getTextWidthString( width )
        self.addLine( '\\includegraphics[%s]{%s}'%(width_str,epsfile) )

    #____________________________________________________________
    def addFigure( self, epsfiles, nx, addCaption = False ):
        self.addLine( '\\begin{figure}[h!]' )
        width_str = self.getTextWidthStringForN( nx )
        for eps in epsfiles:
            self.addLine( '\\includegraphics[%s]{%s}'%(width_str,eps) )
        if addCaption: 
            for eps in epsfiles: self.addLine( '{\\tiny \\verb=%s=}'%(eps))

        self.addLine( '\\end{figure}' )


    #____________________________________________________________
    def clearPage( self ):
        self.addLine( '\\clearpage' )


    #____________________________________________________________
    def compile( self ):
        print 'compiling %s.tex'%self.tex_name
        self.tex_file.close()
        output = subprocess.Popen(["latex", '-interaction=batchmode', self.tex_name], stdout=subprocess.PIPE).communicate()[0]
        print output


    #____________________________________________________________
    def makePDF( self ):
        self.compile()
        print 'generating PDF %s.pdf ...'%self.tex_name
        output = subprocess.Popen(["dvipdf", self.tex_name], stdout=subprocess.PIPE).communicate()[0]
        print output
    

#------------------------------------------------------------
class LatexGallery(LatexDocument):
    '''
    class for creating picture galleries with latex 
    '''
    #____________________________________________________________
    def __init__(self,
            _tex_filename,
            _epsfiles,
            _nx             = 2, 
            _ny             = 3, 
            _captions = False,
            _title        = None,
            _title_fig = None,

            ):
        LatexDocument.__init__(self,_tex_filename, _doc_class = 'article' )
        self.epsfiles = _epsfiles
        self.nx = _nx
        self.ny    = _ny 
        self.captions = _captions
        self.width = self.calcFloatWidth( self.nx )
        self.title = _title
        self.title_fig = _title_fig

    #____________________________________________________________
    def constructHeader( self ):
        self.addLine( '\\documentclass[11pt,a4paper,twoside]{%s}'%self.doc_class )
        self.addLine( '\\setlength\\paperheight{11in}' )
        self.addLine( '\\setlength\\paperwidth{8.5in}' )
        self.addLine( '\\setlength\\voffset{-1in}' )
        self.addLine( '\\setlength\\hoffset{-1in}' )
        self.addLine( '\\setlength\\oddsidemargin{0.75in}' )
        self.addLine( '\\setlength\\evensidemargin{0.75in}' )
        self.addLine( '\\setlength\\topmargin{0.5in}' )
        self.addLine( '\\setlength\\textwidth{7.0in}' )
        self.addLine( '\\setlength\\textheight{10.25in}' )
        self.addLine( '\\usepackage{graphicx}' )
        if self.title: self.addLine( '\\title{%s}'%self.title )
        self.addLine( '\\begin{document}' )
        self.addLine( '\\pagestyle{empty}' )


    #____________________________________________________________
    def execute(self):
        self.constructHeader()

        if self.title: self.addLine( '\\maketitle' )
        if self.title_fig: self.addFigure( [self.title_fig], 1 ) 
        if self.title or self.title_fig: self.clearPage()
        self.addLine()


        figtuple = []
        # split into groups of 'nx'
        for i in range( 0, len( self.epsfiles ), self.nx ):
            figtuple.append( self.epsfiles[i:i+self.nx] )
    
        pagetuple = []
        # split figs into groups of 'ny'
        for i in range( 0, len( figtuple ), self.ny ):
            pagetuple.append( figtuple[i:i+self.ny] )
 
        for page in pagetuple:
            for fig in page:
                self.addFigure( fig, self.nx, self.captions ) 
            self.clearPage()

        self.constructFooter()
        self.makePDF()

#------------------------------------------------------------
class LatexTable(LatexDocument):
    '''
    class for creating tables with latex 
    '''
    #____________________________________________________________
    def __init__(self,
            _tex_filename,
            _column_map,
            _row_labels = None,
            _column_order = None,
            _title        = None,
            _caption = None,
            _label   = None,
            _size = 'small',
            _table_only = False,
            ):
        LatexDocument.__init__(self,_tex_filename, _doc_class = 'article' )
        self.column_map = _column_map
        self.row_labels = _row_labels
        self.column_order = _column_order
        self.title     = _title
        self.caption = _caption
        self.label = _label
        self.size = _size
        self.table_only = _table_only
    #____________________________________________________________
    def constructHeader( self ):
        self.addLine( '\\documentclass[11pt,a4paper,twoside]{%s}'%self.doc_class )
        self.addLine( '\\setlength\\paperheight{11in}' )
        self.addLine( '\\setlength\\paperwidth{8.5in}' )
        self.addLine( '\\setlength\\voffset{-1in}' )
        self.addLine( '\\setlength\\hoffset{-1in}' )
        self.addLine( '\\setlength\\oddsidemargin{0.75in}' )
        self.addLine( '\\setlength\\evensidemargin{0.75in}' )
        self.addLine( '\\setlength\\topmargin{0.5in}' )
        self.addLine( '\\setlength\\textwidth{7.0in}' )
        self.addLine( '\\setlength\\textheight{10.25in}' )
        self.addLine( '\\usepackage{graphicx}' )
        self.addLine( '\\begin{document}' )
        self.addLine( '\\pagestyle{empty}' )

    #____________________________________________________________
    def addHLine( self ):
        self.addLine( '\\hline' )

    #____________________________________________________________
    def addRow( self, row_arr ):
        row_str = ''
        for i in range(0,len(row_arr)):
            entry = row_arr[i]
            row_str += ' %s '%str(entry)
            if i == (len(row_arr)-1): row_str += '\\\\'
            else                                        : row_str += '&'
        
        self.addLine( row_str )


    #____________________________________________________________
    def startTable( self, opt_cols, opt_pos = 'h!' ):
        self.addLine( '\\begin{table}[%s]'%opt_pos )
        self.addLine( '\\%s'%self.size )
        self.addLine( '\\centering' )
        self.addLine( '\\begin{tabular}{%s}'%opt_cols )
        self.addHLine()
        self.addHLine()

    #____________________________________________________________
    def endTable( self ):
        self.addHLine()
        self.addHLine()
        self.addLine( '\\end{tabular}' )
        if self.caption: self.addLine( '\\caption{%s}'%self.caption )
        if self.label: self.addLine( '\\label{%s}'%self.label )
        self.addLine( '\\end{table}' )

    #____________________________________________________________
    def execute(self):
        if not self.table_only: self.constructHeader()
        
        # construct table header 
        opt_col = ''
        if self.row_labels: opt_col += 'l'
        opt_col += 'c'*len(self.column_map)
        self.startTable( opt_col )
     
        # determine column order
        order = self.column_order
        if not order:
            order = []
            for key in self.column_map: 
                order.append( key )
        
        # determin number of rows
        nrow = 0
        for key in order: 
            if not nrow: nrow = len( self.column_map[key] )
            else: nrow = min( nrow, len( self.column_map[key] ) )


        # construct row headings
        row_headings = []
        if self.row_labels: row_headings.append( ' ' )
        for key in order: row_headings.append( key )
        self.addRow( row_headings )
        self.addHLine()

        # fill columns
        for i in range(0,nrow):
            row = []
            if self.row_labels: row.append( self.row_labels[i] )
            for key in order: 
                row.append( self.column_map[key][i] )
            self.addRow( row )


        self.endTable()
        if not self.table_only: 
            self.constructFooter()
            self.makePDF()




# - - - - - - - - - - function defs - - - - - - - - - - - - #
#____________________________________________________________
def my_function():
    '''
    description of my_function
    '''
    pass






## EOF
