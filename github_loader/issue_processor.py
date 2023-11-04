import os

import pandas as pd
import numpy as np

from langchain.document_loaders.csv_loader import CSVLoader

df = pd.read_csv('output.csv')
df = df[df['comments'].apply(lambda x: len(x) > 3)]

loader = CSVLoader(file_path='./output.csv')
data = loader.load()

print(data[0])