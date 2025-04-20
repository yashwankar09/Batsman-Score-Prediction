import pandas as pd
import mysql.connector
import os


conn = mysql.connector.connect(user='root', password='12345', host='localhost', port='3306', database='IPL_2022')
cursor = conn.cursor()

folder_path = r'D:\Yash\Projects\IPL-2024\Output Files - 2022\Combined'

csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

def load_to_db(dataframe,table_name):
    row_count = 0
    for i,row in dataframe.iterrows():
    #     sql = "INSERT INTO batsman VALUES {}".format(tuple(row))
        query = "insert into {} values {}.".format(table_name,tuple(row))
        query = query.rstrip('.')
        cursor.execute(query)
        row_count+=1

    conn.commit()
    print(row_count,'rows loaded to table {}'.format(table_name))

for files in csv_files:
    path = os.path.join(folder_path,files)
    df = pd.read_csv(path)
    df.fillna(0,inplace=True)
    if files == 'batting_combined.csv':
        load_to_db(df,'batsman')
    elif files == 'bowlingcombined.csv':
        load_to_db(df,'bowler')
    elif files == 'potm_combined.csv':
        load_to_db(df,'POTM')
    else:
        load_to_db(df,'Extra_runs')

conn.close()