import pandas as pd



class DataPipeline():

    def __init__(self, data_path):

        self.df = pd.read_csv(data_path).dropna()

    
    def get_data(self):
        return self.df
    
    
    def get_column_list(self, only_desc = False):

        column_list = self.df.columns.drop('Timestamp')
        
        if only_desc:
            column_list = column_list.drop(['Gender', 'Country'])
            
        return list(column_list)
    

    def get_country_list(self):
        return list(self.df.Country.drop_duplicates())


    def filter_country(self, country):

        if country != 'Total':
            df_country = self.df[self.df['Country'] == country]
        else:
            df_country = self.df
        
        return df_country
        

    def get_kpi_obs(self, country):

        df_country = self.filter_country(country)
        people_requested = df_country.shape[0]
        try:
            man_requested = df_country['Gender'].value_counts()['Male']
        except:
            man_requested = 0
        try:
            woman_requested = df_country['Gender'].value_counts()['Female']
        except: 
            woman_requested = 0

        return people_requested, man_requested, woman_requested


    def get_agg_data(self, country, column, use_gender = False):

        df_country = self.filter_country(country)

        if use_gender:
            df_agg = (
                df_country
                .groupby([column, 'Gender'])
                .agg(count_values = (column, 'count'))
                .reset_index()
            )
        else:
            df_agg = (
                df_country
                .groupby([column])
                .agg(count_values = (column, 'count'))
                .reset_index()
            )

        return df_agg
    

    def get_agg_by_gender(self, country, column, gender):

        df_country = self.filter_country(country)
        df_gender = df_country[df_country['Gender'] == gender]

        df_agg = (
                df_gender
                .groupby([column])
                .agg(count_values = (column, 'count'))
                .reset_index()
        )

        return df_agg