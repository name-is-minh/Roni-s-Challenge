import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
from matplotlib.dates import DateFormatter, MonthLocator

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
print(monthly_sales)
if month != "All":
    fig, ax = plt.subplots()
    monthly_sales_single = monthly_sales.loc[[month]]
    monthly_sales_single.plot(kind="bar", ax=ax)
    # monthly_sales.plot(kind="bar", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Order ID")
    st.pyplot(fig)
else:
    fig, ax = plt.subplots()
    monthly_sales.plot(kind="line", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Order ID")
    st.pyplot(fig)

# 2. Top 10 Most Popular Items
st.subheader("Top 10 Most Popular Options")
top_10_items = data["Modifier"].value_counts().head(10)
color_palette = sns.color_palette("Paired", len(top_10_items))  # "hsv" generates a colorful range
fig, ax = plt.subplots()
sns.barplot(x=top_10_items.values, y=top_10_items.index, palette=color_palette, ax=ax)
ax.set_xlabel("Frequency")
ax.set_ylabel("Modifier")
legend_labels = top_10_items.index
legend_patches = [mpatches.Patch(color=color_palette[i], label=legend_labels[i]) for i in range(len(legend_labels))]
ax.legend(handles=legend_patches, title="Modifier", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig)

# Total Sales Over Time
st.subheader("Total Sales Over Time")
data["Sent Date"] = pd.to_datetime(data["Sent Date"], errors='coerce')
sales_over_time = data.set_index("Sent Date").resample("D")["Order ID"].nunique()
fig, ax = plt.subplots()
sales_over_time.plot(kind="line", ax=ax)
ax.set_xlabel("Date")
ax.set_ylabel("Order ID")
ax.xaxis.set_major_locator(MonthLocator())
date_form = DateFormatter("%b")  # '%b' for abbreviated month only
ax.xaxis.set_major_formatter(date_form)
st.pyplot(fig)

# Average Time of Day for Business
st.subheader("Average Time of Day for Business")
hourly_sales = data.groupby(data["Sent Date"].dt.hour)["Order #"].count()
fig, ax = plt.subplots()
hourly_sales.plot(kind="line", ax=ax)
ax.set_xlabel("Hour")
ax.set_ylabel("Order Count")
st.pyplot(fig)

# Additional Notes Section for Insights
st.sidebar.header("Notes & Insights")
st.sidebar.write("""
    - Most popular items and trends can help Roni's Mac Bar understand customer preferences.
    - The dashboard can be enhanced with seasonal analysis, predictive models, or other insights based on the data.
    - Further customization and exploration are encouraged to meet the specific requirements of Roni's operations.
""")
