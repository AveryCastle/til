import pandas as pd
import streamlit as st
import numpy as np

data = pd.read_csv('data/data.csv')
st.write(data)

chart_data = pd.DataFrame(
  np.random.randn(20, 3),
  columns=["a", "b", "c"]
)

st.bar_chart(chart_data)
st.line_chart(chart_data)
