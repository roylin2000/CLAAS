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

    def if_focus_blink(self):
        x = 0
        EYE_THRESH = 0.3 #0.3 is optimal setting (30fps)
        EYE_CONSEC_FRAME = 2 #3 is optimal setting (30 fps)
        counter = 0

        while x < len(self.l):
            if self.l[x].get_earAvg() < EYE_THRESH:
                counter += 1
            else:
                if counter >= EYE_CONSEC_FRAME:
                    self.l[x].set_blink(1) #Mark the frame that a blink is completed
                    counter = 0
            x += 1

        times = len(self.l) // 20 #number of frames to go through to match 20 second period with 1fps (to convert back to 30 fps, change 30 to 900)

       # mean_data = np.array(mean_data)

        eyeResult = []
        w = 0
        for w in range(times):
            count = 0
            y = 0
            #while (y+20*w) < (20+20*w):
            #while (y) < (20):
            for w in range(len(self.l)):
                count = 3 #MUST BE FIXED
            if count*3 <= 9:
                attention =1
                eyeResult.append(1)
            if (count*3 > 10) and (count*3 <=21):
                attention =0.5
                eyeResult.append(0.5)
            if count*3 > 21:
                attention =0 
                eyeResult.append(0)

        return eyeResult

def sum(lean, headpos, blink):
    '''
    lean: boolean arrays -> 5s intervals
    headpos: boolean arrays -> 10s intervals
    blink: 0, 0.5, 1 array -> 20s intervals
    output: Individual Average Attention Score array
    '''
    lean_weight = 0.3
    headpos_weight = 0.3
    blink_weight = 0.4
    result = [] # should be the same size as lean

    for i in range(len(lean)):
        result.append(lean[i]*lean_weight + headpos[i // 5]*headpos_weight + blink[i // 10]*blink_weight)

    return result



## IMPORT AND TESTING OF A 20 FRAME LONG DATASET ##


objectList = []

a1 = frameObject(629.9,265.5,630.4,287.3,607.3,277.5,656.3,278.5,789.5,263.8,792.8,286.3,816.6,274.4,766.5,280.5,366,366,0.9,-4.1)
objectList.append(a1)

a2 = frameObject(576.2,267.6,576.4,284.7,556.7,276.5,596,277.9,708.6,264,710.4,279.9,728.8,270,692.3,275.3,311,311,-1.2,-5.8)
objectList.append(a2)

a3 = frameObject(612.1,245.6,612.3,264.3,593.2,255.2,632.3,258.5,725.7,245.2,735.9,260.3,750.6,255,719.7,256,292,292,20.4,1.4)
objectList.append(a3)

a4 = frameObject(605.2,298.2,599.9,321.9,574.9,307.5,626.4,315.8,775.1,311.9,777.6,335,805.6,322.1,747.9,325.7,407,407,3.1,-14.2)
objectList.append(a4)

a5 = frameObject(564.6,255.2,566.2,275.2,547.1,271.9,587.4,265.1,712.4,234.8,715.8,255,737.1,245.8,693.8,251.6,335,335,-4.4,8.9)
objectList.append(a5)

a6 = frameObject(516,292.1,519.1,300.6,496.2,304.2,540.1,291.2,664.5,262,666.3,269.9,691.4,261.5,641.4,271.6,361,361,-13.3,-0.4)
objectList.append(a6)

a7 = frameObject(500.2,361.9,504,370.7,476.7,370,527.6,354,659.5,308.3,662.9,317.8,686.8,300.7,632.4,321,359,359,-4.1,-20.8)
objectList.append(a7)

a8 = frameObject(545.4,306,549.5,325.1,522.2,321.5,573.8,311.5,696.9,270.5,703.9,288.2,722.4,276,680.9,288.6,375,375,6.3,-7.8)
objectList.append(a8)

a9 = frameObject(513.9,268.9,515.9,290.9,289.9,283.5,538.8,280.8,678.7,247.3,680.6,266.1,704.8,252.8,653.9,262.1,386,386,-4.6,-15.4)
objectList.append(a9)

a10 = frameObject(610.5,221.7,610,244,586.6,234,637.7,237.9,762.1,220.3,764.7,241.1,783.9,231.7,742.1,236.1,369,369,20.9,-1.5)
objectList.append(a10)

a11 = frameObject(590.7,341.9,590.2,353.8,576.4,349.4,604.6,349.9,684.6,342.8,685.8,354.2,699.2,349.2,670.7,350.4,216,216,-1.5,8.2)
objectList.append(a11)

a12 = frameObject(578.2,362.7,577.5,375.1,562.5,369.8,592.2,370.5,675.7,358,676.4,370.7,690.6,364.4,661.2,368.4,222,222,-2.9,3.9)
objectList.append(a12)

a13 = frameObject(558.3,341.2,559.1,353.6,545,349.8,574.9,347.3,666.2,331.2,668,345.1,682,337.7,651.2,342.5,247,247,-2.2,1.6)
objectList.append(a13)

a14 = frameObject(541.7,301.4,542.8,316.2,524,313,561.4,304.8,666.4,291.2,669,308.1,688.6,297.5,647.3,304.8,288,288,-1.8,-2.8)
objectList.append(a14)

a15 = frameObject(554,300.2,552.5,318.5,530.7,309.1,574,311.6,702.1,291.3,706.7,310.4,726.5,298.5,682.4,306,351,351,-0.6,-8.7)
objectList.append(a15)

a16 = frameObject(531,291.7,532.9,310.1,505.8,305,558.8,302.5,707.5,282,712.3,300.4,736,288.9,686.2,298.5,407,407,-1.4,-8.3)
objectList.append(a16)

a17 = frameObject(517,294.9,518.3,316.2,489.9,309.2,544.9,306.5,697.9,278.4,702.9,301.5,729.1,287.5,670.8,298.5,425,425,-2.4,-8.2)
objectList.append(a17)

a18 = frameObject(459.7,243.8,457.6,270.8,435,259,484.2,263.4,609.2,236.8,609.7,261,636.6,249.1,582.9,254.4,377,377,-30.4,-0.6)
objectList.append(a18)

a19 = frameObject(657.9,287.9,656.3,303.7,631.7,293.3,686.4,297,811.2,287.9,810.9,304.6,833.1,297.2,790.6,296.9,382,382,19.5,-8.4)
objectList.append(a19)

a20 = frameObject(454.8,303.8,458.8,324.7,434.9,318,481.3,311.8,614.1,271.9,619.2,295.1,642.4,279.4,590.2,291,394,394,-15.6,-10.8)
objectList.append(a20)


#print(len(objectList))

frameR = 1
mul = multipleFrames(objectList, frameR)
leanResult = mul.if_focus_lean()
headPosResult = mul.if_focus_headpos()
blinkResult = mul.if_focus_blink()

print(mul.if_focus_lean())
print(mul.if_focus_headpos())
print(mul.if_focus_blink())

print(sum(leanResult, headPosResult, blinkResult))

