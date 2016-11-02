from samples import *

## set tree
for s in all_samples: s.set_property_recursive( 'treename', 'tau' )

## set skim hist details
for s in all_mc: 
    s.set_property_recursive( 'skim_hist_name', 'h_cut_flow_raw_preselection' )
    s.set_property_recursive( 'skim_hist_bin', 1 )


## set input files
datadir = '/home/wedavey/data/TNTs/data12_8TeV_zptthh.v00-02.pp00-00'
mcdir    = '/home/wedavey/data/TNTs/mc12_8TeV_zptthh.v00-03.pp00-00'
mcdir01  = '/home/wedavey/data/TNTs/mc12_8TeV_zptthh.v00-03-01.pp00-00'

data.filename = '%s/user.wdavey.data12_8TeV.JetTauEtMiss.NTUP_TAU.p1130.zptthh.v00-02.merge.root'%(datadir)    

## v00-03 MC
ttbar_1lep.filename = '%s/user.fscutti.mc12_8TeV.105200.ttbar.NTUP_TAU.e1193_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
ttbar_allhad.filename = '%s/user.fscutti.mc12_8TeV.105204.ttbar_allhad.NTUP_TAU.e1305_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WW_Herwig.filename = '%s/user.fscutti.mc12_8TeV.105985.WW.NTUP_TAU.e1350_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03.root'%mcdir
ZZ_Herwig.filename = '%s/user.fscutti.mc12_8TeV.105986.ZZ.NTUP_TAU.e1350_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03.root'%mcdir
WZ_Herwig.filename = '%s/user.fscutti.mc12_8TeV.105987.WZ.NTUP_TAU.e1350_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03.root'%mcdir
WenuNp0.filename = '%s/user.fscutti.mc12_8TeV.107680.WenuNp0.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WenuNp1.filename = '%s/user.fscutti.mc12_8TeV.107681.WenuNp1.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WenuNp2.filename = '%s/user.fscutti.mc12_8TeV.107682.WenuNp2.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WenuNp3.filename = '%s/user.fscutti.mc12_8TeV.107683.WenuNp3.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WenuNp4.filename = '%s/user.fscutti.mc12_8TeV.107684.WenuNp4.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WenuNp5.filename = '%s/user.fscutti.mc12_8TeV.107685.WenuNp5.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WmunuNp0.filename = '%s/user.fscutti.mc12_8TeV.107690.WmunuNp0.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WmunuNp1.filename = '%s/user.fscutti.mc12_8TeV.107691.WmunuNp1.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WmunuNp2.filename = '%s/user.fscutti.mc12_8TeV.107692.WmunuNp2.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WmunuNp3.filename = '%s/user.fscutti.mc12_8TeV.107693.WmunuNp3.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WmunuNp4.filename = '%s/user.fscutti.mc12_8TeV.107694.WmunuNp4.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WmunuNp5.filename = '%s/user.fscutti.mc12_8TeV.107695.WmunuNp5.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WtaunuNp0.filename = '%s/user.fscutti.mc12_8TeV.107700.WtaunuNp0.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WtaunuNp2.filename = '%s/user.fscutti.mc12_8TeV.107702.WtaunuNp2.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WtaunuNp3.filename = '%s/user.fscutti.mc12_8TeV.107703.WtaunuNp3.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WtaunuNp4.filename = '%s/user.fscutti.mc12_8TeV.107704.WtaunuNp4.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
WtaunuNp5.filename = '%s/user.fscutti.mc12_8TeV.107705.WtaunuNp5.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
SingleTopSChanWenu.filename = '%s/user.fscutti.mc12_8TeV.108343.SingleTopSChanWenu.NTUP_TAU.e1242_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
SingleTopSChanWmunu.filename = '%s/user.fscutti.mc12_8TeV.108344.SingleTopSChanWmunu.NTUP_TAU.e1242_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
SingleTopSChanWtaunu.filename = '%s/user.fscutti.mc12_8TeV.108345.SingleTopSChanWtaunu.NTUP_TAU.e1242_s1469_s1470_r3752_r3549_p1130.zptthh.v00-03.root'%mcdir
SingleTopWt.filename = '%s/user.fscutti.mc12_8TeV.108346.SingleTopWtChanIncl.NTUP_TAU.e1242_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
SingleTopTChane.filename = '%s/user.fscutti.mc12_8TeV.117360.singletop_tchan_e.NTUP_TAU.e1195_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
SingleTopTChanmu.filename = '%s/user.fscutti.mc12_8TeV.117361.singletop_tchan_mu.NTUP_TAU.e1195_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
SingleTopTChantau.filename = '%s/user.fscutti.mc12_8TeV.117362.singletop_tchan_tau.NTUP_TAU.e1195_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03.root'%mcdir
Ztautau.filename = '%s/user.fscutti.mc12_8TeV.147818.Ztautau.NTUP_TAU.e1176_s1479_s1470_r3553_r3549_p1130.zptthh.v00-03.root'%mcdir
DYtautau_180M250.filename = '%s/user.fscutti.mc12_8TeV.158731.DYtautau_180M250.NTUP_TAU.e1518_s1499_s1504_r3658_p1130.zptthh.v00-03.root'%mcdir
DYtautau_250M400.filename = '%s/user.fscutti.mc12_8TeV.158732.DYtautau_250M400.NTUP_TAU.e1518_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03.root'%mcdir
DYtautau_400M600.filename = '%s/user.fscutti.mc12_8TeV.158733.DYtautau_400M600.NTUP_TAU.e1518_s1499_s1504_r3658_p1130.zptthh.v00-03.root'%mcdir
DYtautau_600M800.filename = '%s/user.fscutti.mc12_8TeV.158734.DYtautau_600M800.NTUP_TAU.e1518_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03.root'%mcdir
DYtautau_800M1000.filename = '%s/user.fscutti.mc12_8TeV.158735.DYtautau_800M1000.NTUP_TAU.e1518_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03.root'%mcdir
DYtautau_1000M1250.filename = '%s/user.fscutti.mc12_8TeV.158736.DYtautau_1000M1250.NTUP_TAU.e1518_s1499_s1504_r3658_p1130.zptthh.v00-03.root'%mcdir
DYtautau_1250M1500.filename = '%s/user.fscutti.mc12_8TeV.158737.DYtautau_1250M1500.NTUP_TAU.e1518_s1499_s1504_r3658_p1130.zptthh.v00-03.root'%mcdir
DYtautau_1500M1750.filename = '%s/user.fscutti.mc12_8TeV.158738.DYtautau_1500M1750.NTUP_TAU.e1518_s1499_s1504_r3658_p1130.zptthh.v00-03.root'%mcdir
DYtautau_1750M2000.filename = '%s/user.fscutti.mc12_8TeV.158739.DYtautau_1750M2000.NTUP_TAU.e1518_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03.root'%mcdir
DYtautau_2000M2250.filename = '%s/user.fscutti.mc12_8TeV.158740.DYtautau_2000M2250.NTUP_TAU.e1518_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03.root'%mcdir
DYtautau_2250M2500.filename = '%s/user.fscutti.mc12_8TeV.158741.DYtautau_2250M2500.NTUP_TAU.e1518_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03.root'%mcdir
Zprime250tautau.filename = '%s/user.fscutti.mc12_8TeV.170201.Zprime250tautau.NTUP_TAU.e1176_s1479_s1470_r3553_r3549_p1130.zptthh.v00-03.root'%mcdir
Zprime500tautau.filename = '%s/user.fscutti.mc12_8TeV.170202.Zprime500tautau.NTUP_TAU.e1176_s1479_s1470_r3553_r3549_p1130.zptthh.v00-03.root'%mcdir
Zprime750tautau.filename = '%s/user.fscutti.mc12_8TeV.170203.Zprime750tautau.NTUP_TAU.e1176_s1479_s1470_r3553_r3549_p1130.zptthh.v00-03.root'%mcdir
Zprime1000tautau.filename = '%s/user.fscutti.mc12_8TeV.170204.Zprime1000tautau.NTUP_TAU.e1176_s1479_s1470_r3553_r3549_p1130.zptthh.v00-03.root'%mcdir
Zprime1250tautau.filename = '%s/user.fscutti.mc12_8TeV.170205.Zprime1250tautau.NTUP_TAU.e1176_s1479_s1470_r3553_r3549_p1130.zptthh.v00-03.root'%mcdir


## v00-03-01 MC
ZeeNp0.filename = '%s/user.fscutti.mc12_8TeV.107650.ZeeNp0.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZeeNp1.filename = '%s/user.fscutti.mc12_8TeV.107651.ZeeNp1.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZeeNp2.filename = '%s/user.fscutti.mc12_8TeV.107652.ZeeNp2.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZeeNp3.filename = '%s/user.fscutti.mc12_8TeV.107653.ZeeNp3.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZeeNp4.filename = '%s/user.fscutti.mc12_8TeV.107654.ZeeNp4.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZeeNp5.filename = '%s/user.fscutti.mc12_8TeV.107655.ZeeNp5.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZmumuNp0.filename = '%s/user.fscutti.mc12_8TeV.107660.ZmumuNp0.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZmumuNp1.filename = '%s/user.fscutti.mc12_8TeV.107661.ZmumuNp1.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZmumuNp2.filename = '%s/user.fscutti.mc12_8TeV.107662.ZmumuNp2.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZmumuNp3.filename = '%s/user.fscutti.mc12_8TeV.107663.ZmumuNp3.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZmumuNp4.filename = '%s/user.fscutti.mc12_8TeV.107664.ZmumuNp4.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZmumuNp5.filename = '%s/user.fscutti.mc12_8TeV.107665.ZmumuNp5.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZtautauNp0.filename = '%s/user.fscutti.mc12_8TeV.107670.ZtautauNp0.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZtautauNp1.filename = '%s/user.fscutti.mc12_8TeV.107671.ZtautauNp1.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZtautauNp2.filename = '%s/user.fscutti.mc12_8TeV.107672.ZtautauNp2.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZtautauNp3.filename = '%s/user.fscutti.mc12_8TeV.107673.ZtautauNp3.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZtautauNp4.filename = '%s/user.fscutti.mc12_8TeV.107674.ZtautauNp4.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ZtautauNp5.filename = '%s/user.fscutti.mc12_8TeV.107675.ZtautauNp5.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
'''
ggHtautauhh_MA100TB20.filename = '%s/user.fscutti.mc12_8TeV.146651.ggHtautauhh_MA100TB20.NTUP_TAU.e1571_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ggHtautauhh_MA170TB20.filename = '%s/user.fscutti.mc12_8TeV.146658.ggHtautauhh_MA170TB20.NTUP_TAU.e1571_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ggHtautauhh_MA200TB20.filename = '%s/user.fscutti.mc12_8TeV.146659.ggHtautauhh_MA200TB20.NTUP_TAU.e1571_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ggHtautauhh_MA250TB20.filename = '%s/user.fscutti.mc12_8TeV.146660.ggHtautauhh_MA250TB20.NTUP_TAU.e1571_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ggHtautauhh_MA350TB20.filename = '%s/user.fscutti.mc12_8TeV.146662.ggHtautauhh_MA350TB20.NTUP_TAU.e1571_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ggHtautauhh_MA400TB20.filename = '%s/user.fscutti.mc12_8TeV.146663.ggHtautauhh_MA400TB20.NTUP_TAU.e1571_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ggHtautauhh_MA450TB20.filename = '%s/user.fscutti.mc12_8TeV.146664.ggHtautauhh_MA450TB20.NTUP_TAU.e1571_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
ggHtautauhh_MA800TB20.filename = '%s/user.fscutti.mc12_8TeV.146668.ggHtautauhh_MA800TB20.NTUP_TAU.e1571_s1499_s1504_r3658_r3549_p1130.zptthh.v00-03-01.root'%mcdir01
'''



