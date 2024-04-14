import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

sites = spacex_df['Launch Site'].unique()

options = [{'label': 'All Sites', 'value': 'ALL'}]
options.extend([{'label': site, 'value': site} for site in sites])

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',
                                             options=options,
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={i: '{}'.format(i) for i in range(0, 10001, 2000)},
                                                value=[min_payload, max_payload]),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
# TASK 2:
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')]
)
def update_pie_chart(selected_site):
    # Filter data based on selected launch site
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    # Group data by outcome
    pie_chart_data = filtered_df.groupby('class').size().reset_index(name='count')
    
    # Create pie chart
    pie_fig = px.pie(pie_chart_data, values='count', names='class', title='Total Success Launches by Site')
    
    return pie_fig

# TASK 4:
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter data based on selected launch site
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    # Filter data based on payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]
    
    # Create scatter plot
    scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                              color='Booster Version Category', 
                              title='Payload Success Scatter Chart',
                              labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Outcome'},
                              hover_name='Launch Site')
    
    # Update layout
    scatter_fig.update_layout(xaxis={'title': 'Payload Mass (kg)'},
                              yaxis={'title': 'Launch Outcome'},
                              margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                              hovermode='closest')
    
    return scatter_fig

# Run the app
if __name__ == '__main__':
    app.run_server() 