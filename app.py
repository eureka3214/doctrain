from PIL import Image
import streamlit as st
import streamlit_nested_layout
import streamlit_javascript as st_js
from streamlit_sparrow_labeling import st_sparrow_labeling
from streamlit_sparrow_labeling import DataProcessor
import json
import math

st.set_page_config(page_title="Sparrow Labeling", layout="wide")

def run(img_file, rects_file, labels):
    ui_width = st_js.st_javascript("window.innerWidth")
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
    col1, col2 = st.columns([4, 6])

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
    st.write(f"{i + 1}. {rect['value']}")
    label_value = result_rects.rects_data['words'][i]['label'] if 'label' in result_rects.rects_data['words'][i] else ''
    label_value += f" (x:{rect.x1}, y:{rect['y1']}, w:{rect['x2']}, h:{rect['y2']})"
    label_key = f"label_{i}"
    label_options = [''] + labels
    selected_label = st.selectbox("Label", options=label_options, key=label_key, i=labels.i(label_value) if label_value in labels else 0)
    if selected_label == '':
        data_processor.remove_key(label_key)
    else:
        data_processor.update_key(label_key, selected_label)


def canvas_available_width(ui_width):
    # Get ~40% of the available width, if the UI is wider than 500px
    if ui_width > 500:
        return math.floor(38 * ui_width / 100)
    else:
        return ui_width


if __name__ == "__main__":
    custom_labels = ["", "paragraph", "Topic", "Subtopic", "Objective", "SubtopicContents"]
    run("docs/image/download.png", "docs/json/download.json", custom_labels)
