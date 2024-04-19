
from fractions import Fraction
import re
from notation import fraction_to_lilypond,durations_fraction, change_arest
from cut_beat import find_combinations
import copy

def extract_duration_digit(note_string):
  match = re.search(r'\d+', note_string)
  if match:
      return int(match.group())
  else:
      raise ValueError("No duration digit found in the string.")
  
def dotted_rest(melody, lowertime, check):
  value = beatp = 0
  main_list = [0]
  main_beat=Fraction(1,lowertime)
  check = Fraction(1, check)
  while beatp < len(melody):
    if value%main_beat==0:
        main_list.append(beatp)
    if "r" in melody[beatp][0] and str(melody[beatp][1]) == str(main_beat) :
      if beatp  not in main_list:
        #print(main_list,beatp)
        melody[beatp:beatp + 1] = change_arest(
            main_beat * Fraction(1, 2)), change_arest(main_beat * Fraction(1, 2))
        #print("breaklong")
        return dotted_rest(melody, lowertime, check)
    if "r" in melody[beatp][0] and "." in melody[beatp][0] and check<melody[beatp][1]<=check*2:
        ex_value = abs(melody[beatp][1] - check)
        if ex_value in fraction_to_lilypond and check in fraction_to_lilypond:
          melody[beatp:beatp + 1] = change_arest(ex_value),change_arest(check)
          beatp = 0
        print("breakdotted", check)
        #return dotted_rest(melody, lowertime, check)
    beatp += 1

  return melody

def clean_cut_beat(melody,check,lowertime):
  value = beat_p = 0
  main_beat=[0]
  m_beat=Fraction(1,lowertime)
  target = m_beat * Fraction(2,3)
  for note in melody:
    value += note[1]
    if value % Fraction(1,lowertime)==0:
      main_beat.append(beat_p+1)
    beat_p += 1
  #print("cleancut main beat",main_beat,melody)
  for i in range(len(main_beat)-1):
    lh ,rh = main_beat[i],main_beat[i+1]
    s_value=s_mid = 0
    for sub_note in melody[lh:rh]:
      s_value+= sub_note[1]
      if s_value>target and "r" in sub_note[0] and sub_note[1] == target:
        print("break quarter")
        melody[lh+s_mid:lh+s_mid+1]= change_arest(target*Fraction(1,2)),change_arest(target*Fraction(1,2))
        return clean_cut_beat(melody,check,lowertime)
      s_mid+=1
  #print("after break crochet",check,melody)
  value = beat_p = 0
  while beat_p < (len(melody)):
    value += melody[beat_p][1]
    if value % Fraction(1,check)==0:
      value = 0
    elif melody[beat_p][1] <= Fraction(1,check)*3 and value> Fraction(1,check) and "r" in melody[beat_p][0]:
      ex_beat = abs(value - Fraction(1,check))
      in_beat = abs(melody[beat_p][1]- ex_beat) 
      #print("cut beat",melody[beat_p],beat_p,check, in_beat,ex_beat)
      if ex_beat in fraction_to_lilypond and in_beat in fraction_to_lilypond:
        if ex_beat + in_beat > melody[beat_p][1]:
          ex_beat=abs(melody[beat_p][1]-in_beat)
          print(">original", melody)
        if ex_beat and in_beat and ex_beat + in_beat == melody[beat_p][1]:
          print("splited",check,melody[beat_p],beat_p,ex_beat,ex_beat)
          melody[beat_p:beat_p+1] = change_arest(abs(in_beat)),change_arest(abs(ex_beat))
          return clean_cut_beat(melody,check,lowertime)
       
    beat_p += 1
  return melody

def clean_dotted_rest(melody,uppertime,lowertime,compound):
  #uppertime,lowertime,compound = check_compound_time(uppertime,lowertime)
  rhythm_checklist = []
  if compound == True:
    rhythm_checklist = [Fraction(1,lowertime*Fraction(1,2)),lowertime,lowertime*3,
                        (lowertime*3)*2,(lowertime*3)*4]
    if uppertime ==3:
      rhythm_checklist = [lowertime,lowertime*3,
                        (lowertime*3)*2,(lowertime*3)*4]
  else:
    rhythm_checklist = [lowertime//2,lowertime,lowertime*2,lowertime*4,lowertime*8]
  print("checklist for clean cut",compound,rhythm_checklist)
  for check in rhythm_checklist:
    melody = clean_cut_beat(melody,check,lowertime)
  print("dotted",melody,"check",rhythm_checklist)
  for check in rhythm_checklist:
    melody = dotted_rest(melody,lowertime,check)
  
  return melody

"""melody =[['f8', Fraction(1, 8)], ['a4.', Fraction(3, 8)], ['r4', Fraction(1, 4)], ['r2.', Fraction(3, 4)]]
melody1= clean_dotted_rest(melody,uppertime=2,lowertime = Fraction(4,3),compound=True)
print("1",melody1)"""
#
