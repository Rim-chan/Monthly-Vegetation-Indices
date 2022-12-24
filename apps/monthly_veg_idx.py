import streamlit as st
import leafmap.foliumap as leafmap
import ee, geemap
import time
geemap.ee_initialize()

from src.args import *
from src.cloud_mask import *
from src.indices import *
from src.monthly_composites import *


def app():
    st.title("Monthly Vegetation Indices")
    
    start_time = time.time()
    args = get_main_args()
