import googlemaps, requests

from datetime import datetime

#gmaps = googlemaps.Client(key='')
# Geocoding an address
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

#now = datetime.now()
#directions_result = gmaps.directions("8001 25th St W, University Place, WA",
#                                     "Tacoma Dome Station, Tacoma, WA",
#                                     mode="driving",
#                                     departure_time=now)
#print(directions_result)
# Python program to get a google map  
# image of specified location using  
# Google Static Maps API 
  
# Enter your api key here 
api_key = ""
  
# url variable store url 
url = "https://maps.googleapis.com/maps/api/staticmap?"
  
# center defines the center of the map, 
# equidistant from all edges of the map.  
center = "Des Moines, IA"
  
# zoom defines the zoom 
# level of the map 
zoom = 10
  
# get method of requests module 
# return response object
r = requests.get(url + "center=" + center + "&zoom=" +
                   str(zoom) + "&size= 500x500&key=" +
                             api_key + "&sensor=false") 
  
# wb mode is stand for write binary mode 
f = open('/home/pi/run/map.jpg', 'wb') 
  
# r.content gives content, 
# in this case gives image 
f.write(r.content) 
  
# close method of file object 
# save and close the file 
f.close()

#End result needed:https://maps.googleapis.com/maps/api/staticmap?size=480x480&path=weight:3%7Ccolor:blue%7Cenc:a_i_Hjj}jV@~EcJ@_CCqD@kK?_TAuKAyECiA@gJEsDAkAAKsDGiCCe@Kk@g@cCm@qCiB}IQk@O]U[m@g@YMOE_@CwADa@Ia@UWWQg@Wy@Ea@CaB?{BM?{B@gA?mCBmBFo@@EgBk@{Jg@{KOkMCc@AEIS?sABqAHaErAmb@n@gSLcDLcBVoBZ}Al@uBb@kAh@eAd@y@h@u@d@k@`@_@r@m@`Ak@bBm@nJkBrB_@dA[tAq@lA}@nSoQvDeDzD}ClIkHjD}CzA{AjJ_I~BkBjDmCpDiCzA_A`CyAhC{A`B_ArA_At@{@n@{@x@uA`A{BVu@b@_Bb@gCTiBNwCBkCOuP@qLKuPGc\\EoOAc\\AeXEaAAiG?W@sDFgBNgBh@qDr@qCjAyCjAoBxBiCzA_BvBkCfCqC~A{AdAkAVY^w@XmADc@Dc@?cAGiAKw@uAuKMkBEwB?cBBuA\\}F\\cFHUVeFJmCJuHE_HEsBWeFe@kF]oC_AsFqAgHwBiKmAuHOoAQoB[kEWoHIcAMu@[_AU][i@{@q@MG{@W}AUEGKIoEqAiBc@eAKy@AuAJqBN]CyC^SiEWFw@LiBTc@gHGYQsD&key=
