
import os
import string
import signal
import alsaaudio

class VideoController:
	
	def __init__(self):
		pass

	def is_running(self):
		process = os.popen('pgrep vlc').readline()
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

	def play_tv(self, channel):
		pid = self.is_running()
		if pid > 0:
			print "Another mplayer is running with pid", pid
			return
		else:
			q = "tmux neww '/home/honza801/bin/tv "+channel+"'"
			ret = os.system(q)
			print q, ret
	
	def play(self, file):
		if not os.path.isfile(file):
			return
		pid = self.is_running()
		if pid > 0:
			print "Another mplayer is running with pid", pid
			return
		else:
			q = "tmux neww '/home/honza801/bin/tv \""+file+"\"'"
			ret = os.system(q)
			print q, ret


class VolumeController:

	def __init__(self, mixdevice='Master'):
		self.mixdevice = alsaaudio.Mixer(mixdevice)

	def getvolume(self):
		return self.mixdevice.getvolume()
	
	def volup(self):
		newvol = int(self.mixdevice.getvolume()[0])+10
		if newvol > 100:
			newvol = 100
		self.mixdevice.setvolume(newvol)
	
	def voldown(self):
		newvol = int(self.mixdevice.getvolume()[0])-10
		if newvol < 0:
			newvol = 0
		self.mixdevice.setvolume(newvol)

class MonitorController:
	
	def turnon(self):
		ret = os.system("m on")
		return ret

	def turnoff(self):
		ret = os.system("m off")
		return ret


if __name__ == "__main__":
	mpc = VideoController()
	mpc.play_tv("ct1")

