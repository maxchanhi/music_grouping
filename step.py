import streamlit as st
import copy
from c_melody_gen import main_generation
from score_generation import lilypond_generation
from cut_beat import main_grouping
from grouprest import switch_rest_position
from clean_cut_rest import clean_dotted_rest
from combinerest import combine_rests, break_rest_weak_beat
from notation import rhythm_dic

st.title("Grouping 101")

time_signature = st.text_input("Enter a regular time signature (e.g., 4/4 or 6/8)")

if time_signature:
    try:
        main_uppertime, main_lowertime = map(int, time_signature.split("/"))
        st.write(f"You entered a time signature: {main_uppertime}/{main_lowertime}")
        
        melody, uppertime, lowertime, compound = main_generation(rhythm_dic[main_lowertime], main_uppertime, main_lowertime)
        print("Time signature", uppertime, lowertime, compound)
        lilypond_generation(melody, "raw", main_uppertime, main_lowertime)
        print("step1", melody)
        st.image('cropped_score_raw.png', "Question")

        melody = main_grouping(melody, uppertime, lowertime)
        lilypond_generation(melody, "cutbeat", main_uppertime, main_lowertime)
        st.image('cropped_score_cutbeat.png', "Breakdown to find all beat locations.")
        print("step2", melody)

        melody = clean_dotted_rest(melody,uppertime, lowertime, compound)
        lilypond_generation(melody, "cleandotted", main_uppertime, main_lowertime)
        st.image('cropped_score_cleandotted.png', "Breakdown all dotted rests and any long rest, except strong beat dotted rest in compound time.")
        print("step3", melody)

        melody = break_rest_weak_beat(melody, lowertime, compound)
        print("step6", melody)

        melody = combine_rests(melody, lowertime, compound)
        lilypond_generation(melody, "combine_rests", main_uppertime, main_lowertime)
        st.image('cropped_score_combine_rests.png', "Combine rests according to the beat, don't cross the beat")
        print("step7", melody)

    except ValueError:
        st.write("Invalid time signature format. Please enter in the format 'uppertime/lowertime' (e.g., 4/4 or 6/8).")
else:
    st.write("Please enter a time signature.")

st.button("New Example")

