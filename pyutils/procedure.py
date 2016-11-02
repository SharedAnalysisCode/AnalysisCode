"""
procedure.py
"""

## std
#import time
#import os
#import sys
#import optparse
#import dircache

## pyutils
import progressbar

#path_of_this_file = os.path.abspath( __file__ )
#dir_of_this_file = os.path.dirname( path_of_this_file )


#------------------------------------------------------------------------------
class Procedure(object):

    #__________________________________________________________________________
    def __init__(self):
        self._steps = []
        self._i_step = 0

    #_________________________________________________________________________
    def __iadd__(self, s):
        self._steps.append(s)
        return self

    #_________________________________________________________________________
    def go(self):
        progress_bar = progressbar.ProgressBar('blue', width=20, block='=', empty='-', min=0, max=self.n_steps())
        done = False
        while not done:
            error_code = self.execute()
            if error_code == 0:
                print 'Step completed successfully.'
                uin = raw_input('Press enter to continue:').strip()
                self.next()
            elif error_code == 1:
                print 'This step failed.'
                uin = raw_input('Press enter to continue:').strip()
                 pass
            elif error_code == 2:
                 pass
            else:
                 pass

    #_________________________________________________________________________
    def next(self):
        if self._i_step+1 < self.n_steps():
            self._i_step += 1
            return True
        else:
             return False

    #_________________________________________________________________________
    def prev(self):
        if self._i_step-1 >= 0:
            self._i_step -= 1
            return True
        else:
             return False

    #_________________________________________________________________________
    def execute(self, i=None):
        if not i is None:
            self._i_step = i
        return self._steps[self._i_step].execute()
        
    #_________________________________________________________________________
    def n_steps(self):
        return len(self._steps)

    #_________________________________________________________________________
    def get_step(self):
        return self._i_step


#------------------------------------------------------------------------------
class Step(object):

    #__________________________________________________________________________
    def __init__(self):
        pass

    #__________________________________________________________________________
    def execute(self):
    """
    Over-write this method.
    """
        return True

    #__________________________________________________________________________
    def check(self):
    """
    Over-write this method.  Return True on success.
    """
        return True

    #__________________________________________________________________________
    def finalize(self):
    """
    Over-write this method to cleanup after execute finished successfully.
    """
        return True

    #__________________________________________________________________________
    def cleanup(self):
    """
    Over-write this method to cleanup before retrying.
    """
        return True

    #__________________________________________________________________________
    def retry(self):
        self.cleanup()
        return self.execute()


# EOF
