# from PIL import Image
# import streamlit as st
# from streamlit_sparrow_labeling import st_sparrow_labeling
# import json
# import streamlit_javascript as st_js
# import fitz  # PyMuPDF
# import streamlit_nested_layout
# import math


# st.set_page_config(page_title="Sparrow Labeling", layout="wide")

# def run(img_file, label_data_file):

#     def canvas_available_width(ui_width):
#     # Get ~40% of the available width, if the UI is wider than 500px
#         if ui_width > 500:
#             return math.floor(38 * ui_width / 100)
#         else:
#             return ui_width

#     ui_width = st_js.st_javascript("window.innerWidth")
#     img = Image.open(img_file)
#     st.write(img)
#     if 'saved_state' not in st.session_state:
#         with open(label_data_file, "r") as f:
#             saved_state = json.load(f)
#             st.session_state['saved_state'] = saved_state
#     else:
#         saved_state = st.session_state['saved_state']
    
#     height = 1296
#     width = 864
#     doc_height = img.height
#     doc_width  = img.width

#     st.write(doc_height)
#     canvas_wid = canvas_available_width(ui_width)

#     result_rects = st_sparrow_labeling(
#        fill_color="rgba(0, 151, 255, 0.3)",
#             stroke_width=2,
#             stroke_color="rgba(0, 50, 255, 0.7)",
#             background_image=img,
#             initial_rects=saved_state,
#             height=height,
#             width=width,
#             drawing_mode="transform",
#             display_toolbar=True,
#             update_streamlit=True,
#             canvas_width=canvas_wid,
#             doc_height=doc_height,
#             doc_width=doc_width,
#             image_rescale=True,
#             key="doc_annotation"
#     )

#     return result_rects
    
    
#     # st.image(img)



# # Set page width to half of the screen width

# st.title("PDF Viewer")

# # File uploader
# pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

# # Number input field
# page_number = st.number_input("Page number", min_value=1, value=1, step=1)

# # Display selected page

#     # Make sure the selected page number is within bounds
#     # page_number = max(1, min(count, page_number))
# col1, col2 = st.columns(2)
# with col1:
#     val = f"image_{page_number}.png"
    
#     img_file = val
#     label_data_file = "docs/json/download.json"
#     run(img_file, label_data_file)

# with col2:
#     st.image(val)


#     # Extract the selected page as an image
    
    
#     # Display the image and the number input field


