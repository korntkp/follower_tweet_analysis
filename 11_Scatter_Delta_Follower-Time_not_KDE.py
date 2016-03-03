import fileinput
import math
import matplotlib.pyplot as plt
# from numpy import *
import numpy as np
import pandas as pd
# import statsmodels.api as sm

# def process_data(source_path_param, output, choice):
#     for line in fileinput.input([source_path_param]):
#         value = line.split(',')
#         # print(value)
#         x = int(value[12].strip())  # hour
#         y = 0.0
#         if choice == 'retweet':
#             y = float(value[3].strip())  # diff_retweet
#         elif choice == 'follower_wt_mc':
#             y = float(value[10].strip())  # diff_follower_wt_mc
#         elif choice == 'follower_wo_mc':
#             y = float(value[13].strip())  # diff_follower_wo_mc
#         output[x].append(y)


def extract_diff_ret_or_fol(source_path_param, output, choose_str, is_log_delta_retweet_param, is_log_delta_follower_param, log_base):
    for line in fileinput.input([source_path_param], openhook=fileinput.hook_encoded("utf8")):
        x = int(line.split(',')[12])  # hour
        if choose_str == 'retweet':
            diff_ret = line.split(',')[3]
            dot_index = diff_ret.find(".")
            diff_ret_int = int(diff_ret[0:dot_index])
            if is_log_delta_retweet_param:  # Log
                if diff_ret_int > 0:
                    diff_ret_log = math.log(diff_ret_int, log_base)
                    output[x].append(diff_ret_log)
                else:
                    output[x].append(0.0)
            else:
                output[x].append(diff_ret_int)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! START EDIT HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        elif choose_str == 'follower w/t mc':
            diff_fol = float(line.split(',')[10])
            if is_log_delta_follower_param:  # Log
                if diff_fol > 0:
                    diff_fol_log = math.log(diff_fol, log_base)
                    output[x].append(diff_fol_log)
                else:
                    output[x].append(0.0)
            else:
                output[x].append(diff_fol)

        elif choose_str == 'follower w/o mc':
            diff_fol = float(line.split(',')[13])
            if is_log_delta_follower_param:  # Log
                if diff_fol > 0:
                    diff_fol_log = math.log(diff_fol, log_base)
                    output[x].append(diff_fol_log)
                else:
                    output[x].append(0.0)
            else:
                output[x].append(diff_fol)
                print(str(x) + "," + str(diff_fol))
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! END EDIT HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    fileinput.close()


def plot_diff_fol_and_time(list_fol, choose_str, topic_name, fold_num, is_log_delta_follower_param):
    for i in range(0, len(list_fol)):
        plt.plot(list_fol[i], 1652, 'ro')
    plt.axis([min(list_fol), max(list_fol), 0, 1660])

    if is_log_delta_follower_param:
        plt.xlabel('Time (Hour)')
        if choose_str == 'follower w/t mc':
            plt.ylabel('Log(Delta Follower with Message Count)')
            plt.title('Graph of Log(Delta Follower(with Message Count)) and Time [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
        elif choose_str == 'follower w/o mc':
            plt.ylabel('Log(Delta Follower without Message Count)')
            plt.title('Graph of Log(Delta Follower(without Message Count)) and Time [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')

    else:
        plt.xlabel('Time (Hour)')
        if choose_str == 'follower w/t mc':
            plt.ylabel('Delta Follower with Message Count')
            plt.title('Graph of Delta Follower(with Message Count) and Time [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
        elif choose_str == 'follower w/o mc':
            plt.ylabel('Delta Follower without Message Count')
            plt.title('Graph of Delta Follower(without Message Count) and Time [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
    plt.show()


# SET PARAMETER
# follower_choices = ['follower w/t mc', 'follower w/o mc']
follower_choices = ['follower w/o mc']
# topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
topics = ["apple"]
# folds = ["1", "2", "3", "4", "5"]
folds = ["1"]
is_log_delta_retweet = False
is_log_delta_follower = False
logarithm_base_num = 10

last_hour_app_aroii = 1651
last_hour_hor_theface = 1627

for each_choice in follower_choices:
    for each_topic in topics:
        for each_fold in folds:

            data_diff_fol = []
            source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/" + each_topic + "/fold_" + each_fold + "/all_tweet.csv"

            if each_topic == "apple" or each_topic == "aroii":
                for i in range(0, last_hour_app_aroii):
                    data_diff_fol.append([])
            else:
                for i in range(0, last_hour_hor_theface):
                    data_diff_fol.append([])

            extract_diff_ret_or_fol(source_path, data_diff_fol, each_choice, is_log_delta_retweet, is_log_delta_follower, logarithm_base_num)

            print("============ Topic: " + each_topic + ", Fold: " + each_fold + ", " + each_choice + " =============")
            # print("Log Delta Follower: " + str(is_log_delta_follower))
            # if is_log_delta_follower:
            #     print("Logarithm Base Number: " + str(logarithm_base_num))
            # print("Max of Delta follower -> " + str(max(data_diff_fol[1])))
            # print("Min of Delta follower -> " + str(min(data_diff_fol[1])))



            """
            TEST
            """
            # print("Length of data_ret_fol: " + str(len(data_diff_fol)))
            # temp_data = []
            # for i in range(1, len(data_diff_fol)):
            #     for j in range(0, len(data_diff_fol[i])):
            #         temp_data.append(data_diff_fol[i].pop())
            #     print(temp_data)
            #     # print(data_diff_fol[i].pop())
            # print("Test" + str(data_diff_fol[1]))
            # print(range(0, len(data_diff_fol)))

            # plot_diff_fol_and_time(data_diff_fol, each_choice, each_topic, each_fold, is_log_delta_follower)

            """
            Pandas Plot
            """
            dataf = pd.DataFrame(np.random.rand(50, 4), columns=['a', 'b', 'c', 'd'])
            dataf.plot(kind='scatter', x='a', y='b')
            plt.show()

            test_diff_follower = pd.read_csv('test_pandas_scatter_plot.csv',
                              names=['Hours', 'DeltaFollower'])
            test_diff_follower.plot(kind='scatter', x='Hours', y='DeltaFollower')
            plt.show()
            print("End of Program")
