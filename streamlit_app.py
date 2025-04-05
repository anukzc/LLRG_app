import streamlit as st

processor = st.Page("processor_streamlit.py", title="Data Processor", icon=":material/add_circle:")
plotter = st.Page("plotter_streamlit.py", title="Plotter", icon=":material/delete:")

pg = st.navigation([processor, plotter])
st.set_page_config(page_title="LLRG App", page_icon=":material/edit:")

pg.run()