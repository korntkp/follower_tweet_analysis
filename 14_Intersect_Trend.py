import fileinput
from math import *
from statistics import *
import matplotlib.pyplot as plt


def read_csv_file(source_path_param):
    list1 = []
    for line in fileinput.input([source_path_param], openhook=fileinput.hook_encoded("utf8")):
        new_line_index = line.find('\n')
        # print(new_line_index)
        list1.append(line[:new_line_index])
    fileinput.close()
    return list1


def two_plot_before(before_scale_retweet, before_scale_follower, topic_name, fold_num):
    fig, ax = plt.subplots()

    ax.plot(range(0, len(before_scale_retweet)), before_scale_retweet, '-', label='Trend Delta Retweet')
    ax.plot(range(0, len(before_scale_follower)), before_scale_follower, '-', label='Trend Delta Follower')

    ax.set_xlabel("Time")
    ax.set_ylabel('Trend Value Before Scaling')
    ax.set_title('Trend Graph (Before Scaling) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')

    axes = plt.gca()
    axes.set_xlim([0, len(before_scale_retweet)])
    axes.legend(loc='upper right')

    plt.show()
    return


def two_plot_after(after_scale_retweet, after_scale_follower, topic_name, fold_num):
    # print("dfgjhjtrter")
    fig, ax = plt.subplots()

    ax.plot(range(0, len(after_scale_retweet)), after_scale_retweet, '-', label='Trend Delta Retweet')
    ax.plot(range(0, len(after_scale_follower)), after_scale_follower, '-', label='Trend Delta Follower')

    ax.set_xlabel("Time")
    ax.set_ylabel('Trend Value After Scaling')
    ax.set_title('Trend Graph (After Scaling) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')

    axes = plt.gca()
    axes.set_xlim([0, len(after_scale_retweet)])
    axes.legend(loc='upper right')

    plt.show()
    return


def four_plot(before_scale_retweet, after_scale_retweet, before_scale_follower, after_scale_follower, choose_str, topic_name, fold_num):
    # print("dfgjhjtrter")
    fig, ax = plt.subplots()

    ax.plot(range(0, len(after_scale_retweet)), after_scale_retweet, '-', label='After Scale Retweet')
    ax.plot(range(0, len(before_scale_retweet)), before_scale_retweet, '-', label='Before Scale Retweet')
    ax.plot(range(0, len(after_scale_follower)), after_scale_follower, '-', label='After Scale Follower')
    ax.plot(range(0, len(before_scale_follower)), before_scale_follower, '-', label='Before Scale Follower')

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
    axes.set_xlim([0, len(after_scale_retweet)])
    axes.legend(loc='upper right')

    plt.show()
    return

y_axis_choices = ['follower_wo_mc']
# y_axis_choices = ['retweet']
topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
# topics = ["apple"]
folds = ["1", "2", "3", "4", "5"]
# folds = ["5"]

for each_choice in y_axis_choices:
    for each_topic in topics:
        for each_fold in folds:

            print("============ Topic: " + each_topic + ", Fold: " + each_fold + ", " + each_choice + " =============")
            source_decomposition_retweet = "E:/tweet_process/result_follower-ret/11_trend_decomposed/" + each_topic + "/decomposition_" + each_fold + "_retweet.csv"
            source_decomposition_follower = "E:/tweet_process/result_follower-ret/11_trend_decomposed/" + each_topic + "/decomposition_" + each_fold + "_follower_wo_mc.csv"
            retweet_list = read_csv_file(source_decomposition_retweet)
            follower_list = read_csv_file(source_decomposition_follower)

            sum_of_retweet = 0
            count_retweet = 0
            only_value_retweet = []

            sum_of_follower = 0
            count_follower = 0
            only_value_follower = []

            new_scale_retweet = []
            new_scale_follower = []

            for i in range(0, len(retweet_list)):
                if retweet_list[i] != 'nan' and retweet_list[i] != 'na':
                    sum_of_retweet += float(retweet_list[i])
                    count_retweet += 1
                    only_value_retweet.append(float(retweet_list[i]))
                if follower_list[i] != 'nan' and follower_list[i] != 'na':
                    sum_of_follower += float(follower_list[i])
                    count_follower += 1
                    only_value_follower.append(float(follower_list[i]))

            avg_retweet = sum_of_retweet / count_retweet
            avg_follower = sum_of_follower / count_follower
            sd_retweet = pstdev(only_value_retweet)
            sd_follower = pstdev(only_value_follower)

            """
            Manual Standard Deviation (Unused)
            """
            # sum_sqr_retweet = 0
            # for i in range(0, len(only_value_retweet)):
            #     sum_sqr_retweet += (only_value_retweet[i] - avg_retweet) * (only_value_retweet[i] - avg_retweet)
            # sd_retweet_manual = sqrt(sum_sqr_retweet / count_retweet)
            # sum_sqr_follower = 0
            # for i in range(0, len(only_value_follower)):
            #     sum_sqr_follower += (only_value_follower[i] - avg_follower) * (only_value_follower[i] - avg_follower)
            # sd_follower_manual = sqrt(sum_sqr_follower / count_follower)

            """
            Print Info
            """
            # print("Sum Follower:", sum_of_follower)
            # print("Sum Retweet:", sum_of_retweet)
            # print("N: ", count_follower)
            # print("Average Follower:", avg_follower)
            # print("Average Retweet:", avg_retweet)
            # print("Standard Variable Follower:", sd_follower)
            # print("Standard Variable Retweet:", sd_retweet)

            for i in range(0, len(only_value_retweet)):
                new_scale_retweet.append((only_value_retweet[i] - avg_retweet) / (sd_retweet * sqrt(count_retweet)))
                new_scale_follower.append((only_value_follower[i] - avg_follower) / (sd_follower * sqrt(count_follower)))

            """
            Print Trend Value
            """
            # print("Trend Value Retweet Before Scale:", only_value_retweet)
            # print("Trend Value Retweet After Scale:", new_scale_retweet)
            # print("Trend Value Follower Before Scale:", only_value_follower)
            # print("Trend Value Retweet After Scale:", new_scale_follower)
            # print("Trend Value Retweet Before Scale:", len(only_value_retweet))
            # print("Trend Value Retweet After Scale:", len(new_scale_retweet))
            # print("Trend Value Follower Before Scale:", len(only_value_follower))
            # print("Trend Value Retweet After Scale:", len(new_scale_follower))

            # two_plot_before(only_value_retweet, only_value_follower, each_topic, each_fold)
            # two_plot_after(new_scale_retweet, new_scale_follower, each_topic, each_fold)
            # four_plot(only_value_retweet, new_scale_retweet, only_value_follower, new_scale_follower, 'follower_wo_mc', each_topic, each_fold)

            """
            Find The Lowest Trend Value
            """
            lowest_trend_ret = min(new_scale_retweet)
            lowest_trend_fol = min(new_scale_follower)
            if lowest_trend_ret < lowest_trend_fol:
                lowest_trend_ret_fol = lowest_trend_ret
            else:
                lowest_trend_ret_fol = lowest_trend_fol
            # print("The Lowest of Retweet", lowest_trend_ret)
            # print("The Lowest of Follower", lowest_trend_fol)
            # print("The Lowest of Retweet and Follower", lowest_trend_ret_fol)

            """
            Find Diff from The Lowest
            """
            diff_from_lowest_retweet = []
            diff_from_lowest_follower = []
            sum_area_retweet = 0
            sum_area_follower = 0
            for i in range(0, len(new_scale_retweet)):
                diff_from_lowest_retweet.append(new_scale_retweet[i] - lowest_trend_ret_fol)
                diff_from_lowest_follower.append(new_scale_follower[i] - lowest_trend_ret_fol)
                print(diff_from_lowest_retweet[i])
                print(diff_from_lowest_follower[i])
                # sum_area_retweet += diff_from_lowest_retweet[i]
                # sum_area_follower += diff_from_lowest_follower[i]

            # print(sum(diff_from_lowest_retweet))
            # print(sum(diff_from_lowest_follower))
            # print(diff_from_lowest_retweet)
            # print(diff_from_lowest_follower)
            # print(sum_area_retweet)
            # print(sum_area_follower)
