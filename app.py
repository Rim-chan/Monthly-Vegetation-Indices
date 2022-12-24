import streamlit as st
from multiapp import MultiApp
from apps import monthly_veg_idx

st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Monthly Vegetation Indices", monthly_veg_idx.app)


# The main app
apps.run()
