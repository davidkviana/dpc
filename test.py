#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

def get_dataset_size():
    fl = open('result.jsonl', 'r')
    lines = fl.readlines()
    lines = str(lines)
    dict_lines=lines.strip('}, {')
    dict_lines = eval(dict_lines)
    dict_result = []
    for reg in dict_lines:
        dict_result.append(eval(str(reg).replace('\n', '')))
    df = pd.DataFrame(dict_result)
    
    dup = df[df.duplicated(subset=['id'])]
    if len(dup) == 0:
        print("There isn't duplicated values by id:", len(dup), ". ok")
    else:
        print("There is duplicated values by id:", len(dup), ". fail")
    
    cols = df.columns.tolist()
    if cols == ['id', 'localidade', 'faixa_de_cep']:
        print("Dataset columns name:", cols, ". ok")
    else:
        print("Dataset columns name:", cols, ". fail")
        
    
    return df.shape

def verify_dataset_size():
    h, w = get_dataset_size()
    if h >= 5568 and h <= 5573:
        print("Dataset height:", h, ". ok")
    else:
        print("Dataset height:", h, ". fail")
    
    if w == 3:
        print("Dataset width:", w, ". ok")
    else:
        print("Dataset width:", w, ". fail")

if __name__ == "__main__":
    verify_dataset_size()
    