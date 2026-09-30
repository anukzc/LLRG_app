# LLRG App

A Streamlit app for the Language Learning Research Group (LLRG) at Western Washington University. It processes, merges, and plots Qualtrics survey data for Jordan Sandoval and Kirsten Drickey's Spanish language learning research.

**Live app:** https://llrgapp.streamlit.app/

**Publication for senior capstone project:** [Improving Language Learning](https://mabel.wwu.edu/do/deef27e7-cc40-465d-ac82-40c3b31da1d0)

## Pages

The app has three pages:

### 1. Data Processor

Upload an `.xlsx` export from Qualtrics and download a cleaned copy (`processed_<filename>.xlsx`). The processor:

- Removes Qualtrics metadata columns (IP address, location, recipient info, duration, etc.)
- Standardizes student ID numbers
- Adds a `Division` column from the course (`1` = upper division, `0` = lower division)
- Converts Likert responses to numbers from 1 (Strongly Disagree) to 7 (Strongly Agree)
- Adds an empty `Times Taken` column

### 2. Data Plotter

Upload a processed file to make a scatter plot comparing two survey categories (Anxiety, Attitudes, Classroom Environment, Confidence, Independent Practice, Measures of Student Success, Motivation, and Departmental Measures of Success). Options include:

- Jitter to separate overlapping points
- Color and shape by experimental/control group, by upper/lower division, or both
- Plotting only one subgroup
- Best-fit lines for each group
- Advanced settings for transparency, jitter amount, colors, and marker shapes

Plots can be downloaded as PNG files.

> The plotter expects an `Experimental Group` column (`1` = experimental, `0` = control) and the `Division` column added by the processor.

### 3. File Merger

Upload the main data file and a new file to append to it, then download the combined `all_data.xlsx`. The merger:

- Skips the first two (header) rows of the new file and uses the main file's column names
- Optionally sorts responses by student ID number and start date, keeping the question row at the top
- Fills in `Times Taken` with how many times each student has taken the survey

## Running locally

Requires Python 3.11 or newer.

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app opens at http://localhost:8501.

## Project structure

| File | Purpose |
| --- | --- |
| `streamlit_app.py` | Entry point that sets up navigation between the pages |
| `processor_streamlit.py` | Data Processor page |
| `excel_merger.py` | File Merger page |
| `plotter_streamlit.py` | Data Plotter page |
| `requirements.txt` | Python dependencies |
| `.devcontainer/` | Configuration for GitHub Codespaces / VS Code dev containers |

## Author

Anuk Centellas
