# This is a sample PBS script. It will request 1 processor on 1 node
# for 1 hours.
#   
#   Request 1 processors on 1 node 
#   
#PBS -l nodes=1:ppn=1


#PBS -l walltime=1:00:00
#PBS -m n
#
#   Request 4 gigabyte of memory per process
#
#PBS -l pmem=1gb
#!/bin/bash
STARTTIME=`date +%s`
date

#-------------------------------- ENV VARS -------------------------------
echo 
echo "Environment variables..."
echo " User name:   $USER"
echo " User home:   $HOME"
echo " Queue name:  $PBS_O_QUEUE"
echo " Job name:    $PBS_JOBNAME"
echo " Job-id:      $PBS_JOBID"
echo " Task-id:     $PBS_ARRAYID"
echo " Work dir:    $PBS_O_WORKDIR"
echo " Submit host: $PBS_O_HOST"
echo " Worker node: $HOSTNAME"
echo " Temp dir:    $TMPDIR"
echo " parameters passed: $*"
echo 

echo " VAR:       $VAR"
echo " REG:       $REG"
echo " LAB:       $LAB"
echo " TAG:       $TAG"
echo " ICUT:      $ICUT"
echo " MAKEPLOT:  $MAKEPLOT"
echo " FAKEST:    $FAKEST"
echo " INDIR:     $INDIR"
echo " OUTDIR:    $OUTDIR"
echo " SCRIPT:    $SCRIPT"
echo " INTARBALL: $INTARBALL"

echo 
export 

MYDIR=Plots_${RANDOM}${RANDOM}

#-------------------------------- NODE CONFIG ------------------------------
echo "going to tmp node dir: $TMPDIR"
cd $TMPDIR
ls -alh

echo "ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "mkdir ${MYDIR}"
mkdir ${MYDIR}

echo "ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "cd ${MYDIR}"
cd ${MYDIR}

setupATLAS
lsetup root

## copy over working area
echo "copying input tarball ${INTARBALL}..."
cp $INTARBALL .
date
ENDTIME=`date +%s`
TOTALTIME=$(($ENDTIME-$STARTTIME))
echo "Total Time: ${TOTALTIME}s"

ls -alh

echo "extracting input tarball..."
tar xvzf *.tar.gz 
ls -alh

date
ENDTIME=`date +%s`
TOTALTIME=$(($ENDTIME-$STARTTIME))
echo "Total Time: ${TOTALTIME}s"
echo "done setting working area"

echo 
echo "setting up workarea..."
source setup.sh

echo ""
echo "executing job..."
echo "python ${SCRIPT} --var=${VAR} --reg=${REG} --lab=${LAB} --tag=${TAG} --icut=${ICUT} --makeplot=${MAKEPLOT} --fakest=${FAKEST} --input=${INDIR} --output=${OUTDIR}"
python ${SCRIPT} --var=${VAR} --reg=${REG} --lab=${LAB} --tag=${TAG} --icut=${ICUT}  --makeplot=${MAKEPLOT} --fakest=${FAKEST} --input=${INDIR} --output=${OUTDIR}
echo "finished execution"

echo "copying output"

#echo "cp ${MYDIR}/*.eps ${OUTDIR}"
#cp ${MYDIR}/*.eps ${OUTDIR}

echo "cd ${TMPDIR}"
cd ${TMPDIR}

echo "ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "rm -rf ${MYDIR}"
rm -rf ${MYDIR}

echo "ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "finished job"

date
ENDTIME=`date +%s`
TOTALTIME=$(($ENDTIME-$STARTTIME))
echo "Total Time: ${TOTALTIME}s"


