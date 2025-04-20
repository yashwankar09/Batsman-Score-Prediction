import pandas as pd
import os
import functions as fn
import re

def replace_special_characters(input_string):
    return re.sub(r'[^a-zA-Z0-9]+', '_', input_string)

def run():

    folder_path = r'D:\Yash\Projects\IPL-2024\CSV Data\bowling'
    try:
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        print('loaded successfully.')
    except Exception as e:
        print('Dataset load failed.',e)

    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        processFile(file_path)

def processFile(filePath):
    
    match_id = ''
    bowler_df = pd.read_csv(filePath)

    try:

        #id column
        new_id = bowler_df['id'].str.split(' ',1,expand=True)
        bowler_df = bowler_df.drop(['id'],axis=1)
        bowler_df['id2'] = new_id[1]
        bowler_df['day/night'] = bowler_df['id2'].apply(lambda x:'Night' if x == 'Match (N)' else 'Day')
        bowler_df = bowler_df.drop(['id2'],axis=1)

        if 'Qualifier' in new_id[0][0]:
            bowler_df['id'] = new_id[0]+new_id[1][0]
            match_id = new_id[0][0]+new_id[1][0]
            match_id = replace_special_characters(match_id)
        else:
            bowler_df['id'] = new_id[0]
            match_id = new_id[0][0]

        #dates column
        dates = bowler_df['date'].str.strip()
        bowler_df = bowler_df.drop(['date'],axis=1)
        bowler_df['date'] = dates.str.replace(' ','/')
        season = bowler_df['date'].str.split('/',n=-1,expand=True)
        bowler_df['season'] = season[2]

        #toss column
        toss = bowler_df['toss'].str.split(',',expand=True)
        bowler_df['toss winner'] = toss[0]
        bowler_df['toss decision'] = toss[1]
        bowler_df = bowler_df.drop(['toss'],axis=1)

        #winner column
        winners = bowler_df['winner'].str.split('won',n=1,expand=True)[0].str.strip()

        if winners[0] == 'No Result' or winners[0] == 'No result':
            bowler_df['winner'] = winners
        else:
            summary = bowler_df['winner'].str.split(' ',n=1,expand=True)[1]
            bowler_df.drop(['winner'],axis=1)
            bowler_df['winner'] = winners
            bowler_df['summary'] = summary
            bowler_df['winner'] = bowler_df['winner'].apply(fn.changeAwbbrev)
            bowler_df['win_by'] = bowler_df['summary'].apply(fn.winBy)

        #stats column
        stats = bowler_df['stats'].str.split(',',expand=True)
        bowler_df['no_balls'] = stats[0].replace('\W','',regex=True).str.strip()
        bowler_df['wide_balls'] = stats[1].replace('\W','',regex=True).str.strip()
        bowler_df['6s_conceded'] = stats[2].replace('\W','',regex=True).str.strip()
        bowler_df['4s_conceded'] = stats[3].replace('\W','',regex=True).str.strip()
        bowler_df['0s_conceded'] = stats[4].replace('\W','',regex=True).str.strip()
        bowler_df['Econ'] = stats[5].replace('[^.a-zA-Z0-9]','',regex=True).str.strip()
        bowler_df['runs'] = stats[6].replace('\W','',regex=True).str.strip()
        bowler_df['maidan'] = stats[7].replace('\W','',regex=True).str.strip()
        bowler_df['overs'] = stats[8].replace('[^.a-zA-Z0-9]','',regex=True).str.strip()
        bowler_df = bowler_df.drop(['stats'],axis=True)

        bowler_df = bowler_df[['id','date', 'season','bowler','wicket','overs','maidan','runs','Econ',
          '0s_conceded','4s_conceded','6s_conceded','wide_balls','no_balls',
           'batting_team', 'bowling_team','venue','day/night','toss winner', 'toss decision',
          'winner','win_by','summary']]
        
        print('processed successfully.')

    except Exception as e:
        print('data processing failed!',e)

    try:
        temp_file_name = r'D:\Yash\Projects\IPL-2024\Output Files\bowling cleaned\bowling_data_cleaned_{}.csv'.format(match_id)
        bowler_df.fillna('-',inplace=True)
        bowler_df.to_csv(temp_file_name,index=False)
        print('exported successfully.')
    except:
        print('failed to load data!')