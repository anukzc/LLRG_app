# Author: Anuk Centellas
# This script processes an excel sheet downloaded from Qualtrics and saves a new
# modified version that looks the way LLRG needs it
# For Jordan Sandoval and Kirsten Drickey's Spanish Language Learning Research

import io
import pandas as pd
import streamlit as st

# function that determines which columns to drop
def drop_determiner(data, prefixes) :
    # initialize empty list of columns to drop
    cols_to_drop = []
    for col in data :
        for prefix in prefixes :
            if col.startswith(prefix) :
                cols_to_drop.append(col)
    return cols_to_drop

# function that changes the likert scale responses to their corresponding numbers
def likert_to_num(data, cols, dict) :
    data[cols] = data[cols].replace(dict)
    return data

# function that adds a W to the W number if it is missing
def add_W(data, col) :
    # setting cell to start at 1 is so that it skips the first cell, which is the question
    for cell in range(1, len(data)) :
        num = str(data.at[cell, col])
        # if the number doesn't start with W and is not empty/nan, add a W
        if not num.startswith("W") and not pd.isna(num) and not num.strip() == "" and not num == "nan":
            data.at[cell, col] = "W" + num
        # if the number starts with lowercase w, replace it with uppercase W
        if num.startswith("w") :
            data.at[cell, col] = "W" + num[1:]
    return data

# function that adds
def add_upper_lower_division(data, division_vals) :
    for cell in data['Q3.1'].fillna(''):
        if ('30' in cell) or ('31' in cell) or ('33' in cell) or ('34' in cell) or ('35' in cell) or ('44' in cell) or ('45' in cell):
            division = 1
        else :
            division = 0
        division_vals.append(division)
    return division_vals

# main method
if __name__=="__main__" :

    st.title(body="Welcome to the LLRG processor!")

    # creates the upload file widget
    uploaded_file = st.file_uploader(label="Choose the file with the data you want to process:", type="xlsx")
    
    # once the file is uploaded, read it as a dataframe
    if uploaded_file is not None:

        data = pd.read_excel(uploaded_file)
    
        # gets the list of names of all the columns from the file
        data_cols = list(data.columns)

        # to drop columns

        # make a list of column names to drop
        prefixes = ["Status", "IPAddress", "Duration (in seconds)", "RecordedDate", "ResponseId", 
                    "RecipientLastName", "RecipientFirstName", "RecipientEmail", "ExternalReference", 
                    "LocationLatitude", "LocationLongitude", "DistributionChannel", "UserLanguage"]

        # gets a list of all the columns to drop
        cols_to_drop = drop_determiner(data.columns, prefixes)

        # new data after the columns have been dropped
        # axis 1 is cols
        # axis 0 is rows
        # inplace True edits the file itself
        # inplace False creates a copy of the file and leaves the original file as it was
        data = data.drop(cols_to_drop, axis=1, inplace=False) 

        data = add_W(data, "Q2.1")

        # adds a column at the end of the excel file with a 1 if the student is upper division and a 0 if they are lower division
        division_vals = []
        data["Division"] = add_upper_lower_division(data, division_vals)

        # changing likert scale values to numbers
        likert_cols = ["Q4.1", "Q4.2", "Q4.3", "Q4.4", "Q4.5", "Q4.6", "Q4.7", "Q5.1", "Q5.2", "Q5.3", 
                    "Q5.4", "Q5.5", "Q5.6" , "Q6.1", "Q6.2", "Q6.3", "Q6.5", "Q6.6", "Q6.7", "Q7.1",
                    "Q7.2", "Q7.3", "Q7.4", "Q7.5", "Q7.6", "Q7.7", "Q7.8", "Q7.9", "Q7.10", "Q7.12", 
                    "Q8.1", "Q8.2", "Q8.3", "Q8.4", "Q8.5", "Q8.6", "Q8.7", "Q8.8", "Q9.1", "Q9.2", 
                    "Q9.3", "Q9.4", "Q9.5", "Q10.1", "Q10.2", "Q10.3", "Q10.4", "Q10.5", "Q10.6", 
                    "Q11.1", "Q11.2", "Q11.3", "Q11.4", "Q11.5", "Q11.6", "Q11.7", "Q11.8", "Q11.9", 
                    "Q11.10", "Q11.11", "Q11.12", "Q11.13", "Q11.14"]
        
        # dictionary to match likert string with corresponding number
        # want the number to be an int
        replacement_dict = {
            "Strongly Agree": 7,
            "Agree" : 6,
            "Somewhat Agree": 5,
            "Neither Agree Nor Disagree": 4,
            "Somewhat Disagree": 3,
            "Disagree": 2,
            "Strongly Disagree": 1
        }

        data = likert_to_num(data, likert_cols, replacement_dict)

        # for the two questions where we wanted to reverse the likert scale values
        likert_cols_to_reverse = ["Q6.4", "Q7.11"]

        reverse_dict = {
            "Strongly Agree": 1,
            "Agree" : 2,
            "Somewhat Agree": 3,
            "Neither Agree Nor Disagree": 4,
            "Somewhat Disagree": 5,
            "Disagree": 6,
            "Strongly Disagree": 7
        }

        data = likert_to_num(data, likert_cols_to_reverse, reverse_dict)

        # put the data into excel format without actually saving it to your files
        output_file = io.BytesIO()
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False)
        output_file.seek(0)

        # displays a button to download the processed file
        st.download_button(label="Download Processed Data", data=output_file, file_name="processed_" + uploaded_file.name, icon=":material/download:")