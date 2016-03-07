#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import sl
from sl import SlData
from string import Template
import Image
import ImageDraw
import ImageFont
import time
from rgbmatrix import Adafruit_RGBmatrix

matrix = Adafruit_RGBmatrix(32, 1)
image = Image.new("RGB", (32, 32), "black")
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
			width, ignore = fontSmall.getsize('Ingen')
			draw.text((16-width/2, 8), 'Ingen', fill=(255,255,0), font=fontSmall)
		else:
			print bus['LineNumber'] + ' ' + bus['DisplayTime'] 
			width, ignore = fontBig.getsize(bus['LineNumber'])
			draw.text((16-width/2, 0), bus['LineNumber'], fill=(255,0,0), font=fontBig)
			width, ignore = fontSmall.getsize(bus['DisplayTime'])
			draw.text((16-width/2, 16), bus['DisplayTime'], fill=(0,255,0), font=fontSmall)

		matrix.Clear()
		matrix.SetImage(image.im.id, 0, 0)
		time.sleep(30)
	except ValueError:
		print ' Failed to get data from SL'
		time.sleep(15)
	
	


