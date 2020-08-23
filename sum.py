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

# test code
if __name__ == "__main__": 
    lean = [True, False, True, True, True, False, False, False, True, False, True, False]
    headpos = [True, False, True]
    blink = [1, 0.5]

    print(sum(lean, headpos, blink))
