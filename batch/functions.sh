function mergeOutput {
  for line in `ls | grep part | sed "s/\(.*\)\.part.*/\1/g" | sort | uniq`; do
    if [ -f  $line.root ]; then
      #continue
      echo "file ${line}.root already exists, removing it"
      # rm $line.root
    fi
    array=($(ls|grep $line))
    for t in "${array[@]:1}"; do
      echo "cp $t $t.temp"
      cp $t $t.temp
      echo "rm -f $t"
      rm -f $t
      echo "cp $t.temp $t"
      cp $t.temp $t
      rm -f $t.temp
      echo "rootrm $t:MetaData_EventCount"
      rootrm $t:MetaData_EventCount
    done
    echo hadd $line.root `ls | grep $line | xargs`
    hadd $line.root `ls | grep $line | xargs`
  done
}