import serial,time,sys,ntpath,os,subprocess,threading,binascii,sqlite3
from shutil import *
from zipfile import *
from DeviceScan import *

class Connector:
    inq=""
    state=0
    """
    state 0-1: read pkt start
    state 2: tid
    state 3: cmd
    state 4: length
    state 5: data
    state 6: crc
    """
    bytecount=0
    pktstr=""
    plist={'camera':[],'card':[],'fp':[],'pv':[]}
    
    def __init__(self,port=5,baudrate=115200):
        self.port=port
        self.baudrate=baudrate

    def initiate(self):
        self.serial=serial.Serial(self.port,self.baudrate,timeout=1)
        inq=""

    def Run(self):
        self.processCollector()
        while 1:
            if self.serial.inWaiting()!=0:
                tmp=self.serial.read()
                print str(ord(tmp))+' stat:'+str(self.state)+'\n'

                if self.state==0 and ord(tmp)==0x55:
                    self.state=1
                elif self.state==1 and ord(tmp)==0xAA:
                    self.state=2
                    self.pktstr=""
                    self.bytecount=4
                    self.pkt=Packet()
                elif self.state==2:
                    self.pktstr=self.pktstr+tmp
                    self.bytecount=self.bytecount-1
                    if self.bytecount==0:
                        self.pkt._TID=self.pktstr
                        self.pktstr=""
                        self.bytecount=2
                        self.state=3
                elif self.state==3:
                    self.pktstr=self.pktstr+tmp
                    self.bytecount=self.bytecount-1
                    if self.bytecount==0:
                        self.pkt._CMD=self.pktstr
                        self.pktstr=""
                        self.bytecount=4
                        self.state=4
                elif self.state==4:
                    self.pktstr=self.pktstr+tmp
                    self.bytecount=self.bytecount-1
                    if self.bytecount==0:
                        self.pkt._LENGTH=self.pktstr
                        self.pktstr=""
                        self.bytecount=self.pkt.toInt(self.pkt._LENGTH)
                        if self.bytecount==0:
                            self.state=6
                            self.bytecount=4
                        else:
                            self.state=5
                elif self.state==5:
                    self.pktstr=self.pktstr+tmp
                    self.bytecount=self.bytecount-1

                    cmd=self.pkt.toInt(self.pkt._CMD)
                    if cmd==7 and self.bytecount+20==self.pkt.toInt(self.pkt._LENGTH):
                        self.pkt._DATA=self.pktstr.strip()
                        self.state=10
                        self.pktstr=""
                        f=open(self.pkt._DATA,'wb')
                        
                    elif self.bytecount<=0:
                        self.pkt._DATA=self.pktstr
                        self.state=6
                        self.bytecount=4
                        self.pktstr=""
                elif self.state==6:
                    self.pktstr=self.pktstr+tmp
                    self.bytecount=self.bytecount-1
                    if self.bytecount==0:
                        self.pkt._CRC=self.pktstr
                        self.pktstr=""
                        self.bytecount=0
                        self.state=7
                elif self.state==7 and tmp=='\n':
                    self.state=0
                    self.ExecuteCMD()
                elif self.state==10:#read bianary state
                    f.write(tmp)
                    time.sleep(0.005)
                    self.bytecount-=1
                    if self.bytecount==0:
                       f.close()
                       self.bytecount=4
                       self.state=6
                       
                else:
                    self.state=0
                    self.bytecount=0

    def send(self,packet):
	count=0
	for i in packet:
        	self.serial.write(i)
		#print count
		time.sleep(0.008)
		if count%3072==0:
			time.sleep(0.2)
		count=count+1

    def ExecuteCMD(self):
        cmd=self.pkt.toInt(self.pkt._CMD)
        if cmd==1:
            print "getCitizenID"
            self.plist['card'].append([subprocess.Popen(["python","id.py"],stdout=subprocess.PIPE),self.idCP])
        elif cmd==2:
            print "getImage"
            self.plist['camera'].append([subprocess.Popen(["python","console.py"],stdout=subprocess.PIPE),self.imageCP])
        elif cmd==3:
            print "getDCInfo"
            self.getDCInfo()
        elif cmd==4:
            print "enrollFP"
            self.plist['fp'].append([subprocess.Popen(["./enroll"],stdout=subprocess.PIPE),self.enrollFP])
            #self.enrollFP('')
        elif cmd==5:
            print "verifyFP"
	    self.plist['fp'].append([subprocess.Popen(["./verify",self.pkt._DATA],stdout=subprocess.PIPE),self.verifyFP])
            #self.verifyFP()
        elif cmd==7:
            print "uploadFP"
            self.uploadFP(self.pkt._DATA)
            
        elif cmd==14:
            print "cancel"
            for i in self.plist:
                for j in self.plist[i]:
                    p,f=j
                    p.terminate()

    def processCollector(self):
        self.time=threading.Timer(5,self.processCollector)
        for i in self.plist:
            for j in self.plist[i]:
                p,f=j
                if p.poll()!=None:
                    f(p.communicate()[0])
                    self.plist[i].remove(j)
	self.time.start()

    def close(self):
        self.time.cancel()
        self.serial.close()

    def imageCP(self,filename):
	filename=filename.strip(' \t\n\r')
        fs=0
        
        if len(filename)>0:
            fs=os.stat(filename).st_size

        with open(filename,'rb') as fi:
            content=fi.read()
        
        p=Packet()
        tid=self.pkt.toInt(self.pkt._TID)+1
        p._TID=p._TID+chr((tid>>24)&0b11111111)
        p._TID=p._TID+chr((tid>>16)&0b11111111)
        p._TID=p._TID+chr((tid>>8)&0b11111111)
        p._TID=p._TID+chr((tid)&0b11111111)
        cmd=2
        p._CMD=p._CMD+chr((cmd>>8)&0b11111111)
        p._CMD=p._CMD+chr((cmd)&0b11111111)
        length=fs
        p._LENGTH=p._LENGTH+chr((length>>24)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length>>16)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length>>8)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length)&0b11111111)

        p._DATA=content

        p.computeCRC()

        pkt=p.pack()

        self.send(pkt)

    def idCP(self,cid):
        p=Packet()
        tid=self.pkt.toInt(self.pkt._TID)+1
        p._TID=p._TID+chr((tid>>24)&0b11111111)
        p._TID=p._TID+chr((tid>>16)&0b11111111)
        p._TID=p._TID+chr((tid>>8)&0b11111111)
        p._TID=p._TID+chr((tid)&0b11111111)
        cmd=1
        p._CMD=p._CMD+chr((cmd>>8)&0b11111111)
        p._CMD=p._CMD+chr((cmd)&0b11111111)
        length=13
        p._LENGTH=p._LENGTH+chr((length>>24)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length>>16)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length>>8)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length)&0b11111111)

        p._DATA=cid

        p.computeCRC()

        pkt=p.pack()

        self.send(pkt)

    def uploadFP(self,filename):
        #result=os.system("unzip -u -qq "+filename+" -d db")
        z=ZipFile(filename)
        numberofrow=len(z.filelist)
        z.extractall('db/')

        p=Packet()
        tid=self.pkt.toInt(self.pkt._TID)+1
        p._TID+=chr((tid>>24)&0b11111111)
        p._TID+=chr((tid>>16)&0b11111111)
        p._TID+=chr((tid>>8)&0b11111111)
        p._TID+=chr((tid)&0b11111111)
        cmd=7
        p._CMD=p._CMD+chr((cmd>>8)&0b11111111)
        p._CMD=p._CMD+chr((cmd)&0b11111111)
        length=2
        p._LENGTH=p._LENGTH+chr((length>>24)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length>>16)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length>>8)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length)&0b11111111)

        p._DATA=p._DATA+chr((numberofrow>>8)&0b11111111)
        p._DATA=p._DATA+chr((numberofrow)&0b11111111)

        p.computeCRC()

        pkt=p.pack()

        self.send(pkt)

    def enrollFP(self,filename):

        #timetoretry=20

        #fps=FPS('/dev/ttyUSB1',9600)
        #fps.initiate()

        #ChangeBaudrate(fps)

        #fps.close()

        #fps.baudrate=115200
        #fps.initiate()

        #print 'open'
        #result=OpenCMD(fps)
        #print 'enroll start'
        #EnrollStart(fps,-1)
        #print 'turn on cmos'
        #CMOSLED(fps,1)

        #print 'try to get'

        #count=0
        #while IsPressFinger(fps)!=0:
        #    time.sleep(0.5)
        #    count+=1
        #    if count>timetoretry:
        #        break
        #result=CaptureFinger(fps,1)
        #result=Enroll1(fps)

        #count=0
        #while IsPressFinger(fps)!=0:
        #    time.sleep(0.5)
        #    count+=1
        #    if count>timetoretry:
        #        break
        #result=CaptureFinger(fps,1)
        #result=Enroll2(fps)

        #count=0
        #while IsPressFinger(fps)!=0:
        #    time.sleep(0.5)
        #    count+=1
        #    if count>timetoretry:
        #        break
        #result=CaptureFinger(fps,1)
        #finger=Enroll3(fps,1)

        #rawimage=GetRawImage(fps)

        #print len(rawimage)

        #CMOSLED(fps,0)

        #result=CloseCMD(fps)

        #ChangeBaudrate(fps,9600)

        #fps.close()

        #content=chr(0)+finger


        filename=filename.strip(' \t\n\r')
	print filename
	[status,fp]=filename.split(',')
        if os.path.exists(fp):
            with open(fp,'rb') as fi:
                content=fi.read()
            content=chr(int(status))+content
        else:
            content=chr(int(status))

        p=Packet()
        tid=self.pkt.toInt(self.pkt._TID)+1
        p._TID+=chr((tid>>24)&0b11111111)
        p._TID+=chr((tid>>16)&0b11111111)
        p._TID+=chr((tid>>8)&0b11111111)
        p._TID+=chr((tid)&0b11111111)
        cmd=4
        p._CMD=p._CMD+chr((cmd>>8)&0b11111111)
        p._CMD=p._CMD+chr((cmd)&0b11111111)
        length=499
        p._LENGTH=p._LENGTH+chr((length>>24)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length>>16)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length>>8)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length)&0b11111111)

        p._DATA=content

        p.computeCRC()

        pkt=p.pack()

        self.send(pkt)

    def verifyFP(self,result):
	if result=="p":
		r=0
	else:
		r=1
	p=Packet()
	tid=self.pkt.toInt(self.pkt._TID)+1
	
        p._TID+=chr((tid>>24)&0b11111111)
        p._TID+=chr((tid>>16)&0b11111111)
        p._TID+=chr((tid>>8)&0b11111111)
        p._TID+=chr((tid)&0b11111111)
	cmd=5
        p._CMD=p._CMD+chr((cmd>>8)&0b11111111)
        p._CMD=p._CMD+chr((cmd)&0b11111111)
        length=1
        p._LENGTH=p._LENGTH+chr((length>>24)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length>>16)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length>>8)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length)&0b11111111)

        p._DATA=chr(r)

        p.computeCRC()

        pkt=p.pack()

        self.send(pkt)

    def getDCInfo(self):
        ds=DeviceScan()
        ds.check()
        result=str(ds)

        p=Packet()
        tid=self.pkt.toInt(self.pkt._TID)+1

        p._TID+=chr((tid>>24)&0b11111111)
        p._TID+=chr((tid>>16)&0b11111111)
        p._TID+=chr((tid>>8)&0b11111111)
        p._TID+=chr((tid)&0b11111111)
	cmd=3
        p._CMD=p._CMD+chr((cmd>>8)&0b11111111)
        p._CMD=p._CMD+chr((cmd)&0b11111111)
        length=6
        p._LENGTH=p._LENGTH+chr((length>>24)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length>>16)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length>>8)&0b11111111)
        p._LENGTH=p._LENGTH+chr((length)&0b11111111)

        p._DATA=result

        p.computeCRC()

        pkt=p.pack()

        self.send(pkt)

class Packet:
    _TID=""
    _CMD=""
    _LENGTH=""
    _DATA=""
    _CRC=""

    def computeCRC(self):
        result=binascii.crc32(self._TID+self._CMD+self._LENGTH+self._DATA)
        self._CRC=""
        self._CRC=self._CRC+chr((result>>24)&0b11111111)
        self._CRC=self._CRC+chr((result>>16)&0b11111111)
        self._CRC=self._CRC+chr((result>>8)&0b11111111)
        self._CRC=self._CRC+chr((result)&0b11111111)
        return self._CRC

    def toInt(self,data):
        leng=len(data)
        result=0
        for i in range(leng):
            result=result+(ord(data[i])<<8*(leng-1-i))
        return result

    def pack(self):
        result=""
        result=chr(0x55)+chr(0xAA)
        result=result+self._TID+self._CMD+self._LENGTH+self._DATA+self._CRC+'\n'
        
        return result

    def toByte(self,data,size):
        result=""
        for i in range(size):
            result+=chr((data>>8*(size-i-1))&0b11111111)
        return result

test=Connector('/dev/ttyUSB0',115200)
test.initiate()
test.Run()
test.close()
