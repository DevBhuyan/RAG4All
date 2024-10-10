#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 23:21:15 2024

@author: dev
"""

from hf_llm import hf_ask
from chroma import query_top_n
import json


def askLLM(prompt: str,
           log: bool = False):

    docs, ids = query_top_n(prompt)

    context = "\n\n".join(docs) if len(docs) else "None"

    with open('./config.json', 'r') as f:
        sys_prompt = json.load(f)["SYSTEM_PROMPT"]

    sys_prompt = "{System Prompt}:" + sys_prompt + " | {Context}:" + context

    return hf_ask(prompt, sys_prompt, log), docs, ids


if __name__ == "__main__":
    print(askLLM("Introduce yourself"))
