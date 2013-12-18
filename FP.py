import serial,time
from Define import *

class FPS:
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
    
    def __init__(self,port=5,baudrate=115200):
        self.port=port
        self.baudrate=baudrate

    def initiate(self):
        self.serial=serial.Serial(self.port,self.baudrate,timeout=1)
        inq=""

    def readAck(self):
        p=RespPacket()
        count=0
        while 1:
            if self.serial.inWaiting()!=0:
                tmp=self.serial.read()
                p.packet+=tmp
                count+=1
                #print 'rd '+str(hex(ord(tmp)))
                if count==12:
                    break
        p.decode()
        return p

    def readData(self,datatype):
        p=DataPacket()
        count=0
        while 1:
            if self.serial.inWaiting()!=0:
                tmp=self.serial.read()
                p.packet+=tmp
                count+=1
                #if count%3072==0:
                #fi=open('log','w+')
                #fi.write(str(count)+':rd '+str(hex(ord(tmp))))
                #fi.close()
                if count==datatype+6:
                    break
        p.decode(datatype)
        return p

    def sendCMD(self,param,cmd):
        p=CMDPacket()
        p._DeviceID=chr(1)+chr(0)
        p._Param=Convert.toByte(param,4)
        p._CMD=Convert.toByte(cmd,2)
        p.checksum()
        
        pkt=p.pack()
        for c in pkt:
            #print 's '+str(hex(ord(c)))
            self.serial.write(c)

    def sendData(self,data):
        p=DataPacket()
        p._DeviceID=chr(1)+chr(0)
        p._Data=data
        p.checksum()
        
        pkt=p.pack()
        for c in pkt:
            print c
            self.serial.flush()
            self.serial.write(c)
    
    def close(self):
        self.serial.close()

class Packet:
    _DeviceID=""
    _Param=""
    _CHECKSUM=""

    packet=""
    
    def pack(self):
        result=""
        result=chr(0x55)+chr(0xAA)
        result+=self._DeviceID+self._Param+self.CHECKSUM
        return result

class CMDPacket(Packet):
    _CMD=""

    def checksum(self):
        data=chr(0x55)+chr(0xAA)+self._DeviceID+self._Param+self._CMD
        cs=0
        for i in data:
            cs+=ord(i)
        self._CHECKSUM=Convert.toByte(cs,2)

    def pack(self):
        return chr(0x55)+chr(0xAA)+self._DeviceID+self._Param+self._CMD+self._CHECKSUM

class RespPacket(Packet):
    _Resp=""

    packet=""
    offset=[0,1,2,4,8,10]
    size=[1,1,2,4,2,2]

    def checksum(self):
        data=chr(0x55)+chr(0xAA)+self._DeviceID+self._Param+self._Resp
        cs=0
        for i in data:
            cs+=ord(i)
        self._CHECKSUM=Convert.toByte(cs,2)

    def decode(self):
        self._Device=self.packet[2:4]
        self._Param=self.packet[4:8]
        self._Resp=self.packet[8:10]
        self._CHECKSUM=self.packet[10:12]
        
        
    def pack(self):
        return chr(0x55)+chr(0xAA)+self._DeviceID+self._Param+self._Resp+self._CHECKSUM

class DataPacket(Packet):
    _Data=""

    packet=""

    def checksum(self):
        data=chr(0x5A)+chr(0xA5)+self._DeviceID+self._Data
        cs=0
        for i in data:
            cs+=ord(i)
        self._CHECKSUM=Convert.toByte(cs,2)

    def decode(self,datatype):
        self._Device=self.packet[2:4]
        self._Data=self.packet[4:datatype+4]
        self._CHECKSUM=self.packet[datatype+14:datatype+16]
        
        
    def pack(self):
        return chr(0x5A)+chr(0xA5)+self._DeviceID+self._Data+self._CHECKSUM

def OpenCMD(fps,getinfo=False):
    if not getinfo:
        fps.sendCMD(0,0x01)
        result=fps.readAck()
        return result._Param
    else:
        fps.sendCMD(1,0x01)
        result=fps.readAck()
        result=fps.readData(DataType.DEVINFO)
        return DevInfoDescription(result._Data)

def CloseCMD(fps):
    fps.sendCMD(0,0x02)
    result=fps.readAck()
    return result._Param

def EnrollStart(fps,ID=-1):
    fps.sendCMD(ID,0x22)
    result=fps.readAck()
    if result._Resp==DataType.ACK:
        #print 'started'
        return 0
    else:
        #print 'start fail'
        return 1

def CaptureFinger(fps,quality=0):
    fps.sendCMD(quality,0x60)
    result=fps.readAck()
    if result._Resp==DataType.ACK:
        #print 'OK'
        return 0
    else:
        #print 'Finger is not pressed'
        return 1

def IsPressFinger(fps):
    fps.sendCMD(0,0x26)
    result=fps.readAck()
    return Convert.toInt(result._Param)#0-Valid;nonzero-invalid    

def CMOSLED(fps,s):
    fps.sendCMD(s,0x12)
    result=fps.readAck()

def Enroll1(fps):
    fps.sendCMD(0,0x23)
    result=fps.readAck()
    return Convert.toInt(result._Resp)

def Enroll2(fps):
    fps.sendCMD(0,0x24)
    result=fps.readAck()
    return Convert.toInt(result._Resp)

def Enroll3(fps,r):
    fps.sendCMD(0,0x25)
    result=fps.readAck()
    ack=Convert.toInt(result._Resp)
    if r==1:
        result=fps.readData(DataType.TEMPLATESIZE)
        return result._Data
    else:
        return ack

def GetImage(fps):
    fps.sendCMD(0,0x62)
    result=fps.readAck()
    if result._Resp==DataType.ACK:
        result=fps.readData(DataType.RAWIMAGESIZE)
        return result._Data
    else:
        return Convert.toInt(result._Resp)

def ChangeBaudrate(fps,rate=115200):
    fps.sendCMD(rate,0x04)
    result=fps.readAck()

def SetTemplate(fps,ID,template):
    fps.sendCMD(ID,0x71)
    result=fps.readAck()
    print Convert.toInt(result._Param)
    fps.sendData(template)
    result=fps.readAck()
    return Convert.toInt(result._Param)

def Verify(fps,ID):
    fps.sendCMD(ID,0x50)
    result=fps.readAck()
    return Convert.toInt(result._Param)

def DeleteID(fps,ID):
    fps.sendCMD(ID,0x40)
    result=fps.readAck()
    return Convert.toInt(result._Param)

def DeleteAll(fps):
    fps.sendCMD(0,0x41)
    result=fps.readAck()
    return Convert.toInt(result._Resp)

##timetoretry=20
##
##test=FPS(8,9600)
##test.initiate()
###test.sendCMD(1,0x01)
###result=test.readAck()
###result=test.readData(DataType.DEVINFO)
##
##print 'open'
##result=OpenCMD(test)
##print 'enroll start'
##EnrollStart(test,-1)
##print 'turn on cmos'
##CMOSLED(test,1)
##
##print 'try to get'
##count=0
##while IsPressFinger(test)!=0:
##    time.sleep(0.5)
##    count+=1
##    if count>timetoretry:
##        break
##result=CaptureFinger(test)
##result=Enroll1(test)
##count=0
##while IsPressFinger(test)!=0:
##    time.sleep(0.5)
##    count+=1
##    if count>timetoretry:
##        break
##result=CaptureFinger(test)
##result=Enroll2(test)
##count=0
##while IsPressFinger(test)!=0:
##    time.sleep(0.5)
##    count+=1
##    if count>timetoretry:
##        break
##result=CaptureFinger(test)
##finger=Enroll3(test,1)
##CMOSLED(test,0)
##
##print 'end'
##result=CloseCMD(test)
##test.close()
