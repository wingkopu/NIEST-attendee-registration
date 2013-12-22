import serial,time,sys,ntpath,os,binascii

class Connector:
    inq=""
    pkgheader=[2,4,2,4]
    count=0
    leng=0
    
    def __init__(self,port=5,baudrate=115200):
        self.port=port
        self.baudrate=baudrate

    def initiate(self):
        self.serial=serial.Serial(self.port,self.baudrate,timeout=1)
        inq=""

    def Run(self):
        
        while 1:
            if self.serial.inWaiting()!=0:
                tmp=self.serial.read()
                
                print ord(tmp)
        
        

    def close(self):
        #self.send('q')
        self.serial.close()

    def send(self,msg):
        self.serial.write(msg)

with open('20131215180343.zip','rb') as fi:
        content=fi.read()

head=chr(85)+chr(170)
tid=chr(0)+chr(0)+chr(0)+chr(0)
cmd=chr(0)+chr(4)
data="1111111111111"

leng=len(data)
length=""
length+=chr((leng>>24)&0b11111111)
length+=chr((leng>>16)&0b11111111)
length+=chr((leng>>8)&0b11111111)
length+=chr((leng)&0b11111111)

crc=binascii.crc32(tid+cmd+length+data)
crc1=chr((crc>>24)&0b11111111)
crc2=chr((crc>>16)&0b11111111)
crc3=chr((crc>>8)&0b11111111)
crc4=chr((crc)&0b11111111)

pend='\n'

test=Connector(4,115200)
test.initiate()
test.send(head+tid+cmd+length+data+crc1+crc2+crc3+crc4+pend)
test.Run()
test.close()
quit()

