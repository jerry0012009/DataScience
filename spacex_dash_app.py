# Import required libraries
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

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[{'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],value='ALL',placeholder='Select a Launch Site here',searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,  # 滑块的起始点
                                    max=10000,  # 滑块的结束点
                                    step=1000,  # 滑块的间隔
                                    # marks={i: '{} Kg'.format(i) for i in range(0, 10001, 1000)},  # 滑块上的标记
                                    marks={i: '{} Kg'.format(i) for i in range(0, 10001, 1000)},
                                    value=[min_payload, max_payload]  # 当前选择的范围
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches for All Sites')
        return fig
    # else:
    #     filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    #     fig = px.pie(filtered_df, values='class', 
    #     names='class', 
    #     title=f'Total Launches by Outcome for {entered_site}')
    #     return fig
        # return the outcomes piechart for a selected site
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site].copy()
        filtered_df['Outcome'] = filtered_df['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(filtered_df, names='Outcome', 
                    title=f'Total Launches by Outcome for {entered_site}',
                    color='Outcome',
                    color_discrete_map={'Success':'green', 'Failure':'red'})
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter(selected_site, payload_range):
    # 根据有效载荷范围筛选数据
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    # 检查是否选择了所有发射场地或特定发射场地
    if selected_site == 'ALL':
        # 为所有发射场地渲染散点图
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
    else:
        # 筛选特定发射场地的数据
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        # 为特定发射场地渲染散点图
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Outcome for {selected_site}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
