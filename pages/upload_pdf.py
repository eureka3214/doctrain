import streamlit as st
import fitz  # PyMuPDF
import streamlit_javascript as st_js

# Set page width to half of the screen width
PAGE_WIDTH =  st_js.st_javascript("window.innerWidth")

def main():
    st.title("PDF Viewer")

    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    # Page number input

    # Display selected page
    if uploaded_file is not None:
        # Load PDF document
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page_num = st.number_input("Enter a page number", value=1, min_value=0, step=1)


        # Get selected page
        page = doc.load_page(page_num - 1)

        # Render page as image and display on left half of screen
        with st.container():
            st.image(page.get_pixmap(alpha=False), width=PAGE_WIDTH)

        # Clean up
        doc.close()

def get_num_pages(uploaded_file):
    """
    Helper function to get the number of pages in a PDF document.
    """
    if uploaded_file is not None:
        # Load PDF document
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        num_pages = doc.page_count

        # Clean up
        doc.close()

        return num_pages
    else:
        return 0

if __name__ == "__main__":
    main()
