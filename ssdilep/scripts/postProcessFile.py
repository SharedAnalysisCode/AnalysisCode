## modules
import ROOT

import histmgr
import funcs
import os
import re

from optparse import OptionParser

#-----------------
# input
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

sysSamplePairs = []

for triplet in sysSampePairNames:
  target = triplet.split(":")
  for key in infile.GetListOfKeys():
    histoName = key.GetName()
    if target[1]+"Nom_" in histoName:
      hSys = infile.Get(histoName.replace(target[1],target[0]))
      tempNom = infile.Get(histoName)
      tempHigh = tempNom.Clone( histoName.replace("Nom_",target[2]+"High_") )
      tempLow = tempNom.Clone( histoName.replace("Nom_",target[2]+"Low_") )
      tempHigh.SetNameTitle( histoName.replace("Nom_",target[2]+"High_"),histoName.replace("Nom_",target[2]+"High_") )
      tempLow.SetNameTitle( histoName.replace("Nom_",target[2]+"Low_"),histoName.replace("Nom_",target[2]+"Low_") )
      for bin in range(hSys.GetNbinsX()+2):
        dBin = abs(hSys.GetBinContent(bin-1)-tempNom.GetBinContent(bin-1))
        tempHigh.SetBinContent(bin-1, tempHigh.GetBinContent(bin-1) + dBin )
        tempLow.SetBinContent(bin-1, tempLow.GetBinContent(bin-1) - dBin if (tempLow.GetBinContent(bin-1) - dBin) > 0. else 0. )
      tempNom.Write()
      tempHigh.Write()
      tempLow.Write()
    elif "Nom_" in histoName and target[0] not in histoName:
      print "copying histogram ", histoName, " to ", histoName.replace("Nom_",target[2])
      tempNom = infile.Get(histoName)
      tempHigh = tempNom.Clone( histoName.replace("Nom_",target[2]+"High_") )
      tempLow = tempNom.Clone( histoName.replace("Nom_",target[2]+"Low_") )
      tempHigh.SetNameTitle( histoName.replace("Nom_",target[2]+"High_"),histoName.replace("Nom_",target[2]+"High_") )
      tempLow.SetNameTitle( histoName.replace("Nom_",target[2]+"Low_"),histoName.replace("Nom_",target[2]+"Low_") )
      tempNom.Write()
      tempHigh.Write()
      tempLow.Write()
    elif target[0] not in histoName:
      tempNom = infile.Get(histoName)
      tempNom.Write()


outfile.Close()
    


 ## EOF



