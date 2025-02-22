import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", page_icon=":material/file_present:")

# User's Information Optional
st.sidebar.title("User's Information")
name = st.sidebar.text_input("Name")
email = st.sidebar.text_input("Email")

# Title and Subtitle
st.title("Data Sweeper")
st.subheader("Upload your Excel file to sweep through it")
uploaded_file = st.file_uploader("Choose an CSV or Excel file:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported File: {file_ext}")
            continue

        # Displaying the information of the file
        st.write(f"File Name: {file.name}")
        st.write(f"File Size: {file.size}")

        # Showing the first five rows of the file
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Data Cleaning options
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write(f"Duplicates Removed Successfully")

            with col2:
                if st.button(f"Fill Missing Values from {file.name}"):
                    numeric_cols = df.select_dtypes(include={'number'}).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Filled Successfully")

        # Columns keep and convert to string
        st.subheader("📌 Select Columns to Keep and Convert")
        columns_to_keep = st.multiselect(f"Select Columns from {file.name}", df.columns)
        if st.button("Keep and Convert Columns"):
            df = df[columns_to_keep]
            df = df.astype(str)
            st.write("Columns Kept and Converted to String Successfully")

        # Create some visualizations
        st.subheader("Create Visualizations")
        if st.checkbox(f"Show visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Converting the file
        st.subheader("🔄 Convert the file")
        convertion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=f"convert_{file.name}")

        if st.button(f"Convert {file.name} to {convertion_type}"):
            buffer = BytesIO()
            if convertion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif convertion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)  # Reset buffer position
            st.download_button(
                label=f"Download {convertion_type} file",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
st.success("🎉 All operations completed successfully")