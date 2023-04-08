from model.model import *
from experimental_data.experiments import *
from plotting.plot_results  import *

if __name__ == "__main__":
    ##TODO make cli args 
    #predictions
    # d_pred2 = exp2_prediction()
    # d_pred3 = exp3_prediction()
    # plot_exp2(d_pred2, "Model Predictions for experiment 2")
    # plot_exp3(d_pred3, "Model Predictions for experiment 3")
    # #behavioural data
    # d_data2 = exp2_data()
    # errors2 = get_errors2() 
    d_data3 = exp3_data()
    errors3 = get_errors3()
    # plot_exp2(d_data2, "Results for experiment 2", errors2)
    plot_exp3(d_data3, "Results for experiment 3", errors3)
    # plot_correlation2(d_pred2, d_data2)

