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
		bus = SlData.nextBusFromSiteId('3277', 1)
		
		draw.rectangle([(0, 0), image.size], fill = (0,0,0))

		if bus is None:
			print 'No next bus'
			drawText('Ingen', 0, 8, (255,255,0), fontSmall)
		else:
			print bus['LineNumber'] + ' ' + bus['DisplayTime'] 
			drawText(bus['LineNumber'], -1, 0, (0,200,0), fontBig)
			drawText(bus['DisplayTime'], 0, 17, (255,0,0), fontSmall)

		matrix.Clear()
		matrix.SetImage(image.im.id, 0, 0)

		wait_time = 60
		if bus is None:
			wait_time = 120
		elif bus['DisplayTime'] == '4 min' or bus['DisplayTime'] == '3 min'or bus['DisplayTime'] == '2 min':
			wait_time = 30
		elif bus['DisplayTime'] == 'Nu' or bus['DisplayTime'] == '1 min':
			wait_time = 15

		wait_start_time = time.time()
		waited_time = 0.01
		while waited_time < wait_time:
			xx = waited_time/wait_time * 32
			line.drawLine(draw, image, xx-2, 30, xx, 30, (210,210,210,20))
			line.drawLine(draw, image, xx-2, 31, xx, 31, (210,210,210,20))
			matrix.SetImage(image.im.id, 0, 0)
			time.sleep(0.25)
			waited_time = time.time() - wait_start_time


	except Exception:
		print ' Failed to get data from SL'
		time.sleep(15)

		
		
accessToken = Spotify.getAccessToken()

displayTextScroll = 32

while time.time() - start_time < 50400:

	try :
		currentlyPlaying = Spotify.currentlyPlaying(accessToken)
		songName = currentlyPlaying['item']['name'].encode('iso-8859-1').strip()
		artistName = currentlyPlaying['item']['artists'][0]['name'].encode('iso-8859-1').strip()
		displayText = artistName + ' - ' + songName
		displayTextWidth = textWidth(displayText, fontSmall)
		durationMs = currentlyPlaying['item']['duration_ms']
		progressMs = currentlyPlaying['progress_ms']
		remainingMs = durationMs - progressMs
		loadMs = int(round(time.time() * 1000))
		nowMs = loadMs
		endMs = nowMs + remainingMs
		
		print displayText
				
		while endMs > nowMs and nowMs - loadMs < 5000:
		
			draw.rectangle([(0, 0), image.size], fill = (0,0,0))
		
			currentProgressMs = progressMs + (nowMs - loadMs)
			progress = currentProgressMs / float(durationMs) * 360
			draw.pieslice([0, 0, 32, 32], 0, int(progress), fill=(60,0,0,255))
			draw.arc([0, 0, 32, 32], 0, 360, fill=(120,0,0,255))
			
			draw.text((displayTextScroll, 8), displayText, fill=(200,200,200), font=fontSmall)
			matrix.SetImage(image.im.id, 0, 0)
			displayTextScroll -= 1
			
			if displayTextScroll < -displayTextWidth:
				displayTextScroll = 32
			nowMs = int(round(time.time() * 1000))
			time.sleep(0.05)
			
		

	except Exception as e:
		print e
		time.sleep(60)
		accessToken = Spotify.getAccessToken()	
	


