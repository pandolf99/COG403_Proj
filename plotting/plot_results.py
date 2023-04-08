import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.offsetbox import AnchoredText

def plot_exp2(d, title, errors=None):
    """Plot bar graph for experiment 2,
    d: dict with keys as conditions and values for condition
    title: title to use (experimental or prediction)
    """
    if errors is not None:
        errs = [(e[1] - e[0]) for e in errors]
    x = d.keys()
    y = [float(v) for v in d.values()]
    text1 = r'Condition1: $\kappa = 10, \theta = 100 $' + "\n"
    text2 = r'Condition2: $\kappa = 17.77, \theta = 100$'+ "\n" 
    text3 = r'Condition3: $\kappa = 20, \theta = 100 $'+ "\n"
    text4 = r'Condition4: $\kappa = 22, \theta = 100 $'+ "\n"
    text5 = r'Condition5: $\kappa = 30, \theta = 100 $'
    anchor = AnchoredText(text1+text2+text3+text4+text5, loc="upper right")
    fig, ax = plt.subplots()
    ax.bar(x, y, yerr=errs)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.set_ylabel('P(c->e|e,c,a)')
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.add_artist(anchor)
    plt.savefig(f'results/{title}.png')
    return

def plot_exp3(d, title, errors=None):
    """Plot bar graph for experiment3
    d: dictionary with conditions as keys and value for condition
    title: title to use (experimental or prediction)
    """
    if errors is not None:
        errs = [(e[1] - e[0]) for e in errors]
    conditions = ("Long", "Short")
    causal_strengths = {
        'causal strength = 0.5': (float(d["weak_short"]), float(d["weak_long"])),
        'causal strength = 0.83': (float(d["strong_short"]), float(d["strong_long"])),
    }
    x = np.arange(len(conditions))  # the label locations
    width = 0.45  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')
    i = 2 #index for error bar array
    j = 0
    for s, val in causal_strengths.items():
        offset = width * multiplier
        ax.bar(x + offset, val, width, label=s, yerr=errs[j:i])
        # ax.bar_label(rects, padding=3)
        multiplier += 1
        i += 2
        j += 2
    text1 = r'Long: $\kappa = 30, \theta = 100 $' + "\n"
    text2 = r'Short: $\kappa = 10, \theta = 100$'+ "\n" 
    props = dict(boxstyle='round', color="wheat")
    ax.text(1, 0.76, text1+text2, bbox=props)
    ax.set_xlabel("Relative causal latencies of target cause")
    ax.set_ylabel('P(c->e|e,c,a)')
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.set_xticks(x + 0.225, conditions)
    ax.legend(loc='upper left', ncols=3)
    plt.savefig(f'results/{title}.png')
    return

def plot_correlation2(mod, exp):
    """Plot the correlation in exp2
    Parameters:
        mod: means of model prediction
        exp: means of experimental data
    """
    x = np.asfarray(list(mod.values()))
    y = np.asfarray(list(exp.values()))
    #find line of best fit
    a, b = np.polyfit(x, y, 1)
    #add points to plot
    plt.scatter(x, y)
    #add line of best fit to plot
    plt.plot(x, a*x+b)
    plt.show()
