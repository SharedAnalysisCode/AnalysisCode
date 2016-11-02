# encoding: utf-8
'''
systematics.py

description:

'''
## modules

# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class Systematic(object):
    '''
    class to hold info about systematics 
    '''
    #____________________________________________________________
    def __init__(self,
            name,
            title=None,
            var_up=None,
            var_dn=None,
            flat_err=None,
            ):
        self.name = name
        if not title: title = name
        self.title = title
        self.var_up=var_up
        self.var_dn=var_dn
        self.flat_err=flat_err 
        assert (self.var_up and self.var_dn) or self.flat_err!=None, 'Must provide either up and dn vars or a flat err!'


sys_dict = {}
# Specific for categories (acceptance unc)

SYS1 = sys_dict['SYS1'] = Systematic(
        'SYS1',
        var_up='SYS1_UP',
        var_dn='SYS1_DN'
        )
SYS2 = sys_dict['SYS2'] = Systematic(
        'SYS2','$\\sigma_{\\rm Diboson}$',      
        flat_err=0.05,
        )

FF = sys_dict['FF'] = Systematic(
        'FF',
        var_up='FF_UP',
        var_dn='FF_DN'
        )

## EOF
