import cv2
import numpy as np
import png

from AzureFaceAPI_Basic import getData
from email.mime import image
print(cv2.__version__)
# defining face detector
#face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

#face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

haar_cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
ds_factor=0.6

images = []

data = []


class VideoCamera(object):
    def __init__(self):
       #capturing video
        self.video = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        self.out = cv2.VideoWriter('please.avi', fourcc, 30, (1280,720))
        self.count = 0
       
       
    
    def __del__(self):
        #releasing camera
        self.video.release()

    def get_frame(self):
        #extracting frames
        
        success, image = self.video.read()
        tempImage = image
        fshape = image.shape
        fheight = fshape[0]
        fwidth = fshape[1]
        #print(fwidth , fheight)
        
       # while(self.video.isOpened()):
           
        #   image = cv2.flip(image,0)

        ###self.out.write(image)
        
        

        

        

        if self.count == 200:
            self.out.release();
            self.video.release()
            cv2.destroyAllWindows()

        #   cv2.imshow('frame',image)
        #  if cv2.waitKey(0) & 0xFF == ord('q'):
        #      break


        #tempImage=cv2.resize(tempImage,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)

        #tempFrame = cv2.imread('video', tempImage)
        #tempImages.append(tempFrame)

        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        face_rects=haar_cascade_face.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in face_rects:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            break
        ret, jpeg = cv2.imencode('.jpg', image)

        print(self.count)
        self.count = self.count+1

        if self.count % 30 == 0:
            data.append(getData(image))


        return jpeg.tobytes()





"""   ret, frame = self.video.read()
        frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor,
        interpolation=cv2.INTER_AREA)                    
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        face_rects=haar_cascade_face.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in face_rects:
         cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
         break
        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()"""