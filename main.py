import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pymysql

# Database connection
connection = pymysql.connect(
    host="127.0.0.1",
    user='root',
    password='',
    database="supermarkets"
)

query_maxima = "SELECT name, fat_content, package_size, price FROM maxima_milk"
query_iki = "SELECT name, fat_content, package_size, price FROM iki_milk"

maxima_data = pd.read_sql(query_maxima, connection)
iki_data = pd.read_sql(query_iki, connection)
connection.close()

# Merg
merged_data = pd.merge(
    maxima_data, iki_data,
    on=['name', 'fat_content', 'package_size'],
    suffixes=('_maxima', '_iki')
)

merged_data['price_difference'] = merged_data['price_maxima'] - merged_data['price_iki']
# app
st.title("Milk Price Comparison")
# canddles bet nelabai veikia su tokia info
# if merged_data.empty:
#     st.write("No matching products found.")
# else:
#     for _, row in merged_data.iterrows():
#         st.subheader(f"Comparison for: {row['name']}")
#         st.write(f"Fat Content: {row['fat_content']}, Package Size: {row['package_size']}")
#
#         fig = go.Figure(
#             data=[
#                 go.Candlestick(
#                     x=['Maxima', 'Iki'],
#                     open=[row['price_maxima'], row['price_iki']],
#                     high=[row['price_maxima'], row['price_iki']],
#                     low=[row['price_maxima'], row['price_iki']],
#                     close=[row['price_maxima'], row['price_iki']],
#                 )
#             ]
#         )
#
#         fig.update_layout(
#             title=f"Price Comparison for {row['name']}",
#             xaxis_title="Store",
#             yaxis_title="Price (€)"
#         )
#
#         st.plotly_chart(fig)

for _, row in merged_data.iterrows():
    st.subheader(f"Comparison for: {row['name']}")
    st.write(f"Fat Content: {row['fat_content']}, Package Size: {row['package_size']}")

    if row['price_maxima'] < row['price_iki']:
        colors = ['green', 'red']
    elif row['price_maxima'] > row['price_iki']:
        colors = ['red', 'green']
    else:
        colors = ['yellow', 'yellow']

    fig = go.Figure(
        data=[
            go.Bar(
                x=['Maxima', 'Iki'],
                y=[row['price_maxima'], row['price_iki']],
                marker_color=colors
            )
        ]
    )

    fig.update_layout(
        title=f"Price Comparison for {row['name']}",
        xaxis_title="Store",
        yaxis_title="Price (€)",
        showlegend=False
    )

    st.plotly_chart(fig)