# -*- coding: UTF-8 -*-

import httplib
import urllib
import json

class Spotify:

	basicAuth='<base 64 encoding of clientId:clientSecret>'
	refreshToken='<refresh token of authenticated user>'

	@staticmethod
	def currentlyPlaying(accessToken):
		
		connection = httplib.HTTPSConnection('api.spotify.com')
		connection.request('GET', '/v1/me/player/currently-playing', headers={'Authorization': 'Bearer ' + accessToken})
		response = connection.getresponse()
		data = json.loads(response.read(), 'utf-8')
		connection.close()

		return data

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


