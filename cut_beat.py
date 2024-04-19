
from fractions import Fraction
from notation import *
import copy
def change_arest(frac):
  st_new_rhythm = fraction_to_lilypond[frac]
  return ["r" + st_new_rhythm, frac]

def find_combinations(target_fraction):
  # Sort the fractions in descending order
  sorted_fractions = sorted(fraction_combinations_list, reverse=True)
  result = []
  remaining = target_fraction

  # Try to subtract the fractions starting from the largest
  for fraction in sorted_fractions:
    while remaining >= fraction:
      remaining -= fraction
      result.append(fraction)
      if remaining == 0 and len(result)==2 :  # If we've exactly reached the target, return
        return result

  # If there is a remainder that cannot be represented, return None or raise an error
  if remaining > 0:
    raise ValueError(
        "Cannot represent the target fraction with the given options.")
  return result

def change_note(note_to_change, new_duration):
  if note_to_change[0].startswith('r'):
    rhythm = fraction_to_lilypond[new_duration]
    return ['r' + str(rhythm), new_duration]

  else:
    pitch = note_to_change[0][0]  # Remove the trailing duration
    rhythm_value = fraction_to_lilypond[new_duration]

  return [pitch + rhythm_value, new_duration]

def beat_cutter(melody, check, compound):
    value = beat_p = 0
    if compound : #isinstance(check, int) and
      max_check = Fraction(1, check)  
    else:
      max_check = Fraction(1, check)* 2 # Fraction(3, 2)
    for note in melody:
        value += note[1]
        pop = None
        if value % Fraction(1, check)==0:
            value = 0
        elif value > Fraction(1, check) and note[1] <= max_check:
            ex_beat = abs(value - Fraction(1, check))
            in_beat = abs(melody[beat_p][1] - ex_beat)
            print(check, melody[beat_p],beat_p,in_beat,ex_beat) 
            if ex_beat not in fraction_to_lilypond:
              ex_beat,pop = find_combinations(ex_beat)
            elif in_beat not in fraction_to_lilypond:
              in_beat,pop = find_combinations(in_beat)
              
            if ex_beat in fraction_to_lilypond and in_beat in fraction_to_lilypond:  
              if pop:
                melody[beat_p:beat_p + 1] = [change_note(melody[beat_p],in_beat),change_note(melody[beat_p],pop),change_note(melody[beat_p],ex_beat)]
              else:
                melody[beat_p:beat_p + 1] = [change_note(melody[beat_p],in_beat),change_note(melody[beat_p],ex_beat)]
                #print("cut rest")
              
              if "r" in melody[beat_p][0]:
                pass
              elif melody[beat_p][0][-1] == "~":
                melody[beat_p+1][0]=melody[beat_p+1][0]+"~"
                if pop:
                  melody[beat_p+2][0]=melody[beat_p+2][0]+"~"
              elif "r" not in melody[beat_p][0]:
                  melody[beat_p][0]=melody[beat_p][0]+"~"
                  if pop:
                    melody[beat_p+1][0]=melody[beat_p+1][0]+"~"
              
              value = 0
              return beat_cutter(melody, check, compound)
        beat_p += 1
    
    return melody


def main_grouping(melody, uppertime, lowertime):
  simple_time = [2,4]
  if type(lowertime) is not int:
    rhythm_checklist = [
        Fraction(1, 2) * lowertime, lowertime
        #,lowertime*3
    ]
    compound = True
    if uppertime == 3:
      rhythm_checklist = [lowertime, lowertime*3]
  else:
    rhythm_checklist = [lowertime // 2, lowertime]
    compound = False
    if uppertime == 3:
      rhythm_checklist = [lowertime]
  
  print("rhythm_checklist",rhythm_checklist,"compound",compound)
  for check_value in rhythm_checklist:
    melody = beat_cutter(melody, check_value, compound)
  return melody


def separate_note(note_to_change, st_new_note, nd_note):
  pitch_with_duration, _ = note_to_change
  pitch = note_to_change[0][0]
  st_new_rhythm = fraction_to_lilypond[st_new_note]
  nd_new_rhythm = fraction_to_lilypond[nd_note] 
  if "r" not in note_to_change[0]:  #is note
    st_combine = [pitch + st_new_rhythm + "~", st_new_note]
  else:
    st_combine = [pitch + st_new_rhythm, st_new_note]

  return st_combine, [pitch + nd_new_rhythm, nd_note]

"""melody =[['b4',Fraction(1,4)],['d1',Fraction(1,1)],['r8',Fraction(1,8)],['e8',Fraction(1,8)]]
print(main_grouping(melody,uppertime=3,lowertime=2))"""

