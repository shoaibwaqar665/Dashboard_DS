# Import necessary libraries
import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the dataset
file_path = 'dataset/JS00001_filtered.csv'  # Make sure this path is correct for your setup
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

# Add plots for each specified section
for lead in leads:
    fig.add_trace(go.Scatter(x=ecg_data['time'], y=ecg_data[lead], mode='lines', name=f'Lead {lead}'), row=1, col=1)

for lead in leads:
    fig.add_trace(go.Histogram(x=ecg_data[lead], name=f'Lead {lead}', opacity=0.75), row=2, col=1)

fig.update_traces(opacity=0.75, bingroup=1, row=2, col=1)
fig.update_layout(barmode='overlay')

fig.add_trace(
    go.Scatter(x=ecg_data['I'], y=ecg_data['II'], mode='markers', name='Lead I vs Lead II'),
    row=3, col=1
)

fig.add_trace(
    go.Scatter(x=ecg_data['time'], y=ecg_data['I'], mode='lines', name='Original Signal'),
    row=4, col=1
)
fig.add_trace(
    go.Scatter(x=ecg_data['time'], y=ecg_data['RollingAvg'], mode='lines', name='Rolling Average'),
    row=4, col=1
)

fig.update_layout(height=1600, title_text="Comprehensive ECG Data Analysis", showlegend=True)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(children=[
    html.H1(children='ECG Data Dashboard', style={'textAlign': 'center', 'color': '#007BFF'}),
    dcc.Graph(
        id='ecg-data-visualization',
        figure=fig
    )
], style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'})

# Optionally, add external CSS for styling
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
