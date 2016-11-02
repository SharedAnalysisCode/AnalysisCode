# encoding: utf-8
'''
utils.py

description:

'''
__author__    = "Will Davey"
__email__     = "will.davey@cern.ch"
__created__   = "2013-02-19"
__copyright__ = "Copyright 2013 Will Davey"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"



## modules
import sys


# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class MyClass():
    '''
    description of MyClass
    '''
    #____________________________________________________________
    def __init__(self):
        pass



# - - - - - - - - - - function defs - - - - - - - - - - - - #


#____________________________________________________________
def print_progress(frac,info=None,width=40,title=''):
    """
    simple implementation of a shell progress bar
    """
    bar = '[%-'+str(width)+'s] %.f%%'

    sys.stdout.write('\r')
    # the exact output you're looking for:
    inc = int(frac * float(width))
    if info!=None:
        sys.stdout.write('%s\n'%(str(info)) + title + bar % ('='*inc, frac*100.))
    else:
        sys.stdout.write(title + bar % ('='*inc, frac*100.))
    sys.stdout.flush()

#____________________________________________________________
def clear_progress():
    sys.stdout.write('\n')







## EOF
