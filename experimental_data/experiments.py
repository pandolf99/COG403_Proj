import pandas as pd
import numpy as np

#ignore a stupid warning
pd.options.mode.chained_assignment = None

alphas = {
        "c1": 0.01,
        "c2": 0.25,
        "c3": 0.5,
        "c4": 0.75,
        "c5": 0.99
        }


#Function to pass to apply in exp2
#and then update rating
def updateRating2(row, *args):
    a = row["Alpha"]
    cond = args[0]
    if a == alphas[cond]:
        return row["Rating"]
    return 10 - row["Rating"]

def cleanData2():
    df = pd.read_csv("experimental_data/Data Exp 2/sca2_data.txt", sep='\t')
    #update ratings based on alpha
    df_c1 = df[df["GammaDiff"] == "S-F_1"]
    df_c1["Rating"] = df_c1.apply(updateRating2, axis=1, args=("c1",))
    df_c2 = df[df["GammaDiff"] == "S-F_2"]
    df_c2["Rating"] = df_c2.apply(updateRating2, axis=1, args=("c2",))
    df_c3 = df[df["GammaDiff"] == "Control"]
    df_c3["Rating"] = df_c3.apply(updateRating2, axis=1, args=("c3",))
    df_c4 = df[df["GammaDiff"] == "F-S_2"]
    df_c4["Rating"] = df_c4.apply(updateRating2, axis=1, args=("c4",))
    df_c5 = df[df["GammaDiff"] == "F-S_1"]
    df_c5["Rating"] = df_c5.apply(updateRating2, axis=1, args=("c5",))
    df_ratings = pd.DataFrame({
        "c1":df_c1["Rating"],
        "c2":df_c2["Rating"],
        "c3":df_c3["Rating"],
        "c4":df_c4["Rating"],
        "c5":df_c5["Rating"],
         })
    return df_ratings

def exp2_data():
    labels = ["Condition1", "Condition2", "Condition3", "Condition4", "Condition5"]
    df_ratings = cleanData2()
    means = np.asarray(df_ratings.apply(np.mean)) / 10
    return dict(zip(labels, means))

#Function to pass to apply in exp3
#and then update rating
def updateRating3(row, *args):
    a = row["Alpha"]
    cond = args[0]
    if a == alphas[cond]:
        return row["Rating"]
    return 1 - row["Rating"]

def cleanData3():
    df = pd.read_csv("experimental_data/Data Exp 3/data_mainDV.txt", sep='\t')
    df_weak = df[df["Power"] == 0.5] 
    df_weak_short = df_weak[df_weak["GammaDiff"] == "S-F_1"]
    df_weak_short["Rating"] = df_weak_short.apply(updateRating3, axis=1, args=("c1",))
    df_weak_long = df_weak[df_weak["GammaDiff"] == "F-S_1"]
    df_weak_long["Rating"] = df_weak_long.apply(updateRating3, axis=1, args=("c5",))
    df_strong = df[df["Power"] == 0.83]
    #data is mislabeled as "S-F_2", should be "S-F_1"
    df_strong_short = df_strong[df_strong["GammaDiff"] == "S-F_2"]
    df_strong_short["Rating"] = df_strong_short.apply(updateRating3, axis=1, args=("c1",))
    #data is mislabeled as "F-S_2", should be "F-S_1"
    df_strong_long = df_strong[df_strong["GammaDiff"] == "F-S_2"]
    df_strong_long["Rating"] = df_strong_long.apply(updateRating3, axis=1, args=("c5",))
    mean_weak_short = np.mean(df_weak_short["Rating"]) 
    mean_weak_long = np.mean(df_weak_long["Rating"]) 
    mean_strong_short = np.mean(df_strong_short["Rating"]) 
    mean_strong_long = np.mean(df_strong_long["Rating"]) 
    d_means = {
            "weak_short": mean_weak_short,
            "weak_long": mean_weak_long,
            "strong_short": mean_strong_short,
            "strong_long": mean_strong_long
            }
    return d_means

##just a wrapper for api purposes
def exp3_data():
    return cleanData3()
