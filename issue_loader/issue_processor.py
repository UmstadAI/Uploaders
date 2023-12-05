import os

import pandas as pd
import numpy as np

df = pd.read_csv('output.csv')
df = df[df['comments'].apply(lambda x: len(x) > 3)]

