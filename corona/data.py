import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load the dataset
df = pd.read_csv('corona_NLP_test_annotated.csv')

# Prepare sentiment counts for the bar and pie charts
sentiment_counts = df['generated annotations'].value_counts().reset_index()
sentiment_counts.columns = ['Sentiment', 'Count']

# Calculate tweet lengths for the histogram
df['Tweet Length'] = df['tweet'].apply(len)

# Create a figure with subplots
fig = make_subplots(
    rows=2, cols=2,  # Adjusted for an additional pie chart
    specs=[[{"type": "bar"}, {"type": "pie"}], [{"colspan": 2}, None]],  # Specifies the types and arrangements of plots
    subplot_titles=('Distribution of Tweet Sentiments', 'Sentiment Proportions', 'Histogram of Tweet Lengths')
)

# Add the bar chart for sentiment distribution to the first row, first column
for sentiment in sentiment_counts['Sentiment'].unique():
    fig.add_trace(
        go.Bar(
            x=[sentiment], 
            y=[sentiment_counts[sentiment_counts['Sentiment'] == sentiment]['Count'].values[0]],
            name=sentiment
        ),
        row=1, col=1
    )

# Add the pie chart for sentiment distribution to the first row, second column
fig.add_trace(
    go.Pie(
        labels=sentiment_counts['Sentiment'],
        values=sentiment_counts['Count'],
        name="Sentiment"
    ),
    row=1, col=2
)

# Add the histogram for tweet lengths to the second row, spanning both columns
fig.add_trace(
    go.Histogram(
        x=df['Tweet Length'],
        name='Tweet Length'
    ),
    row=2, col=1
)

# Update layout for the entire figure
fig.update_layout(
    height=800,
    showlegend=True,
    title_text="COVID-19 Tweet Analysis: Sentiment Distribution and Tweet Length"
)

# Update y-axis labels for the bar chart and histogram
fig.update_yaxes(title_text="Number of Tweets", row=1, col=1)
fig.update_yaxes(title_text="Count", row=2, col=1)

# Update x-axis label for the histogram
fig.update_xaxes(title_text="Tweet Length", row=2, col=1)

# Show the figure
fig.show()
