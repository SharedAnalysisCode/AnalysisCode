#!bin/bash

echo ""
echo "++++++++++++++++"
echo "setup grig proxy"
echo "++++++++++++++++"
echo ""

voms-proxy-init -voms atlas -valid 96:00
voms-proxy-info -all

echo ""
echo "++++++++++++++++++++++++++++"
echo "copying grid proxy to jobdir"
echo "++++++++++++++++++++++++++++"
echo ""
echo "cp /tmp/x509up_u1132 /coepp/cephfs/mel/${USER}/jobdir"

# name of certificate needs to be changed
cp /tmp/x509up_u1132 /coepp/cephfs/mel/${USER}/jobdir



