# -*- coding: UTF-8 -*-

import httplib
import json

class SlData:

	host = 'api.sl.se'
	stationUrl = '/api2/typeahead.json?key=8b5fddea149b4d53b8e3890380fb2bc4&searchstring='
	realtimeUrl = '/api2/realtimedepartures.json?key=1d339807f564493ba4479049f13540b0&TimeWindow=60&siteid='

	@staticmethod
	def findStation(stationSearch):
		
		connection = httplib.HTTPConnection(SlData.host)
		connection.request('GET', SlData.stationUrl + stationSearch)
		response = connection.getresponse()
		stationData = json.loads(response.read(), 'utf-8')
		connection.close()

		if len(stationData['ResponseData']) == 0:
		    raise InputError('Hittade ingen hållplats')

		return stationData['ResponseData'][0]

	@staticmethod
	def nextBusFromStation(station, direction):
		return SlData.nextBusFromSiteId(station['SiteId'], direction)

	@staticmethod
	def nextBusFromSiteId(siteId, direction):

		connection = httplib.HTTPConnection(SlData.host)
		connection.request('GET', SlData.realtimeUrl + siteId)
		response = connection.getresponse()
		realtimeData = json.loads(response.read(), 'utf-8')
		connection.close()

		for bus in realtimeData['ResponseData']['Buses']:
			if bus['JourneyDirection'] == direction:
				return bus

		return None



