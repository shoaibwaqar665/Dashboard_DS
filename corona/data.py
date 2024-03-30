import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

# Load the dataset
df = pd.read_csv('corona_NLP_test_annotated.csv')

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
    vertical_spacing=0.1
)

# Bar chart for sentiment distribution
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

# Pie chart for sentiment proportions
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

# Histogram for tweet lengths
fig.add_trace(
    go.Histogram(
        x=df['Tweet Length'],
        name='Tweet Length',
        marker=dict(color='rgba(0, 0, 0, 0.5)'),
        hoverinfo='x+y'
    ),
    row=2, col=1
)

# Customize the layout
fig.update_layout(
    height=800,
    showlegend=True,
    title_text="COVID-19 Tweet Analysis Dashboard",
    legend_title_text='Sentiment',
    template='plotly_white'
)

# Update axes titles
fig.update_yaxes(title_text="Number of Tweets", row=1, col=1)
fig.update_xaxes(title_text="Sentiment", row=1, col=1)
fig.update_yaxes(title_text="Count", row=2, col=1)
fig.update_xaxes(title_text="Tweet Length", row=2, col=1)

# Add annotations or dynamic titles if necessary
# For example, an annotation for the histogram
fig.add_annotation(
    text="Distribution of tweet lengths",
    xref="paper", yref="paper",
    x=0.5, y=0.4, showarrow=False,
    font=dict(size=12, color="rgba(0, 0, 0, 0.5)"),
    align="center"
)

# Show the figure
fig.show()
