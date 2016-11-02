import ROOT
import ROOT_vector_vector
import os
import sys

# Miscellaneous root utils

#______________________________________________________________________________
def rootify(obj, type):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    Turn python objects into ROOT objects.
    """
    obj_root = None

    ## floats and ints
    if isinstance(obj, float) or isinstance(obj, int):
        obj_root = obj

    ## ROOT vectors
    if isinstance(obj, list):
        """
        http://stackoverflow.com/questions/11673493/instance-of-a-c-vector-in-python-for-ttrees-in-pyroot
        http://root.cern.ch/root/html/tutorials/tree/hvector.C.html
        """
        if not type.startswith('V'):
            sys.exit(' ERROR in %s. List supplied but type specified (%s) does not begin with "V". Exiting.' % (os.path.abspath(__file__), type))

        # retrieve type of list items
        items_type = contents(type)

        # make vector and fill
        obj_root = ROOT.vector(items_type)()
        obj_root.clear()
        for item in obj:
            obj_root.push_back(item)

    return obj_root


########################################################################
## free functions
########################################################################

#-----------------------------------------------------------------------
def contents(type):
    """
    Give the type of list, get the type of items in the list.
    """
    # vector
    if type == 'VF'  : return 'float'
    if type == 'VD'  : return 'double'
    if type == 'VI'  : return 'int'
    if type == 'VUI' : return 'unsigned int'
    if type == 'VTLV': return 'TLorentzVector'
    if type == 'VS'  : return 'string'
    # vector vector
    if type == 'VVF' : return 'vector<float,allocator<float> >'
    if type == 'VVD' : return 'vector<double,allocator<double> >'
    if type == 'VVI' : return 'vector<int,allocator<int> >'
    if type == 'VVS' : return 'vector<string,allocator<string> >'
    if type == 'VVUI': return 'vector<unsigned int,allocator<unsigned int> >'
    if type == 'VVUS': return 'vector<unsigned short,allocator<unsigned short> >'
    # break
    sys.exit(' ERROR in %s. Type "%s" not recognized. Exiting.' % (os.path.abspath(__file__), type))
             

