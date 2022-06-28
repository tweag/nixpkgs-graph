#!/usr/bin/env python3
#!nix-shell -i python3 -p "python3.withPackages(ps: [ ps.pandas ])"
import pandas as pd

data = pd.read_json('rawdata/nodes.json').T
data = data.reset_index()
print("Showing the first ten rows:")
print(data.head(10))
data.to_csv("rawdata/nodes.csv", encoding='UTF-8')
