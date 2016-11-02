#!/bin/bash
#
# file: setup.sh
#
###############################################################################


##-----------------------------------------------------------------------------
## parse command line args
usage() {
  echo
  echo "Bash script for setting PATH and PYTHONPATH for SSDiLep analysis."
  echo
  echo "usage:"
  echo "        $0 [OPTIONS]"
  echo "options:"
  echo "        -h for usage"
  echo
  exit
}

##-----------------------------------------------------------------------------
## pre-setup, don't touch

path_of_this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export MAIN=${path_of_this_dir}

add_to_python_path()
{
    export PYTHONPATH=$1:$PYTHONPATH
    echo "  Added $1 to your PYTHONPATH."
}

add_to_path()
{
    export PATH=$1:$PATH
    echo "  Added $1 to your PATH."
}

##-----------------------------------------------------------------------------
## setup PYTHONPATH

echo "  Setting up your PYTHONPATH."
add_to_python_path ${MAIN}   # metaroot, pyframe
add_to_python_path ${MAIN}/pyutils
add_to_python_path ${MAIN}/metaroot
add_to_python_path ${MAIN}/pyplot
echo "  done."


##-----------------------------------------------------------------------------
## setup ENV

#export LOADERPATH=${MAIN}/pyframe
#echo "LOADERPATH: ${LOADERPATH}"
##-----------------------------------------------------------------------------
## setup PATH

#echo "  Setting up your PATH."
#add_to_path ${PENN_TAU_PATH}/pyscripts
#add_to_path ${PENN_TAU_PATH}/root2html
#add_to_path ${PENN_TAU_PATH}/tree_trimmer
#add_to_path ${PENN_TAU_PATH}/grid
#echo "  done."

##-----------------------------------------------------------------------------
## setup external packages
##TOPDIR=${PWD}
##cd ${TOPDIR}/packages; source setup.sh
##cd ${TOPDIR}

# EOF
