#!/bin/bash

# This is a sample PBS script. 
# It will request 1 processor 
# on 1 node for 1 hours.

#PBS -S /bin/bash

# ------------------------------  
# Request 1 processors on 1 node 
# ------------------------------ 
#PBS -l nodes=1:ppn=1

# --------  
# Walltime
# --------
#PBS -l walltime=24:00:00

# ----------------------------------------
# Request 1 gigabyte of memory per process
# ----------------------------------------
#PBS -l pmem=1gb


STARTTIME=`date +%s`
date

echo 
echo "Environment variables..."
echo " User name:     $USER"
echo " User home:     $HOME"
echo " Queue name:    $PBS_O_QUEUE"
echo " Job name:      $PBS_JOBNAME"
echo " Job-id:        $PBS_JOBID"
echo " Work dir:      $PBS_O_WORKDIR"
echo " Submit host:   $PBS_O_HOST"
echo " Worker node:   $HOSTNAME"
echo " Temp dir:      $TMPDIR"
echo " parameters passed: $*"
echo 

echo " SCRIPT:        $SCRIPT"
echo " TREEFILE:      $TREEFILE"
echo " METAFILE:      $METAFILE"
echo " CUTFLOWFILE:   $CUTFLOWFILE"
echo " MERGEDTREE:    $MERGEDTREE"
echo " MERGEDMETA:    $MERGEDMETA"
echo " MERGEDCUTFLOW: $MERGEDCUTFLOW"
echo " OUTTREE:       $OUTTREE"
echo " OUTMETA:       $OUTMETA"
echo " OUTCUTFLOW:    $OUTCUTFLOW"
echo " MERGED:        $MERGED"
echo " OUTMERGED:     $OUTMERGED"

echo
export 

MYDIR=Get_${RANDOM}${RANDOM}

# ----------------
# This is the job!
# ----------------

export X509_USER_PROXY=/coepp/cephfs/mel/fscutti/jobdir/x509up_u1132
setupATLAS
lsetup rucio
lsetup root

echo ""
echo "executing job..."

echo "-----> ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "-----> rm -rf ${MYDIR}"
rm -rf ${MYDIR}

#echo "-----> rm -rf *.root"
#rm -rf *.root

echo "-----> ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "-----> mkdir ${TMPDIR}/${MYDIR} "
mkdir ${TMPDIR}/${MYDIR} 

echo "-----> ls ${TMPDIR} -la"
ls ${TMPDIR} -la


# ----------------------------
# download and merge tree file
# ----------------------------
echo "-----> rucio download --dir=${TMPDIR}/${MYDIR} ${TREEFILE}"
rucio download --dir=${TMPDIR}/${MYDIR} ${TREEFILE}

echo "-----> ls ${TMPDIR}/${MYDIR}/${TREEFILE} -la"
ls ${TMPDIR}/${MYDIR}/${TREEFILE} -la

echo "-----> cp -rf ${TMPDIR}/${MYDIR}/${TREEFILE} ${OUTTREE}"
cp -rf ${TMPDIR}/${MYDIR}/${TREEFILE} ${OUTTREE}

echo "-----> cd ${TMPDIR}/${MYDIR}/${TREEFILE}"
cd ${TMPDIR}/${MYDIR}/${TREEFILE}

echo "-----> hadd ${MERGEDTREE} *.root*"
hadd ${MERGEDTREE} *.root*

echo "-----> cp ${MERGEDTREE} ${TMPDIR}/${MYDIR}"
cp ${MERGEDTREE} ${TMPDIR}/${MYDIR}

echo "-----> cd ${TMPDIR}/${MYDIR}"
cd ${TMPDIR}/${MYDIR}

echo "-----> ls ${TMPDIR}/${MYDIR} -la"
ls ${TMPDIR}/${MYDIR} -la


# ----------------------------
# download and merge meta file
# ----------------------------
echo "-----> rucio download --dir=${TMPDIR}/${MYDIR} ${METAFILE}"
rucio download --dir=${TMPDIR}/${MYDIR} ${METAFILE}

echo "-----> ls ${TMPDIR}/${MYDIR}/${METAFILE} -la"
ls ${TMPDIR}/${MYDIR}/${METAFILE} -la

echo "-----> cp -rf ${TMPDIR}/${MYDIR}/${METAFILE} ${OUTMETA}"
cp -rf ${TMPDIR}/${MYDIR}/${METAFILE} ${OUTMETA}

echo "-----> cd ${TMPDIR}/${MYDIR}/${METAFILE}"
cd ${TMPDIR}/${MYDIR}/${METAFILE}

echo "-----> hadd ${MERGEDMETA} *.root*"
hadd ${MERGEDMETA} *.root*

echo "-----> cp ${MERGEDMETA} ${TMPDIR}/${MYDIR}"
cp ${MERGEDMETA} ${TMPDIR}/${MYDIR}

echo "-----> cd ${TMPDIR}/${MYDIR}"
cd ${TMPDIR}/${MYDIR}

echo "-----> ls ${TMPDIR}/${MYDIR} -la"
ls ${TMPDIR}/${MYDIR} -la


# -------------------------------
# download and merge cutflow file
# -------------------------------
echo "-----> rucio -v get --dir=${TMPDIR}/${MYDIR} ${CUTFLOWFILE}"
rucio -v get --dir=${TMPDIR}/${MYDIR} ${CUTFLOWFILE}

echo "-----> ls ${TMPDIR}/${MYDIR}/${CUTFLOWFILE} -la"
ls ${TMPDIR}/${MYDIR}/${CUTFLOWFILE} -la

echo "-----> cp -rf ${TMPDIR}/${MYDIR}/${CUTFLOWFILE} ${OUTCUTFLOW}"
cp -rf ${TMPDIR}/${MYDIR}/${CUTFLOWFILE} ${OUTCUTFLOW}

echo "-----> cd ${TMPDIR}/${MYDIR}/${CUTFLOWFILE}"
cd ${TMPDIR}/${MYDIR}/${CUTFLOWFILE}

echo "-----> hadd ${MERGEDCUTFLOW} *.root*"
hadd ${MERGEDCUTFLOW} *.root*

echo "-----> cp ${MERGEDCUTFLOW} ${TMPDIR}/${MYDIR}"
cp ${MERGEDCUTFLOW} ${TMPDIR}/${MYDIR}

echo "-----> cd ${TMPDIR}/${MYDIR}"
cd ${TMPDIR}/${MYDIR}

echo "-----> ls ${TMPDIR}/${MYDIR} -la"
ls ${TMPDIR}/${MYDIR} -la

# ----------------------
# merge cutflow and tree
# ----------------------
echo "-----> hadd ${MERGED} ${MERGEDTREE} ${MERGEDMETA} ${MERGEDCUTFLOW}"
hadd ${MERGED} ${MERGEDTREE} ${MERGEDMETA} ${MERGEDCUTFLOW}

echo "-----> ls ${TMPDIR}/${MYDIR} -la"
ls ${TMPDIR}/${MYDIR} -la

echo "-----> cp ${MERGED} ${OUTMERGED}"
cp ${MERGED} ${OUTMERGED}

echo "-----> cd ${TMPDIR}"
cd ${TMPDIR}

echo "-----> rm -rf ${MYDIR}"
rm -rf ${MYDIR}

#echo "-----> rm -rf *.root"
#rm -rf *.root

echo "-----> ls ${TMPDIR} -la"
ls ${TMPDIR} -la

# EOF

