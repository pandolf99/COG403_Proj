from scipy.stats import pearsonr, ttest_ind
import numpy as np
import model.model as mod
import experimental_data.experiments as exps


def corr_exp2():
    """Calculatet the mean 
    """
    exp_data =  exps.exp2_data()
    exp_data = [float(v) for v in exp_data.values()]
    mod_data = mod.exp2_prediction()
    mod_data = [float(v) for v in mod_data.values()]
    return pearsonr(mod_data,exp_data)

def t_test_within_long():
    data = exps.cleanData3()
    weak_long = np.asarray(data["weak_long"])
    strong_long = np.asarray(data["strong_long"])
    n1 = len(weak_long)
    n2 = len(strong_long)
    s1 = np.var(weak_long, ddof=1)
    s2 = np.var(strong_long, ddof=1)
    s = np.sqrt(((n1 - 1)*s1 + (n2 - 1)*s2) / (n1 + n2 - 2))
    d = (np.mean(weak_long) - np.mean(strong_long)) / s
    stat, p = ttest_ind(weak_long, strong_long)
    print(p, d)
    # long = np.concatenate((weak_long, strong_long))
    weak_short = np.asarray(data["weak_short"])
    strong_short = np.asarray(data["strong_short"])
    short = np.concatenate((weak_short, strong_short))
    print(ttest_ind(weak_short, strong_short))
