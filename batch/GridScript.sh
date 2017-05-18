find .
echo $1
echo $2
echo $3

if [ -z "$1" ]
  then
    echo "No input1 supplied"
fi

if [ -z "$2" ]
  then
    echo "No input2 supplied"
fi

if [ -z "$3" ]
  then
    echo "No input3 supplied"
fi

if [ -z "$4" ]
  then
    echo "no plotter given"
fi

if [ -z "$5" ]
  then
    echo "no data type given"
fi

source setup.sh

if [ -z "$6" ]
  then
    echo "nominal mode"
    echo python $4 --input $1 --sampletype=$5 --config="min_entry:0,max_entry:-1"
    python $4 --input $1 --sampletype=$5 --config="min_entry:0,max_entry:-1"
  else
    echo "running with systematic $6"
    echo python $4 --input $1 --sampletype=$5 --config="min_entry:0,max_entry:-1,sys:$6"
    python $4 --input $1 --sampletype=$5 --config="min_entry:0,max_entry:-1,sys:$6"
fi


echo hadd out.root ntuple.root $2 $3