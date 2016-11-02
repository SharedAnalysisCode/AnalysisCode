"""
fileutils.py
"""

## std modules
import os

## ROOT
import ROOT

quiet = True

#______________________________________________________________________________
def write(obj, filename, dir='', write_option='RECREATE'):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    f = ROOT.gROOT.GetListOfFiles().FindObject(filename)
    if not f:
        f = ROOT.TFile.Open(filename, write_option)
    d = f.GetDirectory(dir)
    if not d:
        d = make_root_dir(f, dir)
    d.cd()
    if not quiet:
        print 'writing %s/%s/%s' % (filename, dir, obj.GetName())
        import sys 
        sys.stdout.flush()
    obj.Write()

#______________________________________________________________________________
def make_root_dir(f, dir):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    dir.rstrip('/')
    dir_split = dir.split('/')
    lead_dir = dir_split[0]
    sub_dirs = dir_split[1:]

    d = f.GetDirectory(lead_dir)
    if not d:
        d = f.mkdir(lead_dir)
    
    if sub_dirs:
        return make_root_dir(d, '/'.join(sub_dirs))
    else:
        return d

#__________________________________________________________________________
def strip_root_ext(filename, exts=None):
#    filename = os.path.basename(filename)
    if exts is None:
        exts = [
                '.canv.root',
                '.hist.root',
                '.skim.root',
                '.root',
                ]
    for ext in exts:
        if filename.endswith(ext):
            return filename[:-1*len(ext)]
    return filename

#______________________________________________________________________________
def walk(top, topdown=True):
    """
    os.path.walk like function for TDirectories.
    Return 4-tuple: (dirpath, dirnames, filenames, top)
        dirpath = 'file_name.root:/some/path' # may end in a '/'?
        dirnames = ['list', 'of' 'TDirectory', 'keys']
        filenames = ['list', 'of' 'object', 'keys']
        top = this level's TDirectory
    """
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    assert isinstance(top, ROOT.TDirectory)
    names = [k.GetName() for k in top.GetListOfKeys()]
    dirpath = top.GetPath()
    dirnames = []
    filenames = []
    ## filter names for directories
    for k in names:
        d = top.Get(k)
        if isinstance(d, ROOT.TDirectory):
            dirnames.append(k)
        else:
            filenames.append(k)
    ## sort
    dirnames.sort()
    filenames.sort()
    ## yield
    if topdown:
        yield dirpath, dirnames, filenames, top
    for dn in dirnames:
        d = top.Get(dn)
        for x in walk(d, topdown):
            yield x
    if not topdown:
        yield dirpath, dirnames, filenames, top


#______________________________________________________________________________
def ls(tfile, path=''):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if path:
        d = tfile.GetDirectory(path)
    else:
        d = tfile
    keys = [ k.GetName() for k in d.GetListOfKeys() ]
    keys.sort()
    for i_key, key in enumerate(keys):
        if isinstance(tfile.Get(key), ROOT.TDirectory):
            keys[i_key] = key + '/'
    return keys


#______________________________________________________________________________
def lsd(tfile, path=''):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    return filter( lambda key: isinstance(tfile.Get(key), ROOT.TDirectory), ls(tfile, path) )


#______________________________________________________________________________
def ls_objects(self):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    return filter( lambda key: not isinstance(tfile.Get(key), ROOT.TDirectory), ls(tfile, path) )


# EOF
