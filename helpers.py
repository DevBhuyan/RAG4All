#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 01:39:53 2024

@author: dev
"""

import json
from streamlit import session_state as ss
import os
import streamlit as st
from shutil import rmtree


def load_message_history(last_n: int = 0,
                         sys_prompt: bool = True):

    try:
        file_path = f"./chains/{ss.session_code}_prompt_chain.json"
    except:
        return False

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            messages = list(json.load(f)['messages'])

        if not last_n:
            return messages
        else:
            try:
                MESSAGES = messages[-4:]
            except:
                MESSAGES = messages[-2:]
            if sys_prompt:
                MESSAGES.insert(0, messages[0])

            return MESSAGES

    return False


def default_context():

    raise Exception("Method not written yet")

    with open('./faq.txt', 'r', encoding='utf-8') as f:
        sys_prompt = f.read()

    return sys_prompt


def display_message_history():

    history = load_message_history()

    if history:
        for message in history:
            if message['role'] == 'user':
                st.chat_message("human").markdown(message['content'])
            elif message['role'] == 'assistant':
                st.chat_message("assistant").markdown(message['content'])


def log_messages(MESSAGES: list[dict],
                 log: bool = True):
    if log:
        filename = f"./chains/{ss.session_code}_prompt_chain.json"
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                json.dump({"messages": MESSAGES}, f, indent=4)
        else:
            # dump only the last two items in MESSAGES, append the content to
            # the existing file without deleting any previous text
            with open(filename, "r+") as f:
                data = json.load(f)
                data["messages"].extend(MESSAGES[-2:])

                f.seek(0)

                json.dump(data, f, indent=4)

        return True


def delete_residue():
    try:
        os.remove('./config.json')
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)
    try:
        rmtree('./chains')
    except Exception as e:
        print(e)
    try:
        rmtree('./datafeed')
    except Exception as e:
        print(e)


def select_prompt(ip: str):
    ss.ip = ip
