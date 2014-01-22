"""This method is used to convert a Temperature, Dewpoint in Celcius
to Ferenheit.  This metod takes in a formated string with /d/d//d/d.  Sometimes these 
numbers can have M infromt of them to signify they are negative. for example 01/M02 would signify a temp of 1 degree in Celcius and negative 2 degrees dewpoint in Celcius """

def findTemp(temp_string):
    mid_slice = temp_string.index('/')
    tmpC = temp_string[0:mid_slice]
    dptC = temp_string[mid_slice+1:]
    temp_F =  tempString(tmpC)
    dpt_F = tempString(dptC)

    return (temp_F, dpt_F)

"""Takes in a Celcius temperature in a metar coded format.  The format may have a leading M which would signify a negative temperature.
@return a String in Fahrenheit"""

def tempString(Celcius):
    #Takes in a Celcius temperature in coded format leading 1 is negative
    Tmp = Celcius.strip()
    if Tmp.startswith('M'):
        negative = '-'
        Temp = float(negative + Tmp[1:])
        Fer = (9/5)*Temp+32.0
        Fer = str(Fer)
    else:
        Fer = ''
        negative = ''
        start = 0
        Temp = float(negative + Tmp[start:3])
        Fer = (9/5)*Temp+32.0
        Fer = str(Fer)

    return Fer

"""This method decodes a metar coded precip with a Qualifier Descriptor and a Weather Phenomena as the parameter
It will then output a decoded string which describes the coded precip.  For more info on the coded precip, read this link...
 http://www.met.tamu.edu/class/metar/quick-metar.html"""
 
def decodeWxObstruct(ob):
    split = ob.split()
    ret = [None,None]
    for i in split:
        temp = i
        intensity = ""
        descriptor = ""
        wx = ""
        obstruct = ""
        if temp.startswith("-"):
            intensity = "Lgt"
            temp = temp.replace("-", "")
        elif temp.startswith("+"):
            intensity = "Hvy"
            temp = temp.replace("+", "")
        else:
            intensity = ""
        if temp.startswith("MI"):
            descriptor = "Shallow"
            temp = temp.replace("MI", "")
        elif temp.startswith("PR"):
            descriptor = "Partial"
            temp = temp.replace("PR", "")
        elif temp.startswith("BC"):
            decriptor = "Patches"
            temp = temp.replace("BC", "")
        elif temp.startswith("DR"):
            descriptor = "Drifting"
            temp = temp.replace("DR", "")
        elif temp.startswith("BL"):
            descriptor = "Blowing"
            temp = temp.replace("BL", "")
        elif temp.startswith("SH"):
            descriptor = "Showerr"
            temp = temp.replace("SH", "")
        elif temp.startswith("TS"):
            descriptor = "T-Storm"
            temp = temp.replace("TS", "")
        elif temp.startswith("FZ"):
            descriptor = "Freezing"
            temp = temp.replace("FZ","")
        else:
            descriptor = ""
        if temp.startswith("DZ"):
            wx= "Drizzle"
        elif temp.startswith("RA"):
            wx = "Rain"
        elif temp.startswith("SN"):
            wx = "Snow"
        elif temp.startswith("SG"):
            wx = "Snow Grains"
        elif temp.startswith("IC"):
            wx= "Ice Crystals"
        elif temp.startswith("PL"):
            wx= "Ice Pellets"
        elif temp.startswith("GR"):
            wx = "Hail"
        elif temp.startswith("GS"):
            wx= "Small Hail"
        elif temp.startswith("SQ"):
            wx = "Squall"
        elif temp.startswith("FC"):
            wx = "Funnel CLoud"
        elif temp.startswith("+FC"):
            wx = "Tornado"
        elif temp.startswith("SS"):
            wx = "Sand Storm"
        elif temp.startswith("DS"):
            wx = "Dust Storm"
        if temp.startswith("BR"):
            obstruct= "BR"
        elif temp.startswith("FG"):
            obstruct = "Fog"
        elif temp.startswith("FU"):
            obstruct = "Smoke"
        elif temp.startswith("VA"):
            obstruct = "Volcanic Ash"
        elif temp.startswith("DU"):
            obstruct = "Dust"
        elif temp.startswith("SA"):
            obstruct = "Sand"
        elif temp.startswith("HZ"):
            obstruct = "Haze"
        elif temp.startswith("PY"):
            obsturct = "Spray"
        if wx != "":
            ret[0] = intensity + " " + descriptor + " " + wx
        if obstruct != "":
            ret[1] = obstruct
    return tuple(ret)

"""Decodes a list,  it may be empty if the observation is poorly coded"""
def decodeClouds(cloudList):
    if len(cloudList) == 0:
        return ["N/A"]
    else:
        for i,j in enumerate(cloudList):
            if j.startswith("FEW"):
                cloudList[i] = "3"
            elif j.startswith("SCT"):
                cloudList[i] = "5"
            elif j.startswith("BKN"):
                cloudList[i] = "8"
            elif j.startswith("OVC"):
                cloudList[i] = "10"
            elif j.startswith("CLR"):
                cloudList[i] = "0"
            elif j.startswith("VV"):
                cloudList[i] = "10"
        cloudList.sort(reverse = True)
        return cloudList

def testMe():
    print("Hello World")
    
"""This method is used to convert a Temperature/Dewpoint in Celcius
to Fahrenheit.  It is used to convert a particular string format of metar encoding.
The encoding which should be passed into this method should the substring /d/d/d/d from T/d/d/d/d/d/d/d/d.
the four numbers should be the first four or the last four, not four from the middle.
@return a String in Fahrenheit
@param takes in a String temperature in Celcius"""

def decTempString(Celcius):
    Tmp = Celcius
    sign = ""
    if Tmp.startswith('1'):
        sign = '-'
    Temp = float(sign + Tmp[1:3] + '.' + Tmp[3:4])
    Fer = round((9/5)*Temp+32.0,2)
    Fer = str(Fer)

    return Fer

def windDir(windstring):
    #Takes in a wind string with leading digits dir
    Winddir = windstring[0:3]
    if Winddir == 'VRB':
        Dir = 'VRB'
    elif Winddir >= '349':
        Dir = 'N'
    elif Winddir <= '011':
        Dir = 'N'
    elif Winddir >= '012' and Winddir <= '034':
        Dir = 'NNE'
    elif Winddir >= '035' and Winddir <= '056':
        Dir = 'NE'
    elif Winddir >= '057' and Winddir <= '079':
        Dir = 'ENE'
    elif Winddir >= '080' and Winddir <= '101':
        Dir = 'E'
    elif Winddir >= '102' and Winddir <= '123':
        Dir = 'ESE'
    elif Winddir >= '124' and Winddir <= '146':
        Dir = 'SE'
    elif Winddir >= '147' and Winddir <= '168':
        Dir = 'SSE'
    elif Winddir >= '169' and Winddir <= '192':
        Dir = 'S'
    elif Winddir >= '193' and Winddir <= '213':
        Dir = 'SSW'
    elif Winddir >= '214' and Winddir <= '237':
        Dir = 'SW'
    elif Winddir >= '238' and Winddir <= '258':
        Dir = 'WSW'
    elif Winddir >= '259' and Winddir <= '282':
        Dir = 'W'
    elif Winddir >= '283' and Winddir <= '303':
        Dir = 'WNW'
    elif Winddir >= '304' and Winddir <= '327':
        Dir = 'NW'
    elif Winddir >= '328' and Winddir <= '348':
        Dir = 'NNW'
    else:
        Dir = "N/A"
    if windstring[3:5] == '00':
        Dir = 'CLM'

    return Dir

def windSpd(windstring):
    Spd = windstring[3:5]
    if Spd == '00':
        speed = '00'
    else:
        try:
            kts = int(Spd)
            mph = round(1.15*kts,1)
            speed = str(mph)
        except:
            speed = None

    return speed

def windGust(windstring):
    if 'G' in windstring:
        gust = windstring[6:8]
        kts = int(gust)
        mph = 1.15*kts
        spd = str(mph)
    else:
        spd = None

    return spd

"""Takes in a peak wind gust string, outputs speed in mph,direction in cardinal and
   the time of the peak wind gust """
   
def peakWind(windString):
        mph = str(1.15 * int(windString[10:12]))
        direction = windDir(windString[7:10])
        time =  windString[13:]
        return (mph, direction, time)
    
def decodeSLP(slpString):
    if int(slpString[3:]) >= 860:#low pressure,  record lows are not able to go below this
        return "9" + slpString[3:5] + "." + slpString[5:]
    else:
        return "10" + slpString[3:5] + "." + slpString[5:]

def decodeAltimeter(altString):
    return altString[1:3] + "." + altString[3:]
