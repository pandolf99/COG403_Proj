import numpy as np
import json


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
    Returns:
        float: alpha value that quantifies preemption prob
    """
    if data["fixed_latency"]:
        return 1 if (data["t_a->e"] + data["t_delta"]) < data["t_c->e"] else 0
    #number of samples to take
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


def exp1_prediction():
    """Run all conditions for experiment 1
    Returns:
        string: json formatted results for every condition
    """
    d = readParams("model/exp1_params.json")
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

def exp2_prediction(): 
    """Run all conditions for experiment 2
    Returns:
        string: json formatted results for every condition
    """
    d = readParams("model/exp2_params.json")
    d_res = {}
    for condition in d:
        #calculate alpha based on MC sampling
        d[condition]["alpha"] = getAlpha(d[condition])
        d_res[condition] = f"{calcProb(d[condition])}"
    #data to plot 
    return d_res

def exp3_prediction(): 
    d = readParams("model/exp3_params.json")
    d_res = {}
    for condition in d:
        #calculate alpha based on MC sampling
        d[condition]["alpha"] = getAlpha(d[condition])
        d_res[condition] = f"{calcProb(d[condition])}"
    return d_res
