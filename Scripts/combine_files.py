import pandas as pd
import os

def combine_files(folder_path,combined_csv_path):
    # Get a list of all CSV files in the directory
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    # Initialize an empty list to hold the dataframes
    df_list = []

    # Loop through each file and read it
    for i, file in enumerate(csv_files):
        file_path = os.path.join(folder_path, file)
        if i == 0:
            # For the first file, include the header
            df = pd.read_csv(file_path)
        else:
            # For subsequent files, skip the header row
            df = pd.read_csv(file_path, header=0)
        df_list.append(df)

    # Concatenate all dataframes into a single dataframe
    combined_df = pd.concat(df_list, ignore_index=True)

    # Save the combined dataframe to a single CSV file
    combined_df.to_csv(combined_csv_path, index=False)

    print(f"Combined CSV file saved to {combined_csv_path}")

combine_files(r'D:\Yash\Projects\IPL-2024\Output Files\batting cleaned',r'D:\Yash\Projects\IPL-2024\Output Files - 2022\Combined\batting_combined.csv')
combine_files(r'D:\Yash\Projects\IPL-2024\Output Files\bowling cleaned',r'D:\Yash\Projects\IPL-2024\Output Files - 2022\Combined\bowlingcombined.csv')
combine_files(r'D:\Yash\Projects\IPL-2024\CSV Data\potm',r'D:\Yash\Projects\IPL-2024\Output Files - 2022\Combined\potm_combined.csv')
combine_files(r'D:\Yash\Projects\IPL-2024\CSV Data\extra runs',r'D:\Yash\Projects\IPL-2024\Output Files - 2022\Combined\rxtra_run_combined.csv')