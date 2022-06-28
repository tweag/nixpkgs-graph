#!/usr/bin/env python3
import pandas as pd

data = pd.read_json('nodes.json').T
data = data.reset_index()
print(data.head(10))
data.to_csv("nodes.csv", encoding='UTF-8')
