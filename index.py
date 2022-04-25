
import requests
import json
from flask import Flask, render_template , request
import phonenumbers
import folium
import os
from phonenumbers import carrier
from phonenumbers import geocoder
from opencage.geocoder import OpenCageGeocode
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


def findGeocode(city):
       
    
    try:
          
        
        geolocator = Nominatim(user_agent="Phone_number_tracker")
          
        return geolocator.geocode(city)
      
    except GeocoderTimedOut:
          
        return findGeocode(city)    
  


      


app= Flask(__name__)
@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        global number
        number = request.form['number']
        
        
        key = "68999bf078c74d3baffc4902e49350ff"
   
        provider = phonenumbers.parse(number)
        service=carrier.name_for_number(provider, "en")
      
        access_key = '78e1e9ee3c20c8dfe1d6b1b7bd19ea01'
        url = 'http://apilayer.net/api/validate?access_key=' + access_key + '&number=' + number
        response = requests.get(url)
        answer=json.loads(response.text)
       
        
        if findGeocode(answer['location']) != None:
           
            loc = findGeocode(answer['location'])
                
                
            lat=loc.latitude
            long=loc.longitude
            
            
        
            
            
            map_my = folium.Map(location=[lat , long ] , zoom_start= 8)
            folium.Marker([lat , long ], popup = [lat,long]).add_to((map_my))

            #print(map_my)
            map_my.save("./templates/Map"+number+".html")
        
        if answer["valid"] == True:
            #print(answer)
            return render_template("isp.html",country_code=answer["country_code"],local_format=answer["local_format"],country=answer["country_name"],location=answer["location"],Service=service,latitude=lat,longitude=long,Line_type=answer["line_type"],Carrier=answer["carrier"],intf=answer['international_format'])
        return render_template("invalid.html")
    except Exception:
        return render_template("invalid.html")
        
@app.route('/map',methods=['GET'])
def show_map():
    
    return render_template("Map"+number+".html")
app.run()