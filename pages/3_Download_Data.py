import streamlit as st
import json
import base64
from io import BytesIO


session_state = st.session_state
json_files = session_state.jsonlist
# Define a list of JSON file paths
# json_files = ["file1.json", "file2.json", "file3.json"]

# Define a function to download multiple JSON files
def download_multiple_files(json_files):
    compressed_file = BytesIO()
    with zipfile.ZipFile(compressed_file, "w") as archive:
        for json_file in json_files:
            data = Path(json_file).read_text()
            archive.writestr(json_file, data)
    compressed_file.seek(0)
    b64 = base64.b64encode(compressed_file.getvalue()).decode()
    href = f'<a href="data:application/zip;base64,{b64}" download="multiple_files.zip">Download JSON Files</a>'
    st.markdown(href, unsafe_allow_html=True)

# Display the download button
download_multiple_files(json_files)
