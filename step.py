import streamlit as st
from c_melody_gen import main_generation, check_compound_time, note_with_fraction, convert_to_list
from score_generation import lilypond_generation
from cut_beat import main_grouping
from beat_sum import dashed_bar,bar_sum
from clean_cut_rest import clean_dotted_rest
from combinerest import combine_rests, break_rest_weak_beat
from notation import rhythm_dic

st.title("Grouping 101")
col1, col2 = st.columns(2)

if "time_sign" not in st.session_state:
    st.session_state["time_sign"]= None

with col1:
    st.session_state["time_sign"] = st.text_input("Enter a regular time signature (e.g., 4/4 or 6/8)",max_chars=5)
    time_signature = st.session_state["time_sign"]
    if time_signature:
        main_uppertime, main_lowertime = map(int, time_signature.split("/"))
with col2:
    random_example = st.button("Generate a random example")
melody_input = st.text_input("Or Enter a melody. Eg: d4= d crotchet, r2 = minim rest, c8. = dotted note")
#melody_input.lower()
if melody_input:
    melody = note_with_fraction(convert_to_list(melody_input))
    uppertime,lowertime,compound= check_compound_time(main_uppertime,main_lowertime)
    if bar_sum(melody, uppertime, lowertime):
        st.success("Melody entered")
    else:
        st.error("The sum of the beats is not equal to the time signature. Please enter the melody again.")
        melody_input = False
        
if random_example:
    melody_input = None

if time_signature and (random_example or melody_input):
    try:
        st.write(f"You entered a time signature: {main_uppertime}/{main_lowertime}")
        if melody_input is None or melody_input.strip() == "":
            melody, uppertime, lowertime, compound = main_generation(rhythm_dic[main_lowertime], main_uppertime, main_lowertime)
        lilypond_generation(melody, "raw", main_uppertime, main_lowertime)
        print("step1", melody)
        st.image('cropped_score_raw.png', "Question")

        melody = main_grouping(melody, uppertime, lowertime)
        print("step2",melody)
        p_melody = dashed_bar(melody, lowertime)
        lilypond_generation(p_melody, "cutbeat", main_uppertime, main_lowertime)
        st.image('cropped_score_cutbeat.png', "Breakdown to find all beat locations.")
    
        melody = clean_dotted_rest(melody, uppertime, lowertime, compound)
        p_melody = dashed_bar(melody, lowertime)
        lilypond_generation(p_melody, "cleandotted", main_uppertime, main_lowertime)
        st.image('cropped_score_cleandotted.png', "Breakdown all dotted rests and any long rest, except strong beat dotted rest in compound time.")
        print("step3", melody)

        melody = break_rest_weak_beat(melody, lowertime, compound)
        print("step4", melody)

        melody = combine_rests(melody, lowertime, compound)
        lilypond_generation(melody, "combine_rests", main_uppertime, main_lowertime)
        st.image('cropped_score_combine_rests.png', "Combine rests according to the beat, don't cross the beat")
        print("step5", melody)

    except ValueError:
        st.write("Invalid time signature format. Please enter in the format 4/4 or 6/8.")
else:
    st.write("Please enter a time signature. Press the button or enter a melody.")
