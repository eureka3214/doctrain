from PIL import Image
import streamlit as st
from streamlit_sparrow_labeling import st_sparrow_labeling
import json
import streamlit_javascript as st_js


st.set_page_config(page_title="Sparrow Labeling", layout="wide")

def run(img_file, label_data_file):
    ui_width = st_js.st_javascript("window.innerWidth")
    img = Image.open(img_file)
    
   
    result_rects = st_sparrow_labeling(
        fill_color="rgba(0, 151, 255, 0.3)",
        stroke_width=2,
        stroke_color="rgba(0, 50, 255, 0.7)",
        background_image=img,
  
        drawing_mode="rect",
        display_toolbar=True,
        update_streamlit=True,
        canvas_width=ui_width,
        key="doc_annotation"
    )
    
    if result_rects is not None:
        with open(label_data_file, "w") as f:
            json.dump(result_rects.rects_data, f, indent=2)
 
    
    st.image(img)

img_file = "docs/image/download.png"
label_data_file = "docs/json/download.json"
run(img_file, label_data_file)

