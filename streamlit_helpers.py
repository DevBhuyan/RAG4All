#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 03:45:14 2024

@author: dev
"""

from llm import (
    askLLM
)
from helpers import (
    load_message_history,
    display_message_history
)
import streamlit as st
from streamlit import session_state as ss
import json
import os


with open('./prompts.json', 'r') as f:
    PROMPTS = dict(json.load(f))


def validate_config(config: dict = None):

    if not config:
        if not os.path.exists('./config.json'):
            raise FileNotFoundError("Configuration file doesn't exist yet")

        else:
            with open('./config.json', 'r') as f:
                config = json.load(f)

    assert len(config.keys()) == 3
    assert len(config['BOT_NAME'])
    assert config['HF_API_TOKEN'][:2] == "hf"


def validate_json(json_data: list[dict]):

    if isinstance(json_data, list):
        for doc in json_data:
            assert len(doc) >= 2
            # assert int(doc['id']) >= 0
            assert len(doc['context'])

    elif isinstance(json_data, dict):
        assert len(json_data) == 2
        # assert int(json_data['id']) >= 0
        assert len(json_data['context'])

    else:
        raise TypeError("Not JSON content or JSON not properly formatted")


def chat():

    with open('./config.json', 'r') as f:
        CONFIG = json.load(f)

    st.title(CONFIG["BOT_NAME"])
    st.divider()

    if not load_message_history():
        st.chat_message("human").markdown(ss.ip)

        chat_response, docs, ids = askLLM(ss.ip, log=True)
        # st.chat_message("assistant").markdown(
        #     chat_response,
        #     help="....\n".join(docs)
        # )

    else:
        display_message_history()

        if ss.ip not in [i['content']
                         for i in load_message_history()
                         if i['role'] == 'user']:
            st.chat_message("human").markdown(ss.ip)

            chat_response, docs, ids = askLLM(ss.ip, log=True)
            # st.chat_message("assistant").markdown(
            #     chat_response,
            #     help="....\n".join(docs)
            # )


def add_files():
    st.title("Upload your files")

    files = st.file_uploader(
        "Upload the data you want the system to learn. (Max 200MB, JSON only)",
        type="json",
        accept_multiple_files=True,
        help="A typical JSON file would include multiple entries of dictionaries containing 'context' and 'id' attributes"
    )

    if len(files):
        for file in files:
            file_content = file.read()
            json_data = json.loads(file_content)

            validate_json(json_data)

            with open(f'./datafeed/{file.name}', 'w') as f:
                json.dump(json_data, f, indent=4)

    ss.page = "home"
    st.rerun()


def home():

    with open('./config.json', 'r') as f:
        CONFIG = json.load(f)

    st.title(CONFIG["BOT_NAME"])
    st.divider()

    st.header(PROMPTS["HAPPY_GREET"])
    st.caption(PROMPTS['DISCLAIMER'])
