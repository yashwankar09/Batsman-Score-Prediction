import streamlit as st
import pickle

with open('../Models/gboost_model_v2.pkl', 'rb') as f:
    model = pickle.load(f)

with open('../Models/target_encoder_v2.pkl', 'rb') as f:
    encoder = pickle.load(f)

st.title("Score Prediction")

#select team1
selected_team = st.selectbox("Select Team",["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Delhi Capitals","Kolkata Knight Riders","Punjab Kings","Rajasthan Royals",
                            "Sunrisers Hyderabad","Lucknow Super Giants","Gujarat Titans"])

#is batting first
batting_first = st.radio("Batting First?",["Yes","No"])

bat_flag = 0
if batting_first == "Yes":
    bat_flag = 1

#select opposition

oppoisiton_list = ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Delhi Capitals","Kolkata Knight Riders","Punjab Kings","Rajasthan Royals",
                            "Sunrisers Hyderabad","Lucknow Super Giants","Gujarat Titans"]
oppoisiton_list.remove(selected_team)

selected_opp = st.selectbox("Select Opposition",oppoisiton_list)

# select venue
selected_venue = st.selectbox("Select Venue",[' Ahmedabad', ' Eden Gardens', ' Wankhede', ' Brabourne',
       ' DY Patil', ' Pune', ' Chennai', ' Bengaluru', ' Delhi',
       ' Dharamsala', ' Hyderabad', ' Lucknow', ' Jaipur', ' Mohali',
       ' Guwahati', 'Guwahati', 'Hyderabad', 'Ahmedabad', ' Mullanpur',
       ' Visakhapatnam'])

