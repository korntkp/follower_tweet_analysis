import fileinput
import math
from statistics import *


def read_csv_file(source_path_param):
    list1 = []
    for line in fileinput.input([source_path_param], openhook=fileinput.hook_encoded("utf8")):
        new_line_index = line.find('\n')
        # print(new_line_index)
        list1.append(line[:new_line_index])
    fileinput.close()
    return list1

y_axis_choices = ['follower_wo_mc']
# y_axis_choices = ['retweet']
# topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
topics = ["apple"]
# folds = ["1", "2", "3", "4", "5"]
folds = ["1"]

for each_choice in y_axis_choices:
    for each_topic in topics:
        for each_fold in folds:

            print("============ Topic: " + each_topic + ", Fold: " + each_fold + ", " + each_choice + " =============")
            source_decomposition_retweet = "E:/tweet_process/result_follower-ret/11_trend_decomposed/" + each_topic + "/decomposition_" + each_fold + "_retweet.csv"
            source_decomposition_follower = "E:/tweet_process/result_follower-ret/11_trend_decomposed/" + each_topic + "/decomposition_" + each_fold + "_follower_wo_mc.csv"

            retweet_list = read_csv_file(source_decomposition_retweet)
            follower_list = read_csv_file(source_decomposition_follower)
            # print(retweet_list)
            # print(follower_list)
            # print(len(retweet_list))

            sum_of_retweet = 0
            count_reweet = 0
            only_value_retweet = []

            sum_of_follower = 0
            count_follower = 0
            only_value_follower = []

            for i in range(0, len(retweet_list)):
                if retweet_list[i] != 'nan' and retweet_list[i] != 'na':
                    sum_of_retweet += float(retweet_list[i])
                    count_reweet += 1
                    only_value_retweet.append(float(retweet_list[i]))
                if follower_list[i] != 'nan' and follower_list[i] != 'na':
                    sum_of_follower += float(follower_list[i])
                    count_follower += 1
                    only_value_follower.append(float(follower_list[i]))

            avg_retweet = sum_of_retweet / count_reweet
            avg_follower = sum_of_follower / count_follower
            sd_retweet = pstdev(only_value_retweet)
            sd_follower = pstdev(only_value_follower)

            # for j in range(0, len(only_value_follower)):
            #     print(str(only_value_follower[j]) + ", ")

            # print(sum_of_retweet)
            # print(count_reweet)
            # print("Average Retweet:", avg_retweet)

            print("Sum Follower:", sum_of_follower)
            print("Sum Retweet:", sum_of_retweet)
            print("N: ", count_follower)
            print("Average Follower:", avg_follower)
            print("Average Retweet:", avg_retweet)

            """
            PLEASE CHECK (sd)
            https://www.easycalculation.com/statistics/standard-deviation.php
            OK
            """
            # print(sd_retweet)
            print("Standard Variable Follower:", sd_follower)
            print("Standard Variable Retweet:", sd_retweet)

            new_scale_retweet = []
            new_scale_follower = []

            print(len(only_value_retweet))
            print(count_reweet)

            for i in range(0, len(only_value_retweet)):
                print(only_value_retweet[i])
                new_scale_retweet[i] = float((only_value_retweet[i] - avg_retweet) / (sd_retweet * count_reweet))
                print(new_scale_retweet[i])

            print(only_value_retweet)
            print(new_scale_retweet)