# encoding: utf-8
'''
var.py
description:

'''

## modules


# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class Var(object):
    '''
    class to hold variable info for plotting
    '''
    #________________________________________________________
    def __init__(self,
            name,
            hname = None,
            title = None,
            path  = None,
            rebin = None,
            xmin  = None,
            xmax  = None,
            log   = None,
            ):
        self.name = name
        if not title: title = name
        if not hname: 
          if "cutflow" in name: hname = name
          else: hname = 'h_'+name
        self.hname = hname
        self.title = title
        self.path  = path
        self.rebin = rebin
        self.xmin  = xmin
        self.xmax  = xmax
        self.log   = log



## EOF
