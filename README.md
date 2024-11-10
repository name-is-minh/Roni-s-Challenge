# Roni's Mac Bar Sales Dashboard

This project is a data-driven dashboard designed to provide valuable insights into the sales operations of Roni's Mac Bar, a local Texas business. The dashboard displays sales trends, popular items, peak hours, and other key metrics, helping the business make informed decisions based on data.

## Table of Contents
- Features
- Technologies Used
- Installation
- Usage
- Project Structure
- Screenshots

## Features
- Monthly Sales Analysis: Visualizes monthly sales with average trend lines for school and non-school months.
- Top 10 Most Popular Options: Displays the most popular modifiers (toppings or add-ons) and their frequencies.
- Total Sales Over Time: Shows daily sales over the selected period with peak sales day highlighted.
- Average Time of Day for Business: Identifies peak business hours to aid in staff planning.
- Interactive Filters: Allows filtering by month and day to narrow down the data.
- Key Insights: Provides quick insights, such as the busiest day of the week, busiest hour, average monthly sales, and the top-selling modifier.

## Technologies Used
- Streamlit: Framework for creating interactive data dashboards in Python.
- Plotly: Used for interactive line charts with hover functionality.
- Pandas: Data manipulation and analysis library.
- Seaborn: For color palettes in bar charts.
- Matplotlib: For additional chart customization.

## Installation
To get started with this project, you need to clone the repository and install the required dependencies.

### Prerequisites
Python 3.7+
pip (Python package installer)
### Steps
1. Clone the repository:

```bash
git clone https://github.com/yourusername/ronis-mac-bar-dashboard.git
cd ronis-mac-bar-dashboard
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv ronivenv
source ronivenv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add the data files:

Place the monthly CSV files (e.g., april_2024.csv, may_2024.csv, etc.) in a folder structured as roni_challenge/roni_challenge_data within the project directory.

## Usage
1. Run the Streamlit app:

```bash
streamlit run ronis_mac_bar_dashboard.py
```

2. Access the dashboard:

Once the app is running, open a browser and go to the address provided in the terminal (usually http://localhost:8501)

3. Interact with the dashboard:
- Use the sidebar to filter data by month or day.
- Hover over line charts to view detailed data for each point.
- Review key insights in the sidebar to quickly understand sales patterns

## Project Structure
ronis-mac-bar-dashboard/ \
├── roni_challenge/ \
│   ├── roni_challenge_data/ \
│   │   ├── april_2024.csv \
│   │   ├── may_2024.csv \
│   │   └── ... (other monthly CSV files) \
│   └── ronis_mac_bar_dashboard.py  # Main application file \
├── requirements.txt  # List of dependencies \
└── README.md         # Project documentation 

## Screenshots
