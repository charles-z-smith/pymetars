import math
class LatLonConversions(object):

    def __init__(self):
        self.RADIUSEARTHKM = 6373.0

    #convers latitude longitude into x,y,z cords to do a distance calculation
    def converToCords(self, lat, lon):
        x = self.RADIUSEARTHKM * math.cos(lat/180 * math.pi) * math.cos(lon/180 * math.pi)
        y = self.RADIUSEARTHKM * math.cos(lat/180 * math.pi) * math.sin(lon/180 * math.pi)
        z = self.RADIUSEARTHKM * math.sin(lat/180 * math.pi)

        return (x,y,z)
    def convertToLatLon(self,x,y,z):
        lat = math.asin(z, 6371*1000)
        lon = math.atan2(y,x)

        return (lat,lon)

    #code from stack overflow
    #http://stackoverflow.com/questions/1140189/converting-latitude-and-longitude-to-decimal-values
    def convertDMStoDD(self, days, minutes, seconds, direction):
        decimal = days + minutes/60 + seconds/(60*60)
        if(direction == "S" or direction == "W"):
            decimal = decimal * -1
        return decimal
    """takes in two lat lons and will output a lineardistance in meters"""
    def linearDistance(self, lat1, lon1, lat2, lon2):
        latLonCart1 = self.converToCords(lat1, lon1)
        latLonCart2 = self.converToCords(lat2, lon2)
        x,y,z = latLonCart1
        x1,y1,z1 = latLonCart2
        distance = math.sqrt((x-x1)**2+(y-y1)**2+(z-z1)**2)

        return distance
    """Takes in tow lat lons and will output a curved distance in meters"""
    """http://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude-python"""
    def distance(self, lat1, lon1, lat2, lon2):
        lat2 = math.radians(lat2)
        lat1 = math.radians(lat1)
        lon2 = math.radians(lon2)
        lon1 = math.radians(lon1)
        dlat = lat2- lat1
        dlon = lon2-lon1
        a = (math.sin(dlat/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2))**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return self.RADIUSEARTHKM * c#units in Km
    
        
        
