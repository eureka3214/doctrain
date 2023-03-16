import streamlit as st
import fitz  # PyMuPDF
import streamlit_javascript as st_js

# Set page width to half of the screen width
PAGE_WIDTH =  st_js.st_javascript("window.innerWidth")


st.title("PDF Viewer")

# File uploader
pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

# Page number input

# Display selected page
if pdf_file is not None:
    # pdf_layout = lp.load_pdf(pdf_file)
    doc =  fitz.open(stream=pdf_file.read(), filetype="pdf")
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    count = 0
    
    # Count variable is to get the number of pages in the pdf
    for p in doc:
        count += 1
    for i in range(count):
        val = f"image_{i+1}.png"
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        pix.save(val)
        # st.image(page.get_pixmap(alpha=False), width=PAGE_WIDTH)

    # Clean up
    doc.close()
