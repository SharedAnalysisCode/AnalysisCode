#!/bin/bash
#
# Merge ntuples
#


if [[ -z ${1+x} ]]; then
  echo "Error: Set the relative input folder (first argument)!" 1>&2
  exit -1
fi

if [[ -z ${2+x} ]]; then
  echo "Error: Set find regex (second argument)!" 1>&2
  exit -1
fi

for f in `find $1 -maxdepth 1 -type d \( -iname "*$2*" -a -iname '*.root' -a -iname '*_metadata.root' \) | sort`; do
  IFS='/'; file=($f); unset IFS;
  file=${file[-1]}
  file=${file//_metadata\.root/}

  out=${file}
  IFS='.'; out=($out); unset IFS;
  if [[ "$file" == *"physics_Main"* ]]; then
    out=${out[-3]}.${out[-2]}
  else
    out=${out[-2]}
  fi

  echo "=== ${out}"

  if [ ! -f $INPUT_DIR/$out.root ]; then
    hadd $out.root `find "$1/${file}_tree.root/" "$1/${file}_metadata.root/" "$1/${file}_cutflow.root/" -type f | tr '\n' ' '`
  else
    echo "File already exists"
  fi
done
