import matplotlib.pyplot as plt


def plot_diff_ret_and_diff_fol(list_ret, list_fol, choose_str, topic_name, fold_num, is_log_delta_retweet_param, is_log_delta_follower_param, is_limit_axis_param, max_fol, max_ret, min_fol, min_ret):
    plt.plot(list_ret, list_fol, 'ro')
    if is_limit_axis_param:
        plt.axis([min_ret, max_ret, min_fol, max_fol])
    else:
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

            source_kde_ret_fol_csv = "E:/tweet_process/result_follower-ret/10_KDE_fol_ret_csv/" + each_topic + "/fold_" + each_fold + "/kde-diff_ret-diff_fol.csv"

            plot_diff_ret_and_diff_fol(list_diff_ret, list_diff_fol, each_choice, each_topic, each_fold, is_log_delta_retweet, is_log_delta_follower, is_limit_axis, max_fol_plot, max_ret_plot, min_fol_plot, min_ret_plot)


