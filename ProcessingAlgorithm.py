
#this is the code to process all the results of the final computation and create a database of attention averages


#Eyeblinking
#All this currently assumes 1 frame per second due to restrictions


x = 0

EYE_THRESH = 0.3 #0.3 is optimal setting (30fps)
EYE_CONSEC_FRAME = 2 #3 is optimal setting (30 fps)
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


    #Code here is run assuming 1 frame a second, and 20 second intervals to used for attention interval calculations
x = 0
times = int(len(photosList) / 20) #number of frames to go through to match 30 second period (to convert back to 30 fps, change 30 to 900)

for x in range(times):
    count = 0
    y = 0
    while (y+20*x) < (20+20*x):
        count = count + photosList[y+20*x].ifBlink()
        y+=1

    if count*3 <= 9:
        attention =1

    if (count*3 > 10) and (count*3 <=21):
        attention =0.5

    if count*3 > 21:
        attention =0 




