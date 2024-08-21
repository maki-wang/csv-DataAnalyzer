# -*- coding: utf-8 -*-
# @Time    : 2024/8/21 17:57
# @Author  : Maki Wang
# @FileName: utils.py
# @Software: PyCharm
# !/usr/bin/env python3

from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import json

PROMPT_TEMPLATE = '''
You are a data analysis assistant, and your responses depend on the user's request.

1. For text-based questions, respond in the following format:
   {"answer": "<write your answer here>"}
For example:
   {"answer": "The product ID with the highest order volume is 'MNWC3-067'"}

2. If the user needs a table, respond in the following format:
   {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

3. If the user's request is suitable for a bar chart, respond in the following format:
   {"bar": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

4. If the user's request is suitable for a line chart, respond in the following format:
   {"line": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

5. If the user's request is suitable for a scatter plot, respond in the following format:
   {"scatter": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
Note: We only support three types of charts: "bar", "line", and "scatter".

Please return all outputs as JSON strings. Make sure to enclose all strings in the "columns" list and data list with double quotes.
For example: {"columns": ["Products", "Orders"], "data": [["32085Lip", 245], ["76439Eye", 178]]}

Here is the user request you need to handle:'''

def dataframe_agent(openai_api_key, df, query):
    model = ChatOpenAI(model='gpt-3.5-turbo',
                       openai_api_key=openai_api_key,
                       temperature=0)
    agent = create_pandas_dataframe_agent(llm=model,
                                          df=df,
                                          agent_executor_kwargs={"handle_parsing_errors": True},
                                          verbose=True)
    prompt = PROMPT_TEMPLATE + query
    response = agent.invoke({"input": prompt})
    response_dict = json.loads(response["output"])
    return response_dict
