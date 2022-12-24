import streamlit as st
from multiapp import MultiApp
from apps import Monthly_Vegetation_Indices

st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Monthly Vegetation Indices", Monthly_Vegetation_Indices.app)


# The main app
apps.run()
