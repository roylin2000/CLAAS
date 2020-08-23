
#this is the code to process all the results of the final computation and create a database of attention averages


#Eyeblinking
#All this currently assumes 1 frame per second due to restrictions


x = 0

EYE_THRESH = 0.3
EYE_CONSEC_FRAME = 2
counter = 0

while x < len(photosList):
    if photosList[x].get_earAvg() < EYE_THRESH:
        counter += 1
    else:
        if counter >= EYE_CONSEC_FRAME:
            #Mark in the object that a blink occured
            photosList[x].set_blink(1)
            counter = 0
    x += 1

x = 0
times = int(len(photosList) / 30) #number of frames to go through (to convert back to 30 fps, change 30 to 900)

for x in range(times):
    count = 0
    y = 0
    while (y+30*x) < (30+30*x):
        count = count + photosList[y+30*x].ifBlink
        y+=1

    if count*2 <= 9:
        attention =2

    if (count*2 > 10) and (count*2 <=21):
        attention =1

    if count*2 > 21:
        attention =0 




