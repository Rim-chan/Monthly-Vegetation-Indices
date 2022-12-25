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

    st.subheader("Define ROI")
    
    AFRICA_DIR = "projects/ee-plottings/assets/Africa"  
    AFRICA = ee.FeatureCollection(AFRICA_DIR)
    
    country_input = st.text_input("Country", label_visibility="collapsed")
    if country_input: 
        with st.spinner('Wait for it...'):
            COUNTRY = AFRICA.filter('ADM0_NAME == '+ country_input)
            Map = geemap.Map()
            Map.centerObject(COUNTRY, 6)
            Map.addLayer(COUNTRY, {}, country_input);
            Map.to_streamlit()
    

