import json

import numpy as np
import pandas as pd

df = pd.read_csv("data/val.csv")
# drop outcome
df = df.drop(columns=["Outcome"])
n = len(df)
columns = df.columns.tolist()
# create 100 requests
request_list = []
for i in range(100):
    id = np.random.randint(1000, 100000)
    num_data = np.random.randint(1, n // 2)
    data = df.sample(num_data)
    # convert to list
    data = data.values.tolist()
    request = {"id": id, "data": data, "columns": columns}
    print(request)
    save_path = f"requests/request_{id}.json"
    with open(save_path, "w") as f:
        json.dump(request, f, indent=4)
