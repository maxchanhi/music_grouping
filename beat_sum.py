from fractions import Fraction
from notation import *

def dashed_bar(melody,lowertime):
    lowtime = Fraction(1,lowertime)
    melody_d=[]
    value = beatp = 0
    while beatp < len(melody):
        value += melody[beatp][1]
        melody_d.append(melody[beatp])
        if value % lowtime ==0 and beatp != len(melody)-1:
            melody_d.append(['\\bar ";"',Fraction(0,1)])
            value = 0    
        beatp += 1  
    return melody_d

def bar_sum(melody,uppertime,lowertime):
    lowtime = Fraction(1,lowertime)
    bar_total = lowtime*uppertime
    value = 0
    for note in melody:
        value += note[1]
    if value == bar_total:
        return True
    else:
        return False
#3(d8 r4)

def get_nplet(melody=["d3","3(d8 d4)"]):  
    for note in melody:
        if "3(" and ")" in note:
            print("triplet found")

