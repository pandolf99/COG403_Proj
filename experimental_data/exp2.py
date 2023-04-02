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


def plot_exp2(x, y):
    """Plot bar graphs for experiment 2
    """
    #TODO add error bars
    text1 = r'Condition1: $\kappa = 10, \theta = 100 $' + "\n"
    text2 = r'Condition2: $\kappa = 17.77, \theta = 100$'+ "\n" 
    text3 = r'Condition3: $\kappa = 20, \theta = 100 $'+ "\n"
    text4 = r'Condition4: $\kappa = 22, \theta = 100 $'+ "\n"
    text5 = r'Condition5: $\kappa = 30, \theta = 100 $'
    anchor = AnchoredText(text1+text2+text3+text4+text5, loc="upper right")
    title = "Model predictions with alpha based on gamma distributions" 
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.set_ylabel('P(c->e|e,c,a)')
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.add_artist(anchor)
    plt.show()

#Function to pass to apply
#and then update rating
def updateRating(row, *args):
    a = row["Alpha"]
    cond = args[0]
    if a == alphas[cond]:
        return row["Rating"]
    return 10 - row["Rating"]

def cleanData():
    df = pd.read_csv("sca2_data.txt", sep='\t')
    #update ratings based on alpha
    df_c1 = df[df["GammaDiff"] == "S-F_1"]
    df_c1["Rating"] = df_c1.apply(updateRating, axis=1, args=("c1",))
    df_c2 = df[df["GammaDiff"] == "S-F_2"]
    df_c2["Rating"] = df_c2.apply(updateRating, axis=1, args=("c2",))
    df_c3 = df[df["GammaDiff"] == "Control"]
    df_c3["Rating"] = df_c3.apply(updateRating, axis=1, args=("c3",))
    df_c4 = df[df["GammaDiff"] == "F-S_2"]
    df_c4["Rating"] = df_c4.apply(updateRating, axis=1, args=("c4",))
    df_c5 = df[df["GammaDiff"] == "F-S_1"]
    df_c5["Rating"] = df_c5.apply(updateRating, axis=1, args=("c5",))
    df_ratings = pd.DataFrame({
        "c1":df_c1["Rating"],
        "c2":df_c2["Rating"],
        "c3":df_c3["Rating"],
        "c4":df_c4["Rating"],
        "c5":df_c5["Rating"],
         })
    return df_ratings

if __name__ == "__main__":
    labels = ["Condition1", "Condition2", "Condition3", "Condition4", "Condition5"]
    df_ratings = cleanData()
    means = np.asarray(df_ratings.apply(np.mean)) / 10
    plot_exp2(labels, means)
    cleanData()
