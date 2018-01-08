from django.shortcuts import redirect,render,get_object_or_404
from .models import Plant,waterTank,location
from django.http import HttpResponse
from django.utils import timezone
import json
# Create your views here.

def plant_list(request):
	d=[]
	A = Plant.objects.all()
	for i in A:
		if i.plantID not in d:
			d.append(i.plantID)

	for i in d:
		locations = location.objects.filter(plantID=i).count()
		if locations == 0:
			location.objects.create(plantID=i)



	return render(request, 'wms/Dashboard_mist/pages/plant_list.html', {'p1':d[0], 'p2':d[1], 'length' : len(d), 'p':d })

def plant_detail(request,pID):
	x=Plant.objects.filter(plantID=pID).order_by('-created_on')
	#plant = Plant.objects.filter(plantID=1).latest('plantID')

	arr = []
	current = timezone.now()

	for p in x:
		delta = current - p.created_on
		if delta.seconds >= 1:
			current = p.created_on
			arr.append(json.dumps({'temperature': p.temperature, 'humidity': p.humidity, 'soilMoisture' : p.soilMoisture}))
		# print p.humidity


	return render(request,'wms/Dashboard_mist/pages/plant_details.html',{'plantsjson': arr, 'plants': x,'latest':x[0], 'levelx':waterTank.objects.order_by("-created_on")[0].tankWaterLevel})

def grab(request):
	temp = request.GET['t']
	plantID=request.GET['plantID']
	soilMoisture = request.GET['s']
	humidity = request.GET['h']
	Plant.objects.create(plantID=plantID,temperature = temp,soilMoisture = soilMoisture,humidity = humidity)

	locations = location.objects.filter(plantID=plantID).count()
	if locations == 0:
		x = location.objects.all().order_by("plantID")[0]
		location.objects.create(plantID=plantID,latitude=x.latitude,longitude=x.longitude)

	return redirect("plant_detail",pID=plantID)

def showTank(request):
    x = waterTank.objects.order_by("-created_on")

    arr = []
    current = timezone.now()

    for p in x:
        delta = current - p.created_on
        if delta.seconds >= 1:
            current = p.created_on
            level = p.tankWaterLevel
        #if z < 0:
        #	z = 35
        arr.append(json.dumps({'level': level}))


    t = waterTank.objects.order_by("-created_on")[0]
    return render(request,"wms/Dashboard_mist/pages/water_tank_details.html",{'plantsjson': arr, 'tank':waterTank.objects.order_by("-created_on")[0],'levelx':waterTank.objects.order_by("-created_on")[0].tankWaterLevel})


def waterLevel(request):
	level = request.GET['level']
	rain = request.GET['rain']
	t = waterTank.objects.all()[0]
	#z = 40-level
	#if z < 0:
		#level = 5
		#z = 35

	waterTank.objects.create(tankWaterLevel=level,radius=t.radius,height=t.height,rain = rain)
	t = waterTank.objects.order_by("-created_on")[0]
	t.saveVolume()
	t.save()
    #if t.volume < 200:
    #    t.alert()
    #return redirect("showTank")

	x = waterTank.objects.order_by("-created_on")

	arr = []
	current = timezone.now()

	for p in x:
		delta = current - p.created_on
		if delta.seconds >= 1:
			current = p.created_on

			arr.append(json.dumps({'level': level}))

	t = waterTank.objects.order_by("-created_on")[0]
	return render(request,"wms/Dashboard_mist/pages/water_tank_details.html",{'plantsjson': arr, 'tank':waterTank.objects.order_by("-created_on")[0],'levelx':level})


def dimensions(request):
    radius = request.GET['r']
    height = request.GET['h']

    if waterTank.objects.all().count() == 0:
        waterTank.objects.create(radius=radius,height=height)
    else:
        x = waterTank.objects.all()[0]
        x.radius = radius
        x.height = height
        x.save()

    #return redirect("showTank")

    x = waterTank.objects.order_by("-created_on")

    arr = []
    current = timezone.now()

    for p in x:
        delta = current - p.created_on
        if delta.seconds >= 1:
            current = p.created_on
            z = p.height-p.tankWaterLevel
            if z < 0:
                z = 35
        arr.append(json.dumps({'level': z}))


    t = waterTank.objects.order_by("-created_on")[0]
    return render(request,"wms/Dashboard_mist/pages/water_tank_details.html",{'plantsjson': arr, 'tank':waterTank.objects.order_by("-created_on")[0],'levelx':t.height-t.tankWaterLevel})



def showMap(request):
	#plant1 = Plant.objects.filter(plantID=1).order_by('-created_on')[0]
	#plant2 = Plant.objects.filter(plantID=2).order_by('-created_on')[0]
	t = waterTank.objects.order_by("-created_on")[0]
	rain = t.rain
	plant=Plant.objects.all()
	locations = location.objects.all()
	d=[]
	A = Plant.objects.all()
	for i in A:
		if i.plantID not in d:
			d.append(i.plantID)
	return render(request,"wms/Dashboard_mist/pages/maps.html",{'plant':plant,'tank' : t.tankWaterLevel , 'rain' : rain, 'locations' : locations[1:] , 'size' : len(d)})

def changeLocation(request):
	ID = request.GET['ID']
	lat = request.GET['lat']
	lon = request.GET['lon']
	x = location.objects.filter(plantID=ID).update(latitude = lat,longitude = lon)

	return redirect('/plants/showLocation')
