from scipy.stats import pearsonr, ttest_ind
import numpy as np
import model.model as mod
import experimental_data.experiments as exps


def corr_exp2():
    """Calculate correlation
    """
    exp_data =  exps.exp2_data()
    exp_data = [float(v) for v in exp_data.values()]
    mod_data = mod.exp2_prediction()
    mod_data = [float(v) for v in mod_data.values()]
    return pearsonr(mod_data,exp_data)

def exp3_t_test():
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
    long = {
            "t_stat": stat,
            "p_value": p,
            "cohen_d": d
            }
    weak_short = np.asarray(data["weak_short"])
    strong_short = np.asarray(data["strong_short"])
    n1 = len(weak_short)
    n2 = len(strong_short)
    s1 = np.var(weak_short, ddof=1)
    s2 = np.var(strong_short, ddof=1)
    s = np.sqrt(((n1 - 1)*s1 + (n2 - 1)*s2) / (n1 + n2 - 2))
    d = (np.mean(weak_short) - np.mean(strong_short)) / s
    stat, p = ttest_ind(strong_short, weak_short)
    short = {
            "t_stat": stat,
            "p_value": p,
            "cohen_d": d
            }
    return {
            "long": long,
            "short": short
            }


def t_test(d1, d2):
    """Perform a t test between d1 and d2
    Also return cohen's d
    """
    s1 = np.var(d1, ddof=1)
    s2 = np.var(d2, ddof=1)
    s = np.sqrt((s1 + s2) /  2)
    d = (np.mean(d1) - np.mean(d2)) / s
    stat, p = ttest_ind(d1, d2)
    return {
            "t_stat": stat,
            "p_value": p,
            "cohen_d": d
            }


def exp1_stats():
    d = exps.cleanData1()
    ret = {}
    for col in d:
        cond = d[col]
        mean = np.mean(cond)
        std = np.std(cond)
        med = np.median(cond)
        CI = exps.get_errors1(col)
        ret[col] = {
                "mean": mean,
                "std": std,
                "med": med,
                "95CI": list(CI)
                }
    return ret

def exp1_t_test():
    d = exps.cleanData1()
    k1 = "ons_diff_delay_same"
    c1 = d.filter(like=k1)
    c1_t = t_test(np.asarray(c1.iloc[:, 1]), np.asarray(c1.iloc[:, 0]))
    k2 = "ons_same_delay_diff"
    c2 = d.filter(like=k2)
    c2_t = t_test(np.asarray(c2.iloc[:, 1]), np.asarray(c2.iloc[:, 0]))
    k3 = "ons_diff_delay_diffA"
    c3 = d.filter(like=k3)
    c3_t = t_test(np.asarray(c3.iloc[:, 1]), np.asarray(c3.iloc[:, 0]))
    k4 = "ons_diff_delay_diffB"
    c4 = d.filter(like=k4)
    c4_t = t_test(np.asarray(c4.iloc[:, 1]), np.asarray(c4.iloc[:, 0]))
    return {
            k1: c1_t,
            k2: c2_t,
            k3: c3_t,
            k4: c4_t
            }

def exp2_stats():
    d = exps.cleanData2()
    ret = {}
    i = 0
    for col in d:
        cond = d[col] / 10
        mean = np.mean(cond)
        std = np.std(cond)
        med = np.median(cond)
        CI = exps.get_errors2()[i]
        ret[col] = {
                "mean": mean,
                "std": std,
                "med": med,
                "95CI": CI
                }
        i+=1
    return ret

def exp3_stats():
    d = exps.cleanData3()
    ret = {}
    i = 0
    for col in d:
        cond = d[col]
        mean = np.mean(cond)
        std = np.std(cond)
        med = np.median(cond)
        CI = exps.get_errors3()[i]
        ret[col] = {
                "mean": mean,
                "std": std,
                "med": med,
                "95CI": CI
                }
        i += 1
    return ret
