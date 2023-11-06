import pandas as pd
import plotly_express as px
from streamlit_option_menu import option_menu
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="CONSUMER PRICE INDEX",
    page_icon=":bar_chart:",
    layout="wide",
)
#------------------------ All Rwanda Data set ------------------------------------------
df = pd.read_excel(
    io="data.xlsx",
    engine="openpyxl",
    sheet_name="All Rwanda",
    skiprows=3,
    usecols="D:FO",
    nrows=19,
)

# Remove rows with all NaN values
df = df.dropna(how="all")

# Remove columns with all NaN values
df = df.dropna(axis=1, how="all")

#------------------------ Urban Data set ------------------------------------------

df_urban = pd.read_excel(
    io="data.xlsx",
    engine="openpyxl",
    sheet_name="Urban",
    skiprows=3,
    usecols="D:FO",
    nrows=19,
)

# Remove columns with all NaN values
df_urban = df_urban.dropna(axis=0, how="all")


#------------------------ Rural Data set ------------------------------------------

df_Rural = pd.read_excel(
    io="data.xlsx",
    engine="openpyxl",
    sheet_name="Rural",
    skiprows=3,
    usecols="D:FO",
    nrows=19,
)

# Remove columns with all NaN values
df_Rural = df_Rural.dropna(axis=0, how="all")

# Create a dictionary to store the DataFrames for each sheet
data_dict = {"All Rwanda": df, "Urban": df_urban, "Rural": df_Rural}


# Initialize the selected sheet name using st.session_state
if "selected_sheet" not in st.session_state:
    st.session_state.selected_sheet = "All Rwanda"

st.sidebar.title("GRAPHINK DUO")

# Use the selected value to get the corresponding DataFrame
selected_sheet_name = st.sidebar.selectbox("Select Data:", ["All Rwanda", "Urban", "Rural"])
st.session_state.selected_sheet = selected_sheet_name

# Add an expander to show/hide the data for the selected sheet
expander = st.expander(f"Data for {selected_sheet_name}")
with expander:
    st.dataframe(data_dict[selected_sheet_name])

# ---------------- SIDEBAR --------------

# Declare Indicators based on the selected sheet
Indicators = data_dict[selected_sheet_name]["Indicators"].unique()

df_selection = data_dict[selected_sheet_name].query("Indicators == @Indicators")

# ----------- MainPage ----------
st.title(":bar_chart: CONSUMER PRICE INDEX")

# ------------ BAR CHART -------------

# Select the indicator to plot
selected_indicators = st.selectbox("Select an Indicator:", data_dict[selected_sheet_name]["Indicators"].unique())

# Set the title
st.header(f"{selected_indicators} Vs month Trend")

# Filter data based on the selected indicator
filtered_data = data_dict[selected_sheet_name][data_dict[selected_sheet_name]["Indicators"] == selected_indicators]

# Extract the columns for the selected range of months
selected_months = data_dict[selected_sheet_name].columns[2:168]

# Reshape the data for plotting
reshaped_data = filtered_data.melt(id_vars=["Indicators"], value_vars=selected_months, var_name="Month", value_name="Value")

# Create a bar chart using the filtered and reshaped data
fig = px.bar(reshaped_data, barmode="group", x="Month", y="Value", title=f"Bar Chart for {selected_indicators}")


#---------------------------------- Scatter-------------------------------------

# Create a scatter plot using the filtered and reshaped data
scatter_fig = px.scatter(reshaped_data, x="Month", y="Value", title=f"Scatter Plot for {selected_indicators}")

# Use st.columns to align the charts side by side
col1, col2 = st.columns(2)

with col1:
    # Show the bar chart in the first column
    st.plotly_chart(fig)

with col2:
    # Show the scatter plot in the second column
    st.plotly_chart(scatter_fig)


# ------------ BAR CHART1 -------------

# Set the title
st.header("Indicators Over months")

# Filter data based on the selected indicator
df_selection = data_dict[selected_sheet_name][data_dict[selected_sheet_name]["Indicators"].isin(Indicators)]

# Set the width of the chart
chart_width = 400

# Extract the columns for the selected range of months
selected_months = data_dict[selected_sheet_name].columns[2:168]

# Reshape the data for plotting
reshaped_data = df_selection.melt(
    id_vars=["Indicators"],
    value_vars=selected_months,
    var_name="Month",
    value_name="Value"
)

# Create a bar chart using the filtered and reshaped data
fig = px.bar(reshaped_data, x="Month", y="Value", color="Indicators")

#------------------------------------------Donut pie chart --------------------------------------------------------

st.title("Indicators Vs Weights")

# Create a donut chart using Plotly Express
figs = px.pie(
    data_dict[selected_sheet_name],
    names="Indicators",
    values="Weights",
    hole=0.6,  # Set hole size to create a donut chart
    labels={"Category": "Categories"},
    title="Indicators Vs Weights",
)


# Use st.columns to align the charts side by side
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(figs)

with col2:
    st.plotly_chart(fig, use_container_width=False, width=chart_width)

# ------------ BAR CHART2 -------------

cpi_by_indicators = data_dict[selected_sheet_name].groupby(by=["Indicators"])[["Weights"]].sum().reset_index()
fig_indicators = px.bar(
    cpi_by_indicators,
    barmode="group",
    x="Weights",
    y="Indicators",
    title="<b>CPI BY INDICATORS</b>",
    color_discrete_sequence=["#0083B8"],
    template="plotly_white",
)

st.plotly_chart(fig_indicators)
