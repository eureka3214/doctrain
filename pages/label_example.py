import streamlit as st
import fitz  # PyMuPDF
# import streamlit_javascript as st_js



from PIL import Image

import streamlit_nested_layout
import streamlit_javascript as st_js
from streamlit_sparrow_labeling import st_sparrow_labeling
from streamlit_sparrow_labeling import DataProcessor
import json
import math


def run(img_file, rects_file, labels):
    
    docImg = Image.open(img_file)
    if 'saved_state' not in st.session_state:
        with open(rects_file, "r") as f:
            saved_state = json.load(f)
            st.session_state['saved_state'] = saved_state
    else:
        saved_state = st.session_state['saved_state']
    assign_labels = st.checkbox("Assign Labels", True)
    mode = "transform" if assign_labels else "rect"
    data_processor = DataProcessor()
    col1, col2 = st.columns([6, 6])

    with col1:
        height = 1296
        width = 864
        doc_height = saved_state['meta']['image_size']['height']
        doc_width = saved_state['meta']['image_size']['width']
        canvas_width = canvas_available_width(ui_width)
        result_rects = st_sparrow_labeling(fill_color="rgba(0, 151, 255, 0.3)",stroke_width=2, stroke_color="rgba(0, 50, 255, 0.7)",background_image=docImg, initial_rects=saved_state, height=height,width=width, drawing_mode=mode, display_toolbar=True, update_streamlit=True, canvas_width=canvas_width, doc_height=doc_height, doc_width=doc_width, image_rescale=True, key="doc_annotation" )
        st.caption("Check 'Assign Labels' to enable editing of labels and values, move and resize the boxes to annotate the document.")
        st.caption("Add annotations by clicking and dragging on the document, when 'Assign Labels' is unchecked.")

    with col2:
        if result_rects is not None:
            with st.form(key="fields_form"):
                if result_rects.current_rect_index is not None and result_rects.current_rect_index != -1:
                    st.write("Selected Field: ",
                             result_rects.rects_data['words'][result_rects.current_rect_index]['value'])
                    st.markdown("---")
                if ui_width > 1500:
                    render_form_wide(result_rects.rects_data['words'], labels, result_rects, data_processor)
                elif ui_width > 1000:
                    render_form_avg(result_rects.rects_data['words'], labels, result_rects, data_processor)
                elif ui_width > 500:
                    render_form_narrow(result_rects.rects_data['words'], labels, result_rects, data_processor)
                else:
                    render_form_mobile(result_rects.rects_data['words'], labels, result_rects, data_processor)
                submit = st.form_submit_button("Save", type="primary")
                if submit:
                    with open(rects_file, "w") as f:
                        json.dump(result_rects.rects_data, f, indent=2)
                    with open(rects_file, "r") as f:
                        saved_state = json.load(f)
                        st.session_state['saved_state'] = saved_state
                    st.write("Saved!")


def render_form_wide(words, labels, result_rects, data_processor):
    col1_form, col2_form, col3_form, col4_form = st.columns([1, 1, 1, 1])
    num_rows = math.ceil(len(words) / 4)

    for i, rect in enumerate(words):
        if i < num_rows:
            with col1_form:
                render_form_element(rect, labels, i, result_rects, data_processor)
        elif i < num_rows * 2:
            with col2_form:
                render_form_element(rect, labels, i, result_rects, data_processor)
        elif i < num_rows * 3:
            with col3_form:
                render_form_element(rect, labels, i, result_rects, data_processor)
        else:
            with col4_form:
                render_form_element(rect, labels, i, result_rects, data_processor)


def render_form_avg(words, labels, result_rects, data_processor):
    col1_form, col2_form, col3_form = st.columns([1, 1, 1])
    num_rows = math.ceil(len(words) / 3)

    for i, rect in enumerate(words):
        if i < num_rows:
            with col1_form:
                render_form_element(rect, labels, i, result_rects, data_processor)
        elif i < num_rows * 2:
            with col2_form:
                render_form_element(rect, labels, i, result_rects, data_processor)
        else:
            with col3_form:
                render_form_element(rect, labels, i, result_rects, data_processor)


def render_form_narrow(words, labels, result_rects, data_processor):
    col1_form, col2_form = st.columns([1, 1])
    num_rows = math.ceil(len(words) / 2)
    for i, rect in enumerate(words):
        if i < num_rows:
            with col1_form:
                render_form_element(rect, labels, i, result_rects, data_processor)
        else:
            with col2_form:
                render_form_element(rect, labels, i, result_rects, data_processor)


def render_form_mobile(words, labels, result_rects, data_processor):
    for i, rect in enumerate(words):
        render_form_element(rect, labels, i, result_rects, data_processor)


def render_form_element(rect, labels, i, result_rects, data_processor):
    default_index = 0
    if rect['label']:
        default_index = labels.index(rect['label'])

    value = st.text_input("Value", rect['value'], key=f"field_value_{i}",
                          disabled=False if i == result_rects.current_rect_index else True)
    label = st.selectbox("Label", labels, key=f"label_{i}", index=default_index,
                         disabled=False if i == result_rects.current_rect_index else True)
    data_processor.update_rect_data(result_rects.rects_data, i, value, label)

def canvas_available_width(ui_width):
    # Get ~40% of the available width, if the UI is wider than 500px
    if ui_width > 500:
        return math.floor(38 * ui_width / 100)
    else:
        return ui_width






if __name__ == "__main__":
    # custom_labels = ["", "paragraph", "Topic", "Subtopic", "Objective", "SubtopicContents"]
    # run("docs/image/download.png", "docs/json/download.json", custom_labels)
    ui_width = st_js.st_javascript("window.innerWidth")
    # Set page width to half of the screen width
    PAGE_WIDTH = ui_width/2

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
        # page_number = max(1, min(count, page_number))
        # col1, col2 = st.beta_columns([PAGE_WIDTH, PAGE_WIDTH])
        # with col1:
        val = f"image_{page_number}.png"
        page = doc.load_page(page_number-1)  # Page numbers start from 0 in PyMuPDF
        pix = page.get_pixmap(matrix=mat)
        pix.save(val)
        # st.image(val)
        custom_labels = ["", "paragraph", "Topic", "Subtopic", "Objective", "SubtopicContents"]
        run( val, "docs/json/download.json", custom_labels)
        # with col2:
        #     page_number = st.number_input("Page number", min_value=1, max_value=count, value=page_number, step=1)    
        # Clean up
        doc.close()
