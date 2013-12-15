import numpy as np
import cv2

def shot(img):
        w=160
        h=240
        nob=8
        channel=3
        nimg=cv2.cv.CreateImage((w,h),nob,channel)
        cv2.cv.Resize(cv2.cv.fromarray(img),nimg,cv2.INTER_LINEAR)
        cv2.cv.SaveImage('outfile.jpg',nimg)
        print 'outfile.jpg'

cap = cv2.VideoCapture(0)
cv2.namedWindow('frame',cv2.cv.CV_WINDOW_NORMAL)
cv2.setWindowProperty('frame',cv2.WND_PROP_FULLSCREEN,cv2.cv.CV_WINDOW_FULLSCREEN)

if cap.isOpened()==True:

        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()

            if ret==False:
                    continue
                # Our operations on the frame come here
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #image size
            #print cv2.cv.GetSize(cv2.cv.fromarray(frame))
            # Display the resulting frame
            frame[0:480,0:160]=np.array([0,0,0])
            frame[0:480,480:640]=np.array([0,0,0])
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == 0x8D:#ord('q'):
                shot(frame[0:480,160:480])
                break
else:
        print 'camera close'
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
