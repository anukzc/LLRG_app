import streamlit as st

processor = st.Page("processor_streamlit.py", title="Data Processor", icon=":material/file_save:") #edit_document
plotter = st.Page("plotter_streamlit.py", title="Plotter", icon=":material/table_chart_view:") #line_axis 

pg = st.navigation([processor, plotter])
st.set_page_config(page_title="LLRG App", page_icon=":material/edit:")

pg.run()