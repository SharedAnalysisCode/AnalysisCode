#!/usr/bin/env python
"""
pflock.py 
    1. process file lock
    2. (German, noun) stake, peg 
    3. a module for limitting parallel processes

A module for limitting the number of processes among several
computers with shared disk space.  Users can request a slot
given a queue_path accessible to all machines where the number
of simultaneous processes is bookkept.

Inspired by some codes here:
   - http://code.activestate.com/recipes/498171/
   - https://svnweb.cern.ch/trac/penn/browser/PhysicsNtuple/PhysicsLight/trunk/macros/batch/runPenn.py
"""

import os
import glob
import time


#------------------------------------------------------------------------------
# user methods
#------------------------------------------------------------------------------

#______________________________________________________________________________
def wait_for_slot(queue_path, n_slots, desc=None):
    sleep_time = 10
    n_simult = get_n(queue_path)
    while n_simult >= n_slots:
        time.sleep(sleep_time)
        n_simult = get_n(queue_path)
    i_slot = take_slot(queue_path, desc)
    n_simult += 1
    return i_slot, n_simult


#______________________________________________________________________________
def release_slot(queue_path, i_slot):
    slot_path =  os.path.join(queue_path, str(i_slot))
    cmd = 'rm %s' % slot_path
    os.system(cmd)


#______________________________________________________________________________
def release_all(queue_path):
    slots = get_occupied(queue_path)
    for i_slot in slots:
        release_slot(queue_path, i_slot)


#------------------------------------------------------------------------------
# helper methods
#------------------------------------------------------------------------------

#______________________________________________________________________________
def take_slot(queue_path, desc=None):
    slots = get_occupied(queue_path)
    i_slot = 0
    while i_slot in slots:
        i_slot += 1
    slot_path =  os.path.join(queue_path, str(i_slot))
#    assert not os.path.exists(slot_path)   ## will we lose the race?
    if desc:
        cmd = 'echo \'%s\' > %s' % (desc, slot_path)
    else:
        cmd = 'touch %s' % slot_path
    os.system(cmd)
    return i_slot


#______________________________________________________________________________
def get_occupied(queue_path):
    slots = glob.glob( os.path.join(queue_path, '*') )
    slot_indexes = [ int( os.path.basename(s) ) for s in slots ]
    slot_indexes.sort()
    return slot_indexes


#______________________________________________________________________________
def get_n(queue_path):
    return len(get_occupied(queue_path))

## EOF
