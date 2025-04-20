import pandas as pd
import numpy as np
import pickle
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

#import encoder & gboost model
with open('../Models/gboost_model_v4.pkl', 'rb') as f:
    model = pickle.load(f)

with open('../Models/target_encoder_v3.pkl', 'rb') as f:
    encoder = pickle.load(f)

with open('../Models/scaler_v4.pkl', 'rb') as f:
    scaler = pickle.load(f)


# Streamlit
st.title("Score Prediction")

#select team1
selected_team = st.selectbox("Select Team",["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Delhi Capitals","Kolkata Knight Riders","Punjab Kings","Rajasthan Royals",
                            "Sunrisers Hyderabad","Lucknow Super Giants","Gujarat Titans"])

#is batting first
batting_first = st.radio("Batting First?",["Yes","No"])

#select opposition

oppositon_list = ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Delhi Capitals","Kolkata Knight Riders","Punjab Kings","Rajasthan Royals",
                            "Sunrisers Hyderabad","Lucknow Super Giants","Gujarat Titans"]
oppositon_list.remove(selected_team)

selected_opp = st.selectbox("Select Opposition",oppositon_list)

bat_flag = selected_opp
if batting_first == "Yes":
    bat_flag = selected_team

# select venue
selected_venue = st.selectbox("Select Venue",[' Ahmedabad', ' Eden Gardens', ' Wankhede', ' Brabourne',
       ' DY Patil', ' Pune', ' Chennai', ' Bengaluru', ' Delhi',
       ' Dharamsala', ' Hyderabad', ' Lucknow', ' Jaipur', ' Mohali',
       ' Guwahati', 'Guwahati', 'Hyderabad', 'Ahmedabad', ' Mullanpur',
       ' Visakhapatnam'])

def perform_operations():

    # connecting to groq cloud
    llm = ChatGroq(
        model_name="llama-3.3-70b-specdec",
        temperature=0,
        groq_api_key = "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"
    )

    teams= "{} and {}".format(selected_team,selected_opp)

    # prompt message
    prompt = ChatPromptTemplate.from_template(
        """
        ### YOU ARE A HELPFUL ASSISTANT THAT PROVIDES DETAILED STATS OF ALL CRICKET PLAYERS FOR THE {INPUT} INDIAN PREMIER LEAGUE TEAM FOR THE CURRENT YEAR
        ### INCLUDE BOWLER'S AS WELL WITH THEIR BATTING AVERAGE
        ### RETURN THE PLAYER STATS IN THE FOLLOWING FORMAT:
        ### "Player Name": {{
        ###    "Role": <Player's Role>, 
        ###    "Strike Rate": <Player's Average Strike Rate in Last 2 Matches>, 
        ###    "Batting Average": <Player's Batting Average From Last 2 Matches> 
        ###    "Team": <Player's Team>
        ### }}
        ### ONLY RETURN VALID JSON WITH NO ADDITIONAL TEXT, EXPLANATIONS, OR INTRODUCTION.
        ### THE RESPONSE SHOULD BE STRICTLY IN PROPER JSON FORMAT, WITHOUT ANY EXTRA INFORMATION OR COMMENTARY.
        ### DO NOT INCLUDE PREAMBLE OR FOOTER. ONLY THE JSON.
        """
    )

    chain = prompt | llm
    resp1 = chain.invoke(input={'INPUT':teams})

    json_parser = JsonOutputParser()
    # print(resp1.content)
    res = json_parser.parse(resp1.content)

    df = pd.DataFrame(res)
    ds = df.T
    ds.reset_index(inplace=True)
    ds.rename(columns={'index':'Player'},inplace=True)

    # print(ds.columns)

    # ds['venue'] = selected_venue
    ds['is_batting_first'] = ds['Team'].apply(lambda x:1 if x == bat_flag else 0)
    ds['Role'].replace("Wicket-keeper","Batsman",inplace=True)

    def create_bowler_list():
        bowler_df = pd.DataFrame()
        bowler_df['bowler'] = ds[((ds['Role'] == "All-rounder") | (ds['Role'] == "Bowler"))]['Player']
        bowler_df['Team'] = ds['Team']
        bowler_df['Role'] = 'Batsman'
        bowler_df['Batting Average'] = ds['Batting Average']
        bowler_df['Strike Rate'] = ds['Strike Rate']
        bowler_df['is_batting_first'] = ds['is_batting_first']
        return bowler_df

    df_b = create_bowler_list()
    merge = pd.merge(ds,df_b,how="left",on="Role")

    team1 = df_b[df_b['Team'] == selected_team]
    team2 = df_b[df_b['Team'] == selected_opp]

    bowler1= pd.merge(team1,team2,on="Role",how="left")
    bowler2 = pd.merge(team2,team1,on="Role",how="left")

    temp1 = bowler1[["bowler_x","Role","Strike Rate_x","Batting Average_x","Team_x","is_batting_first_x","bowler_y","Team_y"]]
    temp2 = bowler2[["bowler_y","Role","Strike Rate_y","Batting Average_y","Team_y","is_batting_first_y","bowler_x","Team_x"]]

    temp1.columns = ['Player', 'Role', 'Strike Rate', 'Batting Average', 'team',
        'is_batting_first', 'bowler', 'Team']
    temp2.columns = ['Player', 'Role', 'Strike Rate', 'Batting Average', 'team',
        'is_batting_first', 'bowler', 'Team']

    bowler_merge = pd.concat([temp1,temp2],ignore_index=True)

    merge.loc[merge['Team_y'].isna() & (merge['Team_x'] == selected_team), 'Team_y'] = selected_opp
    merge.loc[merge['Team_y'].isna() & (merge['Team_x'] == selected_opp), 'Team_y'] = selected_team

    final_ds = merge[(merge['Team_x'] != merge['Team_y'])]

    #adding venue
    # st.write(selected_venue)
    # st.write(res)
    final_ds['venue'] = str(selected_venue)

    final_ds.dropna(inplace=True,axis=0)

    final_ds = final_ds[['Player', 'Role', 'Strike Rate_x', 'Batting Average_x', 'Team_x',
        'is_batting_first_x', 'bowler', 'Team_y','venue']]

    final_ds.columns = ['Player', 'Role', 'Strike Rate', 'Batting Average', 'team',
        'is_batting_first', 'bowler', 'Team','venue']

    final_ds1 = pd.concat([final_ds,bowler_merge],ignore_index=True)
    final_ds1.replace('null',0.00,inplace=True)
    final_ds2 = final_ds1[["Player","bowler","Strike Rate","Batting Average","team","Team","venue","is_batting_first"]]
    final_ds2.columns = ["batsman","bowler","s/r","avg","batting_team","bowling_team","venue","is_batting_first"]

    # final_ds2.to_csv('data.csv',index=False)

    encoded_values = encoder.transform(final_ds2)
    scaled_df = scaler.transform(encoded_values)
    encoded_values.to_csv('encoded.csv',index=False)
    y_pred = model.predict(scaled_df)

    final_ds2['predicted_score'] = np.int64(np.round(np.ceil(y_pred*y_pred),0))

    grp_scored = final_ds2.groupby(['batsman'])['predicted_score'].mean().reset_index()
    grp_scored['predicted_score'] = grp_scored['predicted_score'].round(0).astype(int)

    df_placeholder.write(grp_scored)
    # grp_scored.to_csv('predicted.csv',index=False)

df_placeholder = st.empty()

if st.button('Get Predicitons'):
    perform_operations()
