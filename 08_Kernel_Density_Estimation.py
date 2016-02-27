from __future__ import print_function
import fileinput
import os.path
from numpy import *
from matplotlib import dates
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

from datetime import datetime
from matplotlib.dates import MONDAY
from matplotlib.finance import quotes_historical_yahoo_ochl
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from matplotlib.backends.backend_pdf import PdfPages

import pandas as pd
import statsmodels.api as sm


def plot_example_wtf():
    # hfmt = dates.DateFormatter('%m/%d %H:%M')
    # ax.xaxis.set_major_locator(dates.MinuteLocator())
    # ax.xaxis.set_major_formatter(hfmt)
    # plt.gcf().autofmt_xdate()

    date1 = datetime.date(2002, 1, 5)
    date2 = datetime.date(2003, 12, 1)

    # every monday
    mondays = WeekdayLocator(MONDAY)

    # every 3rd month
    months = MonthLocator(range(1, 13), bymonthday=1, interval=3)
    monthsFmt = DateFormatter("%b '%y")


    quotes = quotes_historical_yahoo_ochl('INTC', date1, date2)
    if len(quotes) == 0:
        print('Found no quotes')
        raise SystemExit

    dates = [q[0] for q in quotes]
    opens = [q[1] for q in quotes]

    fig, ax = plt.subplots()
    ax.plot_date(dates, opens, '-')
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.xaxis.set_minor_locator(mondays)
    ax.autoscale_view()
    #ax.xaxis.grid(False, 'major')
    #ax.xaxis.grid(True, 'minor')
    ax.grid(True)

    fig.autofmt_xdate()

    plt.show()
    return


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


def plot_kde(data_estimate_param, choose_str, topic_name, fold_num):
    fig, ax = plt.subplots()
    ax.plot(range(0, len(data_estimate_param)), data_estimate_param, label='KDE')
    if topic_name == 'apple' or topic_name == 'aroii':
        ax.set_xlabel("Time(Hour) from 17-Nov-2015 06:00 am")
    elif topic_name == 'hormonestheseries' or topic_name == 'thefacethailand':
        ax.set_xlabel("Time(Hour) from 09-Nov-2015 06:00 am")

    if choose_str == 'follower_wt_mc':
        ax.set_ylabel('Delta Follower with Message Count')
        ax.set_title('Graph of Time and Delta Follower(with Message Count) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
    elif choose_str == 'follower_wo_mc':
        ax.set_ylabel('Delta Follower without Message Count')
        ax.set_title('Graph of Time and Delta Follower(without Message Count) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
    elif choose_str == 'retweet':
        ax.set_ylabel('Delta Retweet')
        ax.set_title('Graph of Time and Delta Retweet [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
    axes = plt.gca()
    axes.set_xlim([0, len(data_estimate_param)])
    plt.show()


def write_date_date_csv(output_path, list_data, start_unix_time, topic_name):

    before_start_time = 0
    one_hour = 3600

    if each_topic == "apple" or each_topic == "aroii":
        before_start_time = start_unix_time[0] - one_hour
    elif each_topic == "hormonestheseries" or each_topic == "thefacethailand":
        before_start_time = start_unix_time[1] - one_hour
    unix_time = before_start_time

    fo = open(output_path, "w")
    for line in list_data:

        if unix_time != before_start_time:
            date_time_str = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
            if line == 0.0:
                result = str(date_time_str) + ",NA\n"
            else:
                result = str(date_time_str) + "," + str(int(line)) + "\n"
            # print(result)
            fo.write(result)
        unix_time += one_hour
    fo.close()
    return


def pandas_plot(output_path):

    # file = open(output_path, "r")
    # for line in file:
    #     print(line)
    kde_follower = pd.read_csv(output_path,
                              names=['DateTime', 'DeltaFollower'],
                              index_col=['DateTime'],
                              parse_dates=True)

    # kde_follower.DeltaFollower.plot()

    decomp_freq = int(24*5)

    kde_follower_interpolated_forward = kde_follower.DeltaFollower.interpolate()
    kde_follower_interpolated_only_bfill = kde_follower.DeltaFollower.interpolate().bfill()
    kde_follower_interpolated_complete = kde_follower_interpolated_forward.interpolate().bfill()
    print(kde_follower_interpolated_forward)
    print(kde_follower_interpolated_only_bfill)
    print(kde_follower_interpolated_complete)

    # res_forward = sm.tsa.seasonal_decompose(kde_follower_interpolated_forward.values, freq=decomp_freq, model='additive')
    # res_only_bfill = sm.tsa.seasonal_decompose(kde_follower_interpolated_only_bfill.values, freq=decomp_freq, model='additive')
    # for k in range(1, 10):
    res_complete = sm.tsa.seasonal_decompose(kde_follower_interpolated_complete.values, freq=decomp_freq, model='additive')
    # res_complete1 = sm.tsa.seasonal_decompose(kde_follower_interpolated_complete.values, freq=21, model='additive')
    # res_complete2 = sm.tsa.seasonal_decompose(kde_follower_interpolated_complete.values, freq=22, model='additive')
    # res_complete3 = sm.tsa.seasonal_decompose(kde_follower_interpolated_complete.values, freq=23, model='additive')
    # res_complete4 = sm.tsa.seasonal_decompose(kde_follower_interpolated_complete.values, freq=24, model='additive')
    # res_complete5 = sm.tsa.seasonal_decompose(kde_follower_interpolated_complete.values, freq=25, model='additive')
    # res_complete6 = sm.tsa.seasonal_decompose(kde_follower_interpolated_complete.values, freq=26, model='additive')
    # res_complete7 = sm.tsa.seasonal_decompose(kde_follower_interpolated_complete.values, freq=27, model='additive')
    # res_complete8 = sm.tsa.seasonal_decompose(kde_follower_interpolated_complete.values, freq=28, model='additive')
    # res_complete9 = sm.tsa.seasonal_decompose(kde_follower_interpolated_complete.values, freq=29, model='additive')
    # res_complete10 = sm.tsa.seasonal_decompose(kde_follower_interpolated_complete.values, freq=30, model='additive')
    # res_complete11 = sm.tsa.seasonal_decompose(kde_follower_interpolated_complete.values, freq=31, model='additive')

    """
    PLOTING
    """
    res_plot = res_complete.plot()
    # res_plot1 = res_complete1.plot()
    # res_plot2 = res_complete2.plot()
    # res_plot3 = res_complete3.plot()
    # res_plot4 = res_complete4.plot()
    # res_plot5 = res_complete5.plot()
    # res_plot6 = res_complete6.plot()
    # res_plot7 = res_complete7.plot()
    # res_plot8 = res_complete8.plot()
    # res_plot9 = res_complete9.plot()
    # res_plot10 = res_complete10.plot()
    # res_plot11 = res_complete11.plot()

    plt.show()
    # print(res)
    # print(res_plot)
    return


# y_axis_choices = ['retweet', 'follower_wt_mc', 'follower_wo_mc']
y_axis_choices = ['follower_wo_mc']
# topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
topics = ["apple"]
# folds = ["1", "2", "3", "4", "5"]
folds = ["1"]

unix_time_start = [1447023600, 1447714800]  # 2015-11-09 06:00:00   2015-11-17 06:00:00
last_hour_app_aroii = 1651
last_hour_hor_theface = 1627

for each_choice in y_axis_choices:
    for each_topic in topics:
        for each_fold in folds:

            print(each_topic, each_fold)
            data = []  # Array for collect original data
            data_estimate = []  # Array for collect KDE processed data

            source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/" + each_topic + "/fold_" + each_fold + "/all_tweet.csv"
            # source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/aroii/fold_1/t1.csv"
            output_csv = "E:/tweet_process/result_follower-ret/07_csv_for_find_trend/" + each_topic + "/date_" + each_choice + "_" + each_fold + ".csv"

            if each_topic == "apple" or each_topic == "aroii":
                for i in range(0, last_hour_app_aroii):
                    data.append([])
            else:
                for i in range(0, last_hour_hor_theface):
                    data.append([])

            # Read data from file and collect in array
            process_data(source_path, data, each_choice)
            # print("Process Data Success")
            # for i in range(0, num_index):
            #     print("data[" + str(i) + "]: " + str(data[i]))
            #     if not data[i]:
            #         print("EMPTY")

            # KDE processing
            for i in range(0, len(data)):
                estimate(data[i], data_estimate, i)

            # for i in range(0, len(data_estimate)):
            #     # if data_estimate[i] > 7:
            #     #     print(str(i) + ": " + str(data_estimate[i]))
            #     if data_estimate[i] > 1:
            #         print(str(i) + ": " + str(data_estimate[i]))
            # # print(data_estimate[0])

            # print("Ploting Graph")
            # plot_kde(data_estimate, each_choice, each_topic, each_fold)
            # plot_example_wtf()

            # write_date_date_csv(output_csv, data_estimate, unix_time_start, each_topic)
            # for k in range(1, 10):
            #     pandas_plot(output_csv, k)
            pandas_plot(output_csv)
