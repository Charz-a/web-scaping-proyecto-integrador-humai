import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from datetime import date
import pathlib
import os

months = {  "1":"Enero",
            "2":"Febrero",
            "3":"Marzo",
            "4":"Abril",
            "5":"Mayo",
            "6":"Junio",
            "7":"Julio",
            "8":"Agosto",
            "9":"Septiembre",
            "10":"Octubre",
            "11":"Noviembre",
            "12":"Diciembre"  }

path = str(pathlib.Path(__file__).parent.parent.absolute()) + "/data/" 


li = []

for filename in os.listdir(path):
    if filename not in ["test_auto.txt","actividades.csv"]:
        df = pd.read_csv(path+filename, index_col=None, header=0,sep="\t")
        df["date"] =  filename[12:22]
        li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame['month'] =  frame["date"].str[4]
frame['month'] = frame["month"].replace(months)


############### QUERIES #############
por_lugar = frame.groupby("activty_place").agg({"activity_id": "count"}).reset_index() # Cantidad de actividades por tipo de lugar

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# componentes
dfc = frame[~frame.month.isna()]
a = list(dfc.month.unique())
a.append('Todos')
app.layout = html.Div([
    html.H4('Cantidad de actividades por tipo de lugar filtradas por mes'),
    dcc.Graph(id="graph", figure={}),
    html.P("Elegir mes:"),
    dcc.Dropdown(id='mes',
        options=a,
        value='Todos', clearable=False
    ),
])

@app.callback(
    Output("graph", "figure"),
    Input("mes", "value"))
def generate_chart(mes: str):
    if mes == "Todos":
        fig = px.pie(por_lugar, values="activity_id", names="activty_place") #activity_id tiene valor de count XD
    else:
        dfg = frame[frame["month"] == mes].groupby("activty_place").agg({"activity_id": "count"}).reset_index() #Cantidad de actividades en el mes dado por tipo de lugar
        fig = px.pie(dfg, values="activity_id", names="activty_place")
    
    return fig

if __name__ == '__main__':
    app.run_server(port=8050) #mode='inline'