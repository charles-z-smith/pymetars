from pymetars import metarlist
from datetime import datetime
import os
"""Will changes this to unit tests in the future"""
def testMetarList():
    test = metarlist.MetarList()
def testMetarListLoad():
    test = metarlist.MetarList()
    assert(test.size != 0)
    
def testGetBounded():
    test = metarlist.MetarList()
    bounded = test.sitesInBounds(42.91,-87.92,42.96,-87.86)
    assert(len(bounded) == 1)
    
def testRemoveEmpty():
    test = metarlist.MetarList()
    bounded = test.sitesInBounds(42.91,-87.92,42.96,-87.86)
    bounded = test.removeEmptySites(bounded)#nothing downloaded, must be empty.
    assert(len(bounded) ==0)

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
    bounded = test.sitesInBounds(42.91,-87.92,42.96,-87.86)
    bounded = test.removeEmptySites(bounded)
    assert(len(bounded) == 1)
def testLoadCurrent():
    utcnow = datetime.utcnow()
    test = metarlist.MetarList()
    test.downloadCurrentHour()
    site = test.getSite("KMKE")
    assert( site.getCodedHour(utcnow.hour) != None)

"""This test can actually fail depending on when it's executed.
An observation may not be inserted if executed a quarter to.
Perhaps this isn't a great test, but just want to test that data
is being inserted when we expect it too be."""
def testDownloadCycle():
    now = datetime.now()
    if now.hour < 39:
        test = metarlist.MetarList()
        test.downloadCycle()
        site = test.getSite("KMKE")
        coded = site.getCodedHistory()
        for i in coded:
            assert(i != None)
        site.decodeAll()
        decoded  = site.getDecodedHistory()
"""Tests to make sure this method returns the closets sites """
def testDistance():
    lst = metarlist.MetarList()
    kmke = lst.getSite("KMKE")
    sites = lst.findClosestSites(kmke, 2)
    assert("KMWC" in sites)
    assert("KRAC" in sites)
    kmsn = lst.getSite("KMSN")
    sites = lst.findClosestSites(kmsn, 1)
    assert("KC29" in sites)

testMetarList()
testMetarListLoad()
testGetBounded()
testRemoveEmpty()
testNone()
testOne()
testDownloadCurrent()
testLoadCurrent()
testDownloadCycle()
testDistance()
