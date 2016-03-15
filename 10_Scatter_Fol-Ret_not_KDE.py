"""
Scatter Plot
    - Remove Outlier
        x- Delta_Follower - Delta_Retweet
        x- Log(Delta_Follower) - Delta_Retweet
        - Delta_Follower - Log(Delta_Retweet)
        x- Log(Delta_Follower) - Log(Delta_Retweet)
    - NOT Remove Outlier
        - Delta_Follower - Delta_Retweet
        - Log(Delta_Follower) - Delta_Retweet
        - Delta_Follower - Log(Delta_Retweet)
        - Log(Delta_Follower) - Log(Delta_Retweet)

Coefficient of Correlation
    - Average Pearson Correlation (In each topic)
    - Average Spearman Correlation (In each topic)
"""


import fileinput
import math
import matplotlib.pyplot as plt
import scipy.stats as scs


def extract_diff_ret_or_fol(source_path_param, choose_str, is_log_delta_retweet_param, is_log_delta_follower_param, log_base):
    list1 = []
    for line in fileinput.input([source_path_param], openhook=fileinput.hook_encoded("utf8")):
        if choose_str == 'retweet':
            diff_ret = line.split(',')[3]
            dot_index = diff_ret.find(".")
            diff_ret_int = int(diff_ret[0:dot_index])
            if is_log_delta_retweet_param:  # Log
                if diff_ret_int > 0:
                    diff_ret_log = math.log(diff_ret_int, log_base)
                    list1.append(diff_ret_log)
                else:
                    list1.append(0.0)
            else:
                list1.append(diff_ret_int)  # Normal

        elif choose_str == 'follower w/t mc':
            diff_fol = float(line.split(',')[10])
            if is_log_delta_follower_param:  # Log
                if diff_fol > 0:
                    diff_fol_log = math.log(diff_fol, log_base)
                    list1.append(diff_fol_log)
                else:
                    list1.append(0.0)
            else:
                list1.append(diff_fol)  # Normal

        elif choose_str == 'follower w/o mc':
            diff_fol = float(line.split(',')[13])
            if is_log_delta_follower_param:  # Log
                if diff_fol > 0:
                    diff_fol_log = math.log(diff_fol, log_base)
                    list1.append(diff_fol_log)
                else:
                    list1.append(0.0)
            else:
                list1.append(diff_fol)  # Normal

    fileinput.close()
    return list1


def plot_diff_ret_and_diff_fol(list_ret, list_fol, choose_str, topic_name, fold_num, is_log_delta_retweet_param, is_log_delta_follower_param, is_limit_axis_param, max_fol, max_ret, min_fol, min_ret):
    plt.plot(list_ret, list_fol, 'ro')
    if is_limit_axis_param:
        plt.axis([min_ret, max_ret, min_fol, max_fol])
    else:  # Default
        plt.axis([min(list_ret), max(list_ret), min(list_fol), max(list_fol)])
    # plt.axis('tight')
    if is_log_delta_retweet_param and is_log_delta_follower_param:
        plt.xlabel('Log(Delta Retweet)')
        if choose_str == 'follower w/t mc':
            plt.ylabel('Log(Delta Follower with Message Count)')
            plt.title('Graph of Log(Delta Retweet) and Log(Delta Follower(with Message Count)) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
        elif choose_str == 'follower w/o mc':
            plt.ylabel('Log(Delta Follower without Message Count)')
            plt.title('Graph of Log(Delta Retweet) and Log(Delta Follower(without Message Count)) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')

    elif is_log_delta_retweet_param:
        plt.xlabel('Log(Delta Retweet)')
        if choose_str == 'follower w/t mc':
            plt.ylabel('Delta Follower with Message Count')
            plt.title('Graph of Log(Delta Retweet) and Delta Follower(with Message Count) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
        elif choose_str == 'follower w/o mc':
            plt.ylabel('Delta Follower without Message Count')
            plt.title('Graph of Log(Delta Retweet) and Delta Follower(without Message Count) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')

    elif is_log_delta_follower_param:
        plt.xlabel('Delta Retweet')
        if choose_str == 'follower w/t mc':
            plt.ylabel('Log(Delta Follower with Message Count)')
            plt.title('Graph of Delta Retweet and Log(Delta Follower(with Message Count)) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
        elif choose_str == 'follower w/o mc':
            plt.ylabel('Log(Delta Follower without Message Count)')
            plt.title('Graph of Delta Retweet and Log(Delta Follower(without Message Count)) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')

    else:
        plt.xlabel('Delta Retweet')
        if choose_str == 'follower w/t mc':
            plt.ylabel('Delta Follower with Message Count')
            plt.title('Graph of Delta Retweet and Delta Follower(with Message Count) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
        elif choose_str == 'follower w/o mc':
            plt.ylabel('Delta Follower without Message Count')
            plt.title('Graph of Delta Retweet and Delta Follower(without Message Count) [Topic: ' + topic_name + ', Fold: ' + fold_num + ']')
    plt.show()


def remove_more_than_y(list_ret, list_fol, list_outlier, topic_name, fold_num):
    topic_cal = 0   # 0 1 2 3
    fold_cal = 0    # 0 1 2 3 4

    if topic_name == 'apple':
        topic_cal = 0
    elif topic_name == 'aroii':
        topic_cal = 1
    elif topic_name == 'hormonestheseries':
        topic_cal = 2
    elif topic_name == 'thefacethailand':
        topic_cal = 3

    if fold_num == '1':
        fold_cal = 0
    elif fold_num == '2':
        fold_cal = 1
    elif fold_num == '3':
        fold_cal = 2
    elif fold_num == '4':
        fold_cal = 3
    elif fold_num == '5':
        fold_cal = 4

    for k in range(0, 4):  # k = 0 1 2 3 (Top Bottom Left Right)
        # print(list_outlier[(20 * topic_cal) + (4 * fold_cal) + k])

        want_to_pop = []
        if k == 0:
            if list_outlier[(20 * topic_cal) + (4 * fold_cal) + k] != '-':
                for loop in range(0, len(list_fol)):
                    if list_fol[loop] > float(list_outlier[(20 * topic_cal) + (4 * fold_cal) + k]):  # value > +y
                        want_to_pop.append(loop)

                count_outlier = 0
                for pop_at in want_to_pop:
                    list_fol.pop(pop_at - count_outlier)
                    list_ret.pop(pop_at - count_outlier)
                    count_outlier += 1

        elif k == 1:
            if list_outlier[(20 * topic_cal) + (4 * fold_cal) + k] != '-':
                for loop in range(0, len(list_fol)):
                    if list_fol[loop] < float(list_outlier[(20 * topic_cal) + (4 * fold_cal) + k]):  # value < -y
                        want_to_pop.append(loop)

                count_outlier = 0
                for pop_at in want_to_pop:
                    list_fol.pop(pop_at - count_outlier)
                    list_ret.pop(pop_at - count_outlier)
                    count_outlier += 1

        elif k == 2:
            if list_outlier[(20 * topic_cal) + (4 * fold_cal) + k] != '-':
                for loop in range(0, len(list_ret)):
                    if list_ret[loop] < float(list_outlier[(20 * topic_cal) + (4 * fold_cal) + k]):  # value < -x
                        want_to_pop.append(loop)

                count_outlier = 0
                for pop_at in want_to_pop:
                    list_fol.pop(pop_at - count_outlier)
                    list_ret.pop(pop_at - count_outlier)
                    count_outlier += 1

        elif k == 3:
            if list_outlier[(20 * topic_cal) + (4 * fold_cal) + k] != '-':
                for loop in range(0, len(list_ret)):
                    if list_ret[loop] > float(list_outlier[(20 * topic_cal) + (4 * fold_cal) + k]):  # value > x
                        want_to_pop.append(loop)

                count_outlier = 0
                for pop_at in want_to_pop:
                    list_fol.pop(pop_at - count_outlier)
                    list_ret.pop(pop_at - count_outlier)
                    count_outlier += 1

    return list_ret, list_fol


def explore_diff_ret(list_diff_ret_param, list_diff_fol_param, not_more_than_param):
    count_ret = 0
    outlier_list = []
    outlier_dict = {}
    for i in range(0, len(list_diff_ret_param)):
        if list_diff_ret_param[i] >= not_more_than_param:
            count_ret += 1
            outlier_dict[i] = list_diff_ret_param[i]
            outlier_list.append(list_diff_ret_param[i])
            # print(list_diff_ret_param[i])

    print("Max Delta_Follower:", max(list_diff_fol_param))
    print("Max Delta_Retweet:", max(list_diff_ret_param))
    print("Length of list:", len(list_diff_ret_param))
    print("More than", not_more_than_param, ":", count_ret)
    if len(outlier_list) > 0:
        print("lowwest", min(outlier_list))
    print(len(outlier_dict))
    print(outlier_dict)
    return


# SET PARAMETER
# follower_choices = ['follower w/t mc', 'follower w/o mc']
follower_choices = ['follower w/o mc']
topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
# topics = ["thefacethailand"]
folds = ["1", "2", "3", "4", "5"]
# folds = ["5"]

# is_log_delta_retweet = False
# is_log_delta_follower = True
# is_log_delta_retweet = True
# is_log_delta_follower = False
is_log_delta_retweet = True
is_log_delta_follower = True
logarithm_base_num = 2

max_ret_plot = 1280
min_ret_plot = -5
max_fol_plot = 10
min_fol_plot = -1
is_limit_axis = False


"""
Top(Delta_Follower), Bottom(Delta_Follower), Left(Delta_Retweet), Right(Delta_Retweet)
"""
is_remove_outlier = True
# not_more_than = 580

remove_outlier_both_log = ['-', '-', '-', '-',  # Apple 1
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',  # Aroii 1
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',  # Hormones 1
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',  # TheFace 1
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',
                           '-', '-', '-', '-',
                           '-', '-', '-', '-']

remove_outlier_log_fol = ['7.34', '-', '-', '580',  # Apple 1
                          '7', '-', '-', '300',
                          '-', '-', '-', '240',
                          '6.3', '-', '-', '340',
                          '5.7', '-', '-', '650',
                          '-', '-', '-', '640',  # Aroii 1
                          '7.4', '-', '-', '730',
                          '6.3', '-', '-', '540',
                          '7', '-', '-', '610',
                          '6.5', '-', '-2.5', '590',
                          '6', '-', '-10', '570',  # Hormones 1
                          '-', '-', '-5', '730',
                          '8', '-', '-5', '670',
                          '-', '-', '-5', '715',
                          '-', '-', '-', '780',
                          '7.2', '-', '-', '900',  # TheFace 1
                          '7', '-', '-5', '820',
                          '7.9', '-', '-5', '1360',
                          '7', '-', '-', '800',
                          '7.4', '-', '-5', '1180']

remove_outlier_log_ret = ['170', '-', '-', '10.3',  # Apple 1
                          '130', '-10', '-', '10',
                          '199', '-', '-', '9',
                          '70', '-5', '-', '8.5',
                          '50.5', '-', '-', '10.5',
                          '87', '-5', '-', '10.1',  # Aroii 1
                          '170', '-5', '-', '10.2',
                          '72', '-', '-', '9.7',
                          '107', '-', '-', '9.8',
                          '110', '-', '-', '10',
                          '140', '-10', '-', '10.5',  # Hormones 1
                          '115', '-16.1', '-', '10.3',
                          '300', '-', '-', '11.8',
                          '-', '-10', '-', '10.7',
                          '240', '-', '-', '10.9',
                          '153', '-14', '-', '-',  # TheFace 1
                          '118', '-', '-', '10.63',
                          '265', '-', '-', '10.8',
                          '175', '-', '-', '10.4',
                          '250', '-', '-', '11']

# not_remove_outlier = ['-', '-', '-', '-',  # Apple 1
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',  # Aroii 1
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',  # Hormones 1
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',  # TheFace 1
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-',
#                       '-', '-', '-', '-']


for each_choice in follower_choices:
    for each_topic in topics:
        print(each_topic)
        pearson_5_folds_result = []
        pearson_5_folds_p = []
        spearman_5_folds_result = []
        spearman_5_folds_p = []
        pearson_5_folds_result_not_rm_outlier = []
        spearman_5_folds_result_not_rm_outlier = []

        for each_fold in folds:
            source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/" + each_topic + "/fold_" + each_fold + "/all_tweet.csv"

            list_diff_ret = extract_diff_ret_or_fol(source_path, 'retweet', is_log_delta_retweet, is_log_delta_follower, logarithm_base_num)
            list_diff_fol = extract_diff_ret_or_fol(source_path, each_choice, is_log_delta_retweet, is_log_delta_follower, logarithm_base_num)
            new_list_diff_ret = []
            new_list_diff_fol = []

            """
            Explore List of Delta_Retweet
            """
            explore_diff_ret(list_diff_ret, list_diff_fol, max_ret_plot)

            """
            Print info
            """
            # print("============ Topic: " + each_topic + ", Fold: " + each_fold + ", " + each_choice + " =============")
            # print("Log Delta Retweet:  " + str(is_log_delta_retweet))
            # print("Log Delta Follower: " + str(is_log_delta_follower))
            # if is_log_delta_follower or is_log_delta_retweet:
            #     print("Logarithm Base Number: " + str(logarithm_base_num))
            # print("Max of Delta retweet  -> " + str(max(list_diff_ret)))
            # print("Max of Delta follower -> " + str(max(list_diff_fol)))
            # print("Min of Delta retweet  -> " + str(min(list_diff_ret)))
            # print("Min of Delta follower -> " + str(min(list_diff_fol)))
            # print(scs.pearsonr(list_diff_ret, list_diff_fol))
            # print(scs.spearmanr(list_diff_ret, list_diff_fol))
            # print(len(list_diff_fol), len(list_diff_ret))

            """
            Scatter Plot (NOT Remove Outlier)
            """
            not_rm_outlier_diff_ret = list(list_diff_ret)
            not_rm_outlier_diff_fol = list(list_diff_fol)
            plot_diff_ret_and_diff_fol(list_diff_ret, list_diff_fol, each_choice, each_topic, each_fold, is_log_delta_retweet, is_log_delta_follower, is_limit_axis, max_fol_plot, max_ret_plot, min_fol_plot, min_ret_plot)

            """
            Scatter Plot (Remove Outlier)
            """
            if is_log_delta_retweet is True and is_log_delta_follower is False:
                new_list_diff_ret, new_list_diff_fol = remove_more_than_y(list_diff_ret, list_diff_fol, remove_outlier_log_ret, each_topic, each_fold)
            elif is_log_delta_retweet is False and is_log_delta_follower is True:
                new_list_diff_ret, new_list_diff_fol = remove_more_than_y(list_diff_ret, list_diff_fol, remove_outlier_log_fol, each_topic, each_fold)
            elif is_log_delta_retweet and is_log_delta_follower:
                new_list_diff_ret, new_list_diff_fol = remove_more_than_y(list_diff_ret, list_diff_fol, remove_outlier_both_log, each_topic, each_fold)
            plot_diff_ret_and_diff_fol(new_list_diff_ret, new_list_diff_fol, each_choice, each_topic, each_fold, is_log_delta_retweet, is_log_delta_follower, is_limit_axis, max_fol_plot, max_ret_plot, min_fol_plot, min_ret_plot)

            """
            Coefficient of Correlation
            """
            # print(scs.pearsonr(list_diff_ret, list_diff_fol)[0])
            # print(scs.spearmanr(list_diff_ret, list_diff_fol))
            # print(len(list_diff_fol), len(list_diff_ret))
            pearson_5_folds_result.append(scs.pearsonr(list_diff_ret, list_diff_fol)[0])
            spearman_5_folds_result.append(scs.spearmanr(list_diff_ret, list_diff_fol).correlation)
            pearson_5_folds_result_not_rm_outlier.append(scs.pearsonr(not_rm_outlier_diff_ret, not_rm_outlier_diff_fol)[0])
            spearman_5_folds_result_not_rm_outlier.append(scs.spearmanr(not_rm_outlier_diff_ret, not_rm_outlier_diff_fol).correlation)

            """
            Print Note Outlier
            """
            # print("Top      :")
            # print("Bottom   :")
            # print("Left     :")
            # print("Right    :")

        """
        Average Pearson (In each topic)
        """
        # sum_pearson = 0
        # sum_pearson_not_rm_outlier = 0
        #
        # for each_pearson in pearson_5_folds_result:
        #     sum_pearson += each_pearson
        # avg_pearson = sum_pearson / len(folds)
        #
        # for each_pearson_not_rm_outlierult in pearson_5_folds_result_not_rm_outlier:
        #     sum_pearson_not_rm_outlier += each_pearson_not_rm_outlierult
        # avg_pearson_not_rm_outlier = sum_pearson_not_rm_outlier / len(folds)
        #
        # print("====== Pearson ======")
        # print("Before Remove Outlier")
        # print(pearson_5_folds_result_not_rm_outlier)
        # print(avg_pearson_not_rm_outlier)
        # print("After Remove Outlier")
        # print(pearson_5_folds_result)
        # print(avg_pearson)

        """
        Average Spearman (In each topic)
        """
        # sum_spearman = 0
        # sum_spearman_not_rm_outlier = 0
        #
        # for each_spearman in spearman_5_folds_result:
        #     sum_spearman += each_spearman
        # avg_spearman = sum_spearman / len(folds)
        #
        # for each_spearman_not_rm_outlier in spearman_5_folds_result_not_rm_outlier:
        #     sum_spearman_not_rm_outlier += each_spearman_not_rm_outlier
        # avg_spearman_not_rm_outlier = sum_spearman_not_rm_outlier / len(folds)
        #
        # print("====== Spearman ======")
        # print("Before Remove Outlier")
        # # print(spearman_5_folds_result_not_rm_outlier)
        # print(avg_spearman_not_rm_outlier)
        # print("After Remove Outlier")
        # # print(spearman_5_folds_result)
        # print(avg_spearman)
        # print("==============================")
