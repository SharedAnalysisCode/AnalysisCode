## modules
import ROOT

import histmgr
import funcs
import os
import re

from optparse import OptionParser

#-----------------
# input
# example:
# python ../ssdilep/scripts/postProcessFile.py -i AllR_v3_020_root/merged.root -o AllR_v3_020_root/templateFile.root -s "dibosonSysSample:dibosonSherpa:DBGen,ttbar_Herwig:ttbar_Py8:TTHadron,ttbar_Py8_aMcAtNlo:ttbar_Py8:TTGen,ttbar_Py8_CF:ttbar_Py8:TTCF,ttbar_Py8_up:ttbar_Py8:TTRad:H,ttbar_Py8_do:ttbar_Py8:TTRad:L"
#-----------------
parser = OptionParser()
parser.add_option('-i', '--input', dest='infile',
                  help='input directory',metavar='INFILE',default=None)
parser.add_option('-o', '--output', dest='outfile',
                  help='output directory',metavar='OUTFILE',default=None)
parser.add_option('-s', '--sys', dest='sysSamples',
                  help='list of sys sample names',metavar='SYSSAMPLES',default=None)

(options, args) = parser.parse_args()

infile = ROOT.TFile(options.infile,"READ")

outfile = ROOT.TFile(options.outfile,"RECREATE")
outfile.cd()

sysSampePairNames = options.sysSamples.split(",")

sysSamples= []


for triplet in sysSampePairNames:
  target = triplet.split(":")
  sysSamples += [target[0]]

print sysSamples

for triplet in sysSampePairNames:
  target = triplet.split(":")
  print target
  if len(target)==4:
    if target[3]=="H":
      sysName = target[2].replace("_up","")
    elif target[3]=="L":
      sysName = target[2].replace("_do","")
  else:
    sysName = target[2]
  print sysName
  for key in infile.GetListOfKeys():
    histoName = key.GetName()
    if target[1]+"Nom_" in histoName:
      hSys = infile.Get(histoName.replace(target[1],target[0]))
      tempNom = infile.Get(histoName)
      tempHigh = tempNom.Clone( histoName.replace("Nom_",sysName+"High_") )
      tempLow = tempNom.Clone( histoName.replace("Nom_",sysName+"Low_") )
      tempHigh.SetNameTitle( histoName.replace("Nom_",sysName+"High_"),histoName.replace("Nom_",sysName+"High_") )
      tempLow.SetNameTitle( histoName.replace("Nom_",sysName+"Low_"),histoName.replace("Nom_",sysName+"Low_") )
      for bin in range(hSys.GetNbinsX()+2):
        dBin = abs(hSys.GetBinContent(bin-1)-tempNom.GetBinContent(bin-1))
        tempHigh.SetBinContent(bin-1, tempHigh.GetBinContent(bin-1) + dBin )
        tempLow.SetBinContent(bin-1, tempLow.GetBinContent(bin-1) - dBin if (tempLow.GetBinContent(bin-1) - dBin) > 0. else 0. )
      # tempNom.Write()
      if len(target)==4:
        if target[3]=="H":
          tempHigh.Write()
        elif target[3]=="L":
          tempLow.Write()
      else:
        tempHigh.Write()
        tempLow.Write()
    elif "Nom_" in histoName and sum([x in histoName for x in sysSamples])==0:
      # print "copying histogram ", histoName, " to ", histoName.replace("Nom_",sysName)
      tempNom = infile.Get(histoName)
      tempHigh = tempNom.Clone( histoName.replace("Nom_",sysName+"High_") )
      tempLow = tempNom.Clone( histoName.replace("Nom_",sysName+"Low_") )
      tempHigh.SetNameTitle( histoName.replace("Nom_",sysName+"High_"),histoName.replace("Nom_",sysName+"High_") )
      tempLow.SetNameTitle( histoName.replace("Nom_",sysName+"Low_"),histoName.replace("Nom_",sysName+"Low_") )
      # tempNom.Write()
      if len(target)==4:
        if target[3]=="H":
          print "ASDASD"
          tempHigh.Write()
        elif target[3]=="L":
          tempLow.Write()
          print "ASDASD"
      else:
        tempHigh.Write()
        tempLow.Write()

for key in infile.GetListOfKeys():
  histoName = key.GetName()
  if sum([x in histoName for x in sysSamples])==0:
    tempNom = infile.Get(histoName)
    tempNom.Write()


outfile.Close()
    


 ## EOF



