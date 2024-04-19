import copy
import random
import subprocess
from PIL import Image
import os


def format_melody(melody):
  formatted = []
  for note in melody:
      # Remove unwanted characters
      note = note.replace("'", "").replace(',', '').strip()#.replace('"', '')
      formatted.append(note)
  # Join the list into a string and return
  return ' '.join(formatted)

def plain_melody(melody):
  plain_melody =[]
  for note in melody:
    plain_melody.append(note[0])
  return plain_melody

def lilypond_generation(melody, name, uppertime, lowertime):
  melody = plain_melody(melody)
  lilypond_score = f"""
    \\version "2.24.1"  
    \\header {{
    tagline = "" 
    }}
    
    #(set-global-staff-size 26)
    
    \\score {{
     \\fixed c' {{
            \\time {uppertime}/{lowertime}
            {format_melody(melody)}
            \\bar "|"
        }}
    \\layout {{
      indent = 0\\mm
    
      ragged-right = ##f
      \\context {{
        \\Score
    
        \\remove "Bar_number_engraver"
      }}
    }}
    }}
    """

  with open('score.ly', 'w') as f:
    f.write(lilypond_score)

  subprocess.run(['lilypond', '--png', '-dresolution=300', 'score.ly'],
                 check=True)

  with Image.open('score.png') as img:
    width, height = img.size
    crop_height = height
    crop_rectangle = (0, 75, width, crop_height / 10)

    cropped_img = img.crop(crop_rectangle)
    cropped_img.save(f'cropped_score_{name}.png')
  os.remove('score.ly')
  os.remove('score.png')