import fileinput
import os.path
from numpy import *
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def process_data(source_path_param):
    i = 0
    x = []
    y = []
    for line in fileinput.input([source_path_param]):
        value = line.split(',')
        # print(value)
        time = int(value[12].strip())  # ###### Edit here #########    hour
        if time <= 18:
            # print(value[3].strip())
            x.append(float(value[3].strip()))  # ###### Edit here #########  diff_retweet
            y.append(float(value[10].strip()))  # ###### Edit here #########  diff_follower
            # print(str(x[i]) + ", " + str(y[i]))
            # i += 1
    return x, y


def plot_diff_ret_and_diff_fol(list_ret, list_fol):
    min_ret = min(list_ret)
    max_ret = max(list_ret)
    min_fol = min(list_fol)
    max_fol = max(list_fol)
    plt.plot(list_ret, list_fol, 'ro')
    plt.axis([min_ret, max_ret, min_fol, max_fol])
    # plt.axis('tight')
    plt.ylabel('Delta Follower')
    plt.xlabel('Delta Retweet')
    plt.title('Graph of Delta Retweet and Delta Follower')
    plt.show()


# File to read from
source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/aroii/fold_1/all_tweet.csv"
# source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/aroii/fold_1/t1.csv"

list_diff_ret, list_diff_fol = process_data(source_path)

print(list_diff_ret)
print(list_diff_fol)

plot_diff_ret_and_diff_fol(list_diff_ret, list_diff_fol)
