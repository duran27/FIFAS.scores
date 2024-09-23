import dash
from dash import dcc, html
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Nuevos datos actualizados
data = {
    'ID': ['nicolasdurant27', 'josechure15', 'kenomena15', 'MP11_GT'],
    'PJ': [827, 503, 585, 726],
    'Goles': [751, 96, 488, 288],
    'Asistencias': [409, 150, 240, 481],
    'Efectividad Tiros': [27, 22, 24, 20],
    'Efectividad Pases': [78, 61, 76, 72],
    'MVPs': [229, 10, 106, 137]
}

# Crear DataFrame
df = pd.DataFrame(data)

# Función para obtener el podio de las categorías
def obtener_podio(df, columna):
    return df.nlargest(3, columna)[['ID', columna]]

# Layout de la aplicación
app.layout = dbc.Container([
    html.H1("Ranking de Jugadores - Estadísticas", style={'text-align': 'center'}),

    dbc.Row([
        dbc.Col([
            html.H4("Selecciona una categoría:"),
            dcc.Dropdown(
                id='categoria-dropdown',
                options=[
                    {'label': 'Goles', 'value': 'Goles'},
                    {'label': 'Asistencias', 'value': 'Asistencias'},
                    {'label': 'Efectividad en Tiros', 'value': 'Efectividad Tiros'},
                    {'label': 'Efectividad en Pases', 'value': 'Efectividad Pases'},
                    {'label': 'MVPs', 'value': 'MVPs'}
                ],
                value='Goles'
            )
        ], width=4)
    ], justify='center'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='podio-graph')
        ], width=12)
    ]),

    # Añadir un div para mostrar el ganador
    dbc.Row([
        dbc.Col([
            html.Div(id='mensaje-ganador', style={'text-align': 'center', 'font-size': '20px', 'margin-top': '20px'})
        ], width=12)
    ])

], fluid=True)

# Callback para actualizar el gráfico y mostrar el ganador
@app.callback(
    [Output('podio-graph', 'figure'),
     Output('mensaje-ganador', 'children')],
    [Input('categoria-dropdown', 'value')]
)
def actualizar_podio(categoria):
    podio = obtener_podio(df, categoria)
    
    # Crear gráfico de barras
    fig = go.Figure(data=[
        go.Bar(x=podio['ID'], y=podio[categoria], text=podio[categoria], textposition='auto')
    ])

    fig.update_layout(
        title=f"Top 3 Jugadores por {categoria}",
        xaxis_title="Jugador",
        yaxis_title=categoria,
        template='plotly_dark'
    )

    # Mensaje con el ganador
    ganador = podio.iloc[0]['ID']
    mensaje = f"El ganador en la categoría {categoria} es: {ganador}"

    return fig, mensaje

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
