import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input,dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import os

df =  pd.read_csv(os.path.dirname(__file__)+'\\MorbPorLocRes.csv', encoding='UTF-8',
                                                                   sep=";",
                                                                   decimal=",",
                                                                   low_memory=False,        
                                                                   )
df.insert(0, 'ID',  df['Território da Cidadania'].str[0:3])
df.insert(2, 'UF',  df['Território da Cidadania'].str[-3:])
df.insert(6, 'CM Internação', (df['Valor total']/df['Internações']).round(2))

df['Território da Cidadania'] = df['Território da Cidadania'].str[4:-4]

app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
fig = px.bar(df, x="UF", y="CM Internação", color="UF")
app.layout = html.Div( children=[
    html.H1(children='Análise de dados de Internações do SUS'),

    html.Div(children='''
             Despesas de SUS por Localidade de Residência
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        sort_action='native',
        sort_mode='single',
        style_cell={'textAlign': 'left'} 
    ),
  ],
)

if __name__ == '__main__':
    app.run_server(debug=True, port='8081')



