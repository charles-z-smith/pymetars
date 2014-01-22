
Installation:
for python 3+
This is a python package, so you pull this repository into the Lib/site-packages directory.
It also requires the pytz module for dealing with timezones

Example Usage:

>>> import metars.metarlist
>>> mlst = metars.metarlist.MetarList()#Download stationlist from "http://weather.rap.ucar.edu/surface/stations.txt"
>>> mlst = metars.metarlist.MetarList("C:/Python32/Lib/site-packages/metars/tests/stations.txt")#load it in from a local directory
>>> mlst.downloadCycle()#download the latest 24 hours of metar data
>>> site = mlst.getSite("KMKE")# get a site
>>> site.getCodedHistory()#get the last 24 hours of coded metar data
['KMKE 212352Z 26005KT 10SM FEW027 BKN250 M16/M22 A3021 RMK AO2 SLP250 4/007 T11561217 11122 21156 58006', 'KMKE 220052Z 29005KT 10SM FEW027 BKN250 M16/M22 A3020 RMK AO2 SLP248 T11611217', 'KMKE 220152Z 30007KT 10SM FEW027 SCT250 M17/M22 A3020 RMK AO2 SLP246 T11671222', 'KMKE 220252Z 31005KT 10SM FEW027 SCT250 M17/M22 A3019 RMK AO2 SLP243 T11671222 56007', 'KMKE 220352Z 28004KT 10SM FEW027 FEW250 M17/M22 A3017 RMK AO2 SLP238 T11721222', 'KMKE 220452Z 30005KT 10SM OVC100 M17/M22 A3017 RMK AO2 SLP235 T11671222', None, 'KMKE 210652Z 36018G26KT 8SM OVC039 M15/M22 A3015 RMK AO2 PK WND 35027/0602 SNE45 SLP227 P0000 T11501217', 'KMKE 210752Z 35019G27KT 10SM BKN055 M16/M23 A3018 RMK AO2 PK WND 33028/0709 SLP236 T11561228', 'KMKE 210852Z 34017G21KT 10SM FEW055 M16/M23 A3020 RMK AO2 SLP245 60000 T11611228 53021', 'KMKE 210952Z 34017KT 10SM FEW022 M17/M23 A3023 RMK AO2 SLP253 T11671228', 'KMKE 211052Z 35018G23KT 10SM SCT023 M17/M23 A3025 RMK AO2 SLP262 T11671228', 'KMKE 211152Z 34014KT 10SM FEW023 M17/M22 A3026 RMK AO2 SLP266 4/007 60000 70001 T11721222 11144 21172 51020', 'KMKE 211252Z 33011KT 10SM FEW023 M18/M23 A3028 RMK AO2 SLP272 T11781228', 'KMKE 211352Z 34010KT 10SM FEW023 M18/M23 A3029 RMK AO2 SLP277 T11781228', 'KMKE 211452Z 33007KT 10SM FEW025 M17/M22 A3030 RMK AO2 SLP277 T11721222 51011', 'KMKE 211552Z 34013KT 10SM FEW025 M16/M22 A3030 RMK AO2 SLP278 T11611222', 'KMKE 211652Z 34010KT 10SM FEW027 M15/M22 A3029 RMK AO2 SLP277 T11501217', 'KMKE 211752Z 31009KT 10SM FEW027 M14/M22 A3028 RMK AO2 SLP272 4/007 933022 T11441217 11144 21178 58006', 'KMKE 211852Z 30006KT 10SM FEW028 FEW250 M13/M21 A3026 RMK AO2 SLP264 T11331211', 'KMKE 211952Z 29006KT 10SM FEW030 FEW250 M13/M22 A3024 RMK AO2 SLP257 T11281217', 'KMKE 212052Z 29009KT 10SM FEW030 FEW250 M13/M22 A3023 RMK AO2 SLP255 T11281217 56016', 'KMKE 212152Z 30008KT 10SM FEW027 SCT250 M14/M22 A3023 RMK AO2 SLP256 T11391217', 'KMKE 212252Z 28007KT 10SM FEW027 BKN250 M15/M22 A3023 RMK AO2 SLP256 T11501217']
>>> site.getCodedCurrent()#just decode the current hour, could decode all of them if we wanted too.
'KMKE 220452Z 30005KT 10SM OVC100 M17/M22 A3017 RMK AO2 SLP235 T11671222'
>>> from datetime import datetime
>>> utcnow = datetime.utcnow()
>>> utcnow.hour
5
>>> site.decodeHour(5)#you can also just select one hour to decode
>>> site.getCodedHour(5)
'KMKE 220452Z 30005KT 10SM OVC100 M17/M22 A3017 RMK AO2 SLP235 T11671222'
>>> site.getDecodedHour(5)#the result of the decoded hour comes out in a list the size of the header
[None, '1.94', '-7.96', 'WNW', '5.8', None, 'OVC100', None, None, None, None, None, '1023.5', None, None]
>>> import metars.metar
>>> metars.metar.MetarSite.getHeader()# class method which tells us which index is relative to what
('AUTO', 'Temp(F)', 'Dew(F)', 'Wind Direction(CARDINAL)', 'Wind Speed(mph)', 'Wind Gust(mph)', 'Cloud1', 'Cloud2', 'Cloud3', 'Peak Gust(mph)', 'Peak Gust Dir(Cardinal)', 'Hourly Precip(in)', 'SLP', 'WX', 'Obstruction')
>>> header = metars.metar.MetarSite.getHeader()
>>> header[1]
'Temp(F)'
>>> decodedHour = [None, '1.94', '-7.96', 'WNW', '5.8', None, 'OVC100', None, None, None, None, None, '1023.5', None, None]
>>> decodedHour[1]
'1.94'
>>> site.getState()
'WI'
>>> site.getLongitude()
'087 54W'
>>> site.getLatitude()
'42 57N'
>>> 




Future improvements:

I am going to put out some future upgrade to work with basemap,  but this is a pretty good starting point.


Comments:
This is my first python package, so if you have any comments of suggestions, please email me
czacmith ... gmail.com