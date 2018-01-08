#/usr/bin/python
import serial
import requests

from selenium import webdriver
import urllib

mail = 0


def sendmail(SM1,SM2,WL):

	import smtplib	
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	fromaddr = "arshad.g16@iiits.in"
	toaddr = "arshad.g16@iiits.in"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Farm details"
	body=""

	m1="PLANT 1 IS DYING!!!"
	m2="PLANT 2 IS DYING!!!"
	m3="PLANT 1 IS HEALTHY"
	m4="PLANT 2 IS HEALTHY"    

	if mail==1:
		body=m1+m4
	elif mail==2:
		body=m2+m3
	elif mail==3:
		body=m1+m2
	elif mail==0:
		body=m3+m4

	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "arshad9991")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

ser=serial.Serial('/dev/ttyACM0', 9600)



while(1):
	data=ser.readline()
	f = open("/home/pi/Desktop/check","a")
	f.write(data+"\n")
	x=data.split(" ")
	print(x)
	print(data)
	sm1=int(x[3])
	sm2=int(x[4])
	wlev=float(x[5])
	status = 0
	if(sm1<0 and sm2 >0):
		status = 1
	if(sm1>0 and sm2<0):
		status = 2
	if(sm1<0 and sm2<0):
		status =3
	if(status != mail):
		mail=status
		sendmail(int(x[3]),int(x[4]),int(x[2]))
	if(len(x)==6):
		mark=0
		for i in range(6):
			try:
				d=float(x[i])
			except:
				print(i)
				mark=1
				break
		if(mark==1):
			print("ERROR")
			continue
		print("SENT")
		try:
			urllib.urlopen("http://ad07.pythonanywhere.com/plants/getWaterLevel?level="+x[5]+"&rain="+x[4]);
			urllib.urlopen("http://ad07.pythonanywhere.com/plants/getdata?t="+str(x[1])+"&plantID=1&h="+x[0]+"&s="+x[2]);
			urllib.urlopen("http://ad07.pythonanywhere.com/plants/getdata?t="+str(x[1])+"&plantID=2&h="+x[0]+"&s="+x[3]);
		except:
			pass
		#browser.get("http://10.0.3.23:9090/plants/getdata?t="+str(x[1])+"&plantID=2&h="+x[0]+"&s="+x[-2] );
		#print("http://10.0.3.23:9090/plants/getdata?t="+str(x[1])+"&plantID=2&h="+x[0]+"&s="+x[-2]);
		#browser.get("http://10.0.3.23:9090/plants/getdata?t="+str(x[1])+"&plantID=1&h="+x[0]+"&s="+x[2]);
		#browser.get("http://10.0.3.23:9090/plants/getdata?t="+str(x[1])+"&plantID=2&h="+x[0]+"&s="+x[-2]);
		#browser.get("http://10.0.3.23:9090/plants/getWaterLevel?level="+x[5]+"&rain="+x[4]);
		print(x[-1])
