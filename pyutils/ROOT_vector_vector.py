import re
rex_type = re.compile(r"<type '(\w+)'>\Z")
rex_vector = re.compile(r"<class '__main__.vector\s*<([\w\s]+)\s*(,\s*allocator\s*<[\w\s]+>)?\s*>'>")
rex_vector_vector = re.compile(r"<class '__main__.vector<\s*vector\s*<([\w\s]+)(,\s*allocator<[\w\s]+>\s*)?>\s*(,\s*allocator\s*<\s*vector\s*<[\w\s]+,\s*allocator\s*<[\w\s]+>\s+>\s+>)?\s+>'>")
    
import sys, os
_path_of_this_file = os.path.realpath(os.path.dirname(__file__))
_c_path = os.path.join(_path_of_this_file, 'ROOT_vector_vector.C')

import ROOT
ROOT.gROOT.ProcessLine('.L %s+' % _c_path)

#ROOT.gROOT.ProcessLine("""
#include <string>
#ifdef __MAKECINT__
#pragma link C++ class vector<vector<int> >+;
#pragma link C++ class vector<vector<float> >+;
#pragma link C++ class vector<vector<double> >+;
#pragma link C++ class vector<vector<string> >+;
#endif""")
