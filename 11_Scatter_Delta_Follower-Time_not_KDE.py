import fileinput
import math
import matplotlib.pyplot as plt


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

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! START EDIT HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! END EDIT HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    fileinput.close()
    return list1


def plot_diff_fol_and_time(list_fol, choose_str, topic_name, fold_num, is_log_delta_follower_param):
    plt.plot(list_fol, hour, 'ro')
    plt.axis([min(list_fol), max(list_fol), 0, 1660])
    # plt.axis('tight')
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
topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
# folds = ["1", "2", "3", "4", "5"]
folds = ["2", "3", "4", "5"]
# is_log_delta_retweet = True
is_log_delta_follower = True
logarithm_base_num = 10

for each_choice in follower_choices:
    for each_topic in topics:
        for each_fold in folds:
            source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/" + each_topic + "/fold_" + each_fold + "/all_tweet.csv"

            list_diff_fol = extract_diff_ret_or_fol(source_path, each_choice, is_log_delta_follower, logarithm_base_num)

            print("============ Topic: " + each_topic + ", Fold: " + each_fold + ", " + each_choice + " =============")
            print("Log Delta Follower: " + str(is_log_delta_follower))
            if is_log_delta_follower:
                print("Logarithm Base Number: " + str(logarithm_base_num))
            print("Max of Delta follower -> " + str(max(list_diff_fol)))
            print("Min of Delta follower -> " + str(min(list_diff_fol)))

            plot_diff_fol_and_time(list_diff_fol, each_choice, each_topic, each_fold, is_log_delta_follower)
