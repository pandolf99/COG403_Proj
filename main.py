from model.model import *
from experimental_data.experiments import *
from plotting.plot_results  import *
from stats.stat_tests import *

def run_exp1():
    # print(exp1_stats())
    # print(exp1_t_test())
    # d_data1 = exp1_data()
    # k1 = "ons_diff_delay_same"
    # c1 = d_data1.filter(like=k1)
    # errors1_1 = get_errors1(k1)
    # plot_exp1(c1, "Different onset but same delay", k1, errors1_1)
    # k2 = "ons_same_delay_diff"
    # c2 = d_data1.filter(like=k2)
    # errors1_2 = get_errors1(k2)
    # plot_exp1(c2, "Same onset but different delay", k2, errors1_2)
    # k3 = "ons_diff_delay_diffA"
    # c3 = d_data1.filter(like=k3)
    # errors1_3 = get_errors1(k3)
    # plot_exp1(c3, "Different onset and different delay (A)", k3, errors1_3)
    # k4 = "ons_diff_delay_diffB"
    # c4 = d_data1.filter(like=k4)
    # errors1_4 = get_errors1(k4)
    # plot_exp1(c4, "Different onset and different delay (B)", k4, errors1_4)
    return

def run_exp2():
    # d_pred2 = exp2_prediction()
    # plot_exp2(d_pred2, "Model Predictions for experiment 2")
    # d_data2 = exp2_data()
    # errors2 = get_errors2() 
    # plot_exp2(d_data2, "Results for experiment 2", errors2)
    # plot_correlation2(d_pred2, d_data2)
    # print(t_test_within_long())
    print(exp2_stats())
    return

def run_exp3():
    d_pred3 = exp3_prediction()
    plot_exp3(d_pred3, "Model Predictions for experiment 3")
    d_data3 = exp3_data()
    errors3 = get_errors3()
    plot_exp3(d_data3, "Results for experiment 3", errors3)
    return 

if __name__ == "__main__":
    run_exp2()
