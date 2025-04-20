import pandas as pd
import os
import functions as fn
import re

def replace_special_characters(input_string):
    return re.sub(r'[^a-zA-Z0-9]+', '_', input_string)

def run():
    
    folder_path = r'D:\Yash\Projects\IPL-2024\CSV Data\batting'
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
    batter_df = pd.read_csv(filePath)

    try:
        # id columns
        new_id = batter_df['id'].str.split(' ',1,expand=True)
        batter_df = batter_df.drop(['id'],axis=1)
        batter_df['id2'] = new_id[1]
        batter_df['day/night'] = batter_df['id2'].apply(lambda x:'Night' if x == 'Match (N)' else 'Day')
        batter_df = batter_df.drop(['id2'],axis=1)

        if 'Qualifier' in new_id[0][0]:
            batter_df['id'] = new_id[0]+new_id[1][0]
            match_id = new_id[0][0]+new_id[1][0]
            match_id = replace_special_characters(match_id)
        else:
            batter_df['id'] = new_id[0]
            match_id = new_id[0][0]

        #batsman column
        batter_df['batsman'] = batter_df['batsman'].str.replace('[^(),a-zA-Z0-9]',' ',regex=True).str.rstrip()
        batter_df['captain'] = batter_df['batsman'].apply(fn.markCaptain)
        batter_df['batsman'] = batter_df['batsman'].map(lambda x:x.rstrip('(c) '))


        #stats column
        stats = batter_df['stats'].str.split(',',expand=True)
        batter_df['balls played'] = stats[0].replace('\W','',regex=True).str.strip()
        batter_df['minutes while batting'] = stats[1].replace('\W','',regex=True).str.strip()
        batter_df['4s'] = stats[2].replace('\W','',regex=True).str.strip()
        batter_df['6s'] = stats[3].replace('\W','',regex=True).str.strip()
        batter_df['s/r'] = stats[4].replace('[^.,a-zA-Z0-9 \n\.]','',regex=True).str.strip()
        batter_df = batter_df.drop(['stats'],axis=1)


        #date column
        dates = batter_df['date'].str.strip()
        batter_df = batter_df.drop(['date'],axis=1)
        batter_df['date'] = dates.str.replace(' ','/')
        season = batter_df['date'].str.split('/',n=-1,expand=True)
        batter_df['season'] = season[2]


        #toss column
        toss = batter_df['toss'].str.split(',',expand=True)
        batter_df['toss winner'] = toss[0]
        batter_df['toss decision'] = toss[1]
        batter_df = batter_df.drop(['toss'],axis=1)


        #winner column
        batter_df['summary'] = batter_df['winner']
        winners = batter_df['winner'].str.split('won',n=1,expand=True)[0].str.strip()
        batter_df.drop(['winner'],axis=1)
        batter_df['winner'] = winners
        # batter_df['summary'] = summary
        batter_df['winner'] = batter_df['winner'].apply(fn.changeAbbrev)
        batter_df['win_by'] = batter_df['summary'].apply(fn.winBy)


        #winner_by column
        batter_df['wicket_by'] = batter_df['wicket_by'].replace(' - ','not out')
        batter_df['wicket_by'] = batter_df['wicket_by'].replace('[^()/,a-zA-Z0-9]',' ',regex=True)
        batter_df['wicket_by'] = batter_df['wicket_by'].str.lstrip()
        batter_df['is_notout'] = batter_df['wicket_by'].apply(lambda x:1 if x == 'not out' else 0)
        batter_df['is_out'] = batter_df['is_notout'].apply(lambda x:1 if x == 0 else 0)
        batter_df['is_runout'] = batter_df['wicket_by'].apply(fn.checkRunout)

        batter_df = batter_df[['id','date','season','batsman','runs_scored', 'balls played',
            'minutes while batting', '4s', '6s', 's/r','wicket_by',
            'is_notout','is_out','is_runout','batting_team', 'bowling_team', 
            'venue','day/night','captain','toss winner','toss decision','winner','win_by','summary']]
        
        print('processed successfully.',match_id)
    
    except Exception as e:
        print('data processing failed!',e,match_id)


    try:
        temp_file_name = r'D:\Yash\Projects\IPL-2024\Output Files\batting cleaned\batting_data_cleaned_{}.csv'.format(match_id)
        batter_df.to_csv(temp_file_name,index=False)
        batter_df_nonull = pd.read_csv(temp_file_name)
        batter_df_nonull['s/r'].fillna(0.00,inplace=True)
        batter_df_nonull['minutes while batting'].fillna(0.00,inplace=True)
        batter_df_nonull.fillna('-',inplace=True)
        batter_df_nonull.to_csv(temp_file_name,index=False)
        print('exported successfully.',match_id)
    except Exception as e:
        print('failed to load data!',e,match_id)