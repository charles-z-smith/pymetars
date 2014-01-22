from metars import metarlist
from datetime import datetime


def testMetarList():
    test = metarlist.MetarList()
def testMetarListLoad():
    test = metarlist.MetarList("stations.txt")
    assert(test.size != 0)
def testNone():
    test = metarlist.MetarList()
    site = test.getSite("K")#Doesn't exsist
    assert(site == None)
def testOne():
    test = metarlist.MetarList()
    site = test.getSite("KMKE")
    assert(site != None)

#Not all sites will have observations on the NWS server
def testDownloadCurrent():
    test = metarlist.MetarList()
    test.downloadCurrentHour()

def testLoadCurrent():
    utcnow = datetime.utcnow()
    test = metarlist.MetarList()
    test.downloadCurrentHour()
    site = test.getSite("KMKE")
    assert( site.getCodedHour(utcnow.hour) != None)

def testDownloadCycle():
    test = metarlist.MetarList()
    test.downloadCycle()
    site = test.getSite("KMKE")
    coded = site.getCodedHistory()
    for i in coded:
        assert(i != None)
    site.decodeAll()
    decoded  = site.getDecodedHistory()


##testMetarList()
##testNone()
##testOne()
##testDownloadCurrent()
##testLoadCurrent()
##testDownloadCycle()
    
    
        
