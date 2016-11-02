#
# $Id: PDG.py,v 1.1 2008/10/17 17:50:16 reece Exp $
# File: PDG.py
# Created: sss, Mar 2005
# Modified: Ryan Reece, Oct 2008
# Purpose: Define PDG ID codes.
#

"""
This module contains names for the various PDG particle ID codes.
The names are the same as in EventKernel/PdtPdg.h.

This module also contains a dictionary pdgid_names mapping ID codes
back to printable strings, and a function pdgid_to_name to do this
conversion.
"""


# Define some PDG ID codes.
d = 1 
anti_d = -1 
u = 2 
anti_u = -2 
s = 3 
anti_s = -3 
c = 4 
anti_c = -4 
b = 5 
anti_b = -5 
t = 6 
anti_t = -6 
l = 7 
anti_l = -7 
h = 8 
anti_h = -8 
g = 21 
e_minus = 11 
e_plus = -11 
nu_e = 12 
anti_nu_e = -12 
mu_minus = 13 
mu_plus = -13 
nu_mu = 14 
anti_nu_mu = -14 
tau_minus = 15 
tau_plus = -15 
nu_tau = 16 
anti_nu_tau = -16 
L_minus = 17 
L_plus = -17 
nu_L = 18 
anti_nu_L = -18 
gamma = 22 
Z0 = 23 
W_plus = 24 
W_minus = -24 
Higgs0 = 25 
reggeon = 28 
pomeron = 29 
Z_prime0 = 32 
Z_prime_prime0 = 33 
W_prime_plus = 34 
W_prime_minus = -34 
Higgs_prime0 = 35 
A0 = 36 
Higgs_plus = 37 
Higgs_minus = -37 
R0 = 40 
anti_R0 = -40 
specflav = 81 
rndmflav = 82 
anti_rndmflav = -82 
phasespa = 83 
c_minushadron = 84 
anti_c_minushadron = -84 
b_minushadron = 85 
anti_b_minushadron = -85 
t_minushadron = 86 
anti_t_minushadron = -86 
Wvirt_plus = 89 
Wvirt_minus = -89 
diquark = 90 
anti_diquark = -90 
cluster = 91 
string = 92 
indep = 93 
CMshower = 94 
SPHEaxis = 95 
THRUaxis = 96 
CLUSjet = 97 
CELLjet = 98 
table = 99 
pi0 = 111 
pi_plus = 211 
pi_minus = -211 
pi_diffr_plus = 210 
pi_diffr_minus = -210 
pi_2S0 = 20111 
pi_2S_plus = 20211 
pi_2S_minus = -20211 
eta = 221 
eta_2S = 20221 
eta_prime = 331 
rho0 = 113 
rho_plus = 213 
rho_minus = -213 
rho_2S0 = 30113 
rho_2S_plus = 30213 
rho_2S_minus = -30213 
rho_3S0 = 40113 
rho_3S_plus = 40213 
rho_3S_minus = -40213 
omega = 223 
omega_2S = 30223 
phi = 333 
a_00 = 10111 
a_0_plus = 10211 
a_0_minus = -10211 
f_0 = 10221 
f_prime_0 = 10331 
b_10 = 10113 
b_1_plus = 10213 
b_1_minus = -10213 
h_1 = 10223 
h_prime_1 = 10333 
a_10 = 20113 
a_1_plus = 20213 
a_1_minus = -20213 
f_1 = 20223 
f_prime_1 = 20333 
a_20 = 115 
a_2_plus = 215 
a_2_minus = -215 
f_2 = 225 
f_prime_2 = 335 
K0 = 311 
anti_K0 = -311 
K_S0 = 310 
K_L0 = 130 
K_plus = 321 
K_minus = -321 
K_star0 = 313 
anti_K_star0 = -313 
K_star_plus = 323 
K_star_minus = -323 
K_0_star0 = 10311 
anti_K_0_star0 = -10311 
K_0_star_plus = 10321 
K_0_star_minus = -10321 
K_10 = 10313 
anti_K_10 = -10313 
K_1_plus = 10323 
K_1_minus = -10323 
K_2_star0 = 315 
anti_K_2_star0 = -315 
K_2_star_plus = 325 
K_2_star_minus = -325 
K_prime_10 = 20313 
anti_K_prime_10 = -20313 
K_prime_1_plus = 20323 
K_prime_1_minus = -20323 
D_plus = 411 
D_minus = -411 
D0 = 421 
anti_D0 = -421 
D_star_plus = 413 
D_star_minus = -413 
D_star0 = 423 
anti_D_star0 = -423 
D_0_star_plus = 10411 
D_0_star_minus = -10411 
D_0_star0 = 10421 
anti_D_0_star0 = -10421 
D_1_plus = 10413 
D_1_minus = -10413 
D_10 = 10423 
anti_D_10 = -10423 
D_2_star_plus = 415 
D_2_star_minus = -415 
D_2_star0 = 425 
anti_D_2_star0 = -425 
D_prime_1_plus = 20413 
D_prime_1_minus = -20413 
D_prime_10 = 20423 
anti_D_prime_10 = -20423 
D_s_plus = 431 
D_s_minus = -431 
D_s_star_plus = 433 
D_s_star_minus = -433 
D_s0_star_plus = 10431 
D_s0_star_minus = -10431 
D_s1_plus = 10433 
D_s1_minus = -10433 
D_s2_star_plus = 435 
D_s2_star_minus = -435 
D_prime_s1_plus = 20433 
D_prime_s1_minus = -20433 
B0 = 511 
anti_B0 = -511 
B_plus = 521 
B_minus = -521 
B_star0 = 513 
anti_B_star0 = -513 
B_star_plus = 523 
B_star_minus = -523 
B_0_star0 = 10511 
anti_B_0_star0 = -10511 
B_0_star_plus = 10521 
B_0_star_minus = -10521 
B_10 = 10513 
anti_B_10 = -10513 
B_1_plus = 10523 
B_1_minus = -10523 
B_2_star0 = 515 
anti_B_2_star0 = -515 
B_2_star_plus = 525 
B_2_star_minus = -525 
B_prime_10 = 20513 
anti_B_prime_10 = -20513 
B_prime_1_plus = 20523 
B_prime_1_minus = -20523 
B_s0 = 531 
anti_B_s0 = -531 
B_s_star0 = 533 
anti_B_s_star0 = -533 
B_s0_star0 = 10531 
anti_B_s0_star0 = -10531 
B_s10 = 10533 
anti_B_s10 = -10533 
B_s2_star0 = 535 
anti_B_s2_star0 = -535 
B_prime_s10 = 20533 
anti_B_prime_s10 = -20533 
B_c_plus = 541 
B_c_minus = -541 
B_c_star_plus = 543 
B_c_star_minus = -543 
B_c0_star_plus = 10541 
B_c0_star_minus = -10541 
B_c1_plus = 10543 
B_c1_minus = -10543 
B_c2_star_plus = 545 
B_c2_star_minus = -545 
B_prime_c1_plus = 20543 
B_prime_c1_minus = -20543 
eta_c = 441 
eta_c_2S = 20441 
J_psi = 443 
psi_2S = 20443 
chi_c0 = 10441 
chi_c1 = 10443 
chi_c2 = 445 
eta_b_2S = 20551 
eta_b_3S = 40551 
Upsilon = 553 
Upsilon_2S = 20553 
Upsilon_3S = 60553 
Upsilon_4S = 70553 
Upsilon_5S = 80553 
h_b = 10553 
h_b_2P = 40553 
h_b_3P = 100553 
chi_b0 = 551 
chi_b1 = 20553 
chi_b2 = 555 
chi_b0_2P = 30551 
chi_b1_2P = 50553 
chi_b2_2P = 10555 
chi_b0_3P = 50551 
chi_b1_3P = 110553 
chi_b2_3P = 20555 
eta_b2_1D = 40555 
eta_b2_2D = 60555 
Upsilon_1_1D = 120553 
Upsilon_2_1D = 30555 
Upsilon_3_1D = 557 
Upsilon_1_2D = 130553 
Upsilon_2_2D = 50555 
Upsilon_3_2D = 10557 
Delta_minus = 1114 
anti_Delta_plus = -1114 
n_diffr = 2110 
anti_n_diffr = -2110 
n0 = 2112 
anti_n0 = -2112 
Delta0 = 2114 
anti_Delta0 = -2114 
p_diffr_plus = 2210 
anti_p_diffr_minus = -2210 
p_plus = 2212 
anti_p_minus = -2212 
Delta_plus = 2214 
anti_Delta_minus = -2214 
Delta_plus_plus = 2224 
anti_Delta_minus_minus = -2224 
Sigma_minus = 3112 
anti_Sigma_plus = -3112 
Sigma_star_minus = 3114 
anti_Sigma_star_plus = -3114 
Lambda0 = 3122 
anti_Lambda0 = -3122 
Sigma0 = 3212 
anti_Sigma0 = -3212 
Sigma_star0 = 3214 
anti_Sigma_star0 = -3214 
Sigma_plus = 3222 
anti_Sigma_minus = -3222 
Sigma_star_plus = 3224 
anti_Sigma_star_minus = -3224 
Xi_minus = 3312 
anti_Xi_plus = -3312 
Xi_star_minus = 3314 
anti_Xi_star_plus = -3314 
Xi0 = 3322 
anti_Xi0 = -3322 
Xi_star0 = 3324 
anti_Xi_star0 = -3324 
Omega_minus = 3334 
anti_Omega_plus = -3334 
Sigma_c0 = 4112 
anti_Sigma_c0 = -4112 
Sigma_c_star0 = 4114 
anti_Sigma_c_star0 = -4114 
Lambda_c_plus = 4122 
anti_Lambda_c_minus = -4122 
Xi_c0 = 4132 
anti_Xi_c0 = -4132 
Sigma_c_plus = 4212 
anti_Sigma_c_minus = -4212 
Sigma_c_star_plus = 4214 
anti_Sigma_c_star_minus = -4214 
Sigma_c_plus_plus = 4222 
anti_Sigma_c_minus_minus = -4222 
Sigma_c_star_plus_plus = 4224 
anti_Sigma_c_star_minus_minus = -4224 
Xi_c_plus = 4322 
anti_Xi_c_minus = -4322 
Xi_prime_c0 = 4312 
Xi_primeanti__c0 = -4312 
Xi_c_star0 = 4314 
anti_Xi_c_star0 = -4314 
Xi_prime_c_plus = 4232 
Xi_primeanti__c_minus = -4232 
Xi_c_star_plus = 4324 
anti_Xi_c_star_minus = -4324 
Omega_c0 = 4332 
anti_Omega_c0 = -4332 
Omega_c_star0 = 4334 
anti_Omega_c_star0 = -4334 
Sigma_b_minus = 5112 
anti_Sigma_b_plus = -5112 
Sigma_b_star_minus = 5114 
anti_Sigma_b_star_plus = -5114 
Lambda_b0 = 5122 
anti_Lambda_b0 = -5122 
Xi_b_minus = 5132 
anti_Xi_b_plus = -5132 
Sigma_b0 = 5212 
anti_Sigma_b0 = -5212 
Sigma_b_star0 = 5214 
anti_Sigma_b_star0 = -5214 
Sigma_b_plus = 5222 
anti_Sigma_b_minus = -5222 
Sigma_star_ = 5224 
anti_Sigma_b_star_minus = -5224 
Xi_b0 = 5232 
anti_Xi_b0 = -5232 
Xi_prime_b_minus = 5312 
anti_Xi_prime_b_plus = -5312 
Xi_b_star_minus = 5314 
anti_Xi_b_star_plus = -5314 
Xi_prime_b0 = 5322 
anti_Xi_prime_b0 = -5322 
Xi_b_star0 = 5324 
anti_Xi_b_star0 = -5324 
Omega_b_minus = 5332 
anti_Omega_b_plus = -5332 
Omega_b_star_minus = 5334 
anti_Omega_b_star_plus = -5334 
dd_0 = 1101 
anti_dd_0 = -1101 
ud_0 = 2101 
anti_ud_0 = -2101 
uu_0 = 2201 
anti_uu_0 = -2201 
sd_0 = 3101 
anti_sd_0 = -3101 
su_0 = 3201 
anti_su_0 = -3201 
ss_0 = 3301 
anti_ss_0 = -3301 
cd_0 = 4101 
anti_cd_0 = -4101 
cu_0 = 4201 
anti_cu_0 = -4201 
cs_0 = 4301 
anti_cs_0 = -4301 
cc_0 = 4401 
anti_cc_0 = -4401 
bd_0 = 5101 
anti_bd_0 = -5101 
bu_0 = 5201 
anti_bu_0 = -5201 
bs_0 = 5301 
anti_bs_0 = -5301 
bc_0 = 5401 
anti_bc_0 = -5401 
bb_0 = 5501 
anti_bb_0 = -5501 
dd_1 = 1103 
anti_dd_1 = -1103 
ud_1 = 2103 
anti_ud_1 = -2103 
uu_1 = 2203 
anti_uu_1 = -2203 
sd_1 = 3103 
anti_sd_1 = -3103 
su_1 = 3203 
anti_su_1 = -3203 
ss_1 = 3303 
anti_ss_1 = -3303 
cd_1 = 4103 
anti_cd_1 = -4103 
cu_1 = 4203 
anti_cu_1 = -4203 
cs_1 = 4303 
anti_cs_1 = -4303 
cc_1 = 4403 
anti_cc_1 = -4403 
bd_1 = 5103 
anti_bd_1 = -5103 
bu_1 = 5203 
anti_bu_1 = -5203 
bs_1 = 5303 
anti_bs_1 = -5303 
bc_1 = 5403 
anti_bc_1 = -5403 
bb_1 = 5503 
anti_bb_1 = -5503 

# SUSY Particles names modified from /Control/AthenaCommon/PDGTABLE.MeV
# naming convention change 
#      '~' to 's_'
#      '(' to '_'
#      ')' to nothing
#      '+' to 'plus'
#      '' to '_'
#      for the negatively charged particles so I add "minus" to the name and a corresponding "plus" entry with -pdg code
#      for the neutrals I add a corresponding "anti" entry with -pdg code
#      for the particles with positive charge entries I add a corresponding "minus" entry with -pdg code 
# ************ (the above is not consistant with the convention that minus=particle plus=anti-particle
#
#      Next remove Majorana particles and rename L-R stau to mass eigen states.
#
#      This is all ugly but sort of consistant with previous naming convention

s_e_minus_L    =1000011
s_e_plus_L     =-1000011

s_nu_e_L       =1000012
s_anti_nu_e_L  =-1000012

s_mu_minus_L   =1000013
s_mu_plus_L    =-1000013

s_nu_mu_L      =1000014
s_anti_nu_mu_L =-1000014

#    s_tau_minus_L  =1000015
#    s_tau_plus_L   =-1000015

# L-R mixing significant use _1 and _2 for names instead
s_tau_minus_1  =1000015
s_tau_plus_1   =-1000015

s_nu_tau_L     =1000016
s_anti_nu_tau_L=-1000016

s_e_minus_R    =2000011
s_e_plus_R     =-2000011

s_mu_minus_R   =2000013
s_mu_plus_R    =-2000013

s_tau_minus_2  =2000015
s_tau_plus_2   =-2000015

s_g            =1000021
#    s_anti_g       =-1000021 # Majorana

s_chi_0_1      =1000022
#    s_anti_chi_0_1 =-1000022 # Majorana

s_chi_0_2      =1000023
#    s_anti_chi_0_2 =-1000023 # Majorana

s_chi_plus_1   =1000024
s_chi_minus_1  =-1000024 # Majorana

s_chi_0_3      =1000025
#    s_anti_chi_0_3 =-1000025 # Majorana

s_chi_0_4      =1000035
#    s_anti_chi_0_4 =-1000035 # Majorana

s_chi_plus_2   =1000037
s_chi_minus_2  =-1000037

s_G            =1000039
#    s_anti_G       =-1000039 # Majorana

# note mismatch with PDGTable and pre-existing PdtPdg.h
#M     999                          0.E+00         +0.0E+00 -0.0E+00 Geantino        0
#W     999                          0.E+00         +0.0E+00 -0.0E+00 Geantino        0



# Null particles
deuteron = 0
tritium = 0
alpha = 0
geantino = 0
He3 = 0
Cerenkov = 0
null = 0


# A couple extra synonyms that weren't in PdgPdt.h.
e = e_minus
mu = mu_minus
tau = tau_minus
W = W_plus
    


#
# Table to convert from a PDG ID to a printable string.
# Not very complete at this point.
#
root_names = {
      0 : "unmatched",
      1 : "d",
     -1 : "#bar{d}",
      2 : "u",
     -2 : "#bar{u}",
      3 : "s",
     -3 : "#bar{s}",
      4 : "c",
     -4 : "#bar{c}",
      5 : "b",
     -5 : "#bar{b}",
      6 : "t",
     -6 : "#bar{t}",
     11 : "e^{-}",
    -11 : "e^{+}",
     12 : "#nu_{e}",
    -12 : "#bar{#nu}_{e}",
     13 : "#mu^{-}",
    -13 : "#mu^{+}",
     14 : "#nu_{#mu}",
    -14 : "#bar{#nu}_{#mu}",
     15 : "#tau^{-}",
    -15 : "#tau^{+}",
     16 : "#nu_{#tau}",
    -16 : "#bar{#nu}_{#tau}",
     21 : "g",
     22 : "#gamma",
     23 : "Z",
     24 : "W^{+}",
    -24 : "W^{-}",
     25 : "h^{0}",
     91 : "cluster",
    111 : "#pi^{0}",
    113 : "#rho^{0}",
    130 : "K_{L}^{0}",
    211 : "#pi^{+}",
   -211 : "#pi^{-}",
    213 : "#rho^{+}",
   -213 : "#rho^{-}",
    215 : "a_{2}^{+}",
   -215 : "a_{2}^{-}",
    221 : "#eta",
    223 : "#omega",
    225 : "f_{2}(1270)",
    310 : "K_{S}^{0}",
    311 : "K^{0}",
   -311 : "#bar{K}^0",
    313 : "K^{*}(892)^{0}",
   -313 : "#bar{K}^{*}",
    321 : "K^{+}",
   -321 : "K^{-}",
    323 : "K^{*}(892)^{+}",
   -323 : "K^{*}(892)^{-}",
    325 : "K_{2}^{*+}",
   -325 : "k_{2}^{*-}",
    331 : "#eta'",
    333 : "#phi",
    335 : "f_{2}'(1525)",
    411 : "D^{+}",
   -411 : "D^{-}",
    413 : "D^{*}(2010)^{+}",
   -413 : "D^{*}(2010)^{-}",
    415 : "D^{*}_{2}(2460)^{+}",
   -415 : "D^{*}_{2}(2460)^{-}",
    421 : "D^{0}",
   -421 : "#bar{D}^{0}",
    423 : "D^{*}(2007)^{0}",
   -423 : "#bar{D}^{*}(2007)^{0}",
    425 : "D^{*}_{2}(2460)^{0}",
   -425 : "#bar{D}^{*}_{2}(2460)^{0}",
    431 : "D_{s}^{+}",
   -431 : "D_{s}^{-}",
    433 : "D_{s}^{*+}",
   -433 : "D_{s}^{*-}",
    435 : "D_{s2}^{*}(2573)^{+}",
   -435 : "D_{s2}^{*}(2573)^{-}",
    441 : "#eta_{c}",
    443 : "J/#psi",
    511 : "B^{0}",
   -511 : "#bar{B}^{0}",
    513 : "B^{*0}",
   -513 : "#bar{B}^{*0}",
    521 : "B^{+}",
   -521 : "B^{-}",
    523 : "B^{*+}",
   -523 : "B^{*-}",
    525 : "B_{2}^{*+}",
   -525 : "B_{2}^{*-}",
    531 : "B_{s}^{0}",
   -531 : "#bar{B}_{s}^{0}",
    533 : "B_{s}^{*0}",
   -533 : "#bar{B}_{s}^{*0}",
    541 : "B_{c}^{+}",
   -541 : "B_{c}^{-}",
    543 : "B_{c}^{*+}",
   -543 : "B_{c}^{*-}",
   1114 : "#Delta^{-}",
  -1114 : "#bar{#Delta}^{+}",
   2112 : "n",
  -2112 : "#bar{n}",
   2212 : "p^{+}",
  -2212 : "p^{-}",
   2114 : "#Delta^{0}",
  -2114 : "#bar{#Delta}^{0}",
   2214 : "#Delta^{+}",
  -2214 : "#bar{#Delta}^{-}",
   2224 : "#Delta^{++}",
  -2224 : "#bar{#Delta}^{--}",
   3112 : "#Sigma^{-}",
  -3112 : "#bar{#Sigma}^{+}",
   3114 : "#Sigma^{*-}",
  -3114 : "#bar{#Sigma}^{*+}",
   3122 : "#Lambda^{0}",
  -3122 : "#bar{#Lambda}^{0}",
   3212 : "#Sigma^{0}",
  -3212 : "#bar{#Sigma}^{0}",
   3214 : "#Sigma^{*0}",
  -3214 : "#bar{#Sigma}^{*0}",
   3222 : "#Sigma^{+}",
  -3222 : "#bar{#Sigma}^{-}",
   3224 : "#Sigma^{*+}",
  -3224 : "#bar{#Sigma}^{*-}",
   3312 : "#Xi^{-}",
  -3312 : "#bar{#Xi}^{+}",
   3314 : "#Xi^{*-}",
  -3314 : "#bar{#Xi}^{*+}",
   3322 : "#Xi^{0}",
  -3322 : "#bar{#Xi}^{0}",
   3324 : "#Xi^{*0}",
  -3324 : "#bar{#Xi}^{*0}",
   3334 : "#Omega^{-}",
  -3334 : "#bar{#Omega}^{+}",
   4122 : "#Lambda_{c}^{+}",
  -4122 : "#Lambda_{c}^{-}",
   4222 : "#Sigma_{c}^{++}",
  -4222 : "#Sigma_{c}^{--}",
   4212 : "#Sigma_{c}^{+}",
  -4212 : "#Sigma_{c}^{-}",
   4112 : "#Sigma_{c}^{0}",
  -4112 : "#bar{#Sigma}_{c}^{0}",
   4224 : "#Sigma_{c}^{*++}",
  -4224 : "#Sigma_{c}^{*--}",
   4214 : "#Sigma_{c}^{*+}",
  -4214 : "#Sigma_{c}^{*-}",
   4114 : "#Sigma_{c}^{*0}",
  -4114 : "#bar{#Sigma}_{c}^{*0}",
   4232 : "#Xi_{c}^{+}",
  -4232 : "#Xi_{c}^{-}",
   4132 : "#Xi_{c}^{0}",
  -4132 : "#bar{#Xi}_{c}^{0}",
   4322 : "#Xi'_{c}^{+}",
  -4322 : "#Xi'_{c}^{-}",
   4312 : "#Xi'_{c}^{0}",
  -4312 : "#bar{#Xi}'_{c}^{0}",
   4324 : "#Xi_{c}^{*+}",
  -4324 : "#Xi_{c}^{*-}",
   4314 : "#Xi_{c}^{*0}",
  -4314 : "#bar{#Xi}_{c}^{*0}",
   4332 : "#Omega_{c}^{0}",
  -4332 : "#bar{#Omega}_{c}^{0}",
   4334 : "#Omega_{c}^{*0}",
  -4334 : "#bar{#Omega}_{c}^{*0}",
   4412 : "#Xi_{cc}^{+}",
  -4412 : "#Xi_{cc}^{-}",
   4422 : "#Xi_{cc}^{++}",
  -4422 : "#Xi_{cc}^{--}",
   4414 : "#Xi_{cc}^{*+}",
  -4414 : "#Xi_{cc}^{*-}",
   4424 : "#Xi_{cc}^{*++}",
  -4424 : "#Xi_{cc}^{*--}",
   4432 : "#Omega_{cc}^{+}",
  -4432 : "#Omega_{cc}^{-}",
   4434 : "#Omega_{cc}^{*+}",
  -4434 : "#Omega_{cc}^{*-}",
   4444 : "#Omega_{ccc}^{++}",
  -4444 : "#Omega_{ccc}^{--}",
   5112 : "#Sigma_{b}^{-}",
  -5112 : "#Sigma_{b}^{+}",
   5122 : "#Lambda_{b}^{0}",
  -5122 : "#bar{#Lambda}_{b}^0",
   5132 : "#Xi_{b}^{-}",
  -5132 : "#bar{#Xi}_{b}^{+}",
   5212 : "#Sigma_{b}^{0}",
  -5212 : "#bar{#Sigma}_{b}^{0}",
   5214 : "#Sigma_{b}^{*0}",
  -5214 : "#bar{#Sigma}_{b}^{*0}",
   5222 : "#Sigma_{b}^{+}",
  -5222 : "#bar{#Sigma}_{b}^{-}",
   5224 : "#Sigma_{b}^{*+}",
  -5224 : "#bar{#Sigma}_{b}^{*-}",
   5232 : "#Xi_b^{0}",
  -5232 : "#bar{#Xi}_b^{0}",
   5322 : "#Xi_{b}^{'0}",
  -5322 : "#bar{#Xi}_{b}^{'0}",
  10223 : "h_^{1}",
  10323 : "K_{1}(1270)^{+}",
 -10323 : "K_{1}(1270)^{-}",
  10411 : "D_{0}^{*}(2400)^{+}",
 -10411 : "D_{0}^{*}(2400)^{-}",
  10413 : "D_{1}(2420)^{+}",
 -10413 : "D_{1}(2420)^{-}",
  10423 : "D_{1}(2420)^{0}",
 -10423 : "#bar{D}_{1}(2420)^{0}",
    }


def to_root_str (id):
    """Convert a PDG ID to a ROOT printable string.
    """
    return root_names.get(id, str(id))


