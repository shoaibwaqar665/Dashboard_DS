import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the dataset
file_path = 'dataset/JS00001_filtered.csv'  # Update this path as necessary
ecg_data = pd.read_csv(file_path)

# Define leads
leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']

# Calculate the rolling average for Lead I with a window of 100 data points
ecg_data['RollingAvg'] = ecg_data['I'].rolling(window=100).mean()

# Create subplots with an additional row for the rolling average plot
fig = make_subplots(rows=4, cols=1,
                    subplot_titles=("ECG Signal Over Time", "Histogram of Signal Amplitudes", 
                                    "Scatter Plot: Lead I vs Lead II", "Rolling Average: Lead I"),
                    vertical_spacing=0.1,
                    specs=[[{"type": "scatter"}], [{"type": "histogram"}], [{"type": "scatter"}], [{"type": "scatter"}]])

# Add a line plot for each lead in the first row
for lead in leads:
    fig.add_trace(go.Scatter(x=ecg_data['time'], y=ecg_data[lead], mode='lines', name=f'Lead {lead}'), row=1, col=1)

# Add a histogram for the signal amplitudes of all leads in the second row
for lead in leads:
    fig.add_trace(go.Histogram(x=ecg_data[lead], name=f'Lead {lead}', opacity=0.75), row=2, col=1)

# Update layout for histograms to overlay each other
fig.update_traces(opacity=0.75, bingroup=1, row=2, col=1)
fig.update_layout(barmode='overlay')

# Add a scatter plot comparing Lead I vs Lead II in the third row
fig.add_trace(
    go.Scatter(x=ecg_data['I'], y=ecg_data['II'], mode='markers', name='Lead I vs Lead II'),
    row=3, col=1
)

# Add the rolling average plot for Lead I in the fourth row
fig.add_trace(
    go.Scatter(x=ecg_data['time'], y=ecg_data['I'], mode='lines', name='Original Signal'),
    row=4, col=1
)
fig.add_trace(
    go.Scatter(x=ecg_data['time'], y=ecg_data['RollingAvg'], mode='lines', name='Rolling Average'),
    row=4, col=1
)

# Adjust the layout to accommodate the new plot
fig.update_layout(height=1600, title_text="Comprehensive ECG Data Analysis", showlegend=True)

# Show the figure
fig.show()
