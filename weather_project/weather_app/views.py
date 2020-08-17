from django.shortcuts import render
import urllib.request
import json

# Create your views here.
def index(request):
    if request.method == "POST":
        city = request.POST.get("city")
        try:
            data = urllib.request.urlopen('http://api.weatherapi.com/v1/current.json?key=f8dafc0bda574e0bb4d154724201308&q='+city)
            data1 = data.read().decode()
            data_dict = json.loads(data1)

            city_data = {
            'name': data_dict["location"]["name"],
            'city': data_dict["location"]['region'],
            'country': data_dict["location"]['country'],
            'time' :data_dict["location"]['localtime'],
            'temp': data_dict["current"]['temp_c'],
            'condition' :data_dict["current"]["condition"]['text'],
            'wind': data_dict["current"]['wind_kph'],
            'direction': data_dict["current"]['wind_dir'],
            'humidity': data_dict['current']['humidity'],
            'feels_l': data_dict["current"]['feelslike_c'],
            'icon': data_dict["current"]["condition"]["icon"]
            }
            for i in city_data:
                if city_data[i] == 0 or 0.0:
                    city_data[i] = "0"
        except:
            city_data = {}
    else:
        city_data = {}


    return render(request, "weather_app/index.html", city_data)
