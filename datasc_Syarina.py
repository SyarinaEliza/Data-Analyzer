import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Analyze Your Data 💻",
    page_icon="📊",
    layout="wide"
)

# ================= HEADER =================
st.title("📈 Analyze Your Data")
st.write("🚀 Upload a **CSV** or **Excel** file to explore your data interactively!")

# ================= FILE UPLOAD =================
uploaded_file = st.file_uploader(
    "📂 Upload a CSV or Excel File",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        # Convert boolean columns to string
        bool_cols = data.select_dtypes(include=["bool"]).columns
        data[bool_cols] = data[bool_cols].astype(str)

    except Exception:
        st.error("❌ Oops! Could not read the file. Please check the format.")
        st.stop()

    st.success("✔ File uploaded successfully! Let's explore it 🌟")

    # ================= PREVIEW =================
    st.write("### 👀 Preview of Data")
    st.dataframe(data.head())

    # ================= OVERVIEW =================
    st.write("### 📝 Data Overview")
    st.write(f"**Rows:** {data.shape[0]} 📄")
    st.write(f"**Columns:** {data.shape[1]} 🏷️")
    st.write(f"**Missing Values:** {data.isnull().sum().sum()} ❓")
    st.write(f"**Duplicate Rows:** {data.duplicated().sum()} ⚠️")

    # ================= DATA INFO =================
    st.write("### ℹ️ Complete Dataset Info")
    buffer = io.StringIO()
    data.info(buf=buffer)
    st.text(buffer.getvalue())

    # ================= DESCRIBE (NUMERIC) =================
    st.write("### 📊 Statistical Summary (Numerical)")
    st.dataframe(data.describe())

    # ================= DESCRIBE (NON-NUMERIC) =================
    st.write("### 🧩 Statistical Summary (Non-Numerical)")
    non_numeric_cols = data.select_dtypes(include=["object", "bool"]).columns

    if len(non_numeric_cols) > 0:
        st.dataframe(data.describe(include=["object", "bool"]))
    else:
        st.info("No non-numerical columns found in this dataset 😅")

    # ================= COLUMN SELECTION =================
    st.write("### 🎯 Select Columns for Analysis")
    selected_columns = st.multiselect(
        "Choose Columns (optional)",
        data.columns.tolist()
    )

    if selected_columns:
        st.dataframe(data[selected_columns].head())
    else:
        st.dataframe(data.head())

    # ================= VISUALIZATION =================
    st.write("### 📉 Data Visualization")

    all_columns = data.columns.tolist()
    numeric_columns = data.select_dtypes(include=np.number).columns.tolist()

    x_axis = st.selectbox("🟢 Select X-axis", all_columns)
    y_axis = st.selectbox("🔵 Select Y-axis (numeric)", numeric_columns)

    # ================= AUTO-DISABLE CONDITIONS =================
    line_disabled = x_axis not in numeric_columns
    scatter_disabled = x_axis not in numeric_columns
    hist_disabled = y_axis not in numeric_columns
    pie_disabled = x_axis in numeric_columns
    heatmap_disabled = len(numeric_columns) < 2

    # ================= CHART BUTTONS =================
    c1, c2, c3 = st.columns(3)

    with c1:
        line_btn = st.button(
            "📈 Line Chart",
            disabled=line_disabled,
            help="Requires numeric X and Y columns"
        )
        bar_btn = st.button(
            "📊 Bar Chart",
            help="Shows average of Y grouped by X"
        )

    with c2:
        scatter_btn = st.button(
            "🔹 Scatter Plot",
            disabled=scatter_disabled,
            help="Requires numeric X and Y columns"
        )
        hist_btn = st.button(
            "🟣 Histogram",
            disabled=hist_disabled,
            help="Requires numeric column"
        )

    with c3:
        pie_btn = st.button(
            "🥧 Pie Chart",
            disabled=pie_disabled,
            help="Requires categorical X column"
        )
        heatmap_btn = st.button(
            "🌡️ Heatmap",
            disabled=heatmap_disabled,
            help="Requires at least two numeric columns"
        )

    # ================= PLOTS =================
    if line_btn:
        st.success(f"📈 Plotting Line Chart: {y_axis} vs {x_axis}")
        fig, ax = plt.subplots()
        ax.plot(data[x_axis], data[y_axis], marker='o', linestyle='-', color='teal')
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"{y_axis} vs {x_axis}")
        st.pyplot(fig)

    if scatter_btn:
        st.success(f"🔹 Plotting Scatter Plot: {y_axis} vs {x_axis}")
        fig, ax = plt.subplots()
        ax.scatter(data[x_axis], data[y_axis], color='orange', alpha=0.7)
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"{y_axis} vs {x_axis}")
        st.pyplot(fig)

    if bar_btn:
        st.success(f"📊 Plotting Bar Chart: Average {y_axis} grouped by {x_axis}")
        fig, ax = plt.subplots()
        data.groupby(x_axis)[y_axis].mean().plot(kind="bar", ax=ax, color='purple')
        ax.set_ylabel(f"Average {y_axis}")
        ax.set_title(f"Average {y_axis} by {x_axis}")
        st.pyplot(fig)

    if hist_btn:
        st.success(f"🟣 Plotting Histogram of {y_axis}")
        fig, ax = plt.subplots()
        ax.hist(data[y_axis], bins=20, color='green', alpha=0.7)
        ax.set_xlabel(y_axis)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    if pie_btn:
        st.success(f"🥧 Plotting Pie Chart of {x_axis}")
        fig, ax = plt.subplots()
        data[x_axis].value_counts().plot.pie(
            autopct="%1.1f%%",
            ax=ax,
            startangle=90,
            colors=sns.color_palette("pastel")
        )
        ax.set_ylabel("")
        st.pyplot(fig)

    if heatmap_btn:
        st.success("🌡️ Plotting Heatmap of correlations")
        fig, ax = plt.subplots(figsize=(8,6))
        sns.heatmap(data[numeric_columns].corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

else:
    st.info("ℹ️ Please upload a CSV or Excel file to get started 🚀")
