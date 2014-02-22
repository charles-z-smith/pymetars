from ftplib import FTP
from datetime import datetime
import metars.metardecoder as metardecoder
import os
import re
from pytz import timezone
EASTERN = timezone("US/Eastern")
CENTRAL = timezone("US/Central")

class MetarSimpleSite(object):
    """Takes in lat lon as floats and ID as a string"""
    def __init__(self, params):
        self.__id__ = params[0]
        self.__latitude__ = params[1]
        self.__longitude__ = params[2]
        self.__timezone__ = params[3]
    """Returns the lat as float"""
    def getLatitude(self):
        return self.__latitude__
    """Returns the long as float"""
    def getLongitude(self):
        return self.__longitude__
    def getID(self):
        return self.__id__
    def getTimezone(self):
        return self.__timezone__
    """Sets the timezone, useful if the user doesn't have the timezone at the moment, possible set it later"""
    def setTimezone(self, tz):
        self.__timezone__ = tz

class MetarSite(MetarSimpleSite):
    """May be able to set the timezone off the constructor if we're able to build a databse of metar sites and their appropriate timezones"""
    def __init__(self, idProfile):
        MetarSimpleSite.__init__(self, [idProfile[0], idProfile[4], idProfile[5], None])
        self.id =idProfile[0]
        self.__stateProv__ = idProfile[0]
        self.__name__ = idProfile[1]
        self.codedMetar = 0
        self.obCurrent = []
        self.__codedobHistory__ = [None]*24
        self.__decodedobHistory__ = [[None] * 15]*24
    """This is where the metar is set.  We want a datetime string to move through here as well"""
    def __str__(self):
        ret= ("ID: " + self.__id__ +"\n" +
                "State: " + self.__stateProv__+"\n" +
                "Name : " + self.__name__+"\n" +
                "Lat : " + str(self.__latitude__) + "\n" +
                "Lon : " + str(self.__longitude__) + "\n")
        for i in self.__decodedObHistory__:
            ret = ret + str(i)
        return ret
    def __setHour__(self, utcHour, obs):
        self.__codedobHistory__[utcHour] = obs
    """Returns a boolean value, True if coded obs exsist in __decodedobHistory, False otherwise."""
    def obsInserted(self):
        for ob in self.__codedobHistory__:
            if ob != None:
                return True
        return False
    def getState(self):
        return self.__stateProv__
    def getName(self):
        return self.__name__
    def getCodedHour(self, utcHour):
        return self.__codedobHistory__[utcHour]
    def getCodedHistory(self):
        return self.__codedobHistory__
    def getCodedCurrent(self):
        return self.__codedobHistory__[datetime.utcnow().hour]
    def getCodedHour(self, hour):
        return self.__codedobHistory__[hour]
    def getDecodedHour(self, hour):
        return self.__decodedobHistory__[hour]
    def getDecodedCurrent(self):
        return self.__decodedobHistory__[datetime.utcnow().hour]
    def getDecodedHistory(self):
        return self.__decodedobHistory__
    """Static method, not particular to any instance"""
    def getHeader():
        return ("AUTO", "Temp(F)", "Dew(F)","Wind Direction(CARDINAL)", "Wind Speed(mph)", "Wind Gust(mph)",
                "Cloud1", "Cloud2", "Cloud3", "Peak Gust(mph)", "Peak Gust Dir(Cardinal)", "Hourly Precip(in)","SLP","WX","Obstruction")
    def decodeHour(self, hour):
        ob = self.__codedobHistory__[hour]
        j = [None] * 15
        if ob != None:
            if "AUTO" in ob:
                j[0] = True
            else:
                j[0] = False
            m = re.search("T(\d{8})",ob)
            if m:
                j[1] = metardecoder.decTempString(m.group(0)[1:5])
                j[2] = metardecoder.decTempString(m.group(0)[5:9])
            else:
                m = re.search(" (\d{2})/(\d{2}) ",ob)
                m1 = re.search(" (\d{2})/(\d{2}) ",ob)
                m2 = re.search(" M(\d{2})/M(\d{2}) ",ob)
                if m:
                    j[1], j[2] = metardecoder.findTemp(m.group(0))
                elif m1:
                    j[1], j[2] = metardecoder.findTemp(m1.group(0))
                elif m2:
                    j[1], j[2] = metardecoder.findTemp(m2.group(0))
            m = re.search("(\d{5})G(\d{2})KT",ob)
            m1 = re.search("(\w{3})(\d{2})KT",ob)
            if m:
                j[3] = metardecoder.windDir(m.group(0))
                j[4] = metardecoder.windSpd(m.group(0))
                j[5] = metardecoder.windGust(m.group(0))
            elif m1:
                j[3] = metardecoder.windDir(m1.group(0))
                j[4] = metardecoder.windSpd(m1.group(0))
            m = re.search(" (\w{3})(\d{3}) "  , ob)
            m1 = re.search(" (\w{3})(\d{3}) (\w{3})(\d{3}) "  , ob)
            m2 = re.search(" (\w{3})(\d{3}) (\w{3})(\d{3}) (\w{3})(\d{3}) "  , ob)
            if m2:
                l = m2.group(0).split()
                j[6] = l[0]
                j[7] = l[1]
                j[8] = l[2]
            elif m1:
                l = m1.group(0).split()
                j[6] = l[0]
                j[7] = l[1]
            elif m:
                l = m.group(0).split()
                j[6] = l[0]
            m = re.search('PK WND (\d{5})/(\d{4})',ob)
            if m:
                retStr = metardecoder.peakWind(m.group(0))
                j[9] = retStr[0]
                j[10] = retStr[1]
            m = re.search('P(\d{4})',ob)
            if m:
                hour_precip = m.group(0)
                j[11] = hour_precip[1:3] + '.' + hour_precip[3:5]
            m = re.search('SLP(\d{3})',ob)
            if m:
                j[12] = metardecoder.decodeSLP(m.group(0))
            j[13], j[14] = metardecoder.decodeWxObstruct(ob)
        self.__decodedobHistory__[hour] = j
    def decodeAll(self):
        for hour in range(24):
            self.decodeHour(hour)
