from FP import *

cid='1100200773078'

try:
    with open('db/'+cid+'.txt','rb') as fi:
        data=fi.read()
    cidr=data[0:13]
    template=data[13:511]
except Exception,e:
    print e.message
    exit(1)
print cidr
fps=FPS(4,9600)
fps.initiate()

ChangeBaudrate(fps)

fps.close()

fps.baudrate=115200
fps.initiate()

print 'del'
result=DeleteID(fps,1)
print result
print 'set'
result=SetTemplate(fps,1,template)
print result

print 'openled'
CMOSLED(fps,1)
print 'verify'
count=0
while IsPressFinger(fps)!=0:
    time.sleep(0.5)
    count+=1
    if count>20:
        break
    
CaptureFinger(fps)
result=Verify(fps,1)
print result
print 'closeled'
CMOSLED(fps,0)

ChangeBaudrate(fps,9600)
fps.close()
