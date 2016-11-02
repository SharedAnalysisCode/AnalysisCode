from samples import *

## set tree
for s in all_samples: s.set_property_recursive( 'treename', 'tau' )

## set skim hist details
for s in all_mc: 
    s.set_property_recursive( 'skim_hist_name', 'h_cut_flow_raw_preselection' )
    s.set_property_recursive( 'skim_hist_bin', 1 )


## set input files
datadir = '/home/wedavey/data/TNTs/data12_8TeV_zptthh.v00-02.pp00-00'
mcdir   = '/home/wedavey/data/TNTs/mc12_8TeV_zptthh.v00-01.pp00-00'

data.filename = '%s/user.wdavey.data12_8TeV.JetTauEtMiss.NTUP_TAU.p1130.zptthh.v00-02.merge.root'%(datadir)    

Zprime500tautau.filename = '%s/user.wdavey.mc12_8TeV.170202.Zprime500tautau.NTUP_TAU.e1176_s1479_s1470_r3553_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
Zprime1250tautau.filename = '%s/user.wdavey.mc12_8TeV.170205.Zprime1250tautau.NTUP_TAU.e1176_s1479_s1470_r3553_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)


ttbar_1lep.filename = '%s/user.wdavey.mc12_8TeV.105200.ttbar.NTUP_TAU.e1193_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ttbar_allhad.filename = '%s/user.wdavey.mc12_8TeV.105204.ttbar_allhad.NTUP_TAU.e1305_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WW_Herwig.filename = '%s/user.wdavey.mc12_8TeV.105985.WW.NTUP_TAU.e1350_s1499_s1504_r3658_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZZ_Herwig.filename = '%s/user.wdavey.mc12_8TeV.105986.ZZ.NTUP_TAU.e1350_s1499_s1504_r3658_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WZ_Herwig.filename = '%s/user.wdavey.mc12_8TeV.105987.WZ.NTUP_TAU.e1350_s1499_s1504_r3658_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZeeNp0.filename = '%s/user.wdavey.mc12_8TeV.107650.ZeeNp0.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZeeNp1.filename = '%s/user.wdavey.mc12_8TeV.107651.ZeeNp1.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZeeNp2.filename = '%s/user.wdavey.mc12_8TeV.107652.ZeeNp2.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZeeNp3.filename = '%s/user.wdavey.mc12_8TeV.107653.ZeeNp3.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZeeNp4.filename = '%s/user.wdavey.mc12_8TeV.107654.ZeeNp4.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZeeNp5.filename = '%s/user.wdavey.mc12_8TeV.107655.ZeeNp5.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZmumuNp0.filename = '%s/user.wdavey.mc12_8TeV.107660.ZmumuNp0.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZmumuNp1.filename = '%s/user.wdavey.mc12_8TeV.107661.ZmumuNp1.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZmumuNp2.filename = '%s/user.wdavey.mc12_8TeV.107662.ZmumuNp2.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZmumuNp3.filename = '%s/user.wdavey.mc12_8TeV.107663.ZmumuNp3.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZmumuNp4.filename = '%s/user.wdavey.mc12_8TeV.107664.ZmumuNp4.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZmumuNp5.filename = '%s/user.wdavey.mc12_8TeV.107665.ZmumuNp5.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZtautauNp0.filename = '%s/user.wdavey.mc12_8TeV.107670.ZtautauNp0.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZtautauNp1.filename = '%s/user.wdavey.mc12_8TeV.107671.ZtautauNp1.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZtautauNp2.filename = '%s/user.wdavey.mc12_8TeV.107672.ZtautauNp2.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZtautauNp3.filename = '%s/user.wdavey.mc12_8TeV.107673.ZtautauNp3.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZtautauNp4.filename = '%s/user.wdavey.mc12_8TeV.107674.ZtautauNp4.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
ZtautauNp5.filename = '%s/user.wdavey.mc12_8TeV.107675.ZtautauNp5.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WenuNp0.filename = '%s/user.wdavey.mc12_8TeV.107680.WenuNp0.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WenuNp1.filename = '%s/user.wdavey.mc12_8TeV.107681.WenuNp1.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WenuNp2.filename = '%s/user.wdavey.mc12_8TeV.107682.WenuNp2.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WenuNp3.filename = '%s/user.wdavey.mc12_8TeV.107683.WenuNp3.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WenuNp4.filename = '%s/user.wdavey.mc12_8TeV.107684.WenuNp4.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WenuNp5.filename = '%s/user.wdavey.mc12_8TeV.107685.WenuNp5.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WmunuNp0.filename = '%s/user.wdavey.mc12_8TeV.107690.WmunuNp0.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WmunuNp1.filename = '%s/user.wdavey.mc12_8TeV.107691.WmunuNp1.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WmunuNp2.filename = '%s/user.wdavey.mc12_8TeV.107692.WmunuNp2.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WmunuNp3.filename = '%s/user.wdavey.mc12_8TeV.107693.WmunuNp3.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WmunuNp4.filename = '%s/user.wdavey.mc12_8TeV.107694.WmunuNp4.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WmunuNp5.filename = '%s/user.wdavey.mc12_8TeV.107695.WmunuNp5.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WtaunuNp0.filename = '%s/user.wdavey.mc12_8TeV.107700.WtaunuNp0.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WtaunuNp1.filename = '%s/user.wdavey.mc12_8TeV.107701.WtaunuNp1.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WtaunuNp2.filename = '%s/user.wdavey.mc12_8TeV.107702.WtaunuNp2.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WtaunuNp3.filename = '%s/user.wdavey.mc12_8TeV.107703.WtaunuNp3.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WtaunuNp4.filename = '%s/user.wdavey.mc12_8TeV.107704.WtaunuNp4.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)
WtaunuNp5.filename = '%s/user.wdavey.mc12_8TeV.107705.WtaunuNp5.NTUP_TAU.e1218_s1469_s1470_r3542_r3549_p1130.zptthh.v00-01.merge.root'%(mcdir)















