import fileinput
from numpy import *
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import matplotlib.pyplot as plt


def extract_diff_ret_or_fol(source_path_param, choose_str):
    list1 = []
    for line in fileinput.input([source_path_param], openhook=fileinput.hook_encoded("utf8")):
        if choose_str == 'retweet':
            diff_ret = line.split(',')[3]
            dot_index = diff_ret.find(".")
            diff_ret_int = int(diff_ret[0:dot_index])
            list1.append(diff_ret_int)  # Normal

        elif choose_str == 'follower_wt_mc':
            diff_fol = float(line.split(',')[10])
            list1.append(diff_fol)  # Normal

        elif choose_str == 'follower_wo_mc':
            diff_fol = float(line.split(',')[13])
            list1.append(diff_fol)  # Normal
    fileinput.close()
    return list1


def write_date_date_csv(output_path, list_diff_ret_param, list_diff_fol_param, choice):
    fo = open(output_path, "w")

    if choice == 'all_tweet':
        for j in range(0, len(list_diff_ret_param)):
            result = str(list_diff_ret_param[j]) + "," + str(list_diff_fol_param[j]) + "\n"
            # print(result)  # TEST
            fo.write(result)
    elif choice == 'kde':
        for j in range(1, len(list_diff_ret_param)):
            diff_ret_str = str(list_diff_ret_param[j])
            diff_fol_str = str(list_diff_fol_param[j])
            if diff_fol_str == '0.0':
                diff_fol_str = 'NA'
            if diff_ret_str == '0.0':
                diff_ret_str = 'NA'
            result = diff_ret_str + "," + diff_fol_str + "\n"
            # print(result)  # TEST
            fo.write(result)
    fo.close()
    return


def pandas_df(data_path, topic_name, fold_num):
    kde_follower = pd.read_csv(data_path, names=['DeltaRetweet', 'DeltaFollower'])

    # print(kde_follower)
    decomp_freq = int(18*7)
    # kde_follower_interpolated_bfill = kde_follower.DeltaFollower.interpolate().bfill()

    # SELECT GRAPH PLOT
    # 1 not Interpolate Plot
    # ori_plot = kde_follower.DeltaFollower.plot()
    # ori_plot.set_title("Topic: " + str(topic_name) + " Fold: " + str(fold_num))
    # 2 Interpolate Plot
    # ori_interpolated_plot = kde_follower.DeltaFollower.interpolate().plot()
    # ori_interpolated_plot.set_title("Topic: " + str(topic_name) + " Fold: " + str(fold_num))
    # 3 Decomposition Plot
    # res_plot = res_only_bfill.plot()

    # plt.show()
    return kde_follower


def process_data(source_path_param, output, choice):
    for line in fileinput.input([source_path_param]):
        value = line.split(',')
        # print(value)
        x = int(value[12].strip())  # hour
        y = 0.0
        if choice == 'retweet':
            y = float(value[3].strip())  # diff_retweet
        elif choice == 'follower_wt_mc':
            y = float(value[10].strip())  # diff_follower_wt_mc
        elif choice == 'follower_wo_mc':
            y = float(value[13].strip())  # diff_follower_wo_mc
        output[x].append(y)


def estimate(input_param, output, hour):
    if not input_param:
        nothing_message = "Nothing at t: " + str(hour)
        # print(nothing_message)
        output.append(0.0)
    elif len(input_param) == 1:
        nothing_message = "Only One Source Tweet at t: " + str(hour)
        # print(nothing_message)
        output.append(0.0)
    else:
        # print("Round :" + str(hour))
        # print("input_param:  " + str(input_param))
        x = array(input_param)
        # print("Array x: " + str(x))
        try:
            kde = stats.gaussian_kde(x)
        except np.linalg.linalg.LinAlgError:
            # print("Singular Matrix at t: " + str(hour))
            output.append(0.0)
            return
        xs = linspace(min(input_param), max(input_param), num=100)
        kde.set_bandwidth(bw_method='silverman')
        kde.set_bandwidth(bw_method=kde.factor / 2)
        y = kde(xs)
        sum_weight = 0
        value = 0
        for j in range(0, len(xs)):
            value += xs[j]*y[j]
            sum_weight += y[j]

        avg = value/sum_weight
        output.append(avg)


# SET PARAMETER
# y_axis_choices = ['retweet', 'follower_wt_mc', 'follower_wo_mc']
y_axis_choices = ['follower_wo_mc']
topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
# topics = ["apple"]
folds = ["1", "2", "3", "4", "5"]
# folds = ["1"]

last_hour_app_aroii = 1651
last_hour_hor_theface = 1627

for each_choice in y_axis_choices:
    for each_topic in topics:
        for each_fold in folds:
            print(each_topic, each_fold, each_choice)

            source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/" + each_topic + "/fold_" + each_fold + "/all_tweet.csv"
            output_follower_csv = "E:/tweet_process/result_follower-ret/09_follower_retweet_csv/" + each_topic + "/fold_" + each_fold + "/all_tweet-diff_ret-diff_fol.csv"
            output_kde_ret_fol_csv = "E:/tweet_process/result_follower-ret/10_KDE_fol_ret_csv/" + each_topic + "/fold_" + each_fold + "/kde-diff_ret-diff_fol.csv"

            """
            Read & Write Data
            """
            # list_diff_ret = extract_diff_ret_or_fol(source_path, 'retweet')
            # list_diff_fol = extract_diff_ret_or_fol(source_path, each_choice)
            # write_date_date_csv(output_follower_csv, list_diff_ret, list_diff_fol, 'all_tweet')
            # print(list_diff_fol)
            # print(list_diff_ret)
            # print("================= End Read & Write Data ==================")

            # """
            # NOT KDE
            # """
            # df_follower = pandas_df(output_follower_csv, each_topic, each_fold)
            # print(df_follower)
            # df_follower.boxplot()
            # # df_follower.boxplot(by='DeltaRetweet')
            # plt.show()

            """
            KDE
            """
            data_retweet = []  # Array for collect original data
            data_follower = []  # Array for collect original data
            data_estimate_retweet = []  # Array for collect KDE processed data
            data_estimate_follower = []  # Array for collect KDE processed data

            if each_topic == "apple" or each_topic == "aroii":
                for i in range(0, last_hour_app_aroii):
                    data_retweet.append([])
                    data_follower.append([])
            else:
                for i in range(0, last_hour_hor_theface):
                    data_retweet.append([])
                    data_follower.append([])

            process_data(source_path, data_retweet, 'retweet')
            process_data(source_path, data_follower, 'follower_wo_mc')

            # KDE processing
            for i in range(0, len(data_retweet)):
                estimate(data_retweet[i], data_estimate_retweet, i)
                estimate(data_follower[i], data_estimate_follower, i)

            """
            Write KDE Data
            """
            # print(len(data_estimate_retweet))
            # print(data_estimate_retweet)
            # print(len(data_estimate_follower))
            # print(data_estimate_follower)
            # write_date_date_csv(output_kde_ret_fol_csv, data_estimate_retweet, data_estimate_follower, 'kde')

            kde_df_ret_fol = pd.read_csv(output_kde_ret_fol_csv, names=['DeltaRetweet', 'DeltaFollower'])
            # print(kde_df_ret_fol)
            plotx = kde_df_ret_fol.boxplot(return_type='both', grid='on')
            # kde_df_ret_fol.plot(title='Delta Retweet - Delta Follower')
            # df_follower.boxplot(by='DeltaRetweet')
            print(plotx)
            plt.title('Delta Retweet - Delta Follower (' + each_topic + ', ' + each_fold + ')')
            axes = plt.gca()
            axes.set_ylim([-10, 80])
            plt.show()