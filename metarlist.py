from metars.metar import MetarSite
import os
from metars.latlonconversions import LatLonConversions
from ftplib import FTP as __FTP__
from datetime import datetime as __datetime__

"""Create a large set of MetarSites based off the id, name, state/providence, country, lat and lon"""
class MetarList(object):
    def __init__(self):
        self.__metarSites__ = {}
        direc = os.getcwd()
        with open(direc + "/metar2.tbl.txt","r") as f:
            data = f.readlines()
            f.close()
            for i in data:
                temp = i
                lat = self.__convertLat__(temp[55:60].strip())
                lon = self.__convertLat__(temp[61:67].strip())
                self.__metarSites__[temp[0:4]] = MetarSite([temp[0:4], temp[16:49].strip(),temp[49:51], temp[52:54],lat,lon])
                #insert data in the format of (Site, Location, State/Providence, Country, Lat, Lon)
    
    def __convertLat__(self, latlon):
        sign = ""
        if latlon.startswith("-"):
            sign = "-"
            latlon = latlon.lstrip("-")
        if len(latlon) ==4:#accuracy to decimal place
            return(float(sign + latlon[0:2] + "." + latlon[2:]))
        else:
            return (float(sign + latlon[0:1] + "." + latlon[1:]))

    def __convertLon__(self, latlon):
        sign = ""
        if latlon.startswith("-"):
            sign = "-"
            latlon = latlon.lstrip("-")
        if len(latlon) >3 and latlons.startswith("1"):#includes decimal and is >=100 and <200, although there is no 200 longitude
            return(float(sign + latlon[0:3] + "." + latlon[2:]))
        elif len(latlon)>3:#still includes decimal but <100
            return(float(sign + latlon[0:2] + "." + latlon[2:]))
        else:
            return (float(sign + latlon))
    def __str__(self):
        ret = ""
        for i in self.__metarSites__:
            ret = ret + ":" + print(self.__metarSites__.get(i))
        return ret
    def size(self):
        size = len(self.__metarSites__)
        return size
    """Return Metar specifications if a Site ID is found,  if not will return None.
        Should run in O(1) time as dictionary time is constant"""
    def getSite(self, siteId):
        return self.__metarSites__.get(siteId)
    """Takes in a string parameter, returns any areas which contain that string parameter"""
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
    """Returns a dictionary of sites within the lat lon boundaries """
    def sitesInBounds(self, llLat, llLon, ulLat, ulLon):
        retSites = {}
        for site in self.__metarSites__:
            siteObj = self.__metarSites__.get(site)#should be near constant
            siteLat = siteObj.getLatitude()
            siteLon = siteObj.getLongitude()
            if siteLat >= llLat and siteLon >= llLon and siteLat <= ulLat and siteLon<= ulLon:
                retSites[site] = siteObj

        return retSites
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
        ftp.retrlines("RETR " + "%02d"%(utcnow.hour) + "Z.TXT", hour.append)
        self.__setHour__(utcnow.hour,hour)
        ftp.close()
    

