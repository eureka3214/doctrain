import streamlit as st
import fitz  # PyMuPDF
import streamlit_javascript as st_js
import json

# Set page width to half of the screen width
PAGE_WIDTH = st_js.st_javascript("window.innerWidth")/2

def save_json(data, filename):
    with open(filename, "w") as outfile:
        json.dump(data, outfile)

st.title("Paste profile configurations and Upload PDF")

json_string = st.text_area("Paste Profile Configuration ( and Press CTRL+Enter)")

# Parse the JSON string and save it to a variable
try:
    default_data = json.loads(json_string)
except json.JSONDecodeError:
    st.error("Invalid JSON string")

pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

# Add a multiselect field for page selection
if pdf_file is not None:
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    count = doc.page_count
    page_numbers = st.multiselect(
        "Select pages to display",
        list(range(1, count + 1)),
        default=list(range(1, count + 1))
    )
    col1, col2 = st.columns([PAGE_WIDTH, PAGE_WIDTH]) 
    col1.get  = st.button("Add pages")
    if get:
        with col2:
            for page_number in page_numbers:
                val = f"image_{page_number}.png"
                filename = f"json_annot_{page_number}.json"
                page = doc.load_page(page_number - 1)
                pix = page.get_pixmap()
                pix.save(val)
                st.image(val)
                data = default_data.copy()
                data["meta"]["image_id"] = page_number
                save_json(data, filename)
                st.success(f"JSON file saved as {filename}")
               

    # Clean up
    doc.close()
