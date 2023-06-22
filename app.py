import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np


st.title('歩行データの可視化 今井善太郎 総合2年 72101191')
# データをロード
data = pd.read_csv('steps.csv')


if st.checkbox('生データを表示'):  
    st.table(data)

# Sliderの値を取得 (1000ずつの範囲で指定)

time_range = st.slider(
    'Select a range of time values',
    min_value=1,
    max_value=12448,
    value=(1, 1000),
    step=1000
)

# Sliderで指定された時間範囲のデータをフィルタリング
filtered_data = data[(data['time'] >= time_range[0]) & (data['time'] <= time_range[1])]

# x, y 座標でgroupbyして force の合計を計算
grouped_data = filtered_data.groupby(['x', 'y']).agg({'force': 'sum'}).reset_index()

# x, y, forceを使用してヒートマップデータを作成
max_x = int(max(grouped_data['x']))+10
max_y = int(max(grouped_data['y']))+10
heatmap_data = np.zeros((max_x + 1, max_y + 1))
for index, row in grouped_data.iterrows():
    heatmap_data[int(row['x']), int(row['y'])] = row['force']


fig = px.imshow(heatmap_data, labels=dict(x="X Coordinate", y="Y Coordinate", color="Force"),
                title="Walking Data Heatmap")

st.plotly_chart(fig, use_container_width=True)
