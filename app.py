import streamlit as st
import numpy as np

from src.params import mental_health_data_path
from src.data_pipeline import DataPipeline
from src.data_viz import PlotBuilder

st.set_page_config(layout="wide")

def pct_value(frac, total):
    return round((frac / total)*100, 1)


data_pipeline = DataPipeline(mental_health_data_path)
plot_builder = PlotBuilder(data_pipeline)

list_country = ["Total"] + data_pipeline.get_country_list()
list_column = data_pipeline.get_column_list(only_desc=True)




### sidebar ###
st.sidebar.title('Visualización de datos - PRA 2')
st.sidebar.subheader("José Luis Rodriguez Andreu")
st.sidebar.write("Master Universitario en Ciencia de Datos")



# gender: Género correspondiente
# country: País correspondiente
# Ocupation: situación laboral del entrevistado
# self_employed: El entrevistado trabaja por cuenta propia (autónomo, freelance, etc.)
# family_history: Historial familiar de enfermedad mental
# treatment: Se ha buscado tratamiento para alguna condición de salud mental
# days_indoors: días ingresados
# growing_stress: Padecimiento de estrés
# changes_habits: cambio de habitos
# mental_helath_history: Historial propio de afecciones de salud mental
# mood_swings: cambios de humor
# coping_struggles: capacidad de afrontar los problemas
# work_interest: interés o motivación con el trabajo
# social_weakness: debilidad social
# mental_health_interview: Mención de un problema de salud mental en una entrevista de trabajo
# care_options: Opciones de cuidado


country = st.sidebar.selectbox(  
    "País",  
    list_country
)

column = st.sidebar.selectbox(  
    "Variable",  
    list_column
)


st.sidebar.markdown("""
Variables recogidas en el estudio:

| Variable | Descripción |
| --- | --- |
| gender | Género correspondiente |
| country | País correspondiente |
|Ocupation | situación laboral del entrevistado |
| self_employed | El entrevistado trabaja por cuenta propia (autónomo, freelance, etc.) |
| family_history | Historial familiar de enfermedad mental |
| treatment | Se ha buscado tratamiento para alguna condición de salud mental |
| days_indoors | días ingresados |
| growing_stress | Padecimiento de estrés |
| changes_habits | cambio de habitos |
| mental_helath_history | Historial propio de afecciones de salud mental |
| mood_swings | cambios de humor |
| coping_struggles | capacidad de afrontar los problemas |
| work_interest | interés o motivación con el trabajo |
| social_weakness | debilidad social |
| mental_health_interview | Mención de un problema de salud mental en una entrevista de trabajo |
| care_options | Opciones de cuidado |
""")


# main bar


st.title("Salud mental a lo largo del mundo")
st.subheader("Datos sobre hábitos de salud mental recogidos mediante encuestados")


# metrics
people_requested, man_requested, woman_requested =  data_pipeline.get_kpi_obs(country=country)

pct_woman = pct_value(woman_requested, people_requested)
pct_man = pct_value(man_requested, people_requested)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="total encuestados", value=people_requested)
with col2:
    st.metric(label="Mujeres encuestadas", value=f"{woman_requested} ({pct_woman}%)")
with col3:
    st.metric(label="Hombres encuestados", value=f"{man_requested} ({pct_man}%)")


# barplot
fig_barplot = plot_builder.build_barplot(country, column)
st.plotly_chart(fig_barplot, use_container_width=True)


# donuts
col4, col5 = st.columns(2)
with col4:
    try:
        fig_donut_woman = plot_builder.build_dount_gender(country=country, column=column, gender="Female")
        st.plotly_chart(fig_donut_woman, use_container_width=True)
    except:
        pass

with col5:
    try:
        fig_donut_man = plot_builder.build_dount_gender(country=country, column=column, gender="Male")
        st.plotly_chart(fig_donut_man, use_container_width=True)
    except:
        pass