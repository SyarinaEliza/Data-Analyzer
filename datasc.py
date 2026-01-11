import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Analyze Your Data",page_icon="💻",layout="wide")

st.title("📈 Anyalyze Your Data")
st.write("📂 Upload A **csv** or an **Excel** File To Explore Your Data Interectively!")

# for uploading
uploaded_file = st.file_uploader('Upload a csv or Excel File',type=['csv','xlsx'])
 
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        # convert bool columns as str
        bool_cols = data.select_dtypes(include=['bool']).columns
        data[bool_cols] = data[bool_cols].astype('str')
    except Exception as e:
        st.error('Could Not Read Excel / CSV File. Please Check Your File Format')
        st.exception(e)
        st.stop()
 
    st.success('✔️ File Uploaded Successfully')
    st.write('### Preview of Data')
    st.dataframe(data.head())
 
    st.write("### 🗒️Data Overview")
    st.write("Number Of Rows : ",data.shape[0])
    st.write("Number Of Column :",data.shape[1])
    st.write("Number Of Missing Values : ",data.isnull().sum().sum())
    st.write("Number Of Duplicate Records : ",data.duplicated().sum())

    st.write('### 🗄️ Complete Summary Of Dataset')
    buffer = io.StringIO()
    data.info(buf=buffer)
    i = buffer.getvalue()
    st.text(i)

    # describe()
    st.write('### 📖 Statistical Summary Of Dataset')
    st.dataframe(data.describe())

    st.write('### 📖 Statistical Summary For Non-Numerical Features Of Dataset')
    st.dataframe(data.describe(include=['bool','object']))

    st.write('### 📖 Select The Desired Column For Analysis')
    selected_columns = st.multiselect("Choose Columns",data.columns.tolist())

    if selected_columns:
        st.dataframe(data[selected_columns].head())
    else:
        st.info("No Column Selected. Showing Full Dataset")
        st.dataframe(data.head())
    
    st.write('### 📺 Data Visualization')
    st.write("Select ***Columns*** For Data Visualization")
    columns = data.columns.tolist()
    x_axis = st.selectbox("Select Column For X-Axis",options=columns)
    y_axis = st.selectbox("Select Column For Y-Axis",options=columns)

        # Create Buttons For Diff Diff Charts
    col1, col2 = st.columns(2)
 
    with col1:
        line_btn = st.button('Line Graph')
    with col2:
        scatter_btn = st.button('Scatter Graph')
 
    if line_btn:
        st.write('### Showing A Line Graph')
        fig,ax = plt.subplots()
        ax.plot(data[x_axis], data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_xlabel(x_axis)
        ax.set_title(f'Line Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig)
 
    if scatter_btn:
        st.write('### Showing A Scatter Graph')
        fig,ax = plt.subplots()
        ax.scatter(data[x_axis], data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_xlabel(x_axis)
        ax.set_title(f'Scatter Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig)
else:
    st.info('Please Upload A CSV Or An Excel File To Get Started')