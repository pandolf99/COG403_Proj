import pandas as pd
import numpy as np


alphas = {
        "c1": 0.01,
        "c2": 0.25,
        "c3": 0.5,
        "c4": 0.75,
        "c5": 0.99
        }

#Function to pass to apply
#and update Rating
def cleanData(row, *args):
    a = row["Alpha"]
    cond = args[0]
    print(type(a))
    if a == alphas[cond]:
        return row["Rating"]
    return 10 - row["Rating"]


df = pd.read_csv("sca2_data.txt", sep='\t')
df_c1 = df[df["GammaDiff"] == "S-F_1"]
df_c1["Rating"] = df_c1.apply(cleanData, axis=1, args=("c1",))
df_c2 = df[df["GammaDiff"] == "S-F_2"]
df_c3 = df[df["GammaDiff"] == "Control"]
df_c4 = df[df["GammaDiff"] == "F-S_1"]
df_c5 = df[df["GammaDiff"] == "F-S_2"]
ratings_c1 = np.asarray(df_c1["Rating"])
ratings_c1 = ratings_c1 / 10
print(np.mean(ratings_c1))
