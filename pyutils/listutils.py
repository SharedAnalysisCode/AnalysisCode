"""
listutils

author: Ryan Reeece  <ryan.reece@cern.ch>

2011-08-01
"""

#______________________________________________________________________________
def divide(li, n): 
    """ Yield successive n lists of even size.
>>> [x for x in listutils.divide(range(10), 3)]
[[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    start = 0 
    for i in xrange(n):
        stop = start + len(li[i::n])
        yield li[start:stop]
        start = stop


#______________________________________________________________________________
def chunk(li, n): 
    """ Yield successive n-sized chunks from l.
>>> [x for x in listutils.chunk(range(10), 3)]
[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    for i in xrange(0, len(li), n): 
        yield li[i:i+n]


