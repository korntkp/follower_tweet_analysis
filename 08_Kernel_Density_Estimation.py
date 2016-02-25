from __future__ import print_function
import fileinput
import os.path
from numpy import *
from matplotlib import dates
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

import datetime
from matplotlib.dates import MONDAY
from matplotlib.finance import quotes_historical_yahoo_ochl
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from matplotlib.backends.backend_pdf import PdfPages


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
        elif choice == 'follower w/t mc':
            y = float(value[10].strip())  # diff_follower_wt_mc
        elif choice == 'follower w/o mc':
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
        xs = linspace(0, max(input_param), num=100)
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

    if choose_str == 'follower w/t mc':
        ax.set_ylabel('Delta Follower with Message Count')
        ax.set_title('Graph of Time and Delta Follower(with Message Count) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
    elif choose_str == 'follower w/o mc':
        ax.set_ylabel('Delta Follower without Message Count')
        ax.set_title('Graph of Time and Delta Follower(without Message Count) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
    elif choose_str == 'retweet':
        ax.set_ylabel('Delta Retweet')
        ax.set_title('Graph of Time and Delta Retweet [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
    axes = plt.gca()
    axes.set_xlim([0, len(data_estimate_param)])
    plt.show()


y_axis_choices = ['retweet', 'follower w/t mc', 'follower w/o mc']
topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
folds = ["1", "2", "3", "4", "5"]

for each_choice in y_axis_choices:
    for each_topic in topics:
        for each_fold in folds:

            data = []  # Array for collect original data
            data_estimate = []  # Array for collect KDE processed data

            source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/" + each_topic + "/fold_" + each_fold + "/all_tweet.csv"
            # source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/aroii/fold_1/t1.csv"

            # Index of time
            num_index = 1655  # ###### Edit here ######### all_hours = 24 * 7 * 10  # 1680

            for i in range(0, num_index):
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
            # print("Estimate Success")

            # for i in range(0, len(data_estimate)):
            #     # if data_estimate[i] > 7:
            #     #     print(str(i) + ": " + str(data_estimate[i]))
            #     if data_estimate[i] > 1:
            #         print(str(i) + ": " + str(data_estimate[i]))
            # # print(data_estimate[0])

            # print("Ploting Graph")
            plot_kde(data_estimate, each_choice, each_topic, each_fold)
            # plot_example_wtf()
