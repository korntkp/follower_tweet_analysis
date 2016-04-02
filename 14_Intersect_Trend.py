import fileinput
from math import *
from statistics import *
import matplotlib.pyplot as plt
from scipy import *
from scipy.integrate import simps
from numpy import trapz


def read_csv_file(source_path_param):
    list1 = []
    for line in fileinput.input([source_path_param], openhook=fileinput.hook_encoded("utf8")):
        new_line_index = line.find('\n')
        # print(new_line_index)
        list1.append(line[:new_line_index])
    fileinput.close()
    return list1


def one_plot_before(before_scale_retweet, before_scale_follower, topic_name, fold_num, each_choice_param):
    fig, ax = plt.subplots()
    # print(each_choice_param)
    axes = plt.gca()
    axes.set_xlim([0, len(before_scale_retweet)])

    if each_choice_param == 'follower_wo_mc':
        print("Plot Trend Decomposition (Delta Follower)")
        ax.plot(range(0, len(before_scale_follower)), before_scale_follower, '-', label='Trend Delta Follower')
        ax.set_ylabel('Trend Decomposition (Delta Follower)')
        ax.set_title('Trend Decomposition (Delta Follower) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
        axes.set_ylim([0, 4])
    else:
        print("Plot Trend Decomposition (Delta Retweet)")
        ax.plot(range(0, len(before_scale_retweet)), before_scale_retweet, '-', label='Trend Delta Retweet')
        ax.set_ylabel('Trend Decomposition (Delta Retweet)')
        ax.set_title('Trend Decomposition (Delta Retweet) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
        axes.set_ylim([0, 20])
        # axes.set_ylim([0, max(before_scale_retweet)])

    ax.set_xlabel("Time (Hour)")
    axes.legend(loc='upper right')

    plt.show()
    return


def two_plot_before(before_scale_retweet, before_scale_follower, topic_name, fold_num):
    fig, ax = plt.subplots()

    ax.plot(range(0, len(before_scale_retweet)), before_scale_retweet, '-', label='Trend Delta Retweet')
    ax.plot(range(0, len(before_scale_follower)), before_scale_follower, '-', label='Trend Delta Follower')

    ax.set_xlabel("Time (Hour)")
    ax.set_ylabel('Trend Value Before Scaling')
    ax.set_title('Trend Graph (Before Scaling) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')

    axes = plt.gca()
    axes.set_xlim([0, len(before_scale_retweet)])
    axes.legend(loc='upper right')

    plt.show()
    return


def two_plot_after(after_scale_retweet, after_scale_follower, topic_name, fold_num, shade_option):
    # print("dfgjhjtrter")
    fig, ax = plt.subplots()

    ax.plot(range(0, len(after_scale_retweet)), after_scale_retweet, '-', linewidth=0.8, color='green', label='Trend Delta Retweet')
    ax.plot(range(0, len(after_scale_follower)), after_scale_follower, '-', linewidth=3.5, color='black', label='Trend Delta Follower')
    """
    shade_option = ['none', 'Union', 'Non-Intersect', 'Intersect']
    """
    if shade_option == 'Union':
        print("Union")
        ax.fill_between(range(0, 1), 0, facecolor='black', alpha=0.5, label='Union Area')    # Manual Fill Color
    elif shade_option == 'Non-Intersect':
        print("Non-Intersect")
        ax.fill_between(range(0, 1), 0, facecolor='black', alpha=0.5, label='Non Intersect Area')    # Manual Fill Color
    elif shade_option == 'Intersect':
        print("Intersect")
        ax.fill_between(range(0, 1), 0, facecolor='black', alpha=0.5, label='Intersect Area')    # Manual Fill Color
    else:
        print("none")

    ax.set_xlabel("Time (Hour)")
    ax.set_ylabel('Trend Value After Scaling')
    ax.set_title('Trend Graph (After Scaling) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')

    axes = plt.gca()
    axes.set_xlim([0, len(after_scale_retweet)])
    axes.legend(loc='upper right')
    plt.axhline(0, color='Black')
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

"""
REWRITE THIS
"""
def plot_union(union_list, after_scale_retweet, after_scale_follower, topic_name, fold_num, plus_list, minus_list):
    # print(after_scale_retweet[970], after_scale_follower[970])
    # print(union_list[970])
    fig, ax = plt.subplots()

    ax.plot(range(0, len(after_scale_retweet)), after_scale_retweet, '-', label='Trend Delta Retweet')
    ax.plot(range(0, len(after_scale_follower)), after_scale_follower, '-', label='Trend Delta Follower')
    # ax.fill_between(range(0, len(union_list)), 0, union_list, facecolor='black', alpha=0.5, label='Union Area')
    ax.fill_between(range(0, 1), 0, facecolor='black', alpha=0.5, label='Intersection Area')                # Manual Fill Color
    # ax.fill_between(range(0, len(plus_list)), 0, plus_list, facecolor='black', alpha=0.5)
    # ax.fill_between(range(0, len(minus_list)), 0, minus_list, facecolor='black', alpha=0.5)


    ax.set_xlabel("Time")
    ax.set_ylabel('Trend Value After Scaling')
    ax.set_title('Trend Graph (After Scaling) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')

    axes = plt.gca()
    axes.set_xlim([0, len(after_scale_retweet)])
    axes.legend(loc='upper right')

    plt.axhline(0, color='Black')
    plt.show()
    return


# y_axis_choices = ['follower_wo_mc']
y_axis_choices = ['retweet']
# topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
topics = ["hormonestheseries"]
# folds = ["1", "2", "3", "4", "5"]
folds = ["1", "2", "3"]

shade_area_num_param = 0
shade_area = ['none', 'Union', 'Non-Intersect', 'Intersect']

for each_choice in y_axis_choices:
    for each_topic in topics:
        simi_topic = []
        for each_fold in folds:

            # print("=========== Topic: " + each_topic + ", Fold: " + each_fold + ", " + each_choice + " ============")
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

            for i in range(0, len(only_value_retweet)):
                new_scale_retweet.append(float((only_value_retweet[i] - avg_retweet) / (sd_retweet * sqrt(count_retweet))))
                new_scale_follower.append(float((only_value_follower[i] - avg_follower) / (sd_follower * sqrt(count_follower))))

                # new_scale_retweet.append(float((only_value_retweet[i] - avg_retweet) / (sd_retweet)))
                # new_scale_follower.append(float((only_value_follower[i] - avg_follower) / (sd_follower)))

                # new_scale_retweet.append((only_value_retweet[i] - avg_retweet) / (sd_retweet * count_retweet))
                # new_scale_follower.append((only_value_follower[i] - avg_follower) / (sd_follower * count_follower))

            """
            Find Diff from y axis == 0 (Intersection)
            I Think it ok
            """
            # print("start")
            non_intersection_area = []
            for i in range(0, len(new_scale_follower)):
                temp_abs_diff = new_scale_follower[i] - new_scale_retweet[i]
                if temp_abs_diff < 0:
                    temp_abs_diff *= -1
                non_intersection_area.append(temp_abs_diff)
                # print("Time:", i)
                # print(new_scale_follower[i], new_scale_retweet[i])
                # print(non_intersection_area[i])
            # print(non_intersection_area)

            """
            Find Union Area
            """
            union_area = []
            for_plot_union_area = []
            for_plot_union_area_plus = []
            for_plot_union_area_minus = []
            for i in range(0, len(new_scale_follower)):
                if new_scale_retweet[i] >= 0 and new_scale_follower[i] >= 0:    # + +
                    if new_scale_retweet[i] > new_scale_follower[i]:            # get max
                        union_area.append(new_scale_retweet[i])
                        for_plot_union_area.append(new_scale_retweet[i])
                        for_plot_union_area_plus.append(0)
                        for_plot_union_area_minus.append(0)
                    else:
                        union_area.append(new_scale_follower[i])
                        for_plot_union_area.append(new_scale_follower[i])
                        for_plot_union_area_plus.append(0)
                        for_plot_union_area_minus.append(0)
                elif new_scale_retweet[i] < 0 and new_scale_follower[i] < 0:       # - -
                    if new_scale_retweet[i] < new_scale_follower[i]:                # get |-max|
                        union_area.append(-1 * new_scale_retweet[i])
                        for_plot_union_area.append(new_scale_retweet[i])
                        for_plot_union_area_plus.append(0)
                        for_plot_union_area_minus.append(0)
                    else:
                        union_area.append(-1 * new_scale_follower[i])
                        for_plot_union_area.append(new_scale_follower[i])
                        for_plot_union_area_plus.append(0)
                        for_plot_union_area_minus.append(0)
                else:                                                              # + -, - +
                    temp_abs_diff = new_scale_follower[i] - new_scale_retweet[i]    # find + -> -
                    if temp_abs_diff < 0:
                        temp_abs_diff *= -1
                    union_area.append(temp_abs_diff)
                    # for_plot_union_area.append(temp_abs_diff)
                    if temp_abs_diff < 0:
                        for_plot_union_area.append(0)
                        for_plot_union_area_plus.append(new_scale_follower[i])
                        for_plot_union_area_minus.append(new_scale_retweet[i])
                    else:
                        for_plot_union_area.append(0)
                        for_plot_union_area_plus.append(new_scale_follower[i])
                        for_plot_union_area_minus.append(new_scale_retweet[i])

            sum_non_intersect_area = sum(non_intersection_area)
            sum_union_area = sum(union_area)
            sum_plot_union = sum(for_plot_union_area) + sum(for_plot_union_area_plus) + sum(for_plot_union_area_minus)
            un_similar = (sum_non_intersect_area / sum_union_area) * 100
            similarity_result = 100 - un_similar


            # print("Not Intersect Area:", sum_non_intersect_area)
            # print("Union Area:", sum_union_area)
            # print("Not Intersect Area / Union Area:", un_similar)
            # print("Similarity:", similarity_result)
            # print(similarity_result)
            simi_topic.append(similarity_result)

            """
            Plot Graph
            """
            # print("Plot Before")
            # print("Plot After")
            # one_plot_before(only_value_retweet, only_value_follower, each_topic, each_fold, each_choice)
            # two_plot_before(only_value_retweet, only_value_follower, each_topic, each_fold)
            two_plot_after(new_scale_retweet, new_scale_follower, each_topic, each_fold, shade_area[shade_area_num_param])        # THIS
            # plot_union(for_plot_union_area, new_scale_retweet, new_scale_follower, each_topic, each_fold, for_plot_union_area_plus, for_plot_union_area_minus)
            # four_plot(only_value_retweet, new_scale_retweet, only_value_follower, new_scale_follower, 'follower_wo_mc', each_topic, each_fold)

            """
            Print Info
            """
            # print("Sum Follower:", sum_of_follower)
            # print("Sum Retweet:", sum_of_retweet)
            # print("N Follower: ", count_follower)
            # print("N Retweet: ", count_retweet)
            # print("Average Follower:", avg_follower)
            # print("Average Retweet:", avg_retweet)
            # print("Standard Variable Follower:", sd_follower)
            # print("Standard Variable Retweet:", sd_retweet)

            """
            Print Trend Value
            """
            # print("Trend Value Retweet Before Scale:", only_value_retweet)
            # print("Trend Value Retweet After Scale:", new_scale_retweet)
            # print("Trend Value Follower Before Scale:", only_value_follower)
            # print("Trend Value Follower After Scale:", new_scale_follower)
            # print("Trend Value Retweet Before Scale:", len(only_value_retweet))
            # print("Trend Value Retweet After Scale:", len(new_scale_retweet))
            # print("Trend Value Follower Before Scale:", len(only_value_follower))
            # print("Trend Value Follower After Scale:", len(new_scale_follower))

            # """
            # Unused Code
            # """
            # """
            # Manual Standard Deviation (Unused)
            # """
            # sum_sqr_retweet = 0
            # for i in range(0, len(only_value_retweet)):
            #     sum_sqr_retweet += (only_value_retweet[i] - avg_retweet) * (only_value_retweet[i] - avg_retweet)
            # sd_retweet_manual = sqrt(sum_sqr_retweet / count_retweet)
            # sum_sqr_follower = 0
            # for i in range(0, len(only_value_follower)):
            #     sum_sqr_follower += (only_value_follower[i] - avg_follower) * (only_value_follower[i] - avg_follower)
            # sd_follower_manual = sqrt(sum_sqr_follower / count_follower)
            # """
            # Find The Lowest Trend Value
            # """
            # lowest_trend_ret = min(new_scale_retweet)
            # lowest_trend_fol = min(new_scale_follower)
            # # print(max(new_scale_retweet))
            # # print(max(new_scale_follower))
            # if lowest_trend_ret < lowest_trend_fol:
            #     lowest_trend_ret_fol = lowest_trend_ret
            # else:
            #     lowest_trend_ret_fol = lowest_trend_fol
            # # print("The Lowest of Retweet", lowest_trend_ret)
            # # print("The Lowest of Follower", lowest_trend_fol)
            # # print("The Lowest of Retweet and Follower", lowest_trend_ret_fol)
            # # print("The Lowest of Retweet and Follower, %.45f" % lowest_trend_ret_fol)
            #
            # """
            # Find Diff from The Lowest
            # """
            # # print("index 0:", new_scale_follower[0])
            # # print(new_scale_follower[0] - lowest_trend_ret_fol)
            # # print(min(new_scale_retweet))
            # # print(min(new_scale_follower))
            # print(new_scale_retweet)
            # print(new_scale_follower)
            #
            # diff_from_lowest_retweet = []
            # diff_from_lowest_follower = []
            # sum_area_retweet = 0
            # sum_area_follower = 0
            # for i in range(0, len(new_scale_retweet)):
            #     temp_diff_retweet = new_scale_retweet[i] - lowest_trend_ret_fol
            #     temp_diff_follower = new_scale_follower[i] - lowest_trend_ret_fol
            #
            #     diff_from_lowest_retweet.append(temp_diff_retweet)
            #     diff_from_lowest_follower.append(temp_diff_follower)
            #
            #     sum_area_retweet += diff_from_lowest_retweet[i]
            #     sum_area_follower += diff_from_lowest_follower[i]
            #
            # print(sum(new_scale_retweet))
            # # print(sum(new_scale_follower))
            # print(sum_area_retweet)
            #
            # """
            # Find Area by Library
            # """
            # # print(simps(new_scale_retweet))
            # # print(simps(new_scale_follower))
            # # print(trapz(new_scale_retweet))
            # # print(trapz(new_scale_follower))
            # sum_area_a_and_b = sum_area_retweet + sum_area_follower
            # # print(sum_area_a_and_b)
            #
            # intersect_area = []
            # for i in range(0, len(new_scale_retweet)):
            #     if new_scale_retweet[i] < new_scale_follower[i]:
            #         # temp_intersect = new_scale_retweet[i] - lowest_trend_ret_fol
            #         temp_intersect = new_scale_retweet[i]
            #         intersect_area.append(temp_intersect)
            #     else:
            #         # temp_intersect = new_scale_follower[i] - lowest_trend_ret_fol
            #         temp_intersect = new_scale_follower[i]
            #         intersect_area.append(temp_intersect)
            # # print(sum(intersect_area))
            # # print(len(intersect_area))
            # # print(mean(intersect_area))
            # # print(sum(intersect_area) / len(intersect_area))
            #
            #
            # # print(intersect_area)
            # result = (sum(intersect_area) / sum_area_a_and_b) * 200
            # print("Intersect Area", each_topic, "Fold", each_fold + ":", result)
            #
            # intersect_area_for_plot = []
            # for i in range(0, len(intersect_area)):
            #     # temp_new_intersect = intersect_area[i] + lowest_trend_ret_fol
            #     temp_new_intersect = intersect_area[i]
            #     intersect_area_for_plot.append(temp_new_intersect)
            # # print(intersect_area_for_plot)
            #
            # """
            # Print info
            # """
            # # print(diff_from_lowest_retweet)
            # # print(min(diff_from_lowest_retweet))
            # # print(min(diff_from_lowest_follower))
            # # print(max(diff_from_lowest_retweet))
            # # print(max(diff_from_lowest_follower))
            # # print(diff_from_lowest_follower)
            # # print("%.45f" % mean(diff_from_lowest_retweet))
            # # print("%.45f" % mean(diff_from_lowest_follower))
            # # # print(diff_from_lowest_retweet)
            # # # print(diff_from_lowest_follower)
            # # print("%.45f" % sum_area_retweet)
            # # print("%.45f" % sum_area_follower)
            # # print("%.45f" % (sum_area_retweet - sum_area_follower))
            # def intersect_plot(intersect_list, after_scale_retweet, after_scale_follower, topic_name, fold_num, lowest_y):
            #     # print("dfgjhjtrter")
            #     fig, ax = plt.subplots()
            #
            #     ax.plot(range(0, len(after_scale_retweet)), after_scale_retweet, '-', label='Trend Delta Retweet')
            #     ax.plot(range(0, len(after_scale_follower)), after_scale_follower, '-', label='Trend Delta Follower')
            #     ax.fill_between(range(0, len(intersect_list)), 0, intersect_list, facecolor='black', alpha=0.5, label='Intersect Area')
            #
            #     ax.set_xlabel("Time")
            #     ax.set_ylabel('Trend Value After Scaling')
            #     ax.set_title('Trend Graph (After Scaling) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
            #
            #     axes = plt.gca()
            #     axes.set_xlim([0, len(after_scale_retweet)])
            #     axes.legend(loc='upper right')
            #
            #     plt.show()
            #     return
            # intersect_plot(intersect_area_for_plot, new_scale_retweet, new_scale_follower, each_topic, each_fold, lowest_trend_ret_fol)
        sum_simi_topic = sum(simi_topic)
        # print("Standard Deviation: %0.5f" % pstdev(simi_topic))
        # print("%0.5f" % pstdev(simi_topic))
        # print(pstdev(simi_topic))
        # print("Avg:", sum_simi_topic / len(folds))
