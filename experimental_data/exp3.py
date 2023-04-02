import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.offsetbox import AnchoredText

alphas = {
        "c1": 0.01,
        "c2": 0.25,
        "c3": 0.5,
        "c4": 0.75,
        "c5": 0.99
        }


def plot_exp3(d):
    conditions = ("Long", "Short")
    causal_strengths = {
        'causal strength = 0.5': (float(d["weak_long"]), float(d["weak_short"])),
        'causal strength = 0.83': (float(d["strong_long"]), float(d["strong_short"])),
    }
    x = np.arange(len(conditions))  # the label locations
    width = 0.45  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for s, val in causal_strengths.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, val, width, label=s)
        ax.bar_label(rects, padding=3)
        multiplier += 1
    title = "Experimental Interaction between causal strengths and causal latencies"
    text1 = r'Long: $\kappa = 30, \theta = 100 $' + "\n"
    text2 = r'Short: $\kappa = 10, \theta = 100$'+ "\n" 
    props = dict(boxstyle='round', color="wheat")
    ax.text(-0.25, 0.76, text1+text2, bbox=props)
    ax.set_xlabel("Relative causal latencies of target cause")
    ax.set_ylabel('P(c->e|e,c,a)')
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.set_xticks(x + 0.225, conditions)
    ax.legend(loc='upper left', ncols=3)
    plt.show()

#Function to pass to apply
#and then update rating
def updateRating(row, *args):
    a = row["Alpha"]
    cond = args[0]
    if a == alphas[cond]:
        return row["Rating"]
    return 1 - row["Rating"]

def cleanData():
    df = pd.read_csv("Data Exp 3/data_mainDV.txt", sep='\t')
    df_weak = df[df["Power"] == 0.5] 
    df_weak_short = df_weak[df_weak["GammaDiff"] == "S-F_1"]
    df_weak_short["Rating"] = df_weak_short.apply(updateRating, axis=1, args=("c1",))
    df_weak_long = df_weak[df_weak["GammaDiff"] == "F-S_1"]
    df_weak_long["Rating"] = df_weak_long.apply(updateRating, axis=1, args=("c5",))
    df_strong = df[df["Power"] == 0.83]
    #data is mislabeled as "S-F_2", should be "S-F_1"
    df_strong_short = df_strong[df_strong["GammaDiff"] == "S-F_2"]
    df_strong_short["Rating"] = df_strong_short.apply(updateRating, axis=1, args=("c1",))
    #data is mislabeled as "F-S_2", should be "F-S_1"
    df_strong_long = df_strong[df_strong["GammaDiff"] == "F-S_2"]
    df_strong_long["Rating"] = df_strong_long.apply(updateRating, axis=1, args=("c5",))
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

if __name__ == "__main__":
    means = cleanData()
    plot_exp3(means)

