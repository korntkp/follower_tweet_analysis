import fileinput
import numpy
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from email.utils import parsedate_tz


def extract_diff_ret_or_fol(source_path, choose_str):
    # Open file
    list1 = []
    for line in fileinput.input([source_path], openhook=fileinput.hook_encoded("utf8")):
        if choose_str == 'retweet':
            diff_ret = line.split(',')[3]
            dot_index = diff_ret.find(".")
            diff_ret_int = int(diff_ret[0:dot_index])
            # if diff_ret_int < 1:
            list1.append(diff_ret_int)
            # print(str(diff_ret_int))

        elif choose_str == 'follower w/t mc':
            diff_fol = float(line.split(',')[10])
            # if diff_fol < 1:
            list1.append(diff_fol)
            # print(str(diff_fol))

        elif choose_str == 'follower w/o mc':
            diff_fol = float(line.split(',')[13])
            # if diff_fol < 1:
            list1.append(diff_fol)
            # print(str(diff_fol))

    fileinput.close()
    return list1

"""
def extract_diff_fol(source_path):
    # Open file
    list1 = []
    for line in fileinput.input([source_path], openhook=fileinput.hook_encoded("utf8")):
        diff_fol = line.split(',')[6]
        dot_index = diff_fol.find(".")
        diff_fol_int = int(diff_fol[0:dot_index])
        if diff_fol_int > 1:
            list1.append(diff_fol_int)
        print(str(diff_fol_int))
    return list1
"""

"""
def plot_diff_fol_andNumber(list_fol):
    hist, bin_edges = numpy.histogram(list_fol, bins=range(200))
    # max_in_list = max(list_fol)
    # print(list_fol)
    print(hist)
    # array([0, 2, 4, 1])
    print (bin_edges)
    # array([0, 1, 2, 3, 4]))
    plt.bar(bin_edges[:-1], hist, width=1)
    plt.xlim(min(bin_edges), max(bin_edges))
    plt.ylabel('Number of Tweet')
    plt.xlabel('Difference of Follower')
    plt.title('Histogram of Difference of Follower')
    plt.show()
    return

def plot_diff_ret_andNumber(list_ret):
    hist, bin_edges = numpy.histogram(list_ret, bins=range(28800))
    # max_in_list = max(list_ret)
    # print(list_ret)
    print(hist)
    # array([0, 2, 4, 1])
    print (bin_edges)
    # array([0, 1, 2, 3, 4]))
    plt.bar(bin_edges[:-1], hist, width=1)
    plt.xlim(min(bin_edges), max(bin_edges))
    plt.ylabel('Number of Tweet')
    plt.xlabel('Difference of Retweet')
    plt.title('Histogram of Difference of Retweet')
    plt.show()
"""


def plot_diff_ret_and_diff_fol(list_ret, list_fol, choose_str, topic_name, fold_num):
    plt.plot(list_ret, list_fol, 'ro')
    plt.axis([0, max(list_ret), 0, max(list_fol)])
    # plt.axis('tight')
    plt.xlabel('Delta Retweet')
    if choose_str == 'follower w/t mc':
        plt.ylabel('Delta Follower with Message Count')
        plt.title('Graph of Delta Retweet and Delta Follower(with Message Count) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
    elif choose_str == 'follower w/o mc':
        plt.ylabel('Delta Follower without Message Count')
        plt.title('Graph of Delta Retweet and Delta Follower(without Message Count) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
    plt.show()

# Path

follower_choices = ['follower w/t mc', 'follower w/o mc']
topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
folds = ["1", "2", "3", "4", "5"]

for each_choice in follower_choices:
    for each_topic in topics:
        for each_fold in folds:
            source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/" + each_topic + "/fold_" + each_fold + "/all_tweet.csv"

            list_diff_ret = extract_diff_ret_or_fol(source_path, 'retweet')
            # print("Extract - retweet - Success!!")
            list_diff_fol = extract_diff_ret_or_fol(source_path, each_choice)
            # print("Extract - follower - Success!!")

            print("============= Topic: " + each_topic + ", Fold: " + each_fold + ", " + each_choice + " ==============")
            print("Max of Diff retweet -> " + str(max(list_diff_ret)))
            print("Max of Diff follower -> " + str(max(list_diff_fol)))
            # print(str(max(list_diff_fol)))
            plot_diff_ret_and_diff_fol(list_diff_ret, list_diff_fol, each_choice, each_topic, each_fold)
            print("\n")
