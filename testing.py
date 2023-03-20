from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st



number = st.slider("Choose Something", 0, 50)
number2 = st.slider("Choose Another", 1, 300)

data = []

Point = namedtuple('Point', 'x y')

data.append(Point(number, number2)

st.altair_chart(alt.Chart(pd.DataFrame(data), height = 500, width = 500)
