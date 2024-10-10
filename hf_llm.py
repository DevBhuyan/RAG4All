#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 02:33:04 2024

@author: dev
"""

import json
import requests
from huggingface_hub import InferenceClient
import os
from helpers import (
    load_message_history,
    log_messages
)
import streamlit as st


def hf_ask(prompt: str = "None",
           system_prompt: str = "None",
           log: bool = False):

    try:
        HF_API_TOKEN = os.environ['HF_API_TOKEN']
    except:
        try:
            with open('./config.json', 'r') as f:
                CONFIG = json.load(f)
            HF_API_TOKEN = CONFIG["HF_API_TOKEN"]
        except:
            raise Exception(
                "Please provide a HuggingFace API token to run inference")

    client = InferenceClient(
        "meta-llama/Meta-Llama-3-8B-Instruct",
        token=HF_API_TOKEN,
    )

    if load_message_history():

        MESSAGES = load_message_history(last_n=0,
                                        sys_prompt=False)

        MESSAGES.append({
            "role": "system",
            "content": system_prompt
        })

        MESSAGES.append({
            "role": "user",
            "content": prompt
        })

    else:
        MESSAGES = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

    params = {
        "temperature": 0.0,
        "max_tokens": 2000,
        "stream": True
    }

    st_text = []
    output_placeholder = st.empty()
    for message in client.chat_completion(
            messages=MESSAGES,
            **params
    ):
        st_text.append(message.choices[0].delta.content)

        full_text = ''.join(st_text)
        output_placeholder.markdown(full_text)

    st_text = "".join(st_text)

    MESSAGES.append({
        "role": "assistant",
        "content": st_text
    })

    log_messages(MESSAGES, log)

    return st_text


def hf_embed(docs: list[str]):

    try:
        HF_API_TOKEN = os.environ['HF_API_TOKEN']
    except:
        try:
            with open('./config.json', 'r') as f:
                CONFIG = json.load(f)
            HF_API_TOKEN = CONFIG["HF_API_TOKEN"]
        except:
            raise Exception(
                "Please provide a HuggingFace API token to run inference")

    EMBEDDING_API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

    if isinstance(docs, str):
        docs = [docs]

    response = requests.post(
        EMBEDDING_API_URL,
        headers=headers,
        json={
            "inputs": docs,
            "options": {"wait_for_model": True}
        }).json()

    return response
