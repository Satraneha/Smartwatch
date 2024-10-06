import pandas as pd
from flask import Flask
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go  # Import for custom heatmap

# Load the dataset
data = pd.read_csv('C:\\Users\\BCS\\Desktop\\SMART WATCH ANALYSIS\\smart_watch_data.csv')

# Convert Date column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Initialize the Flask app
server = Flask(__name__)  # Create a Flask app instance

# Initialize the Dash app with the Flask server
app = dash.Dash(__name__, server=server,external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Initialize the Dash app
#app = dash.Dash(__name__)

# Add custom CSS
#app.css.append_css({
 #   'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})

# Define some colors and styles
colors = {
    'background': '#f0f2f5',
    'text': '#34495e',
    'header': '#2980b9',
    'card_background': '#ffffff',
    'card_shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
    'accent': '#e74c3c'
}
# App layout
app.layout = html.Div([
    html.Div([
        html.H1("Smart Watch Activity Dashboard", style={'textAlign': 'center', 'color': colors['header'], 
                       'fontFamily': 'Arial, sans-serif', 'fontWeight': 'bold', 
                       'padding': '20px 0', 'backgroundColor': '#ecf0f1', 
                       'borderRadius': '8px', 'boxShadow': colors['card_shadow']}),
    ], style={'marginBottom': '20px'}),
    #]),
    # Instruction section
    html.Div([
        html.P("Use the dropdown below to select a user and the date range to filter data:",
                style={'textAlign': 'center', 'fontSize': '18px', 'color': colors['text']}),
    ], style={'padding': '15px', 'backgroundColor': '#ffffff', 'borderRadius': '10px', 
              'boxShadow': colors['card_shadow'], 'marginBottom': '20px'}),

         # Dropdown and Date Picker section
    html.Div([
        dcc.Dropdown(
            id='user-id-dropdown',
            options=[{'label': str(i), 'value': i} for i in data['UserId'].unique()],
            placeholder="Select User",
            value=None,
            style={'width': '48%', 'display': 'inline-block', 'marginRight': '10px',
                   'padding': '10px', 'borderRadius': '5px','justify-content': 'center','boxShadow': colors['card_shadow']}
        ),

        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=data['Date'].min().date(),
            end_date=data['Date'].max().date(),
            display_format='YYYY-MM-DD',
            style={'width': '48%', 'display': 'inline-block', 'padding': '10px',
                   'borderRadius': '5px','justify-content': 'center' , 'boxShadow': colors['card_shadow']}
        ),
    ], style={'display': 'flex', 'justify-content': 'center', 'marginBottom': '30px'}),
    
        # Key metrics cards section
    html.Div([
        html.Div([
            html.Div([
                html.H4("Total Steps", style={'color': colors['text']}),
                html.P(id='total-steps', style={'fontSize': '24px', 'color': colors['header']}),
            ], className='card-container', style={'backgroundColor': colors['card_background'], 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center', 'boxShadow': colors['card_shadow']})
        ], className='three columns'),

        html.Div([
            html.Div([
                html.H4("Total Distance", style={'color': colors['text']}),
                html.P(id='total-distance', style={'fontSize': '24px', 'color': colors['header']}),
            ], className='card-container', style={'backgroundColor': colors['card_background'], 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center', 'boxShadow': colors['card_shadow']})
        ], className='three columns'),

        html.Div([
            html.Div([
                html.H4("Calories Burned", style={'color': colors['text']}),
                html.P(id='calories-burned', style={'fontSize': '24px', 'color': colors['header']}),
            ], className='card-container', style={'backgroundColor': colors['card_background'], 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center', 'boxShadow': colors['card_shadow']})
        ], className='three columns'),
    ], className='row', style={'marginTop': '20px', 'padding': '20px'}),

         # Graph section
    html.Div([
        dcc.Graph(id='calories-burned-graph'),   
        dcc.Graph(id='steps-distance-graph'),# New graph for Total Distance vs Active Minutes
        dcc.Graph(id='distance-minutes-graph'),
        dcc.Graph(id='distance-bar-graph'),  # New distance bar graph
        dcc.Graph(id='minutes-bar-graph'),
        dcc.Graph(id='correlation-matrix')
    ], style={'marginTop': '20px', 'padding': '20px', 'backgroundColor': '#ffffff', 'borderRadius': '10px', 'boxShadow': colors['card_shadow']}),
    #], style={'maxWidth': '1200px', 'margin': 'auto', 'padding': '20px', 'backgroundColor': colors['background'], 'borderRadius': '10px'})
    html.Div([
        html.H4("Personalized Health Suggestions", style={'color': colors['text'], 'textAlign': 'center'}),
        html.P(id='health-suggestions', style={'fontSize': '18px', 'color': colors['accent'], 'padding': '20px'})
    ], style={'backgroundColor': '#ffffff', 'borderRadius': '10px', 'boxShadow': colors['card_shadow'], 'marginTop': '30px'})
    ], style={'maxWidth': '1200px', 'margin': 'auto', 'padding': '20px', 'backgroundColor': colors['background'], 'borderRadius': '10px'})

# Callback for updating the dashboard
@app.callback(
    [Output('calories-burned-graph', 'figure'),
     Output('steps-distance-graph', 'figure'),
     Output('distance-minutes-graph', 'figure'),
     Output('distance-bar-graph', 'figure'),  # New distance bar graph output
     Output('minutes-bar-graph', 'figure'),
     Output('correlation-matrix', 'figure'),
     Output('total-steps', 'children'),
     Output('total-distance', 'children'),
     Output('calories-burned', 'children'),
     Output('health-suggestions', 'children')],
    [Input('user-id-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graphs(selected_user, start_date, end_date):
     # Check if a user and date range have been selected
    if selected_user is None or start_date is None or end_date is None:
        # Return empty figures and placeholders if nothing is selected
        empty_figure = {}
        empty_value = 'N/A'
        return (empty_figure, empty_figure, empty_figure, empty_figure, empty_figure,
                empty_value, empty_value, empty_value, empty_value, empty_value)

    # Filter data based on the selected user
    filtered_data = data
    if selected_user is not None:
        filtered_data = filtered_data[filtered_data['UserId'] == selected_user]
    
    # Further filter data based on the selected date range
    filtered_data = filtered_data[
        (filtered_data['Date'] >= start_date) & (filtered_data['Date'] <= end_date)
    ]
    # Calories burned over time
    calories_fig = px.line(filtered_data, x='Date', y='Calories Burned',
                           title='Calories Burned Over Time',
                           color_discrete_sequence=['#e74c3c'])

    # Steps vs Total Distance
    steps_distance_fig = px.scatter(filtered_data, x='Steps', y='Total Distance',
                                    title='Steps vs Total Distance',
                                    trendline="ols", color_discrete_sequence=['#2ecc71'])

    
    # Total Distance vs Active Minutes
    distance_minutes_fig = px.scatter(filtered_data, x='Total Distance', y='Very Active Minutes',
                                      title='Total Distance vs Active Minutes',
                                      trendline="ols", color_discrete_sequence=['#3498db'])

    # Bar graph for distances
    distance_fig = px.bar(
        x=['Very Active Distance', 'Moderately Active Distance', 'Light Active Distance', 'Sedentary Active Distance'],
        y=filtered_data[['Very Active Distance', 'Moderately Active Distance', 'Light Active Distance', 'Sedentary Active Distance']].sum(),
        title="Distance by Activity Type",
        labels={'x': 'Activity Type', 'y': 'Distance (km)'}
    )

    # Bar graph for active minutes
    minutes_fig = px.bar(
        x=['Very Active Minutes', 'Fairly Active Minutes', 'Lightly Active Minutes', 'Sedentary Minutes'],
        y=filtered_data[['Very Active Minutes', 'Fairly Active Minutes', 'Lightly Active Minutes', 'Sedentary Minutes']].sum(),
        title="Active Minutes by Activity Type",
        labels={'x': 'Activity Type', 'y': 'Minutes'}
    )

 # Correlation matrix
    correlation_data = filtered_data[['Steps', 'Total Distance', 'Calories Burned', 'Very Active Minutes', 'Fairly Active Minutes', 'Lightly Active Minutes', 'Sedentary Minutes']]
    correlation_matrix = correlation_data.corr()  # Compute correlation matrix


# Create heatmap for correlation matrix
    heatmap = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='Viridis'
    ))
    heatmap.update_layout(title='Correlation Matrix', xaxis_title="Variables", yaxis_title="Variables")

    # Analyzing user's data to generate health suggestions
    total_steps = filtered_data['Steps'].sum()
    total_distance = filtered_data['Total Distance'].sum()
    total_calories = filtered_data['Calories Burned'].sum()
    active_minutes = filtered_data['Very Active Minutes'].sum()

    suggestions = []

    # Step Analysis
    if total_steps < 7000:
        suggestions.append(f"Your total steps are {total_steps:,}. Consider increasing your daily step count to at least 7,000 for better health.")
    elif total_steps < 10000:
        suggestions.append(f"Great job! You have taken {total_steps:,} steps. Try to reach 10,000 steps a day for optimal health.")
    else:
        suggestions.append(f"Fantastic! You've taken {total_steps:,} steps. Keep up the great work!")

    # Distance Analysis
    if total_distance < 5:
        suggestions.append(f"You have covered {total_distance:.2f} km. Aim for at least 5 km of walking per day to stay active.")
    else:
        suggestions.append(f"Excellent! You've covered {total_distance:.2f} km. You're meeting the recommended activity levels.")

    # Calories Burned Analysis
    if total_calories < 2000:
        suggestions.append(f"You've burned {total_calories:,} kcal. Increase physical activity to burn more calories and maintain a healthy weight.")
    else:
        suggestions.append(f"You're doing well! You've burned {total_calories:,} kcal, which is a good amount for maintaining fitness.")

    # Active Minutes Analysis
    if active_minutes < 30:
        suggestions.append(f"Try to increase your very active minutes. You're currently at {active_minutes} minutes, but 30+ minutes daily is recommended.")
    else:
        suggestions.append(f"You're doing great with {active_minutes} active minutes. Keep it up!")
    
    # Calculate totals for cards
    total_steps = filtered_data['Steps'].sum()
    total_distance = filtered_data['Total Distance'].sum()
    total_calories = filtered_data['Calories Burned'].sum()
    
    return (calories_fig, steps_distance_fig, distance_minutes_fig, distance_fig, minutes_fig,heatmap,
            f"{total_steps:,}", f"{total_distance:.2f} km", f"{total_calories:,} kcal", " ".join(suggestions))

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
