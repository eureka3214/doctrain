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
    
    # Add labels dynamically
    labels = []
    while st.button("Add Label"):
        label = st.text_input("Label Name")
        if label:
            labels.append(label)
    
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
