import plotly.graph_objects as go
import pandas as pd
import datetime
import time
from plotly.subplots import make_subplots

# recebendo a data inicial que o usuário deseja

startDateInput = "14/8/2023 00:00"

# formatando para Y/m/d H:M

_startDateUNIX = datetime.datetime.strptime(startDateInput, "%d/%m/%Y %H:%M")

# recebendo a data final que o usuário deseja

endDateInput = "21/8/2023 23:59"

# formatando para Y/m/d H:M
_endDateUNIX = datetime.datetime.strptime(endDateInput, "%d/%m/%Y %H:%M")

# recebendo o intervalo o usuário deseja

setInterval = int(input("Intervalo: "))

#Transformando datas para UnixTime
start_time = int(time.mktime(_startDateUNIX.timetuple()))
end_time = int(time.mktime(_endDateUNIX.timetuple()))

key = "apikey="

# Acessando os dados do canopus

p0 = pd.read_json(f"https://canopus.eletrica.ufpr.br/emoncms/feed/data.json?id=309&start={start_time}&end={end_time}&interval={setInterval}&skipmissing=1&limitinterval=1&intervaltype=0&{key}")
u0 = pd.read_json(f"https://canopus.eletrica.ufpr.br/emoncms/feed/data.json?id=293&start={start_time}&end={end_time}&interval={setInterval}&skipmissing=1&limitinterval=1&intervaltype=0&{key}")
i0 = pd.read_json(f"https://canopus.eletrica.ufpr.br/emoncms/feed/data.json?id=300&start={start_time}&end={end_time}&interval={setInterval}&skipmissing=1&limitinterval=1&intervaltype=0&{key}")

# salvando os dados necessários

data1 = p0[1]
data2 = u0[1]
data3 = i0[1]
data4 = p0[0]


# Criar uma lista de datas
dates = []
while start_time <= end_time:
    dates.append(datetime.datetime.fromtimestamp(start_time))
    start_time += setInterval  # define o intervalo de atualizões em UNIXTIME

# Criando a figura
fig = go.Figure()

# Adicionando os gráficos
fig.add_trace(go.Scatter(
    x=dates,
    y=data1,
    name='Potência',
    line=dict(color='blue'),
    yaxis='y1'  # Escala da esquerda
))

fig.add_trace(go.Scatter(
    x=dates,
    y=data2,
    name='Voltagem',
    line=dict(color='red'),
    yaxis='y2'  # Escala da direita
))
fig.add_trace(go.Scatter(
    x=dates,
    y=data3,
    name='Corrente',
    line=dict(color='green'),
    yaxis='y3'  # Escala da direita
))

# Configurando as escalas dos eixos
fig.update_layout(
    yaxis=dict(
        title='Potência',
        titlefont=dict(
            color="blue"
        ),
        tickfont=dict(
            color="blue"
        ),
        side='left',

    ),
    yaxis2=dict(
        title='Voltagem',
        titlefont=dict(
            color="red"
        ),
        tickfont=dict(
            color="red"
        ),
        side='right',
        overlaying='y',
    ),
     yaxis3=dict(
        title='Corrente',
        titlefont=dict(
            color="green"
        ),
        tickfont=dict(
            color="green"
        ),
        side='left',
        overlaying='y',
        autoshift=True,
        anchor="free",
    ),
    xaxis=dict(
        title='Dias',
        domain=[0.05, 1]
    ),
)
# Exibindo o gráfico
fig.show()
