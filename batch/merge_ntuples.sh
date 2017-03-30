#!/bin/bash
SOURCEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [[ -z ${1+x} ]]; then
  echo "Error: Set the input folder (first argument)!" 1>&2
  exit -1
fi
if [[ -z ${2+x} ]]; then
  echo "Error: Set find regex (second argument)!" 1>&2
  exit -1
fi
for f in `find $1 -maxdepth 1 -type d \( -iname "*$2*" -a -iname '*.root' -a -iname '*_metadata.root' \) | sort`; do
  file=${f//$1/}
  file=${file//_metadata\.root/}
  out=${file}
  IFS='.'; out=($out); unset IFS;
  out=${out[-1]}
  echo "=== ${out}"
  if [ ! -f $out.root ]; then
    hadd $out.root `find "$1/${file}_tree.root/" "$1/${file}_metadata.root/" "$1/${file}_cutflow.root/" -type f | tr '\n' ' '`
  else
    echo "File already exists"
  fi
done