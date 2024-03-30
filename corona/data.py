import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Load and prepare the dataset
df = pd.read_csv('corona/corona_NLP_test_annotated.csv')
sentiment_counts = df['generated annotations'].value_counts().reset_index()
sentiment_counts.columns = ['Sentiment', 'Count']
df['Tweet Length'] = df['tweet'].apply(len)
color_palette = px.colors.qualitative.Plotly

# Create a Plotly figure
fig = make_subplots(rows=2, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}], [{"colspan": 2}, None]],
                    subplot_titles=('Distribution of Tweet Sentiments', 'Sentiment Proportions', 'Histogram of Tweet Lengths'),
                    vertical_spacing=0.15, horizontal_spacing=0.1)

for i, sentiment in enumerate(sentiment_counts['Sentiment'].unique()):
    fig.add_trace(go.Bar(x=[sentiment], y=[sentiment_counts[sentiment_counts['Sentiment'] == sentiment]['Count'].values[0]],
                        name=sentiment, marker=dict(color=color_palette[i]), hoverinfo='y+name'), row=1, col=1)

fig.add_trace(go.Pie(labels=sentiment_counts['Sentiment'], values=sentiment_counts['Count'], name="Sentiment",
                     hoverinfo='label+percent', marker=dict(colors=color_palette)), row=1, col=2)

fig.add_trace(go.Histogram(x=df['Tweet Length'], name='Tweet Length', marker=dict(color='rgba(0, 0, 0, 0.5)'),
                           hoverinfo='x+y'), row=2, col=1)

fig.update_layout(height=1000, showlegend=True, title_text="COVID-19 Tweet Analysis Dashboard",
                  legend_title_text='Sentiment', template='plotly_white', title_font=dict(size=24, color="RebeccaPurple"),
                  margin=dict(l=20, r=20, t=85, b=20), paper_bgcolor='rgba(243, 243, 243, 1)',
                  plot_bgcolor='rgba(243, 243, 243, 1)')

fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='lightgrey')
fig.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='lightgrey')
fig.update_yaxes(title_font=dict(size=14, color="DarkBlue"))
fig.update_xaxes(title_font=dict(size=14, color="DarkBlue"))

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(style={'textAlign': 'center', 'width': '80%', 'margin': 'auto'}, children=[
    html.H1('COVID-19 Tweet Analysis Dashboard', style={'color': 'RebeccaPurple'}),
    dcc.Graph(id='covid-tweet-analysis', figure=fig),
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
