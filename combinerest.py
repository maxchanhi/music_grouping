from fractions import Fraction
from notation import fraction_to_lilypond, change_arest

def sub_combine(melody,check,target):
    m_value = value = beat_p = 0
    beat = [0]  
    
    for note in melody:
        value += note[1]
        if value % check ==0:
            beat.append(beat_p+1)
        beat_p+= 1
    i=0
    for i in range(len(beat)-1):
        rhidx,lhidx = beat[i],beat[i+1]
        countrest = 0
        for note in melody[rhidx:lhidx]:
            if "r" in note[0] :
                countrest+= 1
        if countrest == len(melody[rhidx:lhidx]) and len(melody[rhidx:lhidx])> 1 :
            if check != target:
                print(check, rhidx,lhidx)
                melody[rhidx:lhidx] = [change_arest(check)]
                return sub_combine(melody,check,target)     
    return melody
            
def combine_rests(melody,lowertime=Fraction(8,3),compound=True):
    lowertime = Fraction(1,lowertime) #3/8
    if compound == True:
        checklist = [lowertime*2,lowertime,lowertime*Fraction(1,3),Fraction(1,3)*lowertime*Fraction(1,2),Fraction(1,3)*lowertime*Fraction(1,4)]
    else:
        checklist = [lowertime*2,lowertime,Fraction(1,2)*lowertime,Fraction(1,4)*lowertime,Fraction(1,8)*lowertime]
    target = lowertime*Fraction(2,3)
    #print("checklist",checklist)
    for check in checklist:
        melody = sub_combine(melody,check,target)
    print("after sub", melody, target)
    idx=note=m_value = 0 
    mainbeat =[0]       
    for note in melody:
        m_value += note[1]
        if m_value % lowertime ==0:
            mainbeat.append(idx+1)  
        idx+=1
    if len(mainbeat)>1:
        i=0
        while i<len(mainbeat)-1:
            rhidx,lhidx=mainbeat[i],mainbeat[i+1]
            #print("range quarter",melody[rhidx:lhidx])
            subvalue=0
            mid = 1
            for note in melody[rhidx:lhidx]:
                subvalue+=note[1]
                if subvalue==target:
                    subvalue=count=0
                    print("mid",melody[rhidx:rhidx+mid])
                    for sub_note in melody[rhidx:rhidx+mid]:
                        if "r" in sub_note[0]:
                            count+=1
                        
                    if count and count==len(melody[rhidx:rhidx+mid]) and melody[rhidx][1] != target:
                        print("combine quarter",count,melody[rhidx:rhidx+mid])
                        melody[rhidx:rhidx+mid]=[change_arest(target)]
                        return combine_rests(melody,Fraction(1,lowertime),compound)
                elif subvalue>target:
                    break
                mid+=1
            i+=1
    return melody

def break_rest_weak_beat(melody,lowertime,compound):
    check = Fraction(1,lowertime)
    subcheck = Fraction(1,lowertime)*Fraction(1,3)
    target = Fraction(1,lowertime)*Fraction(1,3)*2
    if compound:
        mainbeat=[0]
        checklist = [Fraction(1,lowertime),Fraction(1,lowertime)*Fraction(1,3),Fraction(1,lowertime)*Fraction(1,3)*Fraction(1,2),Fraction(1,lowertime)*Fraction(1,3)*Fraction(1,4)]
        #print("break checklist",checklist,check ,subcheck,target)
        for el in checklist:
            beat= value = 0
            while beat < len(melody)-1:
                value += melody[beat][1]
                if value % check == 0:
                    mainbeat.append(beat)
                if str(target) in str(melody[beat][1]) and "r" in melody[beat][0] :
                    #print(mainbeat,melody[beat],beat)
                    if beat == 0:
                        print("on beat")
                    elif beat-1 not in mainbeat:
                        melody[beat:beat+1] = change_arest(subcheck),change_arest(subcheck)
                        print("break beat")
                        beat= value = 0
                        return break_rest_weak_beat(melody,lowertime,compound)
                    elif beat-1 in mainbeat:
                        print("on beat")
                if value % el != 0 and value > el:
                    if melody[beat][1] >= el and "r" in melody[beat][0]:
                        b_value =melody[beat][1]*Fraction(1,2) 
                        melody[beat:beat+1] = change_arest(b_value),change_arest(b_value)
                        print('break syncopation rest',melody)
                        return break_rest_weak_beat(melody,lowertime,compound)
                        beat= value = 0
                    
                beat +=1
        
    return melody



#print(break_rest_weak_beat(melody,lowertime=Fraction(8,3),compound=True))
"""melody =[['d32', Fraction(1, 32)], ['r32', Fraction(1, 32)], ['r32', Fraction(1, 32)], ['d32~', Fraction(1, 32)],
        ['d16', Fraction(1, 16)], ['b16', Fraction(1, 16)], 
        ['e32', Fraction(1, 32)], ['d16.~', Fraction(3, 32)],
        ['d32', Fraction(1, 32)], ['r32', Fraction(1, 32)], ['d16', Fraction(1, 16)]]

melody = break_rest_weak_beat(melody,lowertime=Fraction(16,1),compound=False)
print("break_rest_weak_beat",melody)"""
#print(break_rest_weak_beat(melody,lowertime=Fraction(8,3),compound=True))"""