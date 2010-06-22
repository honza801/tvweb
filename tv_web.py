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
		self.mpc = tv_controller.VideoController()
		self.vol = tv_controller.VolumeController('PCM')
		self.monitor = tv_controller.MonitorController()
		self.lastplayed = 'Unknown'
		self.lastip = "Unknown"

	# main page
	def index(self):
		if not self.hostallowed(): return "You are not alowed."
		tmpl = loader.load('tvweb.html')
		stream = tmpl.generate(
			title="TV Station Web Interface!", 
			channels=self.mpc.getchannels(), 
			lastplayed=self.lastplayed, 
			curvolume=self.vol.getvolume()[0],
			lastip=self.lastip)
		return stream.render('html', doctype='html')
	
	index.exposed = True

	# changes channel
	def changechannel(self, channel=None):
		if not self.hostallowed(): return "You are not alowed."
		if cherrypy.request.method == 'POST':
			if channel : 
				self.lastplayed = channel
				self.lastip = cherrypy.request.remote.ip
				self.mpc.play(channel)
				time.sleep(2)
			raise cherrypy.HTTPRedirect('/tvweb')
		return "POST request expected, but "+cherrypy.request.method+" arrived!"

	changechannel.exposed = True

	# stops playing
	def stopplaying(self):
		if not self.hostallowed(): return "You are not alowed."
		if cherrypy.request.method == 'POST':
			self.lastplayed = 'Stopped'
			self.lastip = cherrypy.request.remote.ip
			self.mpc.kill()
			raise cherrypy.HTTPRedirect('/tvweb')
		return "POST request expected, but "+cherrypy.request.method+" arrived!"

	stopplaying.exposed = True

	# volume up
	def volup(self):
		if not self.hostallowed(): return "You are not alowed."
		if cherrypy.request.method == 'POST':
			self.vol.volup()
			raise cherrypy.HTTPRedirect('/tvweb')
		return "POST request expected, but "+cherrypy.request.method+" arrived!"

	volup.exposed = True

	# volume down
	def voldown(self):
		if not self.hostallowed(): return "You are not alowed."
		if cherrypy.request.method == 'POST':
			self.vol.voldown()
			raise cherrypy.HTTPRedirect('/tvweb')
		return "POST request expected, but "+cherrypy.request.method+" arrived!"

	voldown.exposed = True

	# monitor turn on
	def monitoron(self):
		if not self.hostallowed(): return "You are not alowed."
		if cherrypy.request.method == 'POST':
			self.monitor.turnon()
			raise cherrypy.HTTPRedirect('/tvweb')
		return "POST request expected, but "+cherrypy.request.method+" arrived!"

	monitoron.exposed = True

	# monitor turn off
	def monitoroff(self):
		if not self.hostallowed(): return "You are not alowed."
		if cherrypy.request.method == 'POST':
			self.monitor.turnoff()
			raise cherrypy.HTTPRedirect('/tvweb')
		return "POST request expected, but "+cherrypy.request.method+" arrived!"

	monitoroff.exposed = True
	
	def test(self):
		return "test ok."

	test.exposed = True

	# default function
	def default(self, *another): 
		raise cherrypy.HTTPRedirect('/tvweb')
	
	default.exposed = True
	
	# checks allowed hosts
	def hostallowed(self):
		allowed = [ '128.10.20.5' , '10.10.60.13' ]
		hostip = cherrypy.request.remote.ip
		if hostip in allowed:
			return True
		return False


class Prefix:
	tvweb = TvWeb()
	
import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'cherryd-tvweb.conf')

loader = TemplateLoader('templates', auto_reload=True)
	
if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(HelloWorld(), config=tutconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(Prefix(), config=tutconf)

