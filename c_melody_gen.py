import random
from fractions import Fraction
import copy
import re
from notation import *

def rhythm_generation(all_rhythm_list, number_of_beat=4, lowertime=4):
  available_list = copy.copy(all_rhythm_list[:])
  beat_amount = Fraction(1, lowertime)
  melody = []
  melody_duration_sum = 0

  while melody_duration_sum < (number_of_beat * beat_amount):
    if not available_list:
      raise ValueError("No available rhythm")

    rhythm_choice = random.choice(available_list)
    melody.append(rhythm_choice)
    melody_duration_sum += durations_fraction[rhythm_choice]

    remaining_beat = number_of_beat * beat_amount - melody_duration_sum 
    available_list = []
    for rhythm in all_rhythm_list:
      if durations_fraction[rhythm] <= remaining_beat:
        available_list.append(rhythm)

  return melody


def insert_note_rest(rhythm_in_melody,
                     compound,
                     pitch_a=4,
                     max_attempts=10,
                     current_attempt=0):
  lily_melody = []
  pitch_c = 0
  rest_c = 0
  for rhythm in rhythm_in_melody:
    if random.randint(0, 3) == 0:
      #if (rhythm not in dotted_rest and compound is False) or (compound is True):
        note_with_rhythm = f"r{rhythm}"
        lily_melody.append(note_with_rhythm)
        rest_c += 1
    else:
      # If the random condition for rest was not met, just add a pitch note
      note_pitch = random.choice(pitch)
      note_with_rhythm = f"{note_pitch}{rhythm}"
      lily_melody.append(note_with_rhythm)
      pitch_c += 1

  if (pitch_c < pitch_a
      or rest_c < pitch_a / 2) and current_attempt < max_attempts:
    return insert_note_rest(rhythm_in_melody,
                            compound,
                            pitch_a=pitch_a,
                            max_attempts=max_attempts,
                            current_attempt=current_attempt + 1)
  elif current_attempt >= max_attempts:
    lily_melody = []
    return False

  return lily_melody


def note_with_fraction(melody):
  result = []
  for note in melody:
    rhythm_value = ''.join(filter(str.isdigit, note))
    dots = note.count('.')
    if rhythm_value:  # Check if we have a numeric rhythm value
      rhythm_fraction = Fraction(1, int(rhythm_value))
      for _ in range(dots):
        rhythm_fraction += rhythm_fraction / 2
    elif "3(" and ")"  in note:
      print("triplet found")     
    else:
      raise ValueError(f"No rhythm value found in note '{note}'")
    result.append([note, rhythm_fraction])
  value = 0
  for note in result:
    value += note[1]
  return result

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
    raise ValueError(f"Irregular time signature. {uppertime}/{lowertime}")

def convert_to_list(melody_input):
    return [note.strip() for note in melody_input.split()]

def convert_nplet_list(melody_input):
    melody = []
    for note in melody_input:
        melody.append(note)
    note_list = []
    i = 0
    while i < len(melody):
        if ("3"and"(" in melody[i]) or ("2"and"("in melody[i]):
            triplet ="3("
            i += 1
            while ")" not in melody[i]:
                triplet +=melody[i]
                i += 1
            triplet += ")" 
            note_list.append(triplet)
        elif melody[i] in pitch and melody[i+1] in rhythm_list:
            note_list.append(melody[i]+melody[i+1])
        i += 1
    return note_list

def get_nplet_duration(note=str):
  value_list = []
  #for note in melody:
  if note.startswith("3("):
    for el in note:
      if el in rhythm_list:
        value_list.append(Fraction(1, int(el)))
    return sum(value_list) * Fraction(2, 3)
  elif note.startswith("2("):
    for el in note:
      if el in rhythm_list:
        value_list.append(Fraction(1, int(el)))
    return sum(value_list) * Fraction(3, 2)
  


def main_generation(rhythm_list, uppertime,lowertime ):
  luppertime,llowertime,compound = check_compound_time(uppertime,lowertime)
  melody = rhythm_generation(rhythm_list, luppertime, llowertime)
  melody_rest = insert_note_rest(melody, luppertime,compound)
  if luppertime <=3:
    melody_len = 4
  else:
    melody_len = 8
  while len(melody_rest) < melody_len or len(melody_rest)>melody_len*2:
    return main_generation(rhythm_list, uppertime,lowertime)
  return note_with_fraction(melody_rest), luppertime, llowertime,compound
