import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

# Load the dataset
df = pd.read_csv('corona/corona_NLP_test_annotated.csv')

# Prepare sentiment counts for the bar and pie charts
sentiment_counts = df['generated annotations'].value_counts().reset_index()
sentiment_counts.columns = ['Sentiment', 'Count']

# Calculate tweet lengths for the histogram
df['Tweet Length'] = df['tweet'].apply(len)

# Define a color palette for consistency across plots
color_palette = px.colors.qualitative.Plotly

# Create a figure with subplots
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"type": "bar"}, {"type": "pie"}], [{"colspan": 2}, None]],
    subplot_titles=('Distribution of Tweet Sentiments', 'Sentiment Proportions', 'Histogram of Tweet Lengths'),
    vertical_spacing=0.15,  # Adjusted vertical spacing for clarity
    horizontal_spacing=0.1  # Adjusted horizontal spacing for separation between plots
)

# Add the bar chart for sentiment distribution to the first row, first column
for i, sentiment in enumerate(sentiment_counts['Sentiment'].unique()):
    fig.add_trace(
        go.Bar(
            x=[sentiment], 
            y=[sentiment_counts[sentiment_counts['Sentiment'] == sentiment]['Count'].values[0]],
            name=sentiment,
            marker=dict(color=color_palette[i]),
            hoverinfo='y+name'
        ),
        row=1, col=1
    )

# Add the pie chart for sentiment proportions to the first row, second column
fig.add_trace(
    go.Pie(
        labels=sentiment_counts['Sentiment'],
        values=sentiment_counts['Count'],
        name="Sentiment",
        hoverinfo='label+percent',
        marker=dict(colors=color_palette),
    ),
    row=1, col=2
)

# Add the histogram for tweet lengths to the second row, spanning both columns
fig.add_trace(
    go.Histogram(
        x=df['Tweet Length'],
        name='Tweet Length',
        marker=dict(color='rgba(0, 0, 0, 0.5)'),
        hoverinfo='x+y'
    ),
    row=2, col=1
)

# Customize the layout for styling and spacing
fig.update_layout(
    height=1000,  # Adjusted height for a better layout
    showlegend=True,
    title_text="COVID-19 Tweet Analysis Dashboard",
    legend_title_text='Sentiment',
    template='plotly_white',
    title_font=dict(size=24, color="RebeccaPurple"),  # Styling for the main title
    margin=dict(l=20, r=20, t=85, b=20),  # Margins adjusted for a clean layout
    paper_bgcolor='rgba(243, 243, 243, 1)',  # Consistent background color
    plot_bgcolor='rgba(243, 243, 243, 1)',  # Matching plot background
)

# Update axes and grid lines for clarity and style
fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='lightgrey')
fig.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='lightgrey')

# Update axes titles with custom font styling
fig.update_yaxes(title_font=dict(size=14, color="DarkBlue"))
fig.update_xaxes(title_font=dict(size=14, color="DarkBlue"))

# Annotations for additional insights or comments
fig.add_annotation(
    text="Distribution of tweet lengths",
    xref="paper", yref="paper",
    x=0.5, y=0.4, showarrow=False,
    font=dict(size=12, color="DarkSlateGray"),
    align="center"
)

# Display the dashboard
fig.show()
