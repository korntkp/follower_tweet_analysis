import fileinput


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
topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]
folds = ["1", "2", "3", "4", "5"]

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

            sum_of_follower = 0
            count_follower = 0

            for i in range(0, len(retweet_list)):
                if retweet_list[i] != 'nan' and retweet_list[i] != 'na':
                    sum_of_retweet += float(retweet_list[i])
                    count_reweet += 1
                if follower_list[i] != 'nan' and follower_list[i] != 'na':
                    sum_of_follower += float(follower_list[i])
                    count_follower += 1
            avg_retweet = sum_of_retweet / count_reweet
            avg_follower = sum_of_follower / count_follower
            
            print(sum_of_retweet)
            print(count_reweet)
            print("Average Retweet:", avg_retweet)

            print(sum_of_follower)
            print(count_follower)
            print("Average Follower:", avg_follower)
