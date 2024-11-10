import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.patches as mpatches

# Load Data
@st.cache_data  # Updated cache function
def load_data():
    months = ["april", "may", "june", "july", "august", "september", "october"]
    data_frames = []
    for month in months:
        # Load each month's data with specified encoding
        df = pd.read_csv(f"/mnt/c/hackathon_projects/datathon_fall2024/Roni-s-Challenge/roni_challenge/roni_challenge_data/{month}_2024.csv", encoding='ISO-8859-1')
        df.columns = df.columns.str.strip()  # Strip whitespace from column names
        
        # Add 'Month' column if missing
        if 'Month' not in df.columns:
            df['Month'] = month.capitalize()

        # Handle 'Sent Date' to create 'DayOfWeek' if necessary
        if 'Sent Date' in df.columns:  # Check for 'Sent Date' explicitly
            df['Sent Date'] = pd.to_datetime(df['Sent Date'], errors='coerce')  # Convert to datetime
            df['DayOfWeek'] = df['Sent Date'].dt.day_name()  # Create DayOfWeek based on Sent Date
        
        data_frames.append(df)
    
    # Concatenate all dataframes into one
    data = pd.concat(data_frames, ignore_index=True)
    
    # Define the custom order for months
    month_order = ["April", "May", "June", "July", "August", "September", "October"]
    data["Month"] = pd.Categorical(data["Month"], categories=month_order, ordered=True)
    
    return data

data = load_data()
# unique_orders = data.drop_duplicates(subset="Order #")

# Sidebar: Data Filters
st.sidebar.header("Filter Data")
month = st.sidebar.selectbox("Select Month", ["All"] + list(data["Month"].unique()))
day = st.sidebar.selectbox("Select Day", ["All"] + list(data["DayOfWeek"].unique()))

# Filter data based on user selections
if month != "All":
    data = data[data["Month"] == month]
if day != "All":
    data = data[data["DayOfWeek"] == day]

# Dashboard Title
st.title("Roni's Mac Bar Sales Dashboard")

# Monthly Sales
st.subheader("Monthly Sales")
monthly_sales = data.groupby("Month")["Order ID"].nunique().sort_index()  # Use Order ID for counting

# Define school months and non-school months
school_months = ["August", "September", "October"]
non_school_months = ["April", "May", "June", "July"]

# Calculate the average sales for school and non-school months
average_sales_school_months = monthly_sales.loc[school_months].mean()
average_sales_non_school_months = monthly_sales.loc[non_school_months].mean()

# When "All" months are selected, show an interactive line chart for all months
if month == "All":
    fig = go.Figure()

    # Add main line chart for monthly sales
    fig.add_trace(go.Scatter(
        x=monthly_sales.index,
        y=monthly_sales.values,
        mode='lines+markers',
        name='Monthly Sales',
        hovertemplate='Month: %{x}<br>Sales: %{y}<extra></extra>'
    ))

    # Add average lines for school and non-school months
    fig.add_hline(y=average_sales_school_months, line_dash="dash", line_color="green",
                  annotation_text=f"Avg School Months: {average_sales_school_months:.0f}", 
                  annotation_position="top left")
    fig.add_hline(y=average_sales_non_school_months, line_dash="dash", line_color="orange",
                  annotation_text=f"Avg Non-School Months: {average_sales_non_school_months:.0f}",
                  annotation_position="top right")

    # Customize layout
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Order ID",
        title="Monthly Sales Over Time",
        showlegend=True
    )
    st.plotly_chart(fig)
else:
    # Display single month bar chart if a specific month is selected
    fig = px.bar(
        x=[month],
        y=[monthly_sales.loc[month]],
        labels={'x': 'Month', 'y': 'Order ID'},
        title=f"Monthly Sales for {month}"
    )
    st.plotly_chart(fig)

# 2. Top 10 Most Popular Items
st.subheader("Top 10 Most Popular Options")
top_10_items = data["Modifier"].value_counts().head(10)

# Use Plotly's px.bar and assign a different color to each bar
fig = px.bar(
    x=top_10_items.values,
    y=top_10_items.index,
    orientation='h',
    labels={'x': 'Frequency', 'y': 'Modifier', 'color': 'Modifier'},
    title="Top 10 Most Popular Options",
    color=top_10_items.index,  # Set each bar color differently based on item
    color_discrete_sequence=px.colors.qualitative.Plotly  # Use a diverse color palette
)

st.plotly_chart(fig)


# Total Sales Over Time
st.subheader("Total Sales Over Time")
data["Sent Date"] = pd.to_datetime(data["Sent Date"], errors='coerce')
sales_over_time = data.set_index("Sent Date").resample("D")["Order ID"].nunique()

# Create a Plotly line chart for total sales over time
fig = px.line(
    sales_over_time,
    labels={"value": "Order ID", "index": "Sent Date"},
    title="Total Sales Over Time"
)

# Highlight Peak Day with an Annotation
peak_date = sales_over_time.idxmax()
peak_sales = sales_over_time.max()
fig.add_annotation(
    x=peak_date,
    y=peak_sales,
    text=f"Peak Sales: {peak_sales} on {peak_date.strftime('%b %d')}",
    showarrow=True,
    arrowhead=1,
    ax=-10,
    ay=-40
)

st.plotly_chart(fig)


# Average Time of Day for Business
st.subheader("Average Time of Day for Business")
hourly_sales = data.groupby(data["Sent Date"].dt.hour)["Order #"].count()
fig = px.line(
    x=hourly_sales.index,
    y=hourly_sales.values,
    labels={"x": "Hour", "y": "Order Count"},
    title="Average Time of Day for Business"
)
st.plotly_chart(fig)

# Display Key Insights
st.sidebar.header("Key Insights")

# Busiest Day of the Week
busiest_day = data["DayOfWeek"].value_counts().idxmax()
st.sidebar.write(f"**Busiest Day of the Week:** {busiest_day}")

# Busiest Hour of the Day
busiest_hour = int(data["Sent Date"].dt.hour.value_counts().idxmax())
st.sidebar.write(f"**Busiest Hour of the Day:** {busiest_hour}:00:00")

# Average Monthly Sales
avg_monthly_sales = monthly_sales.mean()
st.sidebar.write(f"**Average Monthly Sales:** ${avg_monthly_sales:.0f}")

# Top Selling Modifier
top_modifier = top_10_items.idxmax()
st.sidebar.write(f"**Top Selling Modifier:** {top_modifier}")
