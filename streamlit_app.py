import streamlit as st

processor = st.Page("processor_streamlit.py", title="Data Processor", icon=":material/file_save:") #file_save #edit_document
plotter = st.Page("plotter_streamlit.py", title="Plotter", icon=":material/line_axis:") #table_chart_view #line_axis #bar_chart_4_bars

pg = st.navigation([processor, plotter])
st.set_page_config(page_title="LLRG App", page_icon=":material/edit:")

pg.run()