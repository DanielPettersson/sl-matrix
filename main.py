#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import sl
from sl import SlData
import spotify
from spotify import Spotify
from string import Template
import Image
import ImageDraw
import ImageFont
import time
import line
import threading
import logging
from rgbmatrix import Adafruit_RGBmatrix

def textWidth(text, font):
	width, ignore = font.getsize(text)
	return width

def drawText(text, xd, y, color, font):
	width = textWidth(text, font)
	draw.text((16+xd-width/2, y), text, fill=color, font=font)

matrix = Adafruit_RGBmatrix(32, 1)
image = Image.new("RGBA", (32, 32), "black")
draw  = ImageDraw.Draw(image)
fontBig = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 16)
fontSmall = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 11)

start_time = time.time()

print 'Initialized...'

while time.time() - start_time < 5400:

	print time.strftime('%Y-%m-%d %T')

	try:
		buses = SlData.nextBusesFromSiteId('3277', 1)
		
		wait_time = 60
		if len(buses) == 0:
			wait_time = 30
		elif buses[0]['DisplayTime'] == '4 min' or buses[0]['DisplayTime'] == '3 min'or buses[0]['DisplayTime'] == '2 min':
			wait_time = 30
		elif buses[0]['DisplayTime'] == 'Nu' or buses[0]['DisplayTime'] == '1 min':
			wait_time = 15

		wait_start_time = time.time()
		waited_time = 0.01
		bus_index = 0

		while waited_time < wait_time:

			draw.rectangle([(0, 0), image.size], fill = (0,0,0))

			if len(buses) == 0:
				drawText('Ingen', 0, 8, (255,255,0), fontSmall)
			else:
				drawText(buses[bus_index]['LineNumber'], -1, 0, (0,200,0), fontBig)
				drawText(buses[bus_index]['DisplayTime'], 0, 17, (255,0,0), fontSmall)

			if len(buses) < 2:
				bus_index = 0
			elif bus_index == 0:
				bus_index = 1
			else:
				bus_inedx = 0

			xx = waited_time/wait_time * 32
			line.drawLine(draw, image, xx-2, 30, xx, 30, (210,210,210,20))
			line.drawLine(draw, image, xx-2, 31, xx, 31, (210,210,210,20))
			matrix.SetImage(image.im.id, 0, 0)

			time.sleep(2)
			waited_time = time.time() - wait_start_time


	except Exception:
		logging.exception("Failed to fetch SL data")
		time.sleep(15)

print 'Start checking for Spotify'		
		
displayTextScroll = 32
currentlyPlaying = False
displayText = ''
displayTextWidth = 0
durationMs = 1000
progressMs = 0
progressFetchMs = 0

def spotifyDataFetcher():

	global currentlyPlaying
	global displayText
	global displayTextWidth
	global durationMs
	global progressMs
	global progressFetchMs
	global start_time

	accessToken = ''
	while time.time() - start_time < 50400:
		try :
			if accessToken == '':
				accessToken = Spotify.getAccessToken()
		
			currentlyPlayingData = Spotify.currentlyPlaying(accessToken)
			
			if currentlyPlayingData['is_playing'] == True:
				currentlyPlaying = True
				songName = currentlyPlayingData['item']['name'].encode('iso-8859-1').strip()
				artistName = currentlyPlayingData['item']['artists'][0]['name'].encode('iso-8859-1').strip()
				displayText = artistName + ' - ' + songName
				displayTextWidth = textWidth(displayText, fontSmall)
				durationMs = currentlyPlayingData['item']['duration_ms']
				progressMs = currentlyPlayingData['progress_ms']
				progressFetchMs = int(round(time.time() * 1000))
				print displayText
				time.sleep(1)
			else:
				print currentlyPlayingData
				currentlyPlaying = False
				if currentlyPlayingData.get('token_expired', False) == True:
					accessToken = ''
				time.sleep(10)
			

		except Exception as e:
			logging.exception("Failed to fetch spotify data")
			time.sleep(10)
			accessToken = ''

thread = threading.Thread(target=spotifyDataFetcher)
thread.daemon = True
thread.start()

while thread.isAlive():
	if currentlyPlaying:
		nowMs = int(round(time.time() * 1000))
		currentProgressMs = min(progressMs + nowMs - progressFetchMs, durationMs)
		progress = currentProgressMs / float(durationMs) * 360
		progressStr = "%d:%02d" % (currentProgressMs / 60000, (currentProgressMs / 1000) % 60)
	
		draw.rectangle([(0, 0), image.size], fill = (0,0,0))
		draw.pieslice([0, 0, 32, 32], 0, int(progress), fill=(60,0,0,255))
		draw.arc([0, 0, 32, 32], 0, 360, fill=(120,0,0,255))
		draw.text((displayTextScroll, 3), displayText, fill=(170,170,170,170), font=fontSmall)
		drawText(progressStr, 0, 17, (170,170,170,170), fontSmall)
		
		matrix.SetImage(image.im.id, 0, 0)

		displayTextScroll -= 2
		if displayTextScroll < -displayTextWidth:
			displayTextScroll = 32
		time.sleep(0.01)
			
	else:
		draw.rectangle([(0, 0), image.size], fill = (0,0,0))
		matrix.SetImage(image.im.id, 0, 0)
		time.sleep(1)

	


