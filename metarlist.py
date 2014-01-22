import urllib.request as __urlreq__
from metars.metar import MetarSite
from metars.latlonconversions import LatLonConversions
from ftplib import FTP as __FTP__
from datetime import datetime as __datetime__

"""Create a large set of MetarSites based off the id, name, state lat and lon"""
class MetarList(object):
    def __init__(self, localDir=None):
        self.__metarSites__ = {}
        if localDir == None:
            req = __urlreq__.urlopen("http://weather.rap.ucar.edu/surface/stations.txt")
            data = req.readlines()
            req.close()
            del(data[0:44])
            for i in data:
                if(len(i) == 84):
                    temp = i.decode("utf-8")
                    self.__metarSites__[temp[20:24]] = MetarSite([temp[0:2], temp[3:19].strip(),temp[20:24],temp[39:45],temp[47:54]])
        else:
            with open(localDir,"r") as f:
                data = f.readlines()
                f.close()
                for i in data:
                    if(len(i) == 84):
                        temp = i
                        self.__metarSites__[temp[20:24]] = MetarSite([temp[0:2], temp[3:19].strip(),temp[20:24],temp[39:45],temp[47:54]])                    


    def __str__(self):
        ret = ""
        for i in self.__metarSites__:
            ret = ret + ":" + print(self.__metarSites__.get(i))
        return ret
    def size(self):
        size = len(self.__metarSites__)
        return size
    """Return Metar specifications if a Site ID is found,  if not will return None"""
    def getSite(self, siteId):
        return self.__metarSites__.get(siteId)
    def getLocation(self, location):
        locations = []
        for i in self.__metarSites__:
            site = self.__metarSites__.get(i)
            if location in site.getName():
                locations.append(site)
        return locations
    """Assign the current 24 hour observations history to all the metars sites in our list"""
    def __setHour__(self, hour,metarData):
        utcnow = __datetime__.utcnow()
        for obs in metarData:
            metarSite = self.__metarSites__.get(obs[0:4])
            if metarSite != None and "RMK" in obs:
                metarSite.__setHour__(hour, obs)
            elif metarSite != None and metarSite.__codedobHistory__[hour] == None:
                metarSite.__setHour__(hour, obs)
    """Downloads cycle from nws ftp server"""         
    def downloadCycle(self):
        ftp = __FTP__("tgftp.nws.noaa.gov")
        ftp.login()
        ftp.cwd("/data/observations/metar/cycles/")
        nlst = ftp.nlst()
        for i in nlst:
            hour = []
            ftp.retrlines("RETR " + i, hour.append)
            self.__setHour__(int(i[0:2]),hour)
        ftp.close()

    """Downloads the current hour from the ftp server"""
    def downloadCurrentHour(self):
        utcnow = __datetime__.utcnow()
        ftp = __FTP__("tgftp.nws.noaa.gov")
        ftp.login()
        ftp.cwd("/data/observations/metar/cycles/")
        hour = []
        print(utcnow.hour)
        ftp.retrlines("RETR " + "%02d"%(utcnow.hour) + "Z.TXT", hour.append)
        self.__setHour__(utcnow.hour,hour)
        ftp.close()
    

