from FP import *

timetoretry=20

fps=FPS('/dev/ttyUSB1',9600)
fps.initiate()

#print 'open'
result=OpenCMD(fps)
#print 'enroll start'
EnrollStart(fps,-1)
#print 'turn on cmos'
CMOSLED(fps,1)

#print 'try to get'

count=0
while IsPressFinger(fps)!=0:
    time.sleep(0.5)
    count+=1
    if count>timetoretry:
        break
result=CaptureFinger(fps,1)
result=Enroll1(fps)

count=0
while IsPressFinger(fps)!=0:
    time.sleep(0.5)
    count+=1
    if count>timetoretry:
        break
result=CaptureFinger(fps,1)
result=Enroll2(fps)

count=0
while IsPressFinger(fps)!=0:
    time.sleep(0.5)
    count+=1
    if count>timetoretry:
        break
result=CaptureFinger(fps,1)
finger=Enroll3(fps,1)

#rawimage=GetRawImage(fps)

#print len(rawimage)

CMOSLED(fps,0)

result=CloseCMD(fps)
#fps.close()

efilename='temp/enrolltemplate'
f=open(efilename,'wb')
for b in finger:
    f.write(b)
f.close()

rfilename='temp/rawimage'
#f=open(rfilename,'wb')
#for b in rawimage:
#    f.write(b)
#f.close()

print efilename+','+rfilename
quit()

