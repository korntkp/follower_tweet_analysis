import fileinput


def read_csv_file(source_path_param):
    list1 = []
    for line in fileinput.input([source_path_param], openhook=fileinput.hook_encoded("utf8")):
        # print(line)
        new_line_index = line.find('\n')
        # print(new_line_index)
        list1.append(line[:new_line_index])
    fileinput.close()
    return list1

y_axis_choices = ['follower_wo_mc']
# y_axis_choices = ['retweet']
topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
folds = ["1", "2", "3", "4", "5"]


for each_choice in y_axis_choices:
    for each_topic in topics:
        for each_fold in folds:

            source_decomposition_retweet = "E:/tweet_process/result_follower-ret/11_trend_decomposed/" + each_topic + "/decomposition_" + each_fold + "_retweet.csv"
            source_decomposition_follower = "E:/tweet_process/result_follower-ret/11_trend_decomposed/" + each_topic + "/decomposition_" + each_fold + "_follower_wo_mc.csv"

            retweet_list = read_csv_file(source_decomposition_retweet)
            follower_list = read_csv_file(source_decomposition_follower)
            print(retweet_list)
            print(follower_list)
            print(len(retweet_list))
