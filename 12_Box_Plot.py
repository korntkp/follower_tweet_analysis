from math import log
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


def normal_boxplot(output_kde_ret_fol_csv_path_param):
    kde_df_ret_fol = pd.read_csv(output_kde_ret_fol_csv_path_param, names=['DeltaRetweet', 'DeltaFollower'])
    kde_df_ret_fol2 = pd.read_csv(output_kde_ret_fol_csv_path_param, names=['DeltaRetweet2', 'DeltaFollower2'])
    print(kde_df_ret_fol)
    plotx = kde_df_ret_fol.boxplot(return_type='both')
    plotx2 = kde_df_ret_fol2.boxplot(return_type='both')
    # plotx = kde_df_ret_fol.boxplot(return_type='both', column='DeltaRetweet')
    # kde_df_ret_fol.plot(title='Delta Retweet - Delta Follower')
    # df_follower.boxplot(by='DeltaRetweet')
    print(plotx)
    plt.title('Delta Retweet - Delta Follower (' + each_topic + ', ' + each_fold + ')')
    axes = plt.gca()
    axes.set_ylim([-10, 80])
    plt.show()


def create_low_medium_high(output_kde_ret_fol_csv_path_param, topic_name, fold_num, is_interpolate_param, is_log_y_axis_param, logarithm_base_num_param):
    topic_cal = 0
    fold_cal = 0
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

    lowwer_bound = float(bound_delta_follower[(10 * topic_cal) + (2 * fold_cal) + 0])
    upper_bound = float(bound_delta_follower[(10 * topic_cal) + (2 * fold_cal) + 1])
    # print(lowwer_bound, upper_bound)

    low_follower_list = []
    medium_follower_list = []
    high_follower_list = []
    dataframe_low_medium_high = []
    kde_df_ret_fol = pd.read_csv(output_kde_ret_fol_csv_path_param, names=['DeltaRetweet', 'DeltaFollower'])
    kde_df_ret_fol_interpolated = kde_df_ret_fol.interpolate().bfill()

    if is_interpolate_param:
        if is_log_y_axis_param:
            # print(kde_df_ret_fol_interpolated.DeltaRetweet)
            for j in range(0, len(kde_df_ret_fol_interpolated)):
                if kde_df_ret_fol_interpolated.DeltaRetweet.values[j] <= 0:
                    kde_df_ret_fol_interpolated.DeltaRetweet.values[j] = np.nan
                kde_df_ret_fol_interpolated.DeltaRetweet.values[j] = math.log(kde_df_ret_fol_interpolated.DeltaRetweet.values[j], logarithm_base_num_param)
            # print(len(kde_df_ret_fol_interpolated))

        for j in range(0, len(kde_df_ret_fol_interpolated)):
            # print(kde_df_ret_fol_interpolated.DeltaFollower.values[j])
            if float(kde_df_ret_fol_interpolated.DeltaFollower.values[j]) <= lowwer_bound:
                low_follower_list.append(kde_df_ret_fol_interpolated.DeltaRetweet.values[j])
                medium_follower_list.append(np.nan)
                high_follower_list.append(np.nan)
            elif lowwer_bound < float(kde_df_ret_fol_interpolated.DeltaFollower.values[j]) <= upper_bound:
                low_follower_list.append(np.nan)
                medium_follower_list.append(kde_df_ret_fol_interpolated.DeltaRetweet.values[j])
                high_follower_list.append(np.nan)
            else:
                low_follower_list.append(np.nan)
                medium_follower_list.append(np.nan)
                high_follower_list.append(kde_df_ret_fol_interpolated.DeltaRetweet.values[j])

        # print(len(high_follower_list))
        combined_data = list(zip(low_follower_list, medium_follower_list, high_follower_list))
        # print(combined_data)

        dataframe_low_medium_high = pd.DataFrame(combined_data, columns=['Low', 'Medium', 'High'])
        # print(dataframe_low_medium_high)

        # df3 = kde_df_ret_fol_interpolated.append(df2, ignore_index=True)
        # print(df3)
        # df3_delete_last = df3.drop(df3.index[[1649]])
        # print(df3_delete_last.DeltaRetweet.values[1649])

    else:
        if is_log_y_axis_param:
            # print(kde_df_ret_fol.DeltaRetweet)
            for j in range(0, len(kde_df_ret_fol)):
                if kde_df_ret_fol.DeltaRetweet.values[j] <= 0:
                    kde_df_ret_fol.DeltaRetweet.values[j] = np.nan
                kde_df_ret_fol.DeltaRetweet.values[j] = math.log(kde_df_ret_fol.DeltaRetweet.values[j], logarithm_base_num_param)
            # print(len(kde_df_ret_fol))
        for j in range(0, len(kde_df_ret_fol)):
            # print(kde_df_ret_fol.DeltaFollower.values[j])
            if float(kde_df_ret_fol.DeltaFollower.values[j]) <= lowwer_bound:
                low_follower_list.append(kde_df_ret_fol.DeltaRetweet.values[j])
                medium_follower_list.append(np.nan)
                high_follower_list.append(np.nan)
            elif lowwer_bound < float(kde_df_ret_fol.DeltaFollower.values[j]) <= upper_bound:
                low_follower_list.append(np.nan)
                medium_follower_list.append(kde_df_ret_fol.DeltaRetweet.values[j])
                high_follower_list.append(np.nan)
            else:
                low_follower_list.append(np.nan)
                medium_follower_list.append(np.nan)
                high_follower_list.append(kde_df_ret_fol.DeltaRetweet.values[j])

        # print(len(high_follower_list))
        combined_data = list(zip(low_follower_list, medium_follower_list, high_follower_list))
        # print(combined_data)

        dataframe_low_medium_high = pd.DataFrame(combined_data, columns=['Low', 'Medium', 'High'])
        # print(dataframe_low_medium_high)

    return dataframe_low_medium_high


def low_medium_high_boxplot_from_df(df_low_medium_high_param, is_log_y_axis_param):
    plotx = df_low_medium_high_param.boxplot(return_type='both')
    # plotx = kde_df_ret_fol.boxplot(return_type='both', column='DeltaRetweet')
    # kde_df_ret_fol.plot(title='Delta Retweet - Delta Follower')
    # df_follower.boxplot(by='DeltaRetweet')
    # print(plotx)

    axes = plt.gca()

    axes.set_xlabel("Delta Follower Group")
    if is_log_y_axis_param:
        axes.set_ylabel("Density of Log(Delta Retweet)")
        axes.set_ylim([-5, 15])
        plt.title('Density of Log(Delta Retweet) - Delta Follower Group (Low, Medium, High) Box plot (' + each_topic + ', ' + each_fold + ')')
    else:
        axes.set_ylabel("Density of Delta Retweet")
        axes.set_ylim([-10, 100])
        plt.title('Density of Delta Retweet - Delta Follower Group (Low, Medium, High) Box plot (' + each_topic + ', ' + each_fold + ')')
    plt.show()


def print_info_quartile_median(df_low_medium_high_param, is_log_y_axis_param):
    if is_log_y_axis_param:
        print("Y Axis: Log(Delta Retweet)")
    else:
        print("Y Axis: Delta Retweet")
    print("----- Low Delta_Follower -----")
    print("1-Quartile: " + str(df_low_medium_high_param.Low.quantile(q=0.25)))
    print("Median: " + str(df_low_medium_high_param.Low.median()))
    print("3-Quartile: " + str(df_low_medium_high_param.Low.quantile(q=0.75)))

    print("----- Medium Delta_Follower -----")
    print("1-Quartile: " + str(df_low_medium_high_param.Medium.quantile(q=0.25)))
    print("Median: " + str(df_low_medium_high_param.Medium.median()))
    print("3-Quartile: " + str(df_low_medium_high_param.Medium.quantile(q=0.75)))

    print("----- High Delta_Follower -----")
    print("1-Quartile: " + str(df_low_medium_high_param.High.quantile(q=0.25)))
    print("Median: " + str(df_low_medium_high_param.High.median()))
    print("3-Quartile: " + str(df_low_medium_high_param.High.quantile(q=0.75)))


# SET PARAMETER
# y_axis_choices = ['retweet', 'follower_wt_mc', 'follower_wo_mc']
y_axis_choices = ['follower_wo_mc']
topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
# topics = ["aroii", "hormonestheseries", "thefacethailand"]
# topics = ["hormonestheseries", "thefacethailand"]
# topics = ["thefacethailand"]
# topics = ["apple"]
# folds = ["1"]
folds = ["1", "2", "3", "4", "5"]
# folds = ["2", "3", "4", "5"]
# folds = ["3", "4", "5"]
# folds = ["4", "5"]
# folds = ["5"]

last_hour_app_aroii = 1651
last_hour_hor_theface = 1627

is_interpolate = False

is_log_y_axis = False
logarithm_base_num = 2

bound_delta_follower = ['1.67', '7.40',         # Apple 1
                        '2.10', '8.00',         # Apple 2
                        '3.8', '16.6',          # Apple 3
                        '2.2', '4.4',           # Apple 4
                        '3.53', '6.2',          # Apple 5
                        '0.92', '2.1',          # Aroii 1
                        '7.3', '12.1',          # Aroii 2
                        '0.585', '1.2',         # Aroii 3
                        '0.98', '1.76',         # Aroii 4
                        '2.7', '4.1',           # Aroii 5
                        '1.1', '2.35',        # Hormones 1
                        '2.7', '3.9',        # Hormones 2   Shit
                        '6.52', '10',        # Hormones 3
                        '2.25', '4.1',        # Hormones 4
                        '2.5', '5',        # Hormones 5
                        '1.59', '3.5',        # TheFace 1
                        '0.995', '1.51',        # TheFace 2
                        '4.7', '7.3',        # TheFace 3        Shit
                        '2.8', '4.1',        # TheFace 4
                        '2.87', '4.75']        # TheFace 5


for each_choice in y_axis_choices:
    for each_topic in topics:
        for each_fold in folds:
            print("============ Topic: " + each_topic + ", Fold: " + each_fold + " =============")

            source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/" + each_topic + "/fold_" + each_fold + "/all_tweet.csv"
            output_follower_csv = "E:/tweet_process/result_follower-ret/09_follower_retweet_csv/" + each_topic + "/fold_" + each_fold + "/all_tweet-diff_ret-diff_fol.csv"
            output_kde_ret_fol_csv = "E:/tweet_process/result_follower-ret/10_KDE_ret_fol_csv/" + each_topic + "/fold_" + each_fold + "/kde-diff_ret-diff_fol.csv"

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
            # df_follower = pd.read_csv(output_follower_csv, names=['DeltaRetweet', 'DeltaFollower'])
            # print(df_follower)
            # df_follower.boxplot()
            # # df_follower.boxplot(by='DeltaRetweet')
            # plt.show()

            """
            Process Data
            """
            # data_retweet = []  # Array for collect original data
            # data_follower = []  # Array for collect original data
            # data_estimate_retweet = []  # Array for collect KDE processed data
            # data_estimate_follower = []  # Array for collect KDE processed data
            #
            # if each_topic == "apple" or each_topic == "aroii":
            #     for i in range(0, last_hour_app_aroii):
            #         data_retweet.append([])
            #         data_follower.append([])
            # else:
            #     for i in range(0, last_hour_hor_theface):
            #         data_retweet.append([])
            #         data_follower.append([])
            #
            # process_data(source_path, data_retweet, 'retweet')
            # process_data(source_path, data_follower, 'follower_wo_mc')

            """
            KDE processing
            """
            # for i in range(0, len(data_retweet)):
            #     estimate(data_retweet[i], data_estimate_retweet, i)
            #     estimate(data_follower[i], data_estimate_follower, i)

            """
            Write KDE Data
            """
            # print(len(data_estimate_retweet))
            # print(data_estimate_retweet)
            # print(len(data_estimate_follower))
            # print(data_estimate_follower)
            # write_date_date_csv(output_kde_ret_fol_csv, data_estimate_retweet, data_estimate_follower, 'kde')

            """
            Normal BoxPlot Test
            """
            # normal_boxplot(output_kde_ret_fol_csv)

            """
            Create Dataframe (Low, Medium, High)
            Plot
            """
            df_low_medium_high = create_low_medium_high(output_kde_ret_fol_csv, each_topic, each_fold, is_interpolate, is_log_y_axis, logarithm_base_num)
            print_info_quartile_median(df_low_medium_high, is_log_y_axis)
            low_medium_high_boxplot_from_df(df_low_medium_high, is_log_y_axis)
