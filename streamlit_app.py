import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

import plotly.io as pio
pio.renderers.default = "browser"

from src import DATA_PATH

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

# Get data
df = pd.read_pickle(DATA_PATH / 'pca_transformed_dataset.pickle')

# Sidebar for input
with st.sidebar:
    # Pick a player
    target_player = st.selectbox(
        label="Pick a player",
        options=df['index'],
        key='pick-target-player'
    )
    st.write("You select:", target_player)

    # Pick player to compare
    comparison_player = st.selectbox(
        label="Pick a player",
        options=df['index'],
        key='pick-comparison-player'
    )
    st.write("You select:", comparison_player)

# Main page
players_comparison_filter = df['index'].isin([target_player, comparison_player])
polar_df = df[players_comparison_filter]
pca_columns = [f'PC{i}' for i in range(1, 7)]
new = polar_df[['index']+pca_columns]
new = pd.melt(new, id_vars='index', value_vars=pca_columns)
fig = px.line_polar(new, r='value', theta='variable', color='index', line_close=True)

col_left, col_middle, col_right = st.beta_columns([1, 2, 1])

# Main page layout
with col_left:
    st.header(target_player)

with col_middle:
    st.write(fig, use_column_width=True)

with col_right:
    st.header(comparison_player)
    st.write("Here's our first attempt at using data to create a table:")
    st.write(pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    }))

    if st.checkbox('Show details'):
        st.write('Hola')

# Magic commands example
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

option = st.selectbox(
    'Which number do you like best?',
    df['first column'])

'You selected: ', option

# Status text
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
# data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

# Slider
# st.slider()

# Caché
# @st.cache
# def load_data(nrows):


left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Press me?')
if pressed:
    right_column.write("Woohoo!")

expander = st.beta_expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")