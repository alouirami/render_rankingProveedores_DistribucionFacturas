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
df['Porcentaje'] = (df['Cantidad facturas'] / total_facturas) * 100
df_filtrado = df[df['Porcentaje'] > 10]

lectura_imposible=df[df['Estado lectura'] != 'Leer bien']
sum_lectura_imposible=lectura_imposible['Cantidad facturas'].sum()

lectura_ok=df[df['Ocr_lee_desde_primero'] == 'ok']
sum_lectura_ok=lectura_ok['Cantidad facturas'].sum()
sum_facturas_corregidas=total_facturas-(sum_lectura_ok+sum_lectura_imposible)

labels = ['Facturas Revisadas','Facturas Por Revisar']
values = [total_facturas, 5927-total_facturas]
colors = ['#5cb85c','#007bff']
pie_chart = go.Figure(data=[go.Pie(labels=labels, values=values)])
pie_chart.update_layout(title_text='TOTAL FACTURAS: 5927', title_x=0.5)
pie_chart.update_traces(marker=dict(colors=colors))

tab_chart = go.Figure(data=[go.Table(
  header=dict(
    values=['','Lectura Mejorada','Facturas Leidas Correctamente Por el OCR','Imposible Lectura Por el OCR','Total de Facturas'],
    line_color='darkslategray',
    fill_color='grey',
    align=['left','center'],
    font=dict(color='white', size=10)
  ),
  cells=dict(
    values=[
      [ 'Numero Facturas	', 'Porcentaje	'],
      [ sum_facturas_corregidas, str(int((sum_facturas_corregidas/total_facturas)*100))+'%'],
      [ sum_lectura_ok, str(int((sum_lectura_ok/total_facturas)*100))+'%'],
      [ sum_lectura_imposible, str(int((sum_lectura_imposible/total_facturas)*100))+'%'],
      [ total_facturas,'' ]],
    line_color='darkslategray',
    # 2-D list of colors for alternating rows
    align = ['left', 'center'],
    font = dict(color = 'darkslategray', size = 11)
    ))
])
                
titles=['Total de Facturas', 'Lectura Mejorada', 'Facturas Leidas Correctamente Por el OCR','Imposible Lectura Por el OCR']

bar_chart = go.Figure([go.Bar(x=titles, y=[total_facturas, sum_facturas_corregidas, sum_lectura_ok,sum_lectura_imposible])])
bar_chart.data[0].marker.color = ('#6a0dad','#5cb85c','#007bff','#fd4d72')
bar_chart.update_layout(title_text='FACTURAS REVISADAS', title_x=0.5)



bar_chart2 = px.bar(df, x='Cantidad facturas', y='Proveedor', orientation='h', title='Distribución de facturas por proveedor')

df_ranking = df.sort_values(by='Cantidad facturas', ascending=False)
df_ranking['Ranking'] = range(1, len(df_ranking) + 1)

ranking_chart = px.bar(df_ranking, x='Cantidad facturas', y='Proveedor', orientation='h', title='Ranking de proveedores por cantidad de facturas')
ranking_chart.update_yaxes(categoryorder='total ascending')


# Crear la aplicación Dash
app = dash.Dash(__name__)
server = app.server

# Diseño de la aplicación
app.layout = html.Div([
    html.A(html.Button("informe proveedors"), href="https://itbid-proveedores-informe.onrender.com/"),
    html.H1('INFORME FACTURAS', style={'textAlign': 'center'}),
    dcc.Graph(figure=pie_chart, id='pie-chart'),
    dcc.Graph(figure=bar_chart, id='bar-chart'),
    dcc.Graph(figure=tab_chart, id='tab-chart'),
    dcc.Graph(figure=bar_chart2, id='bar-chart2'),
    dcc.Graph(figure=ranking_chart, id='ranking-chart')
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
