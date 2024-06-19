import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.graph_objects as go
import plotly.express as px

from src.data_pipeline import DataPipeline


class PlotBuilder:

    def __init__(self, data_pipeline: DataPipeline):
        self.data_pipeline = data_pipeline


    def build_barplot(self, country, column):

        df_agg = self.data_pipeline.get_agg_data(country, column, use_gender = False)

        fig = px.bar(
            df_agg.sort_values('count_values', ascending=False).reset_index(drop=True),
            x=column,
            y="count_values",
            color=column,
            title=f"Frecuencia por {column} (País: {country})"
        )
        fig.update_layout(showlegend=False)

        return fig
    

    def build_dount_gender(self, country, column, gender):

        df_agg = self.data_pipeline.get_agg_by_gender(country, column, gender)

        if gender == "Female":
            donut_title = f'Frecuencia de {column} en mujeres (País: {country})'
        else:
            donut_title = f'Frecuencia de {column} en hombres (País: {country})'

        fig = px.pie(
            df_agg, 
            values='count_values',
            names=column,
            hole=.5, 
            title=donut_title
        )

        return fig

