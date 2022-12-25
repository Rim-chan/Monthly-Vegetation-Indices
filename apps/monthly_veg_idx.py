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


    input_indcies = (
            "NDVI",
            "SAVI",
            "MSAVI2",
            "NDWI"
        )
    
    dates = [i + ' ' + str(j) for j in args.years for i in list(args.calendar.keys())]
    
    col1, col2 = st.columns(2)
    country = col1.selectbox("Indices", input_indcies, label_visibility="collapsed")    
    d = col2.selectbox("Dates", dates, label_visibility="collapsed")
    
    @st.cache(allow_output_mutation=True)
    def get_S2_dataset():
        
        S2Col = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
              .select(['QA60', 'B2', 'B3', 'B4', 'B8', 'B12'])\
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', args.cloud_coverage_percentage))\
              .map(cloud_mask)\
              .map(compute_msavi2) \
              .map(compute_savi) \
              .map(compute_ndvi) \
              .map(compute_ndwi) 

        monthly_ndvi = monthly_Data (S2Col.select('NDVI'), args.years, list(args.calendar.values()))  
        monthly_ndwi = monthly_Data (S2Col.select('NDWI'), args.years, list(args.calendar.values()))  
        monthly_savi = monthly_Data (S2Col.select('SAVI'), args.years, list(args.calendar.values()))  
        monthly_msavi2 = monthly_Data (S2Col.select('MSAVI2'), args.years, list(args.calendar.values())) 

        ndvi_img_list = monthly_ndvi.toList(monthly_ndvi.size().getInfo())
        ndwi_img_list = monthly_ndwi.toList(monthly_ndwi.size())
        savi_img_list = monthly_savi.toList(monthly_savi.size())
        msavi2_img_list = monthly_msavi2.toList(monthly_msavi2.size())

        return ndvi_img_list, ndwi_img_list, savi_img_list, msavi2_img_list
        
        
      
    ndvi_img_list, ndwi_img_list, savi_img_list, msavi2_img_list =  get_S2_dataset()
    
    idx = tuple(dates).index(d)
    ndvi_image = ee.Image(ndvi_img_list.get(idx))
    ndwi_image = ee.Image(ndwi_img_list.get(idx))
    savi_image = ee.Image(savi_img_list.get(idx))
    msavi2_image = ee.Image(msavi2_img_list.get(idx))
    
    
    Map = geemap.Map() 
    Map.centerObject(COUNTRY, 6)
#     Map.addLayer(S2Col.mosaic().clip(COUNTRY), args.RGBvis, 'S2 True Color') 
    Map.addLayer(ndvi_image.clip(COUNTRY), args.ndviVIS, 'S2 NDVI') 
    Map.to_streamlit()
