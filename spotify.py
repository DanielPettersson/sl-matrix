# -*- coding: UTF-8 -*-

import httplib
import urllib
import json

class Spotify:

	basicAuth='XXX'
	refreshToken='XXX'

	@staticmethod
	def currentlyPlaying(accessToken):
		
		connection = httplib.HTTPSConnection('api.spotify.com')
		connection.request('GET', '/v1/me/player/currently-playing', headers={'Authorization': 'Bearer ' + accessToken})
		response = connection.getresponse()
		responseData = response.read()
		connection.close()
		
		if response.status == 200 and responseData != '':
			return json.loads(responseData, 'utf-8')
		else:
			return {'is_playing': False}

	@staticmethod
	def getAccessToken():
		
		headers = {'Authorization': 'Basic ' + Spotify.basicAuth,  'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded'}
		params = urllib.urlencode({'grant_type': 'refresh_token', 'refresh_token': Spotify.refreshToken})
		
		connection = httplib.HTTPSConnection('accounts.spotify.com')
		connection.request('POST', '/api/token', params, headers)
		response = connection.getresponse()
		data = json.loads(response.read(), 'utf-8')
		connection.close()

		return data['access_token']


