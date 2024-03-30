import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import psycopg2
# Load and prepare the dataset

db_params = {
    'dbname': 'corona',
    'user': 'postgres',
    'password': 'shoaib123',
    'host': 'localhost'  # or your database server IP
}
# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "COVID-19 Tweet Analysis Dashboard"
conn = psycopg2.connect(**db_params)
cur = conn.cursor()
cur.execute("SELECT DISTINCT generated_annotations FROM tweets;")
dropdown_options = [{'label': row[0], 'value': row[0]} for row in cur.fetchall()]
conn.close()
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
    # Prepare the query with dynamic filtering based on user input
    query = """
    SELECT tweet, generated_annotations, explanation, CHAR_LENGTH(tweet) AS tweet_length
    FROM tweets WHERE 1=1
    """
    params = []
    if selected_sentiments:
        query += " AND generated_annotations IN %s"
        params.append(tuple(selected_sentiments))
    if search_keyword:
        keyword_filter = f'%{search_keyword}%'
        query += " AND (tweet LIKE %s OR explanation LIKE %s)"
        params.extend([keyword_filter, keyword_filter])
    
    # Execute the query
    df_filtered = pd.DataFrame()  # Initialize an empty DataFrame in case the query returns no results
    with psycopg2.connect(**db_params) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        if rows:
            df_filtered = pd.DataFrame(rows, columns=['tweet', 'generated_annotations', 'explanation', 'tweet_length'])

    # Create the subplot structure with increased size
    fig = make_subplots(rows=2, cols=2, 
                        specs=[[{"type": "bar"}, {"type": "pie"}], [{"colspan": 2}, None]],
                        subplot_titles=('Sentiment Distribution', 'Sentiment Proportion', 'Tweet Length Distribution'),
                      vertical_spacing=0.18, horizontal_spacing=0.1)
  # Adjust vertical spacing to accommodate larger charts

    # Check if the filtered DataFrame is not empty
    if not df_filtered.empty:
        sentiment_counts = df_filtered['generated_annotations'].value_counts()

        # Bar Chart for Sentiment Distribution, now with color
        fig.add_trace(
            go.Bar(x=sentiment_counts.index, y=sentiment_counts.values, name='Sentiment Distribution', marker_color='royalblue'),
            row=1, col=1
        )

        # Pie Chart for Sentiment Proportion
        fig.add_trace(
            go.Pie(labels=sentiment_counts.index, values=sentiment_counts.values, name='Sentiment Proportion'),
            row=1, col=2
        )

        # Histogram for Tweet Length Distribution
        fig.add_trace(
            go.Histogram(x=df_filtered['tweet_length'], name='Tweet Length'),
            row=2, col=1
        )

    else:
        # If no data matches the filters, display a message
        fig.add_annotation(text="No data matches the selected filters.", x=0.5, y=0.5, showarrow=False, font_size=16, xref="paper", yref="paper")

    # Update layout for better visual representation and increased size
    fig.update_layout(
        height=800,  # Increased height for larger display
        width=1200,  # New width to accommodate the layout
        showlegend=True,
        title_text="COVID-19 Tweet Analysis Dashboard"
    )

    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
