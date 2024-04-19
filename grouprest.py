from fractions import Fraction
import re
from notation import fraction_to_lilypond,durations_fraction, change_arest
from cut_beat import find_combinations

def check_compound_time(uppertime,lowertime):
  simple_list=[2,3,4]
  compound_list = [6,9,12]
  if uppertime in simple_list:
    compound = False
    return uppertime, lowertime, compound 
  elif uppertime in compound_list:
    uppertime = uppertime//3
    lowertime = durations_fraction[str(lowertime//2)+"."]
    lowertime = Fraction(1,lowertime)
    compound = True
    return uppertime, lowertime, compound 
  else:
    raise ValueError(f"Irragular time signature. {uppertime}/{lowertime}")

def extract_duration_digit(note_string):
  match = re.search(r'\d+', note_string)
  if match:
      return int(match.group())
  else:
      raise ValueError("No duration digit found in the string.")
  


def switch_rest_position(melody,rhythm_checklist,lowertime,compound):
  #print("rhythm_checklist",rhythm_checklist)
  for rhythm in rhythm_checklist:
    def sub_switch(melody, rhythm):
      value  =note = 0
      while note < len(melody)-1:
        value += melody[note][1]
        if value % Fraction(1, rhythm)== 0:
          value = 0
        elif value > Fraction(1, rhythm) and melody[note][1] <= Fraction(1, rhythm) and melody[note-1][1] <= Fraction(1, rhythm):
          if "r" in melody[note][0] and "r" in melody[note-1][0] :
            melody[note-1],melody[note] = melody[note],melody[note-1]
            note =value = 0
            #return sub_switch(melody, rhythm)
        note += 1
      return melody
    melody = sub_switch(melody,rhythm)
  #melody = combine_rests(melody,lowertime,compound)
  return melody




"""
melody = switch_rest_position(melody1,rhythm_checklist,lowertime=Fraction(8,3),compound=True)
print("2",melody)"""

"""melody = clean_cut_beat(melody,rhythm_checklist)
print("3",melody)"""

"""
def dotted_rest(melody, lowertime, check, allowed_dotted_rest):
  value = beatp = 0
  main = [0]
  check = Fraction(1, check)
  for note in melody:
    value += note[1]
    if value % check == 0:
      value = 0
      main.append(beatp)
    beatp += 1
  value = beatp = 0
  target = Fraction(1,(lowertime*Fraction(3,2)))
  targetmain =[0]
  for note in melody:
    value += note[1]
    if value % Fraction(1,lowertime) == 0:
      value = 0
      targetmain.append(beatp)
    beatp += 1
  value = beatp = 0
  while beatp < len(melody)-1:
    if "r" in note[0] and "." in note[0]:
      if note[1] in allowed_dotted_rest and beatp-1 in targetmain:
        pass
      elif check < note [1] < check*2:
        ex_value = abs(note[1]- check)
        melody[beatp:beatp+1]=change_arest(check),change_arest(ex_value)
        beatp =0
    if str(note[1]) == str(target) and beatp-1 not in targetmain:
        melody[beatp:beatp+1]= change_arest(target*Fraction(1,2)),change_arest(target*Fraction(1,2))
        beatp =0
    #elif str(note[1]) == str(target) and beatp-1 in targetmain:
        #print("on beat long rest")
    beatp += 1
  return melody
"""
