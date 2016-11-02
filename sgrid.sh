#!bin/bash

echo ""
echo "+++++++++++++++++++"
echo "setup Rucio clients"
echo "+++++++++++++++++++"
echo ""

localSetupRucioClients


echo ""
echo "++++++++++++++++++"
echo "setup PyAMI client"
echo "++++++++++++++++++"
echo ""

localSetupPyAMI


echo ""
echo "++++++++++++++++++"
echo "setup Panda client"
echo "++++++++++++++++++"
echo ""

localSetupPandaClient
