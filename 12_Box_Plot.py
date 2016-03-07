import fileinput
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

        elif choose_str == 'follower w/t mc':
            diff_fol = float(line.split(',')[10])
            list1.append(diff_fol)  # Normal

        elif choose_str == 'follower w/o mc':
            diff_fol = float(line.split(',')[13])
            list1.append(diff_fol)  # Normal
    fileinput.close()
    return list1


def write_date_date_csv(output_path, list_diff_ret_param, list_diff_fol_param):
    fo = open(output_path, "w")
    for i in range(0, len(list_diff_ret_param)):
        result = str(list_diff_ret_param[i]) + "," + str(list_diff_fol_param[i]) + "\n"
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


# SET PARAMETER
# follower_choices = ['follower w/t mc', 'follower w/o mc']
follower_choices = ['follower w/o mc']
topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
folds = ["1", "2", "3", "4", "5"]
# folds =
for each_choice in follower_choices:
    for each_topic in topics:
        for each_fold in folds:
            print(each_topic, each_fold)

            source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/" + each_topic + "/fold_" + each_fold + "/all_tweet.csv"
            output_follower_csv = "E:/tweet_process/result_follower-ret/09_follower_retweet_csv_for_pandas/" + each_topic + "/fold_" + each_fold + "/all_tweet.csv"

            """
            Read & Write Data
            """
            # list_diff_ret = extract_diff_ret_or_fol(source_path, 'retweet')
            # list_diff_fol = extract_diff_ret_or_fol(source_path, each_choice)
            # write_date_date_csv(output_follower_csv, list_diff_ret, list_diff_fol)
            # print(list_diff_fol)
            # print(list_diff_ret)
            # print("================= End Read & Write Data ==================")

            df_follower = pandas_df(output_follower_csv, each_topic, each_fold)
            print(df_follower)
            df_follower.boxplot()
            plt.show()
