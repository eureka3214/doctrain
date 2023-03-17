from PIL import Image
import streamlit as st
import streamlit_nested_layout
import streamlit_javascript as st_js
from streamlit_sparrow_labeling import st_sparrow_labeling
from streamlit_sparrow_labeling import DataProcessor
import json
import math
import base64
session_state = st.session_state
st.set_page_config(
    page_title="Sparrow Labeling",
    layout="wide"
)

def run(img_file, rects_file):
    def download_button(data):
        json_data = json.dumps(data, indent=4)
        b64 = base64.b64encode(json_data.encode()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="data.json">Download JSON File</a>'
        st.markdown(href, unsafe_allow_html=True)


    ui_width = st_js.st_javascript("window.innerWidth")

    docImg = Image.open(img_file)

    # if 'saved_state' not in st.session_state:
    with open(rects_file, "r") as f:
        saved_state = json.load(f)
            # st.session_state['saved_state'] = saved_state
    # else:
        # saved_state = st.session_state['saved_state']

    assign_labels = st.checkbox("Assign Labels", True)
    mode = "transform" if assign_labels else "rect"

    data_processor = DataProcessor()

    col1, col2 = st.columns([6, 4])

    with col1:
        height = 1555
        width = 1037

        doc_height = saved_state['meta']['image_size']['height']
        doc_width = saved_state['meta']['image_size']['width']
        labels = saved_state['meta']['labels']

        canvas_width = canvas_available_width(ui_width)

        result_rects = st_sparrow_labeling(
            fill_color="rgba(0, 151, 255, 0.3)",
            stroke_width=2,
            stroke_color="rgba(0, 50, 255, 0.7)",
            background_image=docImg,
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

    
    with col2:

        if result_rects is not None:
            selected_index = result_rects.current_rect_index
            if selected_index is not None and selected_index != -1:
                with st.form(key="fields_form"):
                    selected_rect = result_rects.rects_data['words'][selected_index]
                    re = selected_rect["rect"]
                    x1, y1, x2, y2 = re["x1"], re["y1"], re["x2"], re["y2"]
                    value = st.text_input("Value", value=f"x1={x1}, y1={y1}, x2={x2}, y2={y2}", key=f"field_value_{selected_index}")
                    label = st.selectbox("Label", labels, key=f"label_{selected_index}", index=selected_index)
                    st.markdown("---")
                    submit = st.form_submit_button("Save", type="primary")
                    if submit:
                        result_rects.rects_data['words'][selected_index]['value'] = value
                        result_rects.rects_data['words'][selected_index]['label'] = label
                        with open(rects_file, "w") as f:
                            json.dump(result_rects.rects_data, f, indent=2)
                        with open(rects_file, "r") as f:
                            saved_state = json.load(f)
                            st.session_state['saved_state'] = saved_state
                        st.write("Saved!")

            btn = st.download_button(
                                    label="Download image",
                                    data=saved_state,
                                    file_name=rects_file,
                                    mime="application/json"
                                    )
            else:
                st.write("No field selected.")


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




def render_form_element(rect, labels, i, result_rects, data_processor):
    default_index = 0
    if rect['label']:
        default_index = labels.index(rect['label'])

    value = st.text_input("Value", rect['value'], key=f"field_value_{i}",
                          disabled=False if i == result_rects.current_rect_index else True)
    label = st.selectbox("Label", labels, key=f"label_{i}", index=default_index,
                         disabled=False if i == result_rects.current_rect_index else True)
    st.markdown("---")
    data_processor.update_rect_data(result_rects.rects_data, i, value, label)


def canvas_available_width(ui_width):
    # Get ~40% of the available width, if the UI is wider than 500px
    if ui_width > 500:
        return math.floor(38 * ui_width / 100)
    else:
        return ui_width


if __name__ == "__main__":
    page_numbers  = session_state.page_numbers
    pgnos = st.multiselect('Select a Page:', page_numbers)

# Update the selected option
    if pgnos:

        # for page_number in page_numbers:
        #     page_numbers[page_number] = page_number == pgnos[0]
        jsonlist = session_state.jsonlist
        imagelist = session_state.imagelist
        # st.write(pgnos)
        selected_value = pgnos[0]
        selected_index = page_numbers.index(selected_value)
        # st.write(jsonlist,imagelist)
        jval = jsonlist[selected_index]
        imval = imagelist[selected_index]

        run(imval, jval)