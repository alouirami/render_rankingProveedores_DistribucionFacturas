import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

# Leer y procesar los datos
data_file = 'Lectura OCR ALSA.csv'
df = pd.read_csv(data_file)
total_facturas = df['Cantidad facturas'].sum()
total_proveedores=len(df)



lectura_imposible=df[df['Estado lectura'] != 'Leer bien']
nbr_lectura_imposible=len(lectura_imposible)

lectura_ok=df[df['Ocr_lee_desde_primero'] == 'ok']
nbr_lectura_ok=len(lectura_ok)
nbr_proveedores_corregidos=total_proveedores-(nbr_lectura_ok+nbr_lectura_imposible)


labels = ['Proveedores Revisados','Proveedores Por Revisar']
values = [total_proveedores, 209-total_proveedores]
colors = ['#5cb85c','#007bff']
pie_chart = go.Figure(data=[go.Pie(labels=labels, values=values)])
pie_chart.update_layout(title_text='TOTAL PROVEEDORES: 209', title_x=0.5)
pie_chart.update_traces(marker=dict(colors=colors))


tab_chart = go.Figure(data=[go.Table(
  header=dict(
    values=['','Lectura Mejorada','Proveedores Leidos Correctamente Por el OCR','Imposible Lectura Por el OCR','Total de Proveedores'],
    line_color='darkslategray',
    fill_color='grey',
    align=['left','center'],
    font=dict(color='white', size=10)
  ),
  cells=dict(
    values=[
      [ 'Numero Proveedores	', 'Porcentaje	'],
      [ nbr_proveedores_corregidos, str(int((nbr_proveedores_corregidos/total_proveedores)*100))+'%'],
      [ nbr_lectura_ok, str(int((nbr_lectura_ok/total_proveedores)*100))+'%'],
      [ nbr_lectura_imposible, str(int((nbr_lectura_imposible/total_proveedores)*100))+'%'],
      [ total_proveedores,'' ]],
    line_color='darkslategray',
    # 2-D list of colors for alternating rows
    align = ['left', 'center'],
    font = dict(color = 'darkslategray', size = 11)
    ))
])
                
titles=['Total de Proveedores', 'Lectura Mejorada', 'Proveedores Leidos Correctamente Por el OCR','Imposible Lectura Por el OCR']

bar_chart = go.Figure([go.Bar(x=titles, y=[total_proveedores, nbr_proveedores_corregidos, nbr_lectura_ok,nbr_lectura_imposible])])
bar_chart.data[0].marker.color = ('#6a0dad','#5cb85c','#007bff','#fd4d72')
bar_chart.update_layout(title_text='PROVEEDORES REVISADOS', title_x=0.5)



df_ranking = df.sort_values(by='Cantidad facturas', ascending=False)
df_ranking['Ranking'] = range(1, len(df_ranking) + 1)

ranking_chart = px.bar(df_ranking, x='Cantidad facturas', y='Proveedor', orientation='h', title='Ranking de proveedores por cantidad de facturas')
ranking_chart.update_yaxes(categoryorder='total ascending')

# Crear la aplicación Dash
app = dash.Dash(__name__)
server = app.server

# Diseño de la aplicación
app.layout = html.Div([
    html.A(html.Button("informe facturas"), href="https://itbid-facturas-informe.onrender.com/"),
    html.H1('INFORME PROVEEDORES', style={'textAlign': 'center'}),
    dcc.Graph(figure=pie_chart, id='pie-chart'),
    dcc.Graph(figure=bar_chart, id='bar-chart'),
    dcc.Graph(figure=tab_chart, id='tab-chart')
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
