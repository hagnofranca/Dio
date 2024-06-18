import pandas as pd
import numpy  as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import re
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt


def acertaColunas(col_name):
    return re.sub(r"[/| ]", "", col_name).lower()

url = 'https://github.com/neylsoncrepalde/projeto_eda_covid/blob/master/covid_19_data.csv?raw=true'


dataFrame = pd.read_csv (url, parse_dates=['ObservationDate', 'Last Update'])
dataFrame.columns = [acertaColunas(col)for col in dataFrame.columns] 
casosConfirmados = dataFrame.loc [(dataFrame['countryregion'] == 'Brazil') & (dataFrame['confirmed'] > 0)] 

casosConfirmados['newcases'] = list(map(
                                        lambda x: 0 if (x == 0) else casosConfirmados['confirmed'].iloc[x] - casosConfirmados['confirmed'].iloc[x-1],
                                        np.arange(casosConfirmados.shape[0])
                               ))


###########################################################
###################  Mortes por Covid #####################
###########################################################

figDeaths = go.Figure()
figDeaths.add_trace(
            go.Scatter(x=casosConfirmados['observationdate'], y=casosConfirmados['deaths'], name='Mortes', mode='lines+markers',
                       line=dict(color='red'))
        )
figDeaths.update_layout(title='Mortes por COVID-19 no Brasil', xaxis_title='Data',yaxis_title='Número de mortes')

###########################################################
################### Crecimento diário #####################
###########################################################

def txCrescimento(dataFrame, column, dataIni=None, dataFim=None):
    if dataIni is None:
        dataIni = dataFrame.loc[dataFrame[column] > 0, 'observationdate'].min()
    else:
        dataIni = pd.to_datetime(dataIni)
    
    if dataFim is None:
        dataFim = dataFrame['observationdate'].max()
    else:
        dataFim = pd.to_datetime(dataFim)
    
    previous = dataFrame.loc[dataFrame['observationdate'] == dataIni, column].values[0]
    current = dataFrame.loc[dataFrame['observationdate'] == dataFim, column].values[0]
    
    nrDays = (dataFim - dataIni).days

    taxa = ((current / previous) ** (1 / nrDays) - 1)* 100

    return round(taxa,2)


def txDailyGrowth (dataFrame, column, dataIni = None):
    if dataIni is None:
        dataIni = dataFrame.loc[dataFrame[column] > 0, 'observationdate'].min()
    else:
        dataIni = pd.to_datetime(dataIni)

    dataFim = dataFrame['observationdate'].max()
    nrDays  =(dataFim - dataIni).days
    taxas = list(map(
                    lambda x: (dataFrame[column].iloc[x] - dataFrame[column].iloc[x-1]) / dataFrame[column].iloc[x-1], range(1,nrDays+1)
                ))
    return np.round(np.array(taxas)*100,2)
gLineConfirmados = px.line(casosConfirmados, 'observationdate', 'newcases', title=f'Casos Confirmados no Brasil com Crescimento Médio de {'meanGrowth'}%')
gLineConfirmados.show()


firstDay = casosConfirmados.loc[casosConfirmados['confirmed'] > 0, 'observationdate'].min()

txDaily = txDailyGrowth(casosConfirmados,'confirmed')

gLineTxGrowthDaily = px.line (x=pd.date_range(firstDay, casosConfirmados['observationdate'].max())[1:], 
                              y=txDaily,
                              title='Taxa de crescimento de casos confirmados')
gLineTxGrowthDaily.show()

###########################################################
####################### Predições #########################
###########################################################


newcases = casosConfirmados['newcases']
newcases.index = casosConfirmados['observationdate']

res = seasonal_decompose(newcases)

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize = (10,8))
ax1.plot(res.observed)
ax2.plot(res.trend)
ax3.plot(res.seasonal)
ax4.scatter(newcases.index, res.resid)
ax4.axhline(0, linestyle='dashed', c='black')


###########################################################
############ Decompondo a série de confirmados ############
###########################################################

confirmed = casosConfirmados['confirmed']
confirmed.index = casosConfirmados['observationdate']

resConfirmed = seasonal_decompose(confirmed)
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10,8))
ax1.plot(resConfirmed.observed)
ax2.plot(resConfirmed.trend)
ax3.plot(resConfirmed.seasonal)
ax4.scatter(confirmed.index, resConfirmed.resid)
ax4.axhline(0, linestyle='dashed', c='black')
plt.show()

##############################################################
########## Predizendo o número de casos confirmados ##########
##############################################################
order=(1,1,1)
model = ARIMA(confirmed, order=order)
fit_model = model.fit()

# Previsão in-sample
predicted_values = fit_model.predict()

# Previsão para os próximos 30 dias
forecast_values = fit_model.forecast(steps=30)

# Criação do gráfico usando Plotly
figPrediction = go.Figure()

# Dados observados
figPrediction.add_trace(go.Scatter( x=confirmed.index, y=confirmed, mode='lines', name='Observado'))

# Previsão in-sample
figPrediction.add_trace(go.Scatter(x=confirmed.index, y=predicted_values, mode='lines', name='Previsão (in-sample)'))

# Previsão para os próximos 30 dias
forecast_index = pd.date_range(start=confirmed.index[-1] + pd.Timedelta(days=1), periods=30)
figPrediction.add_trace(go.Scatter(x=forecast_index, y=forecast_values, mode='lines', name='Previsão (30 dias)'))
figPrediction.update_layout(title='Previsão de casos para os próximos 30 dias', yaxis_title='Casos Confirmados',xaxis_title='Data')

# Exibição do gráfico
figPrediction.show()