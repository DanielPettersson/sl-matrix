# -*- coding: UTF-8 -*-

import httplib
import urllib
import json

class Spotify:

	basicAuth='YjM0N2UxYThlMmZmNGU5NDgzY2MyN2E3Y2Y0Mzc0ODY6Zjk4MjEyZGNjM2Y2NGQ5MjllMmQ2OWExNGM4NmEzMDE='
	refreshToken='AQD9FAmCU-iN_5ICrYtr5UsW5ZHaJP_pkzPwNTSujwcyl4g4da7eOKnYpbmIgfBzqYl6Zl5qwaz0LSwiKPi2Likb_Y7EYLAI-7gCWvpHxUXcGbqXPXDVlVD_WlTkNByiK_w'

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


