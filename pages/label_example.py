from PIL import Image
import streamlit as st
from streamlit_sparrow_labeling import st_sparrow_labeling
import json
import streamlit_javascript as st_js
import fitz  # PyMuPDF


st.set_page_config(page_title="Sparrow Labeling", layout="wide")

def run(img_file, label_data_file):
    ui_width = st_js.st_javascript("window.innerWidth")
    img = Image.open(img_file)
    
    if 'saved_state' not in st.session_state:
        with open(label_data_file, "r") as f:
            saved_state = json.load(f)
            st.session_state['saved_state'] = saved_state
    else:
        saved_state = st.session_state['saved_state']
    
    height = 1296
    width = 864
    doc_height = img.height
    doc_width  = img.width

    result_rects = st_sparrow_labeling(
       fill_color="rgba(0, 151, 255, 0.3)",
            stroke_width=2,
            stroke_color="rgba(0, 50, 255, 0.7)",
            background_image=img,
            initial_rects=saved_state,
            height=height,
            width=width,
            drawing_mode=mode,
            display_toolbar=True,
            update_streamlit=True,
            canvas_width=canvas_width,
            doc_height=doc_height,
            doc_width=doc_width,
            image_rescale=True,
            key="doc_annotation"
    )
    
    
    # st.image(img)



# Set page width to half of the screen width

st.title("PDF Viewer")

# File uploader
pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

# Number input field
page_number = st.number_input(
    "Page number", min_value=1, value=1, step=1)

# Display selected page
if pdf_file is not None:
    # pdf_layout = lp.load_pdf(pdf_file)
    doc =  fitz.open(stream=pdf_file.read(), filetype="pdf")
    zoom = 1  
    mat = fitz.Matrix(zoom, zoom)
    count = doc.page_count  # Use the built-in page count property
    
    # Make sure the selected page number is within bounds
    # page_number = max(1, min(count, page_number))
    col1, col2 = st.columns(2)
    with col1:
        val = f"image_{page_number}.png"
        page = doc.load_page(page_number-1)  # Page numbers start from 0 in PyMuPDF
        pix = page.get_pixmap(matrix=mat)
        pix.save(val)
        # st.image(val)
        img_file = val
        label_data_file = "docs/json/download.json"
        run(img_file, label_data_file)

    with col2:
        page_number = st.number_input("Page number", min_value=1, max_value=count, value=page_number, step=1)

    # Extract the selected page as an image
    
    
    # Display the image and the number input field
    
    # Clean up
    doc.close()




