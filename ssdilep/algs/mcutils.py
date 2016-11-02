#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mcutils.py
"""

#_________________________________________________________________________
def isztautau_pythia(mc_channel_number):
    return mc_channel_number == 147818

#_________________________________________________________________________
def iszee_powheg(mc_channel_number):
    return mc_channel_number == 147806

#_________________________________________________________________________
def iszmumu_powheg(mc_channel_number):
    return mc_channel_number == 147807

#_________________________________________________________________________
def iszleplep_powheg(mc_channel_number):
    return iszee_powheg(mc_channel_number) or iszmumu_powheg(mc_channel_number) 


#_________________________________________________________________________
def isditau_pythia(mc_channel_number):
    return mc_channel_number in [
            147818, #Ztautau
            158731, #DYtautau_180M250
            158732, #DYtautau_250M400 
            158733, #DYtautau_400M600 
            158734, #DYtautau_600M800 
            158735, #DYtautau_800M1000
            158736, #DYtautau_1000M1250
            158737, #DYtautau_1250M1500
            158738, #DYtautau_1500M1750
            158739, #DYtautau_1750M2000
            158740, #DYtautau_2000M2250
            158741, #DYtautau_2250M2500
            ]
                                 

#_________________________________________________________________________
def isdilep_powheg(mc_channel_number):
    return mc_channel_number in [
            147806, #Zee
            129504, #DYee_120M180
            129505, #DYee_180M250
            129506, #DYee_250M400 
            129507, #DYee_400M600 
            129508, #DYee_600M800 
            129509, #DYee_800M1000
            129510, #DYee_1000M1250
            129511, #DYee_1250M1500
            129512, #DYee_1500M1750
            129513, #DYee_1750M2000
            129514, #DYee_2000M2250
            129515, #DYee_2250M2500
            129516, #DYee_2250M2500
            129517, #DYee_2250M2500
            129518, #DYee_2250M2500

            147807, #Zmumu
            129524, #DYmumu_120M180
            129525, #DYmumu_180M250
            129526, #DYmumu_250M400 
            129527, #DYmumu_400M600 
            129528, #DYmumu_600M800 
            129529, #DYmumu_800M1000
            129530, #DYmumu_1000M1250
            129531, #DYmumu_1250M1500
            129532, #DYmumu_1500M1750
            129533, #DYmumu_1750M2000
            129534, #DYmumu_2000M2250
            129535, #DYmumu_2250M2500
            129536, #DYmumu_2250M2500
            129537, #DYmumu_2250M2500
            129538, #DYmumu_2250M2500
            ]


#_________________________________________________________________________
def iswenu_sherpa(mc_channel_number):
    return mc_channel_number in [
            167740, #Wenu0_BJet
            167741, #Wenu0_CJet
            167742, #Wenu0_LJet
            167761, #Wenu70_140_BJet
            167762, #Wenu70_140_CJet
            167763, #Wenu70_140_LJet
            167770, #Wenu140_280_BJet
            167771, #Wenu140_280_CJet
            167772, #Wenu140_280_LJet
            167779, #Wenu280_500_BJet
            167780, #Wenu280_500_CJet
            167781, #Wenu280_500_LJet
            167788, #Wenu500_BJet
            167789, #Wenu500_CJet
            167790, #Wenu500_LJet
            ]

#_________________________________________________________________________
def iswmunu_sherpa(mc_channel_number):
    return mc_channel_number in [
            167743, #Wmunu0_BJet
            167744, #Wmunu0_CJet
            167745, #Wmunu0_LJet
            167764, #Wmunu70_140_BJet
            167765, #Wmunu70_140_CJet
            167766, #Wmunu70_140_LJet
            167773, #Wmunu140_280_BJet
            167774, #Wmunu140_280_CJet
            167775, #Wmunu140_280_LJet
            167782, #Wmunu280_500_BJet
            167783, #Wmunu280_500_CJet
            167784, #Wmunu280_500_LJet
            167791, #Wmunu500_BJet
            167792, #Wmunu500_CJet
            167793, #Wmunu500_LJet
            ]

#_________________________________________________________________________
def iswtaunu_sherpa(mc_channel_number):
    return mc_channel_number in [
            167746, #Wtaunu0_BJet
            167747, #Wtaunu0_CJet
            167748, #Wtaunu0_LJet
            167767, #Wtaunu70_140_BJet
            167768, #Wtaunu70_140_CJet
            167769, #Wtaunu70_140_LJet
            167776, #Wtaunu140_280_BJet
            167777, #Wtaunu140_280_CJet
            167778, #Wtaunu140_280_LJet
            167785, #Wtaunu280_500_BJet
            167786, #Wtaunu280_500_CJet
            167787, #Wtaunu280_500_LJet
            167794, #Wtaunu500_BJet
            167795, #Wtaunu500_CJet
            167796, #Wtaunu500_LJet
            ]


#_________________________________________________________________________
def iswjets_sherpa(mc_channel_number):
    return iswenu_sherpa(mc_channel_number) \
        or iswmunu_sherpa(mc_channel_number) \
        or iswtaunu_sherpa(mc_channel_number)

#_________________________________________________________________________
def iswenu_sherpa_inclusive(mc_channel_number):
    return mc_channel_number in [
            167740, #Wenu0_BJet
            167741, #Wenu0_CJet
            167742, #Wenu0_LJet
            ]

#_________________________________________________________________________
def iswmunu_sherpa_inclusive(mc_channel_number):
    return mc_channel_number in [
            167743, #Wmunu0_BJet
            167744, #Wmunu0_CJet
            167745, #Wmunu0_LJet
            ]

#_________________________________________________________________________
def iswtaunu_sherpa_inclusive(mc_channel_number):
    return mc_channel_number in [
            167746, #Wtaunu0_BJet
            167747, #Wtaunu0_CJet
            167748, #Wtaunu0_LJet
            ]

#_________________________________________________________________________
def iswjets_sherpa_inclusive(mc_channel_number):
    return iswenu_sherpa_inclusive(mc_channel_number) \
        or iswmunu_sherpa_inclusive(mc_channel_number) \
        or iswtaunu_sherpa_inclusive(mc_channel_number)




# EOF
