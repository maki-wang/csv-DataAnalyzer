# -*- coding: utf-8 -*-
# @Time    : 2024/8/21 22:32
# @Author  : Maki Wang
# @FileName: main.py
# @Software: PyCharm
# !/usr/bin/env python3

from utils import dataframe_agent
import streamlit as st
import pandas as pd

def create_chart(input_data, chart_type):
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
    df_data.set_index(input_data["columns"][0], inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        st.line_chart(df_data)
    elif chart_type == "scatter":
        st.scatter_chart(df_data)

st.title("CSV Data Analysis Smart Tool")
with st.sidebar:
    openai_api_key = st.text_input("Please enter your OpenAI API key：", type="password")
    st.markdown("[Obtain OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.markdown("---")
    st.write("Designed by Xianmu, please contact via ***wangxianmu@gmail.com***")

data = st.file_uploader("Upload your data file (CSV format)：", type="csv")
if data:
    st.session_state["df"] = pd.read_csv(data)
    with st.expander("Original Data"):
        st.dataframe(st.session_state["df"])

query = st.text_area("Please enter your question about the above table, like a data extraction request, or a visualization requirement (supports **Scatter plots**, **Line charts**, **Bar charts**)：")
button = st.button("Generate a response")

if button and not openai_api_key:
    st.info("Please enter your OpenAI API key")
if button and "df" not in st.session_state:
    st.info("Please upload the data file first")
if button and openai_api_key and "df" in st.session_state:
    with st.spinner("AI is processing, please wait..."):
        response_dict = dataframe_agent(openai_api_key, st.session_state["df"], query)
        if "answer" in response_dict:
            st.write(response_dict["answer"])
        if "table" in response_dict:
            st.table(pd.DataFrame(response_dict["table"]["data"],
                                  columns=response_dict["table"]["columns"]))
        if "bar" in response_dict:
            create_chart(response_dict["bar"], "bar")
        if "line" in response_dict:
            create_chart(response_dict["line"], "line")
        if "scatter" in response_dict:
            create_chart(response_dict["scatter"], "scatter")

