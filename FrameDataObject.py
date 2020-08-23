#Class that contains all the data from a single frame
import numpy as np

class frameObject:

    def __init__(self, EyeLTopX, EyeLTopY, EyeLBotX, EyeLBotY, EyeLOutX, EyeLOutY, EyeLInX, EyeLInY, EyeRTopX, EyeRTopY, EyeRBotX, EyeRBotY, EyeROutX, EyeROutY, EyeRInX, EyeRInY):
        self.eyeLTopX = EyeLTopX
        self.eyeLTopY = EyeLTopY
        self.eyeLBotX = EyeLBotX
        self.eyeLBotY = EyeLBotY
        self.eyeLOutX = EyeLOutX
        self.eyeLOutY = EyeLOutY
        self.eyeLInX = EyeLInX
        self.eyeLInY = EyeLInY

        self.eyeRTopX = EyeRTopX
        self.eyeRTopY = EyeRTopY
        self.eyeRBotX = EyeRBotX
        self.eyeRBotY = EyeRBotY
        self.eyeROutX = EyeROutX
        self.eyeROutY = EyeROutY
        self.eyeRInX = EyeRInX
        self.eyeRInY = EyeRInY

        self.ifBlink = 0

    #Setter to set the status of if a blink was detected or not
    def set_blink(self, value):
        self.ifBlink = value
    
    #Left eye setters NOT NECCESARY WILL DELETE LATER
    def set_eyeLTopX(self, value):
        self.eyeLTopX = value
    def set_eyeLTopY(self, value):
        self.eyeLTopY = value

    def set_eyeLBotX(self, value):
        self.eyeLBotX = value
    def set_eyeLBotY(self, value):
        self.eyeLBotY = value

    def set_eyeLOutX(self, value):
        self.eyeLOutX = value
    def set_eyeLOutY(self, value):
        self.eyeLOutY = value

    def set_eyeLInX(self, value):
        self.eyeLInX = value
    def set_eyeLInY(self, value):
        self.eyeLInY = value

    #Return the EAR value of the Left eye
    def get_earL(self): 
        eyeLTop = np.array([self.eyeLTopX, self.eyeLTopY])
        eyeLBot = np.array([self.eyeLBotX,self.eyeLBotY])
        distLV = np.linalg.norm(eyeLTop-eyeLBot) 

        eyeLOut = np.array([self.eyeLOutX,self.eyeLOutY])
        eyeLIn = np.array([self.eyeLInX,self.eyeLInY])
        distLH = np.linalg.norm(eyeLOut-eyeLIn) 
        return (distLV / distLH)

    #Return the EAR value of the Right eye
    def get_earR(self): 
        eyeRTop = np.array([self.eyeRTopX, self.eyeRTopY])
        eyeRBot = np.array([self.eyeRBotX,self.eyeRBotY])
        distRV = np.linalg.norm(eyeRTop-eyeRBot) 

        eyeROut = np.array([self.eyeROutX,self.eyeROutY])
        eyeRIn = np.array([self.eyeRInX,self.eyeRInY])
        distRH = np.linalg.norm(eyeROut-eyeRIn) 
        return (distRV / distRH)

    #Return the average EAR value of the face
    def get_earAvg(self):
        earL = self.get_earL()
        earR = self.get_earR()
        return (earL+earR)/2


#Testing

#Brian = frameObject( 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 180, 160)
#print(Brian.eyeLTopY)
#print(Brian.eyeLInX)
#print(Brian.get_earL())
#print("Now for right test")
#print(Brian.eyeRInX)
#print(Brian.eyeRBotY)
#print(Brian.get_earR())
#print((Brian.get_earR()<0.8))
#print("average:")
#print(Brian.get_earAvg())



##NOTES##
#If no value is found for pixel data location --> default to 0 (MUST ADD ERROR CASES[TRY CATCH STATEMENTS, or perhaps a if statement when calculating the attentive lvl])
#Go through the list of objects look at first set of 900 frames (or at least start at frame 1 end at frame 900) 
#or first set of 600 frames
#find number of intervals to run for? (or have a minimum submission length that must be met










