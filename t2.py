import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title("Data Visualization App 📈📊")

# File uploader to load the dataset
data = st.file_uploader("Upload Your Datasheet Here:", type="xlsx")

if data is not None:
    # Load the data into a DataFrame
    df = pd.read_excel(data, engine='openpyxl')
    original_df = df.copy()  # Keep a copy of the original DataFrame
    
    # Select the visualization type
    type_sel = st.selectbox("Select the Visualization Type:", ["Line Graph", "Bar Graph", "Scatter Chart"])
    column_list = df.columns.tolist()
    
    # Select x-axis column
    x_ax = st.selectbox("Select x-axis:", column_list)
    
    # Visualization based on selected type
    if type_sel == "Line Graph":
        st.subheader("Line Graph")
        st.line_chart(df.set_index(x_ax))
    
    if type_sel == "Bar Graph":
        st.subheader("Bar Graph")
        fig, ax = plt.subplots()
        df.set_index(x_ax).plot(kind='bar', ax=ax)
        y_ax = st.text_input("Enter the label of Y-axis:")
        ax.set_xlabel(x_ax)
        ax.set_ylabel(y_ax)
        st.pyplot(fig)
    
    if type_sel == "Scatter Chart":
        st.subheader("Scatter Chart")
        st.scatter_chart(df.set_index(x_ax))
    
    st.subheader("This is your Data:")
    st.dataframe(original_df)

    # Display summary statistics
    st.subheader("Summary of data")
    st.write(df.describe())

    st.subheader("Custom Summary Statistics")
    st.write(f"Number of rows: {len(df)}")
    st.write(f"Number of columns: {len(df.columns)}")
    st.write(f"Missing values: {df.isnull().sum().sum()}")

    # Multi-select for filtering
    st.subheader("Multi-Factor Data Filtering")
    filter_columns = st.multiselect("Select Columns to Filter Data By:", column_list)
    st.write("Selected options:", filter_columns)
    
    # Dictionary to store filter criteria
    filters = {}

    # Loop through selected columns to create dynamic filters
    for column in filter_columns:
        if pd.api.types.is_numeric_dtype(original_df[column]):
            min_value = original_df[column].min()
            max_value = original_df[column].max()
            slider_values = st.slider(f"Select range for {column}", min_value, max_value, (min_value, max_value))
            filters[column] = slider_values

        elif pd.api.types.is_string_dtype(original_df[column]):
            unique_values = original_df[column].unique()
            selected_values = st.multiselect(f"Select values for {column}", unique_values)
            filters[column] = selected_values

        elif pd.api.types.is_datetime64_any_dtype(original_df[column]):
            min_date = original_df[column].min().date()
            max_date = original_df[column].max().date()
            selected_date_range = st.date_input(f"Select date range for {column}", [min_date, max_date])
            filters[column] = selected_date_range
    
    # Apply filters
    if filters:
        filtered_df = original_df.copy()
        for column, criteria in filters.items():
            if pd.api.types.is_numeric_dtype(original_df[column]):
                filtered_df = filtered_df[(filtered_df[column] >= criteria[0]) & (filtered_df[column] <= criteria[1])]
            elif pd.api.types.is_string_dtype(original_df[column]):
                filtered_df = filtered_df[filtered_df[column].isin(criteria)]
            elif pd.api.types.is_datetime64_any_dtype(original_df[column]):
                filtered_df = filtered_df[(filtered_df[column].dt.date >= criteria[0]) & (filtered_df[column].dt.date <= criteria[1])]
        
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

