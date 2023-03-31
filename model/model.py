import numpy as np
import json

#read parameters from file
#see dummy.json for format
def readParams(file):
    with open(file) as f:
        d = json.load(f)
    return d


def runMC(data):
    """Run the MonteCarlo Alogirthm as specified in the paper
    Parameters:
        data: dict with data, see dummy.json
    Returns:
        float: alpha value that quantifies preemption prob
    """
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
    #calculate t_(a->e) + t_delta
    s_a = s_a + data["t_delta"]
    #count samples that are < sc
    count = np.count_nonzero(s_a < s_c)
    ret = count / N
    print(ret)
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

if __name__ == "__main__":
    d= readParams("dummy.json")
    d["alpha"] = runMC(d)
    print(calcProb(d))