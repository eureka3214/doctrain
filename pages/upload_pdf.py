import streamlit as st
import fitz  # PyMuPDF
import streamlit_javascript as st_js
import streamlit_sparrow_labeling
from streamlit_sparrow_labeling import st_sparrow_labeling
# Set page width to half of the screen width
PAGE_WIDTH =  st_js.st_javascript("window.innerWidth")/2
PAGE_HEIGHT =  st_js.st_javascript("window.innerHeight")/2


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
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    count = doc.page_count  # Use the built-in page count property
    
    # Make sure the selected page number is within bounds
    # page_number = max(1, min(count, page_number))
    col1, col2 = st.beta_columns([PAGE_WIDTH, PAGE_WIDTH])
    with col1:
        val = f"image_{page_number}.png"
        page = doc.load_page(page_number-1)  # Page numbers start from 0 in PyMuPDF
        pix = page.get_pixmap(matrix=mat)
        pix.save(val)
        height = 1296
        width = 864
        # doc_height = saved_state['meta']['image_size']['height']
        # doc_width = saved_state['meta']['image_size']['width']
        # canvas_width = canvas_available_width(ui_width)
        result_rects = st_sparrow_labeling(fill_color="rgba(0, 151, 255, 0.3)",stroke_width=2, stroke_color="rgba(0, 50, 255, 0.7)",background_image=val, drawing_mode=mode, display_toolbar=True, update_streamlit=True, canvas_width=PAGE_WIDTH, doc_height=PAGE_HEIGHT, doc_width=PAGE_WIDTH, image_rescale=True, key="doc_annotation" )

        # st.image(val)
    with col2:
        page_number = st.number_input("Page number", min_value=1, max_value=count, value=page_number, step=1)

    # Extract the selected page as an image
    
    
    # Display the image and the number input field
    
    # Clean up
    doc.close()
