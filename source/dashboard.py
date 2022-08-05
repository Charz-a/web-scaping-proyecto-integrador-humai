import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import pathlib
from datetime import date


path = str(pathlib.Path(__file__).parent.absolute())
hoy = date.today().strftime("%d-%m-%Y") # dd/mm/YY
file = path + f'/actividades_{hoy}.csv'

try:
    df = pd.read_csv(file, sep='\t')
except:
    # correr el scrapper? avisar que no corrió todavia?
    df =  pd.read_csv("/home/developer/training/proyecto_integrador_humai/data/prueba.csv", sep='\t')


df['count'] = df[df.columns[0]].count()

dftodos = df.groupby("activity_district").agg({"activity_id": "count"}).reset_index()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# componentes
dfc = df[~df.activty_place.isna()]
a = list(dfc.activty_place.unique())
a.append('Todos')
app.layout = html.Div([
    html.H4('Cantidad de actividades por zona'),
    dcc.Graph(id="graph", figure={}),
    html.P("Tipos de lugar:"),
    dcc.Dropdown(id='zona',
        options=a,
        value='Todos', clearable=False
    ),
])

# callbacks
@app.callback(
    Output("graph", "figure"),
    Input("zona", "value"))
def generate_chart(lugar: str):
    if lugar == "Todos":
        fig = px.pie(dftodos, values="activity_id", names="activity_district") #activity_id tiene valor de count XD
    else:
        dfg = df[df["activty_place"] == lugar].groupby("activity_district").agg({"activity_id": "count"}).reset_index()
        fig = px.pie(dfg, values="activity_id", names="activity_district")
    
    return fig

if __name__ == '__main__':
    app.run_server(port=8050) #mode='inline'