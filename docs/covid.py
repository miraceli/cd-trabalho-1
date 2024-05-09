# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# %%
df = pd.read_csv('./dados/covid19_casos_brasil.csv')

df.describe()

# %% [markdown]
# 1) Apresentar gráfico do crescimento de casos e mortes de Joinville e os das capitais das regiões Sul e Sudeste. Descreva observações sobre estes gráficos.

# %%
cities = {
    'Sul': ['Florianópolis', 'Curitiba', 'Porto Alegre', 'Joinville'],
    'Sudeste': ['Vitória', 'Belo Horizonte', 'Rio de Janeiro', 'São Paulo']
}

df_filtered = df[df['city'].isin(cities['Sul'] + cities['Sudeste'])]

df_filtered['date'] = pd.to_datetime(df_filtered['date'])

print(df_filtered)

# %%
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates 

sns.lineplot(data=df_filtered, x='date', y='last_available_confirmed', hue='city', palette='tab10')
plt.xlabel('')
plt.ylabel('Número de Casos')
plt.title('Número de Casos por Cidade')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))

plt.xticks(rotation=45)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True, linestyle='--', color='lightgray')

plt.show()

# %%
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates 

sns.lineplot(data=df_filtered, x='date', y='last_available_deaths', hue='city', palette='tab10')
plt.xlabel('')
plt.ylabel('Número de Mortes')
plt.title('Número de Mortes por Cidade')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))

plt.xticks(rotation=45)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True, linestyle='--', color='lightgray')

plt.show()

# %%
capitais_brasileiras = [
    "Rio Branco", "Maceió", "Macapá", "Manaus", "Salvador", "Fortaleza", "Brasília", "Vitória", "Goiânia",
    "São Luís", "Cuiabá", "Campo Grande", "Belo Horizonte", "Belém", "João Pessoa", "Curitiba", "Recife",
    "Teresina", "Rio de Janeiro", "Natal", "Porto Alegre", "Porto Velho", "Boa Vista", "Florianópolis",
    "São Paulo", "Aracaju", "Palmas"
]

capitais = df[df['city'].isin(capitais_brasileiras)]

capitais = capitais.drop_duplicates(subset=['city_ibge_code', 'last_available_date'])

grouped = capitais.groupby('city_ibge_code').agg({
    'city': 'last',
    'estimated_population_2019': 'last',
    'last_available_confirmed': 'sum',
    'last_available_deaths': 'sum'
})

grouped['cases_per_100k'] = (grouped['last_available_confirmed'] / grouped['estimated_population_2019'] * 100000).round(2)
grouped['deaths_per_100k'] = (grouped['last_available_deaths'] / grouped['estimated_population_2019'] * 100000).round(2)

grouped = grouped.sort_values(by='cases_per_100k', ascending=False)

maiores_problemas = grouped.head(5)
pouco_sem_problema = grouped.tail(5)

plt.figure(figsize=(11, 4))

plt.subplot(1, 2, 1)
plt.barh(maiores_problemas['city'], maiores_problemas['cases_per_100k'], color='firebrick', label='Casos por 100 mil habitantes', height=0.6)
plt.barh(maiores_problemas['city'], maiores_problemas['deaths_per_100k'], color='cornflowerblue', left=maiores_problemas['cases_per_100k'], label='Mortes por 100 mil habitantes', height=0.6)
plt.xlabel('Taxa por 100 mil habitantes')
plt.title('Capitais com maiores problemas')
plt.legend(loc='upper left')

plt.subplot(1, 2, 2)
plt.barh(pouco_sem_problema['city'], pouco_sem_problema['cases_per_100k'], color='forestgreen', label='Casos por 100 mil habitantes', height=0.6)
plt.barh(pouco_sem_problema['city'], pouco_sem_problema['deaths_per_100k'], color='khaki', left=pouco_sem_problema['cases_per_100k'], label='Mortes por 100 mil habitantes', height=0.6)
plt.xlabel('Taxa por 100 mil habitantes')
plt.title('Capitais com menos problemas')
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()


# %%
cidades_grupo = [
    "Duque de Caxias", "Nova Iguaçu", "Campos dos Goytacazes", "Belford Roxo",
    "Ananindeua", "Santarém", "Parauapebas", "Marabá", "Castanhal",
    "Florianópolis", "Ponta Grossa"
]

grupo = df[df['city'].isin(cidades_grupo)]

grupo = grupo.drop_duplicates(subset=['city_ibge_code', 'last_available_date'])

grouped = grupo.groupby('city_ibge_code').agg({
    'city': 'last',
    'estimated_population_2019': 'last',
    'last_available_confirmed': 'sum',
    'last_available_deaths': 'sum'
})

grouped['cases_per_100k'] = (grouped['last_available_confirmed'] / grouped['estimated_population_2019'] * 100000).round(2)
grouped['deaths_per_100k'] = (grouped['last_available_deaths'] / grouped['estimated_population_2019'] * 100000).round(2)

grouped = grouped.sort_values(by='cases_per_100k', ascending=False)

maiores_problemas = grouped.head(3)
pouco_sem_problema = grouped.tail(3)

plt.figure(figsize=(11, 4))

x_values = np.linspace(0, max(maiores_problemas['cases_per_100k']), 7)  
x_values = [int(x) for x in x_values] 

y_values = np.linspace(0, max(pouco_sem_problema['cases_per_100k']), 7)  
y_values = [int(x) for x in y_values] 

plt.subplot(1, 2, 1)
plt.barh(maiores_problemas['city'], maiores_problemas['cases_per_100k'], color='firebrick', label='Casos por 100 mil habitantes', height=0.6)
plt.barh(maiores_problemas['city'], maiores_problemas['deaths_per_100k'], color='cornflowerblue', left=maiores_problemas['cases_per_100k'], label='Mortes por 100 mil habitantes', height=0.6)
plt.xlabel('Taxa por 100 mil habitantes')
plt.title('Cidades com maiores problemas')
plt.xticks(x_values)
plt.legend(loc='upper right')

plt.subplot(1, 2, 2)
plt.barh(pouco_sem_problema['city'], pouco_sem_problema['cases_per_100k'], color='forestgreen', label='Casos por 100 mil habitantes', height=0.6)
plt.barh(pouco_sem_problema['city'], pouco_sem_problema['deaths_per_100k'], color='khaki', left=pouco_sem_problema['cases_per_100k'], label='Mortes por 100 mil habitantes', height=0.6)
plt.xlabel('Taxa por 100 mil habitantes')
plt.title('Cidades com menos problemas')
plt.xticks(y_values)
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()



