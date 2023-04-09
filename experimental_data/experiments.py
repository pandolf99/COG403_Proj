import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#ignore a stupid warning
pd.options.mode.chained_assignment = None

alphas = {
        "c1": 0.01,
        "c2": 0.25,
        "c3": 0.5,
        "c4": 0.75,
        "c5": 0.99
        }

def bootstrap_95_CI(data):
    """Calculate 95% confidence interval with bootstrap method
    Parameters:
        data: pd frame 
    Returns:
        [2]: 95% confidence interval
    """
    percentiles = []
    for col in data:
        s_means = np.zeros(10000)
        for i in range(10000):
            sample = np.random.choice(data[col], len(data[col]))
            s_mean = np.mean(sample)
            s_means[i] = s_mean
        percentiles.append(np.percentile(s_means, [2.5, 97.5]))
    return np.asarray(percentiles)

def cleanData1():
    exp1_data = pd.read_csv("experimental_data/Data Exp 1/sca1_data.txt", sep = '\t')
    exp1_data = exp1_data.drop(
            ["subjID", "sex", "age", "taskOrder", "firstTower",
             "scaleOrientation", "respTime", "title", "earlyTower", "targetCause"],
            axis=1)
    ons_diff_delay_same_late = exp1_data[(exp1_data['condition'] == 'Ons-diff_Delay-same') & 
                                    (exp1_data["targetCauseRec"] == "Late Tower")]["rating"]
    ons_diff_delay_same_early = exp1_data[(exp1_data['condition'] == 'Ons-diff_Delay-same') & 
                                    (exp1_data["targetCauseRec"] == "Early Tower")]["rating"]
    ons_same_delay_diff_late = exp1_data[(exp1_data['condition'] == 'Ons-same_Delay-diff') & 
                                    (exp1_data["targetCauseRec"] == "Late Tower")]["rating"]
    ons_same_delay_diff_early = exp1_data[(exp1_data['condition'] == 'Ons-same_Delay-diff') & 
                                    (exp1_data["targetCauseRec"] == "Early Tower")]["rating"]
    ons_diff_delay_diffA_late = exp1_data[(exp1_data['condition'] == "Ons-diff_Delay-diff_A") & 
                                    (exp1_data["targetCauseRec"] == "Late Tower")]["rating"]
    ons_diff_delay_diffA_early = exp1_data[(exp1_data['condition'] == "Ons-diff_Delay-diff_A") & 
                                    (exp1_data["targetCauseRec"] == "Early Tower")]["rating"]
    ons_diff_delay_diffB_late = exp1_data[(exp1_data['condition'] == "Ons-diff_Delay-diff_B") & 
                                    (exp1_data["targetCauseRec"] == "Late Tower")]["rating"]
    ons_diff_delay_diffB_early = exp1_data[(exp1_data['condition'] == "Ons-diff_Delay-diff_B") & 
                                    (exp1_data["targetCauseRec"] == "Early Tower")]["rating"]
    series = [
            pd.Series.reset_index(
                ons_diff_delay_same_late.rename("ons_diff_delay_same_late"), drop=True),
            pd.Series.reset_index(
                ons_diff_delay_same_early.rename("ons_diff_delay_same_early"), drop=True),
            pd.Series.reset_index(
                ons_same_delay_diff_late.rename("ons_same_delay_diff_late"), drop=True),
            pd.Series.reset_index(
                ons_same_delay_diff_early.rename("ons_same_delay_diff_early"), drop=True),
            pd.Series.reset_index(
                ons_diff_delay_diffA_late.rename("ons_diff_delay_diffA_late"), drop=True),
            pd.Series.reset_index(
                ons_diff_delay_diffA_early.rename("ons_diff_delay_diffA_early"), drop=True),
            pd.Series.reset_index(
                ons_diff_delay_diffB_late.rename("ons_diff_delay_diffB_late"), drop=True),
            pd.Series.reset_index(
                ons_diff_delay_diffB_early.rename("ons_diff_delay_diffB_early"), drop=True)
            ]
    return pd.concat(series, axis=1)

def exp1_data():
    d = cleanData1()
    d = d.apply(np.mean)
    return d

#get the errors for condition c
def get_errors1(k):
    df = cleanData1()
    df = df.filter(like=k)
    return bootstrap_95_CI(df)

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
    df_c1 = pd.Series.reset_index(df_c1.apply(updateRating2, axis=1, args=("c1",)), drop=True)
    df_c2 = df[df["GammaDiff"] == "S-F_2"]
    df_c2 = pd.Series.reset_index(df_c2.apply(updateRating2, axis=1, args=("c2",)), drop=True)
    df_c3 = df[df["GammaDiff"] == "Control"]
    df_c3 = pd.Series.reset_index(df_c3.apply(updateRating2, axis=1, args=("c3",)), drop=True)
    df_c4 = df[df["GammaDiff"] == "F-S_2"]
    df_c4 = pd.Series.reset_index(df_c4.apply(updateRating2, axis=1, args=("c4",)), drop=True)
    df_c5 = df[df["GammaDiff"] == "F-S_1"]
    df_c5 = pd.Series.reset_index(df_c5.apply(updateRating2, axis=1, args=("c5",)), drop=True)
    ratings = [ 
               df_c1.rename("condition1"),
               df_c2.rename("condition2"),
               df_c3.rename("condition3"),
               df_c4.rename("condition4"),
               df_c5.rename("condition5"),
               ]
    return pd.concat(ratings, axis=1)

def exp2_data():
    labels = ["Condition1", "Condition2", "Condition3", "Condition4", "Condition5"]
    df_ratings = cleanData2()
    means = np.asarray(df_ratings.apply(np.mean)) / 10
    return dict(zip(labels, means))

def get_errors2():
    data = cleanData2()
    return bootstrap_95_CI(data) / 10

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
    df_weak_short_ratings = pd.Series.reset_index(df_weak_short.apply(updateRating3, axis=1, args=("c1",)), drop=True)
    df_weak_long = df_weak[df_weak["GammaDiff"] == "F-S_1"]
    df_weak_long_ratings = pd.Series.reset_index(df_weak_long.apply(updateRating3, axis=1, args=("c5",)), drop=True)
    df_strong = df[df["Power"] == 0.83]
    #data is mislabeled as "S-F_2", should be "S-F_1"
    df_strong_short = df_strong[df_strong["GammaDiff"] == "S-F_2"]
    df_strong_short_ratings = pd.Series.reset_index(df_strong_short.apply(updateRating3, axis=1, args=("c1",)), drop=True)
    #data is mislabeled as "F-S_2", should be "F-S_1"
    df_strong_long = df_strong[df_strong["GammaDiff"] == "F-S_2"]
    df_strong_long_ratings = pd.Series.reset_index(df_strong_long.apply(updateRating3, axis=1, args=("c5",)), drop=True)
    ratings = [
            df_weak_short_ratings.rename("weak_short"),
            df_weak_long_ratings.rename("weak_long"),
            df_strong_short_ratings.rename("strong_short"),
            df_strong_long_ratings.rename("strong_long")
            ]
    df_ratings = pd.concat(ratings, axis=1,)
    return df_ratings

def get_errors3():
    data = cleanData3()
    return bootstrap_95_CI(data)


##just a wrapper for api purposes
def exp3_data():
    df_ratings = cleanData3()
    mean_weak_short = np.mean(df_ratings["weak_short"]) 
    mean_weak_long = np.mean(df_ratings["weak_long"]) 
    mean_strong_short = np.mean(df_ratings["strong_short"]) 
    mean_strong_long = np.mean(df_ratings["strong_long"]) 
    d_means = {
            "weak_short": mean_weak_short,
            "weak_long": mean_weak_long,
            "strong_short": mean_strong_short,
            "strong_long": mean_strong_long
            }
    return d_means
