mkdir -p temp
for line in `ls | grep SSDiLep`; do
  tmp=true
  rucio list-files $line > temp/tmp.$line;
  done;
  if $tmp; then
    echo "${line} not OK";
  fi
done;