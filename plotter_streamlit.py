# Author: Anuk Centellas
# This script uses the processed excel file and generates scatter plots
# For Jordan Sandoval and Kirsten Drickey's Spanish Language Learning Research

import io
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# function that cleans the data by smushing it into two fully filled columns of each response to one question category and 
# each response to the other category
def clean_data(df):
    # takes all responses from the two categories, makes sure they are all numeric values, turns then to NaNs if not
    category_x = df.filter(like=x_question.split(":")[0]).apply(pd.to_numeric, errors="coerce")
    category_y = df.filter(like=y_question.split(":")[0]).apply(pd.to_numeric, errors="coerce")

    # takes the first number per row for the whole category of the specified questions and puts them all into a single column
    df[x_question.split(":")[0]] = category_x.stack().groupby(level=0).first()
    df[y_question.split(":")[0]] = category_y.stack().groupby(level=0).first()

    # removes NaNs
    df_clean = df.dropna(subset=[x_question.split(":")[0], y_question.split(":")[0]])

    # returns the clean data
    return df_clean

# function to format the plot
def format_plot(ax):
    # sets the axes range for both x and y, from 0.5 to 7.5
    ax.set_xlim(0.5, 7.5)
    ax.set_ylim(0.5, 7.5)
    
# function to add jitter if the user specifies that they want jitter
def add_jitter(x_data, y_data, jitter_val=0.1):
    x_jitter = x_data + np.random.uniform(-jitter_val, jitter_val, len(x_data))
    y_jitter = y_data + np.random.uniform(-jitter_val, jitter_val, len(y_data))

    return x_jitter, y_jitter

# function that creates the plot with different shapes and colors for the experiemntal and control groups
def plot_for_differentiating_experimental_control(x_data, y_data, df, transparency=0.3, experimental_color='blue', control_color='orange', experimental_shape='*', control_shape='s'):
    global exp_best_fit_line, control_best_fit_line
    
    # gets the keys of each valid entry in the excel file, since invalid entries were removed, some numbers are skipped, so it is a dictionary rather than a list
    key_list = x_data.keys()
    fig, ax = plt.subplots()

    # initialize lists to store data to then use for plotting the best fit line
    experimental_x = []
    experimental_y = []
    control_x = []
    control_y = []

    # loops through all of the valid entries, using the keys
    for key in key_list:
        if df['Experimental Group'][key] == '0': # CONTROL GROUP
            # if the user selected to only plot experimental group, skip plotting these points
            if diff_group == "Experimental Only":
                continue
            ax.plot(x_data[key], y_data[key], alpha=transparency, marker=control_shape, c=control_color, linestyle='none') 
            # saving data for best fit line
            control_x.append(x_data[key])
            control_y.append(y_data[key])
        elif df['Experimental Group'][key] == '1': # EXPERIMENTAL GROUP
            # if the user selected to only plot control group, skip plotting these points
            if diff_group == "Control Only":
                continue
            ax.plot(x_data[key], y_data[key], alpha=transparency, marker=experimental_shape, c=experimental_color, linestyle='none')
            # saving data for best fit line
            experimental_x.append(x_data[key])
            experimental_y.append(y_data[key])
        # skips points where the experimental group is not 1 or 0 just incase, this is to avoid unforseen errors, but this case should never happen
        else:
            continue

    # gets the labels of the axes and title by taking the drop down menu input and taking the second element, which is the words rather than the Q#
    ax.set_xlabel(x_question.split(":")[1].strip())
    ax.set_ylabel(y_question.split(":")[1].strip())
    title = ax.set_title(x_question.split(":")[1].strip() + ' vs ' + y_question.split(":")[1].strip())
    
    # plots best fit line for experimental group points
    if exp_best_fit_line:
        exp_m, exp_b = np.polyfit(experimental_x, experimental_y, 1)
        x_fit = np.linspace(min(x_data), max(x_data), 100)
        ax.plot(x_fit, exp_m*x_fit+exp_b, color=experimental_color)

    # plots best fit line for control group points
    if control_best_fit_line:
        control_m, control_b = np.polyfit(control_x, control_y, 1)
        x_fit = np.linspace(min(x_data), max(x_data), 100)
        ax.plot(x_fit, control_m*x_fit+control_b, color=control_color)

    format_plot(ax) # format the axes for the plot

    st.pyplot(fig) # displays the plot in streamlit

    # this saves the plot in RAM as a stepping stone to saving it to files
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    # the title variable from ax.set_title has a weird format, and the part we care about is in between single quotes, so we split it at
    # those single quotes and grab the stuff in between them
    title = str(title).split("'")[1]
    filename = title.replace(" ", "_") # then replace spaces with underscores for proper file naming

    # creates a download button with the RAM version of the file and the name and saves it to files as a png
    st.download_button(label="Download Plot", data=buf, file_name=filename+".png", icon=":material/download:")
   
# function that creates the plot with different shapes and colors for the upper and lower division students
def plot_for_differentiating_division(x_data, y_data, df, transparency=0.3, upper_color='lime', lower_color='magenta', upper_shape='^', lower_shape='o'):
    global upper_best_fit_line, lower_best_fit_line
    
    # gets the keys of each valid entry in the excel file, since invalid entries were removed, some numbers are skipped, so it is a dictionary rather than a list
    key_list = x_data.keys()
    fig, ax = plt.subplots()

    # initialize lists to store data to then use for plotting the best fit line
    lower_x = []
    lower_y = []
    upper_x = []
    upper_y = []

    # loops through all of the valid entries, using the keys
    for key in key_list:
        if df['Division'][key] == 0: # LOWER DIVISION
            # if the user selected to only plot upper division, skips plotting these points
            if div_group == "Upper Division Only":
                continue
            ax.plot(x_data[key], y_data[key], alpha=transparency, marker=lower_shape, c=lower_color, linestyle='none') 
            lower_x.append(x_data[key])
            lower_y.append(y_data[key])
        elif df['Division'][key] == 1: # UPPER DIVISION
            # if the user selected to only plot lower division, skips plottin these points
            if div_group == "Lower Division Only":
                continue
            ax.plot(x_data[key], y_data[key], alpha=transparency, marker=upper_shape, c=upper_color, linestyle='none')
            upper_x.append(x_data[key])
            upper_y.append(y_data[key])
        # skips points where the Division value is not 1 or 0 just incase
        else:
            continue

    # gets the labels of the axes and title by taking the drop down menu input and taking the second element, which is the words rather than the Q#
    ax.set_xlabel(x_question.split(":")[1].strip())
    ax.set_ylabel(y_question.split(":")[1].strip())
    title = ax.set_title(x_question.split(":")[1].strip() + ' vs ' + y_question.split(":")[1].strip())

    # plots best fit line for upper division points
    if upper_best_fit_line:
        upper_m, upper_b = np.polyfit(upper_x, upper_x, 1)
        x_fit = np.linspace(min(x_data), max(x_data), 100)
        ax.plot(x_fit, upper_m*x_fit+upper_b, color=upper_color)

    # plots best fit line for lower division points
    if lower_best_fit_line:
        lower_m, lower_b = np.polyfit(lower_x, lower_y, 1)
        x_fit = np.linspace(min(x_data), max(x_data), 100)
        ax.plot(x_fit, lower_m*x_fit+lower_b, color=lower_color)

    format_plot(ax) # format the axes for the plot

    st.pyplot(fig) # displays the plot in streamlit

    # this saves the plot in RAM as a stepping stone to saving it to files
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    # the title variable from ax.set_title has a weird format, and the part we care about is in between single quotes, so we split it at
    # those single quotes and grab the stuff in between them
    title = str(title).split("'")[1]
    filename = title.replace(" ", "_") # then replace spaces with underscores

    # creates a download button with the RAM version of the file and the name and saves it to files as a png
    st.download_button(label="Download Plot", data=buf, file_name=filename+".png", icon=":material/download:")
   
# function that creates a plot with different colors for experimental and control and different shapes for upper and lower division
def plot_for_differentiating_both(x_data, y_data, df, transparency=0.3, experimental_color='blue', control_color='orange', upper_shape='^', lower_shape='o'):
    # gets the keys of each valid entry in the excel file, since invalid entries were removed, some numbers
    # are skipped, so it is a dictionary rather than a list
    key_list = x_data.keys()
    fig, ax = plt.subplots()

    # loops through all of the valid entries, using the keys
    for key in key_list:
        # for students in the control group
        if df['Experimental Group'][key] == '0':
            # for lower division students
            if df['Division'][key] == 0:
                ax.plot(x_data[key], y_data[key], alpha=transparency, marker=lower_shape, c=control_color, linestyle='none')
            # for upper division students
            elif df['Division'][key] == 1:
                ax.plot(x_data[key], y_data[key], alpha=transparency, marker=upper_shape, c=control_color, linestyle='none')
            else:
                continue
        # for students in the experimental group
        elif df['Experimental Group'][key] == '1':
            # for lower division students
            if df['Division'][key] == 0:
                ax.plot(x_data[key], y_data[key], alpha=transparency, marker=lower_shape, c=experimental_color, linestyle='none')
            # for upper division students
            elif df['Division'][key] == 1:
                ax.plot(x_data[key], y_data[key], alpha=transparency, marker=upper_shape, c=experimental_color, linestyle='none')
            else:
                continue 
        # skips points where the experimental group is not 1 or 0 just incase
        else:
            continue

    # gets the labels of the axes and title by taking the drop down menu input and taking the second element, which is the words rather than the Q#
    ax.set_xlabel(x_question.split(":")[1].strip())
    ax.set_ylabel(y_question.split(":")[1].strip())
    title = ax.set_title(x_question.split(":")[1].strip() + ' vs ' + y_question.split(":")[1].strip())
    
    format_plot(ax) # format the axes for the plot

    st.pyplot(fig) # displays the plot in streamlit

    # this saves the plot in RAM as a stepping stone to saving it to files
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    # the title variable from ax.set_title has a weird format, and the part we care about is in between single quotes, so we split it at
    # those single quotes and grab the stuff in between them
    title = str(title).split("'")[1]
    filename = title.replace(" ", "_") # then replace spaces with underscores

    # creates a download button with the RAM version of the file and the name and saves it to files as a png
    st.download_button(label="Download Plot", data=buf, file_name=filename+".png", icon=":material/download:")

# function to create a plot where are the dots are the same color and shape regardless of experimental or control group
def plot_without_differentiation(x_data, y_data, transparency = 0.1):
    fig, ax = plt.subplots()
    ax.scatter(x_data, y_data, alpha=transparency)

    # gets the labels of the axes and title by taking the drop down menu input and taking the second element, which is the words rather than the Q#
    ax.set_xlabel(x_question.split(":")[1].strip())
    ax.set_ylabel(y_question.split(":")[1].strip())
    title = ax.set_title(x_question.split(":")[1].strip() + ' vs ' + y_question.split(":")[1].strip())
    
    format_plot(ax) # format the axes for the plot
    
    st.pyplot(fig) # displays plot in streamlit
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    title = str(title).split("'")[1]
    filename = title.replace(" ", "_")

    st.download_button(label="Download Plot", data=buf, file_name=filename+".png", icon=":material/download:")
   
# main function to produce the specific pltos
def plot(df):
    global jitter_select, advanced, diff_select, division_select

    # get the clean data
    df = clean_data(df)

    # get the data for the x axis and y axis
    x_data = df[x_question.split(":")[0]]
    y_data = df[y_question.split(":")[0]]

    # if jitter is Yes, then we replace our data with the jittered version
    if jitter_select == "Yes":
        # if the advanced settings are turned on, then we use the user selected jitter value
        if advanced:
            x_data, y_data = add_jitter(x_data, y_data, jitter)
        else:
            x_data, y_data = add_jitter(x_data, y_data)

    # if differentiating between experimental and control is Yes
    if diff_select == "Yes":
        # if differentiating between division is Yes
        if division_select == "Yes":
            # if advanced settings are on
            if advanced:
                plot_for_differentiating_both(x_data, y_data, df, transparency, experimental_color, control_color, upper_shape, lower_shape)
            # if advanced settings are off
            else:
                plot_for_differentiating_both(x_data, y_data, df)
        # if differentiation between division is No
        else:
            if advanced:
                plot_for_differentiating_experimental_control(x_data, y_data, df, transparency, experimental_color, control_color, experimental_shape, control_shape)
            else:
                plot_for_differentiating_experimental_control(x_data, y_data, df)
    # if differentiating between experimental and control is No
    else:
        # if differentiating between division is Yes
        if division_select == "Yes": 
            if advanced:
                plot_for_differentiating_division(x_data, y_data, df, transparency, upper_color, lower_color, upper_shape, lower_shape)
            else:
                plot_for_differentiating_division(x_data, y_data, df)
        # if both are No
        else:
            if advanced:
                plot_without_differentiation(x_data, y_data, transparency)
            else:
                plot_without_differentiation(x_data, y_data)
    
# main method
if __name__ == '__main__':

    st.title(body="Welcome to the LLRG plotter!")

    # creates the upload file widget
    uploaded_file = st.file_uploader(label="Choose the file with the data you want to plot:", type="xlsx")
    
    # once a file is selected, the rest of the elements are displayed
    if uploaded_file is not None:
        # sets df as the datafram that holds the data from the uploaded file
        df = pd.read_excel(uploaded_file)

        question_options = ["Q4: Anxiety", "Q5: Attitudes", "Q6: Classroom Environment", "Q7: Confidence", "Q8: Independent Practice", "Q9: Measures of Student Success", "Q10: Motivation", "Q11: Departmental Measures of Success"]

        # displays two drop down menus for the x and y axes
        x_question = st.selectbox(label="Select the category to be displayed on the **x axis**:", options=question_options, index=0)
        y_question = st.selectbox(label="Select the category to be displayed on the **y axis**:", options=question_options, index=0)

        # displays two drop down menus for selecting jitter, differentiating between experimental and control, and differentiating between division
        jitter_select = st.selectbox(label="Select if you want **jitter** in your plot:", options=["Yes", "No"], index=0)
        diff_select = st.selectbox(label="Select if you want to differentiate between **experimental and control**:", options=["Yes", "No"], index=0)
        division_select = st.selectbox(label="Select if you want to differentiate between **upper and lower division**:", options=["Yes", "No"], index=1)

        # if exp/control and upper/lower are not both Yes, then allow the user to select only a subgroup to plot
        if diff_select == "Yes" and division_select == "No":
            diff_group = st.selectbox(label="Select which groups you would like to plot:", options=["Both", "Experimental Only", "Control Only"])
        if diff_select == "No" and division_select == "Yes":
            div_group = st.selectbox(label="Select which groups you would like to plot:", options=["Both", "Upper Division Only", "Lower Division"])

        # if at least one of them is No, then display checkboxes so the user can select best fit line options
        if diff_select == "No" or division_select == "No":
            if diff_select == "Yes":
                if diff_group == "Both":
                    exp_best_fit_line = st.checkbox(label="Show Best Fit Line for Experimental Group")
                    control_best_fit_line = st.checkbox(label="Show Best Fit Line for Control Group")
                elif diff_group == "Experimental Only":
                    exp_best_fit_line = st.checkbox(label="Show Best Fit Line for Experimental Group")
                    control_best_fit_line = False # necessary to set this to False so that there is no variable undefined errors later, since the code assumes that this variable exists
                elif diff_group == "Control Only":
                    exp_best_fit_line = False
                    control_best_fit_line = st.checkbox(label="Show Best Fit Line for Control Group")
            elif division_select == "Yes":
                if div_group == "Both":
                    upper_best_fit_line = st.checkbox(label="Show Best Fit Line for Upper Division")
                    lower_best_fit_line = st.checkbox(label="Show Best Fit Line for Lower Division")
                elif div_group == "Upper Division Only":
                    upper_best_fit_line = st.checkbox(label="Show Best Fit Line for Upper Division")
                    lower_best_fit_line = False
                elif div_group == "Lower Division Only":
                    upper_best_fit_line = False
                    lower_best_fit_line = st.checkbox(label="Show Best Fit Line for Lower Division")

        # displays a toggle to open the advanced settings options
        advanced = st.toggle(label="Advanced Settings")

        # if the toggle is on, it displays additional drop down menus, including transparency and jitter
        if advanced:
            transparency_options = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            transparency = st.selectbox(label="Select the **transparency** level for the dots:", options=transparency_options, index=1)
            jitter_options = [0.05, 0.10, 0.15, 0.20]
            jitter = st.selectbox(label="Select the amount of **jitter** you want in your plot:", options=jitter_options, index=1)

            color_options = ['red', 'orange', 'yellow', 'green', 'lime', 'blue', 'cyan', 'purple', 'magenta']
            shape_options = ['square', 'star', 'dot', 'triangle', 'plus']
            shape_options_dictionary = {'square': 's', 'star': '*', 'dot': 'o', 'triangle': '^', 'plus':'+'}

            # allows the user to select the color and shape for each subgroup of students
            # all of these logic branches are to account for all possibe combinations of selections that the user can make
            if diff_select == "Yes" and division_select == "Yes":
                experimental_color = st.selectbox(label="Select the **color** for the **experimental** group:", options=color_options, index=5)
                control_color = st.selectbox(label="Select the **color** for the **control** group:", options=color_options, index=1)
                upper_select = st.selectbox(label="Select the **shape** for the **upper division** students:", options=shape_options, index=3)
                upper_shape = shape_options_dictionary[upper_select]
                lower_select = st.selectbox(label="Select the **shape** for the **lower division** students:", options=shape_options, index=2)
                lower_shape = shape_options_dictionary[lower_select]

            elif diff_select == "Yes":
                if diff_group == "Both":
                    experimental_color = st.selectbox(label="Select the **color** for the **experimental** group:", options=color_options, index=5)
                    control_color = st.selectbox(label="Select the **color** for the **control** group:", options=color_options, index=1)
                    experimental_select = st.selectbox(label="Select the **shape** for the **experimental** group:", options=shape_options, index=1)
                    experimental_shape = shape_options_dictionary[experimental_select]
                    control_select = st.selectbox(label="Select the **shape** for the **control** group:", options=shape_options, index=0)
                    control_shape = shape_options_dictionary[control_select]
                elif diff_group == "Experimental Only":
                    experimental_color = st.selectbox(label="Select the **color** for the **experimental** group:", options=color_options, index=5)
                    experimental_select = st.selectbox(label="Select the **shape** for the **experimental** group:", options=shape_options, index=1)
                    experimental_shape = shape_options_dictionary[experimental_select]
                    control_color = None # necessary to set this to None so that there is no variable undefined errors later, since the code assumes that this variable exists
                    control_shape = None
                elif diff_group == "Control Only":
                    control_color = st.selectbox(label="Select the **color** for the **control** group:", options=color_options, index=1)
                    control_select = st.selectbox(label="Select the **shape** for the **control** group:", options=shape_options, index=0)
                    control_shape = shape_options_dictionary[control_select]
                    experimental_color = None
                    experimental_shape = None

            elif division_select == "Yes":
                if div_group == "Both":
                    upper_color = st.selectbox(label="Select the **color** for the **upper division** students:", options=color_options, index=4)
                    lower_color = st.selectbox(label="Select the **color** for the **lower division** students:", options=color_options, index=8)
                    upper_select = st.selectbox(label="Select the **shape** for the **upper division** students:", options=shape_options, index=3)
                    upper_shape = shape_options_dictionary[upper_select]
                    lower_select = st.selectbox(label="Select the **shape** for the **lower division** students:", options=shape_options, index=2)
                    lower_shape = shape_options_dictionary[lower_select]
                elif div_group == "Upper Division Only":
                    upper_color = st.selectbox(label="Select the **color** for the **upper division** students:", options=color_options, index=4)
                    upper_select = st.selectbox(label="Select the **shape** for the **upper division** students:", options=shape_options, index=3)
                    upper_shape = shape_options_dictionary[upper_select]
                    lower_color = None
                    lower_shape = None
                elif div_group == "Lower Division Only":
                    lower_color = st.selectbox(label="Select the **color** for the **lower division** students:", options=color_options, index=8)
                    lower_select = st.selectbox(label="Select the **shape** for the **lower division** students:", options=shape_options, index=2)
                    lower_shape = shape_options_dictionary[lower_select]
                    upper_color = None
                    upper_shape = None

        # displays a button that, when clicked, will display the specified plot
        if st.button(label="Show Plot"):
            plot(df)