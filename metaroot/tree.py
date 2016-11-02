"""
metaroot.tree module

Module for creating, filling, and saving ROOT.TTree objects.

Part of the metaroot package.
"""

__author__ = 'Ryan D. Reece'
__email__ = 'ryan.reece@cern.ch'
__created__ = '2008-05-01'
__copyright__ = 'Copyright 2008-2010 Ryan D. Reece'
__license__ = 'GPL http://www.gnu.org/licenses/gpl.html'

#------------------------------------------------------------------------------

from array import array
import ROOT
import metaroot

#------------------------------------------------------------------------------
# TreeMaker Class
#------------------------------------------------------------------------------
class TreeMaker(object):
    """Class for creating ROOT TTrees from Python lists of data."""
#______________________________________________________________________________
    def __init__(self, name, vars, types=metaroot.default, title='',
            root_file_name='', max_array=599):
        """
        vars:   List of variable names. ex: ['var1', 'var2', 'var3']
            If the variable is an array, then one can specify the size as
            a literal number: 'a[10]', or as a previously named variable:
            ['size', 'vec[size]']. There is only support for 1-dimensional
            arrays.
        types:  A list of the typecodes specifying the type of the data that
            will be stored in the variables named by vars. The typecodes are
            those used by array.array. ex: ['i', 'f', ]
            By default, all typecodes will be set to 'f'. Note that ROOT's
            typecodes are generally the swapcase of array's, so this __init__
            uses the str function swapcase(), and you should only use typecodes
            for which there are corresponding array and ROOT codes. See
            documentation for ROOT.TTree and array.array.
            array code      ROOT code   C Type (ROOT)       
            'c'             'C'         character
            'b'             'B'         signed integer (8 bit Char_t)
            'B'             'b'         unsigned integer (8 bit UChar_t)
            'i'             'I'         signed integer (32 bit Int_t)
            'I'             'i'         unsigned integer (32 bit UInt_t)
            'l'             'L'         signed integer (64 bit Long64_t)
            'L'             'l'         unsigned integer (64 bit Long64_t)
            'f'             'F'         floating point (32 bit Float_t)
            'd'             'D'         floating point (64 bit Double_t)
                            'S'         (16 bit Short_t)
                            's'         (16 bit UShort_t)
                            'O'         (Bool_t)
            'u'                         Unicode character
            'h'                         signed integer   
            'H'                         unsigned integer 
        name:   Name of TTree. By default, this is set to the name of the first
            variable.
        title:  Title of TTree. By default, this is set to name.
        root_file_name:  name of ROOT file. Should include the '.root'
            suffix. By default, this is set to <name of the tree>.root.
        max_array:  the maximum size of any array used. The size is specified
            as a previous variable name, as in vars = ['size', 'vec[size]'].
        """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # set defaults
        if types is metaroot.default:
            types = ['f']*len(vars)
        assert len(vars) == len(types)
        title = title or name
        root_file_name = root_file_name or name + '.root'
        # initialize
        self._root_file = ROOT.TFile(root_file_name, 'RECREATE')
        self._tree = ROOT.TTree(name, title)
        self._bufs = []
        # create branches
        for v, t in zip(vars, types):
            if v.find('[') == -1: # single var
                self._bufs.append(array(t, [0]))
                self._tree.Branch(v, self._bufs[-1], '%s/%s' % (v, t.swapcase()))
            else: # array
                v_split = v.split('[')
                v_no_brak = v_split[0]
                v_braks = [x.rstrip(']') for x in v_split[1:]]
                assert len(v_braks) == 1
                if v_braks[0].isdigit():
                    self._bufs.append(array(t, int(v_braks[0])*[0]))
                else:
                    self._bufs.append(array(t, max_array*[0]))
                self._tree.Branch(v_no_brak, self._bufs[-1], '%s/%s' % (v, t.swapcase()))
#______________________________________________________________________________
    def fill(self, data):
        """
        Fills an entry (event) in the TTree with data.
        data:   A list of the data in the same order as the corresponding
            vars passed to __init__.
        """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        assert len(data) == len(self._bufs), 'len(data) = %s, len(self._bufs) = %s' % (len(data), len(self._bufs))
        for b, d in zip(self._bufs, data):
            if isinstance(d, list):
                for i, x in enumerate(d):
                    b[i] = x
            else:
                b[0] = d
        self._tree.Fill()
#______________________________________________________________________________
    def fill_many(self, datas):
        """
        Fills multiple entries in the TTree, where datas is a list of data lists.
        """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        for data in zip(*datas):
            self.fill(data)
#______________________________________________________________________________
    def write(self):
        """
        Writes the tree to the ROOT file, closes the file, and returns the file
        name.
        """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self._root_file.cd()
        self._tree.Write()
        root_file_name = self._root_file.GetName()
        self._root_file.Close()
        return root_file_name

#------------------------------------------------------------------------------

