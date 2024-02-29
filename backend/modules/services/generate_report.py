import random
import base64
from datetime import datetime, timedelta
from io import BytesIO
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

###############################################################################

STATIC_PATH = 'resources/static/'

class Report:

    @staticmethod
    def generate_charts(metadata_list):
        series = metadata_list
        ChartsPaths = []

        # Create a new dictionary to restructure the data
        restructured_data = {}
        # Loop through each dictionary in the series
        for data_dict in series:
            # Get the key (e.g., 'Minimal', 'Recommended', 'Extended')
            key = list(data_dict.keys())[0]

            # Get the value (a list of dictionaries)
            value = data_dict[key]

            # Add the value to the restructured_data dictionary with the key
            restructured_data[key] = value

        # Initializing variables
        x_values = ['F', 'A', 'I', 'R']
        chartTitle = ''

        # Custom legend text based on color
        # Custom legend text based on color
        color_legend_mapping = {
            'blue': 'Partially completed',
            'red': 'No metadata found',
            'green': 'Totally Completed',
            'white': 'N/A (hashed)'
        }

        for key, value_list in restructured_data.items():
            chartTitle = key
            for value_dict in value_list:
                data = value_dict['data']

                # Create a new list to store updated colors and y-axis values
                colors = []
                y_values = []

                # Update the colors and y-axis values based on the condition
                for index, value in enumerate(data):
                    if value == 0:
                        if index == 1 or index == 2: 
                            # Set value to 100 and color to white for the hashed pattern
                            y_values.append(100)
                            colors.append('white')
                        else:
                            y_values.append(value)
                            colors.append('red')
                    elif value == 100:
                        y_values.append(value)
                        colors.append('green')
                    else:
                        y_values.append(value)
                        colors.append('blue')

                # Custom legend text for each color
                custom_legend_text = [color_legend_mapping[color] for color in colors]

                # Create a new figure for each data set
                fig = go.Figure()
                for i in range(len(data)):
                    if i == 1 or i == 2:
                        fig.add_trace(go.Bar(x=[x_values[i]], y=[y_values[i]], marker=dict(color=colors[i], pattern_shape='x'), name=custom_legend_text[i]))
                    else:
                        fig.add_trace(go.Bar(x=[x_values[i]], y=[y_values[i]], marker=dict(color=colors[i]), name=custom_legend_text[i]))

                # Set the maximum value for the y-axis
                max_y_value = 100  # Set your desired maximum value here
                fig.update_yaxes(range=[0, max_y_value])

                fig.update_layout(title="FAIR metadata distribution", showlegend=True)
                
                image_path = chartTitle + '.png'
                pio.write_image(fig, STATIC_PATH + image_path)
                ChartsPaths.append(image_path)

        if (ChartsPaths!=""):
            # Create the response dictionary
            AllChartsPaths = {
                "minimal_chart": ChartsPaths[0],
                "recommended_chart": ChartsPaths[1],
                "extended_chart": ChartsPaths[2],
            }   
        
        else : 
           AllChartsPaths={}

        return AllChartsPaths

###################

    @staticmethod
    def generate_and_save_scatter_chart(img_path, scatter_data):
        y_dates = [point.get('y_date', None) for point in scatter_data]
        x_scores = [point.get('x_score', None) for point in scatter_data]

        if None in y_dates or None in x_scores:
            raise ValueError("Invalid scatter data format")

        plt.figure(figsize=(10, 6))
        plt.scatter(y_dates, x_scores)
        plt.xlabel('Y Date d\'evaluation')
        plt.ylabel('X Score de FAIRness')
        plt.title('Scatter Chart')

        # Save the scatter chart as a PNG image
        plt.savefig(STATIC_PATH+img_path)
        plt.close()

###################

    @staticmethod
    def generate_and_save_scatter_chart_plotly(img_path, scatter_data):
        y_dates = [point.get('y_date', None) for point in scatter_data]
        x_scores = [point.get('x_score', None) for point in scatter_data]
        print("ydates", y_dates)
        if None in y_dates or None in x_scores:
            raise ValueError("Invalid scatter data format")

        # Create a scatter chart using Plotly
        fig = px.scatter(x=y_dates, y=x_scores, labels={'x': "Date d'évaluation", 'y':  'Score de FAIRness'},
                         title='Scatter Chart')
        fig.update_xaxes(type='date')  # Set x-axis type to date
        fig.update_layout(yaxis_range=[0,100])
        # Save the scatter chart as an HTML file
        #plotly_html_path = STATIC_PATH + img_path + ".html"
        #fig.write_html(plotly_html_path)

        # If you want to save an image (PNG), you can use the write_image function
        fig.write_image(STATIC_PATH + img_path)
        
##############################################################################


