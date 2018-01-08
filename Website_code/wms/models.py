from django.db import models
from django.utils import timezone
import math
#from twilio.rest import Client
# Create your models here.




class Plant(models.Model):
	plantID = models.IntegerField()
	created_on = models.DateTimeField(auto_now_add=True)
	#tankLinked=models.ForeignKey(Tank, on_delete=models.CASCADE)
	soilMoisture = models.FloatField(default=370)
	temperature=models.FloatField(default=25)
	humidity = models.FloatField(default=40)

	def __str__(self):
		return str(self.plantID)


class waterTank(models.Model):
	radius = models.FloatField()
	height = models.FloatField()
	tankWaterLevel = models.FloatField(default=0)
	volume = models.FloatField(default=0)
	created_on = models.DateTimeField(auto_now_add=True)
	rain = models.IntegerField(default=0)

	def saveVolume(self):
		self.volume = round( (math.pi * self.radius * self.radius) * float(self.tankWaterLevel) )

class location(models.Model):
	plantID = models.IntegerField(unique=True)
	latitude = models.FloatField(default=13.549549)
	longitude = models.FloatField(default=79.99999)

