#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 01:46:40 2024

@author: dev
"""

import json
from chroma import load_faq_to_chroma
import os
import streamlit as st
from streamlit import session_state as ss
from random import randint
from streamlit_helpers import (
    chat,
    home,
    validate_config,
    add_files
)
from helpers import delete_residue


if 'session_code' not in ss:
    delete_residue()
    ss['session_code'] = randint(1000, 2000)

if 'page' not in ss:
    ss['page'] = 'home'

if 'ip' not in ss:
    ss.ip = ""


os.makedirs('./chains', exist_ok=True)
os.makedirs('./datafeed', exist_ok=True)


def setup():

    st.title("Welcome!")
    st.subheader("Start building your own RAG system in minutes....")

    st.caption("A few more steps before we're up and running")

    CONFIG = {}

    with st.form(key="bot_config_form"):
        CONFIG["BOT_NAME"] = st.text_input(
            "Enter a name for your Bot",
            placeholder="Assistant"
        )

        if len(CONFIG["BOT_NAME"]):
            CONFIG["HF_API_TOKEN"] = st.text_input(
                "Enter your HuggingFace API key",
                placeholder="hf_abcdefghijklmnopqrstuvwxyzABCDEFGH",
                help="[Get a free HuggingFace API key](https://huggingface.co/settings/tokens/new?globalPermissions=inference.serverless.write&tokenType=read)"
            )

            if len(CONFIG["HF_API_TOKEN"]):
                CONFIG["SYSTEM_PROMPT"] = st.text_input(
                    "Set the behavior of your Bot (Set the System prompt)",
                    placeholder="I want you to act as a storyteller. You will come up with entertaining stories that are engaging, imaginative and captivating for the audience.",
                    help="[Here are some good system prompt examples](https://huggingface.co/datasets/fka/awesome-chatgpt-prompts)"
                )

        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if len(CONFIG["BOT_NAME"]) \
                and len(CONFIG["HF_API_TOKEN"]) \
                and len(CONFIG["SYSTEM_PROMPT"]):

            validate_config(CONFIG)

            with open("config.json", 'w') as f:
                json.dump(CONFIG, f, indent=4)

            os.environ["HF_API_TOKEN"] = CONFIG["HF_API_TOKEN"]

            ss.page = "home"
            st.rerun()


def init():

    if ss.page == "home":

        try:
            validate_config()
        except:
            ss.page = "setup"
            st.rerun()

        with open('./config.json', 'r') as f:
            CONFIG = json.load(f)

        with st.spinner(f"Setting up your {CONFIG['BOT_NAME']}"):
            load_faq_to_chroma()
        home()

    elif ss.page == "chat":
        chat()

    elif ss.page == "setup":
        setup()

    elif ss.page == "add_files":
        add_files()

    if ss.page != "setup":

        with open('./config.json', 'r') as f:
            CONFIG = json.load(f)

        col1, col2 = st.columns([1, 2])

        with col1:
            if st.button(f'Feed data to your {CONFIG["BOT_NAME"]}'):
                ss.page = "add_files"
                st.rerun()

        with col2:
            ip = st.chat_input("Ask me....")

            if ip:
                ss.ip = ip
                ss.page = 'chat'
                st.rerun()

    if ss.page != "auth":
        # Show a st.button at the top-right corner of the screen that will
        # invoke add_files() upon clicking. The button will always stay at the
        # same top-right corner.
        pass

    with st.sidebar:
        st.write(ss)


if __name__ == "__main__":
    init()
