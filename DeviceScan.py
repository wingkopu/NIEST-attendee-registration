#---require pyusb-------
#--http://sourceforge.net/apps/trac/pyusb/---
import usb.core
import os

class DeviceScan:
	devlist={1:False,2:False,4:False}
	
	def check(self):
		#check smart card reader
		#idvendor=0x058f idproduct=0x9540
		dev=usb.core.find(idVendor=0x058f,idProduct=0x9540)
		if dev is not None:
			self.devlist[1]=True

		#check finger print
		#idvendor=0x04d9 idproduct=0x8008
		dev=usb.core.find(idVendor=0x04d9,idProduct=0x8008)
		if dev is not None:	
			self.devlist[2]=True

		#check usb camera
		if os.path.exists('/dev/video0'):
			self.devlist[4]=True


	def __str__(self):
		s=''
		for idx,d in enumerate(self.devlist):
			s+=str(d)
			if self.devlist[d]==True:
				s+='1'
			else:
				s+='0'
		return s
