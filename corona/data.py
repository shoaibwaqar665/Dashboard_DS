import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
# Load and prepare the dataset
df = pd.read_csv('corona/corona_NLP_test_annotated.csv')
df['Tweet Length'] = df['tweet'].apply(len)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "COVID-19 Tweet Analysis Dashboard"

# Define dropdown options for sentiment filter
dropdown_options = [{'label': sentiment, 'value': sentiment} for sentiment in df['generated annotations'].unique()]

# Adjustments to the Dash app layout, focusing on the search bar styling
app.layout = html.Div([
    html.H1('COVID-19 Tweet Analysis Dashboard', style={'textAlign': 'center', 'color': 'RebeccaPurple'}),
    dcc.Dropdown(id='sentiment-filter', options=dropdown_options, value=[], multi=True, placeholder='Filter by sentiment', style={'marginBottom': '10px'}),
    html.Div(dcc.Input(id='keyword-search', type='text', placeholder='Search tweets by keyword', 
                       style={'width': '98%', 'padding': '10px', 'margin': '10px 0', 'borderRadius': '5px', 'border': '1px solid #ddd'})),
    dcc.Graph(id='tweet-analysis-plot'),
], style={'padding': '20px'})


@app.callback(
    Output('tweet-analysis-plot', 'figure'),
    [Input('sentiment-filter', 'value'),
     Input('keyword-search', 'value')]
)
def update_figure(selected_sentiments, search_keyword):
    # Filter the dataframe based on selected sentiments and search keyword
    filtered_df = df
    if selected_sentiments:
        filtered_df = filtered_df[filtered_df['generated annotations'].isin(selected_sentiments)]
    if search_keyword:
        filtered_df = filtered_df[filtered_df['tweet'].str.contains(search_keyword, case=False, na=False)]
    
    # Prepare sentiment counts for the filtered data
    sentiment_counts = filtered_df['generated annotations'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    
    # Recreate the figure with the filtered data
    fig = make_subplots(rows=2, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}], [{"colspan": 2}, None]],
                        subplot_titles=('Distribution of Tweet Sentiments', 'Sentiment Proportions', 'Histogram of Tweet Lengths'),
                        vertical_spacing=0.15, horizontal_spacing=0.1)
    
    color_palette = px.colors.qualitative.Plotly
    for i, sentiment in enumerate(sentiment_counts['Sentiment'].unique()):
        fig.add_trace(go.Bar(x=[sentiment], y=[sentiment_counts[sentiment_counts['Sentiment'] == sentiment]['Count'].values[0]],
                            name=sentiment, marker=dict(color=color_palette[i])), row=1, col=1)
    
    fig.add_trace(go.Pie(labels=sentiment_counts['Sentiment'], values=sentiment_counts['Count'], marker=dict(colors=color_palette)), row=1, col=2)
    fig.add_trace(go.Histogram(x=filtered_df['Tweet Length'], marker=dict(color='pink')), row=2, col=1)
    
    fig.update_layout(height=800, showlegend=True, title_text="Filtered COVID-19 Tweet Analysis")
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
