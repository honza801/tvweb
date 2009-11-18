#!/usr/bin/python

import os
import string
import signal
import alsaaudio

class MplayerController:
	
	def __init__(self):
		self.vars = "XAUTHORITY=/home/honza801/.Xauthority DISPLAY=:0.0"

	def is_running(self):
		process = os.popen('pgrep mplayer').readline()
		if process != "":
			return int(string.strip(process))
		return -1

	def getchannels(self):
		process = os.popen('tv lschan').readline()
		if process != "":
			channels = map(string.strip, process.split(","))
			return channels
		return -1
	
	def kill(self):
		pid = self.is_running()
		if pid < 0:
			print "PID < 0"
			return
		else:
			print "Sending SIGTERM to", pid
			os.kill(pid,signal.SIGTERM)

	def play(self, channel):
		pid = self.is_running()
		if pid > 0:
			print "Another mplayer is running with pid", pid
			return
		else:
			ret = os.system(self.vars+" tv "+channel+" >/dev/null 2>&1 &")
			print ret


class VolumeController:

	def __init__(self, mixdevice='Master'):
		self.mixdevice = alsaaudio.Mixer(mixdevice)

	def getvolume(self):
		return self.mixdevice.getvolume()
	
	def volup(self):
		newvol = self.mixdevice.getvolume()+10
		if newvol > 100:
			newvol = 100
		self.mixdevice.setvolume(newvol)
	
	def voldown(self):
		newvol = self.mixdevice.getvolume()-10
		if newvol < 0:
			newvol = 0
		self.mixdevice.setvolume(newvol)


if __name__ == "__main__":
	mpc = MplayerController()
	mpc.play("ct1")

