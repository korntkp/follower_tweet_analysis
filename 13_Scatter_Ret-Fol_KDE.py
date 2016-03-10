import math
import pandas as pd
import matplotlib.pyplot as plt


# SET PARAMETER
# y_axis_choices = ['retweet', 'follower_wt_mc', 'follower_wo_mc']
y_axis_choices = ['follower_wo_mc']
topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
# topics = ["apple"]
folds = ["1", "2", "3", "4", "5"]
# folds = ["1"]

for each_choice in y_axis_choices:
    for each_topic in topics:
        for each_fold in folds:
            print(each_topic, each_fold, each_choice)

            source_kde_ret_fol_csv = "E:/tweet_process/result_follower-ret/10_KDE_fol_ret_csv/" + each_topic + "/fold_" + each_fold + "/kde-diff_ret-diff_fol.csv"
            kde_df_ret_fol = pd.read_csv(source_kde_ret_fol_csv, names=['DeltaRetweet', 'DeltaFollower'])

            title = 'Delta Retweet - Delta Follower (' + each_topic + ', ' + each_fold + ')'
            kde_df_ret_fol.plot(kind='scatter', x='DeltaRetweet', y='DeltaFollower', title=title)
            axes = plt.gca()
            axes.set_xlim([-5, 80])
            axes.set_ylim([-5, 80])
            # plt.show()

            kde_df_ret_fol.DeltaRetweet[0] = math.log(kde_df_ret_fol.DeltaRetweet[0])
            print(kde_df_ret_fol.DeltaRetweet)  # OK



