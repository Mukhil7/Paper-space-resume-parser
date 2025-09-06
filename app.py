import streamlit as st
from pyresparser import ResumeParser
from pymongo import MongoClient
import os
import warnings
import json
import pandas as pd
import io

warnings.filterwarnings("ignore", category=UserWarning)

MONGO_URI = "mongodb://mongo:27017"
client = MongoClient(MONGO_URI)
db = client["resume_db"]
collection = db["resumes"]

st.title("Paper Space Resume Parser")

uploaded_files = st.file_uploader("Upload your resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    parsed_data_list = []
    file_names = []

    for uploaded_file in uploaded_files:
        file_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        file_names.append(uploaded_file.name)
        try:
            data = ResumeParser(file_path).get_extracted_data()
            parsed_data_list.append(data)
        except Exception as e:
            st.error(f"Error parsing {uploaded_file.name}: {e}")
        finally:
            os.remove(file_path)

    if parsed_data_list:
        st.success(f"Successfully processed {len(parsed_data_list)} resume(s)!")

        st.subheader("Parsed Resume Data")
        for i, (data, file_name) in enumerate(zip(parsed_data_list, file_names), 1):
            st.write(f"**Resume {i}: {file_name}**")
            for key, value in data.items():
                if isinstance(value, list):
                    value_str = ', '.join(map(str, value))
                else:
                    value_str = str(value)
                st.write(f"**{key.capitalize().replace('_', ' ')}:** {value_str}")
            st.write("---")

        st.session_state.parsed_data_list = parsed_data_list
        st.session_state.file_names = file_names

    if "parsed_data_list" in st.session_state and st.button("Save to MongoDB"):
        try:
            for data, file_name in zip(st.session_state.parsed_data_list, st.session_state.file_names):
                data["resume_file"] = file_name
                collection.insert_one(data)
            st.success(f"Saved {len(st.session_state.parsed_data_list)} resume(s) to MongoDB!")
        except Exception as e:
            st.error(f"Error saving to MongoDB: {e}")

st.subheader("Export MongoDB Data")
export_format = st.selectbox("Select export format", ["JSON", "CSV"])
if st.button("Export Data"):
    try:
        resumes = list(collection.find())
        if not resumes:
            st.warning("No data found in MongoDB.")
        else:
            if export_format == "JSON":
                json_data = json.dumps(resumes, default=str)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name="resumes.json",
                    mime="application/json"
                )
            else:
                df = pd.DataFrame(resumes)
                if '_id' in df.columns:
                    df = df.drop('_id', axis=1)
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_buffer.getvalue(),
                    file_name="resumes.csv",
                    mime="text/csv"
                )
            st.success(f"Prepared {export_format} file for download.")
    except Exception as e:
        st.error(f"Error exporting data: {e}")