#!/usr/bin/env python3
import pandas as pd

data = pd.read_json('nodes.json').T
data.na

# print(data)
data.to_csv("nodes.csv", encoding='UTF-8')
