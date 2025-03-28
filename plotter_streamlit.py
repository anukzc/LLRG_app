# Author: Anuk Centellas
# This script uses the processed excel file and generates scatter plots
# For Jordan Sandoval and Kirsten Drickey's Spanish Language Learning Research

import io
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# function that cleans the data by smushing it into two fully filled columns of each response to one question category and each response to the other category
def clean_data(df):
    # takes all responses from the two categories, makes sure they are all numeric values, turns then to NaNs if not
    category_x = df.filter(like=x_question.split(":")[0]).apply(pd.to_numeric, errors="coerce")
    category_y = df.filter(like=y_question.split(":")[0]).apply(pd.to_numeric, errors="coerce")

    # takes the first number per row for the whole category of the specified questions and puts them all into a single column
    df[x_question.split(":")[0] + ' response'] = category_x.stack().groupby(level=0).first()
    df[y_question.split(":")[0] + ' response'] = category_y.stack().groupby(level=0).first()

    # removes NaNs
    df_clean = df.dropna(subset=[x_question.split(":")[0] + ' response', y_question.split(":")[0] + ' response'])

    # returns the clean data
    return df_clean

# function to format the plot
def format_plot():
    # sets the axes range for both x and y, from 0.5 to 7.5
    plt.xlim(0.5, 7.5)
    plt.ylim(0.5, 7.5)
    
# function to add jitter if the user specifies that they want jitter
def jitter(x_data, y_data):
    x_jitter = x_data + np.random.uniform(-0.1, 0.1, len(x_data))
    y_jitter = y_data + np.random.uniform(-0.1, 0.1, len(y_data))

    return x_jitter, y_jitter

def plot_for_differentiating_experimental_control(x_data, y_data, df):
    key_list = x_data.keys()
    fig, ax = plt.subplots()
    for key in key_list:
        # breakpoint()
        # for students not in the experimental group
        if df['Experimental Group'][key] == '0':
            ax.plot(x_data[key], y_data[key], alpha=0.33, marker='s', c='orange', linestyle='none') 
        # for students in the experimental group
        elif df['Experimental Group'][key] == '1':
            ax.plot(x_data[key], y_data[key], alpha=0.33, marker='*', c='blue', linestyle='none')
        # skips points where the experimental group is not 1 or 0 just incase
        else:
            continue

    ax.set_xlabel(x_question.split(":")[1].strip())
    ax.set_ylabel(y_question.split(":")[1].strip())
    title = ax.set_title(x_question.split(":")[1].strip() + ' vs ' + y_question.split(":")[1].strip())
    st.pyplot(fig)

    # buf = io.BytesIO()
    # fig.savefig(buf, format="png")
    # buf.seek(0)

    st.download_button(label="Download Plot", data=fig.savefig(str(title)+".png"), file_name=title+".png")
   
def plot_without_differentiation(x_data, y_data):
    fig, ax = plt.subplots()
    ax.scatter(x_data, y_data, alpha=0.1)
    ax.set_xlabel(x_question.split(":")[1].strip())
    ax.set_ylabel(y_question.split(":")[1].strip())
    title = ax.set_title(x_question.split(":")[1].strip() + ' vs ' + y_question.split(":")[1].strip())
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    st.download_button(label="Download Plot", data=buf, file_name=title+".png")

# main function that produces the final pltos
def plot(df):
    # get the clean data
    df = clean_data(df)

    # format the axes for the plot
    format_plot()

    # get the data for the x axis and y axis
    x_data = df[x_question.split(":")[0] + ' response']
    y_data = df[y_question.split(":")[0] + ' response']

    # jitter 
    if jitter_select == "Yes":
        x_data, y_data = jitter(x_data, y_data)

    # transparency?

    # differentiating b/w experimental and control
    if diff_select == "Yes":
        plot_for_differentiating_experimental_control(x_data, y_data, df)
    else:
        plot_without_differentiation(x_data, y_data)
    

# main method
if __name__ == '__main__':

    st.title(body="Welcome to the LLRG plotter!")

    uploaded_file = st.file_uploader(label="Choose the file with the data you want to plot:", type="xlsx")
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        question_options = ["Q4: Anxiety", "Q5: Attitudes", "Q6: Classroom Environment", "Q7: Confidence", "Q8: Independent Practice", "Q9: Measures of Student Success", "Q10: Motivation", "Q11: Departmental Measures of Success"]

        x_question = st.selectbox(label="Select the category to be displayed on the x axis:", options=question_options, index=0)
        y_question = st.selectbox(label="Select the category to be displayed on the y axis:", options=question_options, index=0)

        jitter_select = st.selectbox(label="Select if you want jitter in your plot:", options=["Yes", "No"], index=0)
        diff_select = st.selectbox(label="Select if you want to differentiate between experimental and control:", options=["Yes", "No"], index=0)

        if st.button(label="Plot"):
            plot(df)