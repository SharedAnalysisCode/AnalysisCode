for line in `ls | grep SSDiLep`; do
  tmp=true
  for str in `cat ~/EXOT12MC`; do
    if echo "$line" | grep -q "$str"; then
      echo "${line} OK";
      tmp=false
      break;
    fi;
  done;
  if $tmp; then
    echo "${line} not OK";
  fi
done;