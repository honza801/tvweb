"""
Interface for controlling tv
"""

# Import CherryPy global namespace
import cherrypy
import time
from genshi.template import TemplateLoader
import tv_controller

class TvWeb:
	# constructor
	def __init__(self):
		self.mpc = tv_controller.MplayerController()
		self.vol = tv_controller.VolumeController()
		self.lastplayed = 'Unknown'

	# main page
	def index(self):
		tmpl = loader.load('choose.html')
		stream = tmpl.generate(title="TV Station Web Interface!", channels=self.mpc.getchannels(), lastplayed=self.lastplayed)
		return stream.render('html', doctype='html')
	
	index.exposed = True

	# changes channel
	def changechannel(self, channel=None):
		if cherrypy.request.method == 'POST':
			if channel : 
				self.lastplayed = channel
				self.mpc.play(channel)
				time.sleep(2)
			raise cherrypy.HTTPRedirect('/tvweb')
		return "POST request expected, but "+cherrypy.request.method+" arrived!"

	changechannel.exposed = True

	# stops playing
	def stopplaying(self):
		if cherrypy.request.method == 'POST':
			self.lastplayed = 'Stopped'
			self.mpc.kill()
			raise cherrypy.HTTPRedirect('/tvweb')
		return "POST request expected, but "+cherrypy.request.method+" arrived!"

	stopplaying.exposed = True

	# volume up
	def volup(self):
		if cherrypy.request.method == 'POST':
			self.vol.volup()
			raise cherrypy.HTTPRedirect('/tvweb')
		return "POST request expected, but "+cherrypy.request.method+" arrived!"

	volup.exposed = True

	# volume down
	def voldown(self):
		if cherrypy.request.method == 'POST':
			self.vol.voldown()
			raise cherrypy.HTTPRedirect('/tvweb')
		return "POST request expected, but "+cherrypy.request.method+" arrived!"

	voldown.exposed = True

	# default function
	def default(self, *another): 
		raise cherrypy.HTTPRedirect('/tvweb')
	
	default.exposed = True


class Prefix:
	tvweb = TvWeb()
	
import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')

loader = TemplateLoader('templates', auto_reload=True)
	
if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(HelloWorld(), config=tutconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(Prefix(), config=tutconf)

