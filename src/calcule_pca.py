from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib

from src.utils.files import read_pickle
from src import DATA_PATH, MODEL_PATH

df = read_pickle(DATA_PATH / 'cleaned-df-2021-05-11.pickle')


# Offensive variables
offensive = ['Per 90 Minutes - Gls', 'Per 90 Minutes - Ast',
             'Per 90 Minutes - G-PK', 'Per 90 Minutes - G+A-PK', 'Per 90 Minutes - xG',
             'Per 90 Minutes - npxG', 'Per 90 Minutes - xA', 'Per 90 Minutes - xG+xA']
shoots = ['Standard - SoT%', 'Standard - Sh/90', 'Standard - SoT/90', 'Standard - G/Sh',
          'Standard - Dist', 'Expected - np:G-xG', 'Expected - npxG/Sh',
          'SCA - SCA90', 'GCA - GCA90']
time = ['Playing Time - Min', 'Playing Time - MP']
passing = ['Total - Att', 'Total - Cmp%', 'Total - TotDist', 'Total - PrgDist',
           'Short - Cmp%', 'Medium - Cmp%', 'Long - Cmp%', 'General - Ast', 'General - xA',
           'General - A-xA', 'General - KP', 'General - Prog']
defensive = ['Tackles - Tkl', 'Tackles - TklW', 'Vs Dribbles - Tkl%', 'Pressures - %',
             'Pressures - Press', 'Pressures - Att 3rd', 'Blocks - Blocks',
             'General - Int']
possession = ['Touches - Touches', 'Touches - Live', 'Touches - Def 3rd', 'Touches - Mid 3rd',
              'Touches - Att 3rd', 'Dribbles - Succ%', 'Dribbles - #Pl', 'Carries - PrgDist',
              'Carries - Mis', 'Receiving - Rec%']
fouls = ['Performance - Fls', 'Performance - Fld']
duels = ['Aerial Duels - Won%']

# Total df
df = df[offensive + shoots + time + passing + defensive + possession + fouls + duels]
df = df.apply(lambda x: x.astype(float), axis=0)
df = df.fillna(0)
df.dtypes
df.head()

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from numpy.linalg import eigh
from sklearn.decomposition import PCA

sca = StandardScaler()
sca.fit(df)
df_scaled = pd.DataFrame(sca.transform(df), columns=df.columns)

# 2 variables example

# Unstandardized chart
px.scatter(df, x='Per 90 Minutes - Gls', y='Aerial Duels - Won%').show()

# Standardized chart
px.scatter(df_scaled, x='Per 90 Minutes - Gls', y='Aerial Duels - Won%').show()

# Calculing eigen vectord and values scaled and not
example_vars = ['Per 90 Minutes - Gls', 'Aerial Duels - Won%']
cov = df[example_vars].cov()
cov_scaled = df_scaled[example_vars].cov()

eigh(cov)
eigh(cov_scaled)

# Using PCA module
pca = PCA()
pca.fit(df_scaled[example_vars])
pca.explained_variance_
pca.components_
df_pca = pd.DataFrame(pca.transform(df_scaled[example_vars]))

# Example
real = df_scaled.iloc[0][example_vars]
first_pc = pca.components_[0]
np.dot(real, first_pc)
df_pca.iloc[0, 0] == np.dot(real, first_pc)  # PCA module to compare

# Using PCA in all data
pca = PCA(random_state=12)
pca.fit(df_scaled)
pca.explained_variance_
pca.components_
df_pca = pd.DataFrame(pca.transform(df_scaled))


# Explained Variance
fig = go.Figure()

index = np.arange(0, len(pca.explained_variance_)+1, 1)
ex_var = np.insert(pca.explained_variance_ratio_.cumsum(), 0, 0)
fig.add_trace(go.Scatter(
    name='Cumulated explained variance',
    x=index,
    y=ex_var,
    fill='tozeroy')
)

for i in np.arange(0, 17):
    fig.add_annotation(x=index[i], y=ex_var[i], text=round(ex_var[i], 2))

var_ratio = np.insert(pca.explained_variance_ratio_, 0, 0)
fig.add_trace(go.Bar(
    name='Explained variance',
    x=index,
    y=var_ratio,
    text=np.round(var_ratio, 2))
)

fig.show()

# Save PCA model
MODEL_PATH.mkdir(exist_ok=True)
joblib.dump(pca, MODEL_PATH / 'pca.pickle')
