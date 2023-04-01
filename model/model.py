import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.offsetbox import AnchoredText

def plot_exp2(x, y):
    """Plot bar graphs for experiment 2
    """
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
    title = "Interaction between causal strengths and causal latencies"
    ax.set_ylabel('P(c->e|e,c,a)')
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.set_xticks(x + 0.225, conditions)
    ax.legend(loc='upper left', ncols=3)
    plt.show()

#read parameters from file
#see dummy.json for format
def readParams(file):
    with open(file) as f:
        d = json.load(f)
    return d


def getAlpha(data):
    """Get the alpha value to quantify time.
    If fixed, just calculate, otherwise run montecarlo algo
    as descibed in paper
    Parameters:
        data: dict with data, see dummy.json
        use_mean: calculate alpha based on mean of gammas
    Returns:
        float: alpha value that quantifies preemption prob
    """
    if data["fixed_latency"]:
        return 1 if (data["t_a->e"] + data["t_delta"]) < data["t_c->e"] else 0
    #number of samples to take
    #test different values of this
    N = 1000000
    #sample for alternative cause
    shape_a = data["shape_a"]
    scale_a = data["scale_a"]
    s_a = np.random.default_rng().gamma(shape_a, scale_a, N)
    #sample for target cause
    shape_c = data["shape_c"]
    scale_c = data["scale_c"]
    s_c = np.random.default_rng().gamma(shape_c, scale_c, N)
    #calc
    s_a = s_a + data["t_delta"]
    #count samples that are < sc
    count = np.count_nonzero(s_a < s_c)
    ret = count / N
    return ret


def calcProb(data):
    """Calculate probability for singular cause
    Parameters:
        data: see dummy.json
    Returns:
        float: probability of c being the singular cause
    """
    w_a = data["w_a"] #causal strength of alternative cause
    w_c = data["w_c"] #causal strength of target cause
    alpha = data["alpha"]
    num = w_c*(1 - w_a*alpha)
    denom = (w_c+w_a)-(w_c*w_a) 
    return num / denom


def run_exp1():
    """Run all conditions for experiment 1
    Returns:
        string: json formatted results for every condition
    """
    d = readParams("exp1_params.json")
    d_res = {} 
    for condition in d: #gets the condition/key of the data
        data = d[condition] #gets the data under each condition
        d_res[condition] = []
        for i, dt in enumerate(data): 
            dt["alpha"] = getAlpha(dt)
            prob = calcProb(dt)
            resStr = f"Cause{i}: {prob}"
            d_res[condition].append(resStr)
    parsed = json.dumps(d_res, indent=4)
    return parsed

def run_exp2(): 
    """Run all conditions for experiment 1
    Returns:
        string: json formatted results for every condition
    """
    d = readParams("exp2_params.json")
    d_res = {}
    for condition in d:
        #calculate alpha based on MC sampling
        d[condition]["alpha"] = getAlpha(d[condition])
        d_res[condition] = f"{calcProb(d[condition])}"
    parsed = json.dumps(d_res, indent=4)
    #data to plot 
    keys = [k for k in d_res.keys()]
    vals = [float(v) for v in d_res.values()]
    plot_exp2(keys, vals)
    return parsed 

def run_exp3(): 
    d = readParams("exp3_params.json")
    d_res = {}
    for condition in d:
        #calculate alpha based on MC sampling
        d[condition]["alpha"] = getAlpha(d[condition])
        d_res[condition] = f"{calcProb(d[condition])}"
    parsed = json.dumps(d_res, indent=4)
    plot_exp3(d_res)
    return parsed 

if __name__ == "__main__":
    # print(run_exp1())
    # print(run_exp2())
    print(run_exp3())

