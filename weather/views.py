import requests

from django.shortcuts import render
from django.http import HttpResponse
from .models import City
from .forms import CityForm


def index(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0830f5b810f6f0d240789074d3cf17b5'

    err_msg=""
    message=""
    message_class=""

    cities = City.objects.all()
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()

            if existing_city_count==0:
                r=requests.get(url.format(new_city)).json()
                print(r)
                if r['cod']==200:
                    form.save()
                else:
                    err_msg="City Doesnt Exist"
            else:
                err_msg="City Already Exists in the DataBase"
        if err_msg:
            message=err_msg
            message_class='is-danger'
        else:
            message=err_msg
            message_class='is-success'

    form = CityForm()
    weather_data=[]

    for city in cities:
        q=requests.get(url.format(city.name)).json()
        city_weather = {
            'city': city.name,
            'temperature':q["main"]["temp"],
            'description':q['weather'][0]['description'],
            'icon':q['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
        print(city_weather)

    context={
            'weather_data':weather_data ,
             'form':form,
            'message':message,
            'message_class':message_class
    }
    return render(request,"weather/weather.html",context)
