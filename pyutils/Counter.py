#
# taken from: http://code.activestate.com/recipes/576611/
#

import math

from operator import itemgetter
from heapq import nlargest
from itertools import repeat, ifilter

class Counter(dict):
    '''Dict subclass for counting hashable objects.  Sometimes called a bag
    or multiset.  Elements are stored as dictionary keys and their counts
    are stored as dictionary values.

    >>> Counter('zyzygy')
    Counter({'y': 3, 'z': 2, 'g': 1})

    '''

    def __init__(self, iterable=None, **kwds):
        '''Create a new, empty Counter object.  And if given, count elements
        from an input iterable.  Or, initialize the count from another mapping
        of elements to their counts.

        >>> c = Counter()                           # a new, empty counter
        >>> c = Counter('gallahad')                 # a new counter from an iterable
        >>> c = Counter({'a': 4, 'b': 2})           # a new counter from a mapping
        >>> c = Counter(a=4, b=2)                   # a new counter from keyword args

        '''        
        self.update(iterable, **kwds)

    def __missing__(self, key):
        return 0

    def most_common(self, n=None):
        '''List the n most common elements and their counts from the most
        common to the least.  If n is None, then list all element counts.

        >>> Counter('abracadabra').most_common(3)
        [('a', 5), ('r', 2), ('b', 2)]

        '''        
        if n is None:
            return sorted(self.iteritems(), key=itemgetter(1), reverse=True)
        return nlargest(n, self.iteritems(), key=itemgetter(1))

    def elements(self):
        '''Iterator over elements repeating each as many times as its count.

        >>> c = Counter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        If an elements count has been set to zero or is a negative number,
        elements() will ignore it.

        '''
        for elem, count in self.iteritems():
            for _ in repeat(None, count):
                yield elem

    # Override dict methods where the meaning changes for Counter objects.

    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError(
            'Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update(self, iterable=None, **kwds):
        '''Like dict.update() but add counts instead of replacing them.

        Source can be an iterable, a dictionary, or another Counter instance.

        >>> c = Counter('which')
        >>> c.update('witch')           # add elements from another iterable
        >>> d = Counter('watch')
        >>> c.update(d)                 # add elements from another counter
        >>> c['h']                      # four 'h' in which, witch, and watch
        4

        '''        
        if iterable is not None:
            if hasattr(iterable, 'iteritems'):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, 0) + count
                else:
                    dict.update(self, iterable) # fast path when counter is empty
            else:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1
        if kwds:
            self.update(kwds)

    def copy(self):
        'Like dict.copy() but returns a Counter instance instead of a dict.'
        return Counter(self)

    def __delitem__(self, elem):
        'Like dict.__delitem__() but does not raise KeyError for missing values.'
        if elem in self:
            dict.__delitem__(self, elem)

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    # Multiset-style mathematical operations discussed in:
    #       Knuth TAOCP Volume II section 4.6.3 exercise 19
    #       and at http://en.wikipedia.org/wiki/Multiset
    #
    # Outputs guaranteed to only include positive counts.
    #
    # To strip negative and zero counts, add-in an empty counter:
    #       c += Counter()

    def __add__(self, other):
        '''Add counts from two counters.

        >>> Counter('abbb') + Counter('bcc')
        Counter({'b': 4, 'c': 2, 'a': 1})


        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] + other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __sub__(self, other):
        ''' Subtract count, but keep only results with positive counts.

        >>> Counter('abbbc') - Counter('bccd')
        Counter({'b': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] - other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __or__(self, other):
        '''Union is the maximum of value in either of the input counters.

        >>> Counter('abbb') | Counter('bcc')
        Counter({'b': 3, 'c': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        _max = max
        result = Counter()
        for elem in set(self) | set(other):
            newcount = _max(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result

    def __and__(self, other):
        ''' Intersection is the minimum of corresponding counts.

        >>> Counter('abbb') & Counter('bcc')
        Counter({'b': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        _min = min
        result = Counter()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = _min(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result


#-----------------------------------------------------------------------------

from OrderedDict import OrderedDict

class OrderedCounter(Counter, OrderedDict):
    """
    Counter that remembers the order elements are first encountered.
    taken from: http://docs.python.org/dev/library/collections.html#ordereddict-examples-and-recipes
    """

    def __init__(self, iterable=None, **kwds):
        OrderedDict.__init__(self)
        Counter.__init__(self, iterable, **kwds)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return self.__class__, (OrderedDict(self),)


#-----------------------------------------------------------------------------

import math

class CutFlow(object):

    def __init__(self):
        self.raw = OrderedCounter()
        self.w = OrderedCounter()
        self.w2 = OrderedCounter()

    def __str__(self):
        s = '%3s %-40s %16s %16s %16s %16s %6s\n' % ('#', 'CUT', 'RAW', 'FRAC', 'WEIGHTED', 'FRAC', 'ERR')
        tab = self.make_table()
        for row in tab:
            i_key, key, raw, frac_raw, val, frac_val, err = row
            s += '%02i %-40s %16i %16.3f %16.1f %16.3f %6.1f\n' % (i_key, key, raw, frac_raw, val, frac_val, err)
        s += '\n'
        return s

    def count(self, key, weight=1):
        self.raw.setdefault(key, 0)
        self.w.setdefault(key, 0)
        self.w2.setdefault(key, 0)
        self.raw.update({key:1})
        self.w.update({key:weight})
        self.w2.update({key:weight*weight})

    def count_if(self, cond, key, weight=1):
        self.raw.setdefault(key, 0)
        self.w.setdefault(key, 0)
        self.w2.setdefault(key, 0)
        if cond:
            self.count(key, weight)
        return cond

    def make_table(self):
        tab = []
        for i_key, key in enumerate(self.w.iterkeys()):
            raw       = self.raw.get(key)
            val       = self.w.get(key)
            if i_key == 0:
                raw_0 = float(raw)
                val_0 = val
            frac_raw  = raw / raw_0 if raw_0 else 0.0
            frac_val  = val / val_0 if val_0 else 0.0
            err       = math.sqrt(self.w2.get(key))
            row = [i_key, key, raw, frac_raw, val, frac_val, err]
            tab.append(row)
        return tab

    def make_hist(self, name='h_cut_flow'):
        tab = self.make_table()
        import ROOT
        n_rows = len(tab)
        h = ROOT.TH1D(name, '', n_rows, 0.0, n_rows)
        x_axis = h.GetXaxis()
        for row in tab:
            i_key, key, raw, frac_raw, val, frac_val, err = row
            i_bin = i_key + 1
            h.SetBinContent(i_bin, val)
            h.SetBinError(i_bin, err)
            x_axis.SetBinLabel(i_bin, key)
        return h

    def make_hist_raw(self, name='h_cut_flow_raw'):
        tab = self.make_table()
        import ROOT
        n_rows = len(tab)
        h = ROOT.TH1D(name, '', n_rows, 0.0, n_rows)
        x_axis = h.GetXaxis()
        for row in tab:
            i_key, key, raw, frac_raw, val, frac_val, err = row
            i_bin = i_key + 1
            h.SetBinContent(i_bin, raw)
            h.SetBinError(i_bin, math.sqrt(raw))
            x_axis.SetBinLabel(i_bin, key)
        return h

#-----------------------------------------------------------------------------

if __name__ == '__main__':
    import doctest
    print doctest.testmod()

