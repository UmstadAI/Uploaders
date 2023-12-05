import os
import ast
import json

import pandas as pd
import numpy as np

df = pd.read_csv('output.csv')
df = df[df['comments'].apply(lambda x: len(x) > 3)]

os.mkdir('issues_txt')

for index, row in df.iterrows():
    writer = row['writer']
    title = row['title']
    is_open = row['is_open']
    issue_body = row['body']
    comments = row['comments']
    comments = ast.literal_eval(comments)

    issue = {
        "title": title,
        "author": writer,
        "is_open": is_open,
        "issue": issue_body,
        "comments": comments
    }       

    file_path = f"issues_json/{index}.txt"
    json_string = json.dumps(issue, indent=4)

    with open(file_path, 'w') as f:
        f.write(json_string)

