# Author: Anuk Centellas
# This script takes two excel files and appends the new data to the main file
# For Jordan Sandoval and Kirsten Drickey's Spanish Language Learning Research

import io
import pandas as pd
import streamlit as st

def get_times_taken(df):
    seen_wnums_counts = {}
    cell_vals = []
    for idx, row in df.iterrows():
        if idx == 0:
            cell = ''
        else:
            wnum = row['Q2.1']
            if pd.isna(wnum):
                cell = 1
            elif wnum not in seen_wnums_counts:
                cell = 1
                seen_wnums_counts[wnum] = 1
            elif wnum in seen_wnums_counts:
                cell = seen_wnums_counts[wnum] + 1
                seen_wnums_counts[wnum] = seen_wnums_counts[wnum] + 1
        cell_vals.append(cell)
    return cell_vals
            

if __name__ == '__main__':

    st.title(body="Welcome to the LLRG merger!")

    main_file = st.file_uploader(label='Upload the main file with all of the data', type='xlsx')
    new_data = st.file_uploader(label='Upload the new file you want to append to the main file', type='xlsx')

    if main_file is not None and new_data is not None:
        # header=None makes the file not require the header row to be present, skiprows=2 skips the first two rows which are the headers
        df_new = pd.read_excel(new_data, header=None, skiprows=2)

        df_main = pd.read_excel(main_file)

        # assignes the columns of the new file to be the columns of the main file since we stripped the headers
        df_new.columns = df_main.columns

        df_merged = pd.concat([df_main, df_new], ignore_index=True)

        # prevents the boolean True and False values in the Finished columns from becoming all caps
        df_merged['Finished'] = df_merged['Finished'].astype(str)

        # add the option to toggle on sorting by W number
        sort = st.toggle(label="Sort by W number", value=True)

        if sort:
            question_row = df_merged.iloc[[0]]   # double brackets keep it as a DataFrame
            responses = df_merged.iloc[1:].sort_values(by=["Q2.1", "StartDate"], ascending=True)
            df_merged = pd.concat([question_row, responses])


        df_merged['Times Taken'] = get_times_taken(df_merged)


        # put the data into excel format without actually saving it to your files
        output_file = io.BytesIO()
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            df_merged.to_excel(writer, index=False)
        output_file.seek(0)

        # displays a button to download the processed file
        st.download_button(label="Download Merged Data", data=output_file, file_name='all_data.xlsx', icon=":material/download:")
