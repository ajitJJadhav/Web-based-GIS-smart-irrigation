from django.shortcuts import redirect,render,get_object_or_404
from django.http import HttpResponse
from xml.dom import minidom
import urllib2, urllib, json
import unicodedata

def dashboard(request):

	baseurl = "https://query.yahooapis.com/v1/public/yql?"
	yql_query = "select item.forecast from weather.forecast where woeid=2295279 AND u='c'"
	yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
	result = urllib2.urlopen(yql_url).read()
	data = json.loads(result)

	forecast = data['query']['results']


	forecasts = []
	for i in range(9):
		L = [1,2,3,4]
		a = forecast[u'channel'][i][u'item'][u'forecast'][u'date']
		b = forecast[u'channel'][i][u'item'][u'forecast'][u'low']
		c = forecast[u'channel'][i][u'item'][u'forecast'][u'high']
		d = forecast[u'channel'][i][u'item'][u'forecast'][u'text']
		L[0] = unicodedata.normalize('NFKD', a).encode('ascii','ignore')
		L[1] = unicodedata.normalize('NFKD', b).encode('ascii','ignore')
		L[2] = unicodedata.normalize('NFKD', c).encode('ascii','ignore')
		L[3] = unicodedata.normalize('NFKD', d).encode('ascii','ignore')
		forecasts.append(L)

	return render(request, 'wms/Dashboard_mist/pages/base.html', { 'forecasts' : forecasts })
