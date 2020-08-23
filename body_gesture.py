# use FaceRectangle: marks the size of the face
# use headPose: yaw, pitch

# continuous frames
# if size increases -> learning forward -> focused
# if size decreases -> learning backward -> unfocused

class frameObject:
    def __init__(self, height, width, yaw, pitch):
        self.height = height
        self.width = width # in pixels
        self.yaw = yaw # left and right head movement, +ve left, -ve right
        self.pitch = pitch # up and down, +ve up, -ve down

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

if __name__ == "__main__":
    frame_1 = frameObject(150, 50, -35, 4)
    threshold_LR = 30
    threshold_UD = 40

    print(frame_1.get_area())
    print(frame_1.if_tilt_LR(threshold_LR)) # True
    print(frame_1.if_tilt_UD(threshold_UD)) # False

    parameters = [[150, 50, -35, 4],
                  [160, 60, -40, 4],
                  [161, 61, -40, 5],
                  [162, 62, -30, 5],
                  [162, 62, -31, 10],

                  [161, 61, -40, 5],
                  [161, 61, -40, 5],
                  [170, 62, -20, 4],
                  [170, 63, -30, 4],
                  [170, 64, -30, -5],

                  [175, 65, -30, -10],
                  [170, 55, -35, -40],
                  [168, 54, -40, -45]
                  ]

    frameL = [frameObject(x[0], x[1], x[2], x[3]) for x in parameters]
    frameR = 1 # set to 1 frame/s for testing purposes
    mul = multipleFrames(frameL, frameR)

    print(mul.if_lean(frameL)) # head is leaning forward -> True
    print(mul.if_headpos(frameL)) # head is always shifted to the left -> False

    print(mul.if_focus_lean())
    print(mul.if_focus_headpos())
