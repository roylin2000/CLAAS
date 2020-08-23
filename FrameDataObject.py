#Class that contains all the data from a single frame
import numpy as np

class frameObject:

    def __init__(self, EyeLTopX, EyeLTopY, EyeLBotX, EyeLBotY, EyeLOutX, EyeLOutY, EyeLInX, EyeLInY, EyeRTopX, EyeRTopY, 
                 EyeRBotX, EyeRBotY, EyeROutX, EyeROutY, EyeRInX, EyeRInY, height, width, yaw, pitch):
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

        self.height = height
        self.width = width # in pixels
        self.yaw = yaw # left and right head movement, +ve left, -ve right
        self.pitch = pitch # up and down, +ve up, -ve down

        self.ifBlink = 0

    #Setter to set the status of if a blink was detected or not
    def set_blink(self, value):
        self.ifBlink = value
    
    
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



    #Body/Face Methods
    def get_area(self):
        return self.height * self.width

    def if_tilt_LR(self, threshold):
        '''
        determine if head is tilted towards left or right, returns True if the head is tilted
        threshold = degree to determine tilt
        '''
        return abs(self.yaw) > threshold

    def if_tilt_UD(self, threshold):
        '''
        determine if head is tilted towards up or down, returns True if the head is tilted
        threshold = degree to determine tilt
        '''
        return abs(self.pitch) > threshold


class multipleFrames:
    def __init__(self, l, frameR):
        self.l = l # list of Face API objects
        self.frameR = frameR # frame rate

    def if_lean(self, interval):
        '''
        interval = list of frameObjects in an interval of 5s, len = frameR * 5
        leaning forward iff face area is becoming bigger
        :return: True if leaning forward for more than 4s worth of frames within each 5s period (80%)
                False otherwise
        '''
        dL = [x.get_area() - interval[i - 1].get_area() for i, x in enumerate(interval)][1:] # difference list
        pos = [n for n in dL if n >= 0]
        pos_count = len(pos) # number of frames head is becoming bigger -> leaning forward -> focused

        return pos_count >= len(interval) * 0.8 # True (focused) if in more than 80% of the frames, head size increases

    def if_headpos(self, interval):
        '''
        interval = list of frameObjects in an interval of 10s, len = frameR * 10
        head is not oriented towards the screen if more than 60% of frames (6s) yaw or pitch is over threshold
        :return: True if head is oriented towards the screen -> focused
                False otherwise -> unfocused
        '''
        over_yaw = [n for n in interval if n.if_tilt_LR]
        over_pitch = [n for n in interval if n.if_tilt_UD]
        return len(over_yaw) <= 0.6 * len(interval) or len(over_pitch) <= 0.6 * len(interval)

    def if_focus_lean(self):
        '''
        divide l into 5s intervals and output attention classification based on lean
        '''
        size = 5 * frameR
        result = [] # result list containing 1 -> focused; 0 -> unfocused

        if len(self.l) // size == len(self.l) / size:
            for i in range(len(self.l) // size):
                result.append(self.if_lean(self.l[size * i: size * i + size]))
        else:
            for i in range(len(self.l) // size + 1):
                if i <= len(self.l) // size:
                    result.append(self.if_lean(self.l[size * i: size * i + size]))
                else:
                    result.append(self.if_lean(self.l[size * i:len(self.l)]))

        return result

    def if_focus_headpos(self):
        '''
        divide l into 10s intervals and output attention classification based on headPose
        '''
        size = 10 * frameR
        result = []  # result list containing 1 -> focused; 0 -> unfocused

        if len(self.l) // size == len(self.l) / size:
            for i in range(len(self.l) // size):
                result.append(self.if_headpos(self.l[size * i: size * i + size]))
        else:
            for i in range(len(self.l) // size + 1):
                if i <= len(self.l) // size:
                    result.append(self.if_headpos(self.l[size * i: size * i + size]))
                else:
                    result.append(self.if_headpos(self.l[size * i:len(self.l)]))

        return result




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










