import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
# Load the dataset
file_path = 'dataset/JS00001_filtered.csv'  # Make sure this path is correct
ecg_data = pd.read_csv(file_path)

# Define leads
leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']

# Create subplots: 1 row for line plots, 1 row for histograms
fig = make_subplots(rows=2, cols=1, subplot_titles=("ECG Signal Over Time", "Histogram of Signal Amplitudes"),
                    vertical_spacing=0.1, specs=[[{"type": "scatter"}], [{"type": "histogram"}]])

# Add a line plot for each lead on the first row
for lead in leads:
    fig.add_trace(go.Scatter(x=ecg_data['time'], y=ecg_data[lead], mode='lines', name=f'Lead {lead}'), row=1, col=1)

# Add a histogram for the signal amplitudes of all leads in the second row
for lead in leads:
    fig.add_trace(go.Histogram(x=ecg_data[lead], name=f'Lead {lead}', opacity=0.75), row=2, col=1)

# Update the layout for histograms to overlay each other
fig.update_traces(opacity=0.75, bingroup=1, row=2, col=1)
fig.update_layout(barmode='overlay')

# Update plot layout
fig.update_layout(title_text="ECG Data Analysis", showlegend=True)

# Show plot
fig.show()
