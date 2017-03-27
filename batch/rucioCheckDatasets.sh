jobList=$1;
mkdir -p ~/rucioCheckDatasets
for line in `cat $jobList`; do
    rucio ls ${line}_tree.root --short 2>&1 | tee ~/rucioCheckDatasets/log.${line}_tree
    rucio ls ${line}_cutflow.root --short 2>&1 | tee ~/rucioCheckDatasets/log.${line}_cutflow
    rucio ls ${line}_metadata.root --short 2>&1 | tee ~/rucioCheckDatasets/log.${line}_metadata
done