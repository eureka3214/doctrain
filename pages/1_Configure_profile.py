import json
import streamlit as st

default_data = {
    "meta": {
        "version": "v0.1",
        "name": "Indian Bank Structure",
        "labels": [
            ""
        ],
        "image_id": 1001,
        "image_size": {
            "width": 510,
            "height": 708
        }
    },
    "words": [
        {
            "rect": {
                "x1": 97,
                "y1": 57,
                "x2": 423,
                "y2": 80
            },
            "value": "",
            "label": "Header"
        }
    ]
}

# Define the Streamlit app
def app():
    version = default_data['meta']['version']
    new_version = f"v{float(version[1:])+0.1:.1f}"
    split = st.text_input("Meta Config Profile Name", default_data["meta"]["name"])
    
    labels = st.multiselect(
    'What are Labels you want to annotate in this configuration',
    ['Objectives', 'Objective', 'Chapter', 'Chapter_name','Topics','Topic_name','Contents','sub_Topics','sub_Topic','sub_Topic_name','sub_Topic_Contents'])
    
    new_data = {
        "meta": {
            "version": new_version,
            "name": split,
            "labels": labels,
            "image_id": "",
            "image_size": {
                "width": 510,
                "height": 708
            }
        },
        "words": [
            {
                "rect": {
                    "x1": 43,
                    "y1": 2,
                    "x2": 437,
                    "y2": 31
                },
                "value": "value",
                "label": "Header"
            }
        ]
    }
    st.code(json.dumps(new_data, indent=4))

app()
