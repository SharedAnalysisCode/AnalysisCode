
## modules
import ROOT
import sys

## logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

open_files = []


# File Access
#____________________________________________________________________________
def open_file( file_name ):
  # search for file existance
  if ROOT.gROOT.GetListOfFiles():
    f = ROOT.gROOT.GetListOfFiles().FindObject(file_name)
    if f:
      log.debug( 'retrieved file: %s from open files' % file_name )
      return f
  f = ROOT.TFile(file_name)
  if f:
    global open_files
    open_files.append(f)
    log.debug( 'opened file: %s' % file_name )
    return f
  else:
    log.error( 'file: %s doesn\'t exist' % file_name )
    return None

#____________________________________________________________________________
def new_file( file_name_base ):
  # search for file existance
  log.debug( 'in newFile:' )
  log.debug( 'file_name_base: %s' % file_name_base )
  file_name = '%s_%s.root' % ( file_name_base,Globals.timestamp ) 
#  file_name = '%s.root' % ( file_name_base ) 
  if ROOT.gROOT.GetListOfFiles():
    f = ROOT.gROOT.GetListOfFiles().FindObject(file_name)
    if f:
      log.debug( 'retrieved file: %s from open files' % file_name )
      return f
  f = ROOT.TFile(file_name,'RECREATE')
  if f:
    global open_files
    open_files.append(f)
    log.info( 'created new file: %s' % file_name )
    return f
  else:
    log.error( 'file: %s doesn\'t exist' % file_name )
    return None

#____________________________________________________________________________
def close( file_name ):
  f = open_file( file_name )
  if f: 
      global open_files
      open_files.remove(f)
      f.Close()

#____________________________________________________________________________
def mkdir( f, dir_name ):
  log.debug( 'in mkdir' )
  directory = f.GetDirectory('')
  if f.GetDirectory(dir_name): 
    directory = f.GetDirectory(dir_name)
    return directory
  else: 
    dirs = []
    temp = dir_name
    log.debug( temp )
    while temp != '' and temp != '/' :
      dirs.insert(0,os.path.basename(temp))
      temp = os.path.dirname( temp )
      log.debug( temp )
    log.debug( 'dir structure for: %s' % dir_name )
    log.debug( dirs )
    for dir in dirs:
      if directory.GetDirectory(dir):
        directory = directory.GetDirectory(dir)
      else:
        directory = directory.mkdir(dir)

  return directory


# ROOT Object Access
#________________________________________________________________________________
def get_object(obj_name,filename):
  log.debug( 'in getObject: %s for file: %s' % (obj_name, filename ))
  f = open_file( filename )
  if not f: log.error( 'failure opening file in getObject, returning None' )
  assert(f)

  temp = f.Get(obj_name)
  if not temp: log.warn( 'failed to retrieve obj: %s from file: %s' % (obj_name,f.GetName()) )
  return temp


#________________________________________________________________________________
def save_object(obj, filename, dirname = None ):
  f = new( filename )
  if dirname: d  = mkdir( f, dirname )
  else      : d  = f
  d.WriteTObject( obj )


