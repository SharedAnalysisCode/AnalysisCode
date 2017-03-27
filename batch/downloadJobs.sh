jobList=$1;
mkdir -p ./logs
for line in `cat $jobList`; do
    rucio download ${line}_tree.root 2>&1 | tee logs/log.${line}_tree
    rucio download ${line}_cutflow.root 2>&1 | tee logs/log.${line}_cutflow
    rucio download ${line}_metadata.root 2>&1 | tee logs/log.${line}_metadata
done