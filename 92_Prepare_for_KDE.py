import fileinput


# data_retweet = []
# data_follower = []
# num_index = 1655  # ###### Edit here #########
# for i in range(0, num_index):
#     data_retweet.append([])
#     data_follower.append([])

source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/aroii/fold_1/all_tweet.csv"
# source_path = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/aroii/fold_1/t1.csv"

max_retweet = 0.0
max_follower = 0.0
max_hour_ret = 0
max_hour_fol = 0
max_ret_tweet_id = 0
max_fol_tweet_id = 0

min_retweet = 0.0
min_follower = 0.0
min_hour_ret = 0
min_hour_fol = 0
min_ret_tweet_id = 0
min_fol_tweet_id = 0

for line in fileinput.input([source_path]):
    value = line.split(',')
    # print(value)
    temp_tweet_id = str(value[0].strip())
    temp_hour = int(value[12].strip())  # ###### Edit here #########    hour
    temp_retweet = float(value[3].strip())  # ###### Edit here #########  diff_retweet
    temp_follower = float(value[10].strip())  # ###### Edit here #########  diff_follower
    temp_follower_wo_mc = float(value[13].strip())

    """
    Max Retweet
    """
    if temp_retweet >= max_retweet:
    # if temp_retweet >= max_retweet and temp_hour != 1334 and temp_hour != 541 and temp_hour != 1335 and temp_hour != 491 and temp_hour != 1336:
        max_retweet = temp_retweet
        max_hour_ret = temp_hour
        max_ret_tweet_id = temp_tweet_id
    # if temp_retweet > 500.0:
    #     print("Hour: " + str(temp_hour) + ", Retweet: " + str(temp_retweet) + ", ID: " + temp_tweet_id)

    """
    Max Follower
    """
    if temp_follower >= max_follower:
    # if temp_follower >= max_follower and temp_hour != 490 and temp_hour != 495 and temp_hour != 111 and temp_hour != 303 and temp_hour != 493:
        max_follower = temp_follower
        max_hour_fol = temp_hour
        max_fol_tweet_id = temp_tweet_id
    # if temp_follower > 60.0:
    #     print("Hour: " + str(temp_hour) + ", Follower: " + str(temp_follower) + ", ID: " + temp_tweet_id)

    """
    Min Retweet
    """
    # if temp_retweet <= min_retweet:
    #     min_retweet = temp_retweet
    #     min_hour_ret = temp_hour
    #     min_ret_tweet_id = temp_tweet_id
    # if temp_retweet < 0.0:
    #     print("Hour: " + str(temp_hour) + ", Retweet: " + str(temp_retweet) + ", ID: " + temp_tweet_id)

    """
    Min Follower
    """
    # if temp_follower <= min_follower:
    #     min_follower = temp_follower
    #     min_hour_fol = temp_hour
    #     min_fol_tweet_id = temp_tweet_id
    # if temp_follower < -500.0:
    #     print("Hour: " + str(temp_hour) + ", Follower: " + str(temp_follower) + ", ID: " + temp_tweet_id)

print("Max Retweet At: " + str(max_hour_ret) + " Value: " + str(max_retweet) + ", ID: " + max_ret_tweet_id)
print("Max Follower At: " + str(max_hour_fol) + " Value: " + str(max_follower) + ", ID: " + max_fol_tweet_id)
# print("Min Retweet At: " + str(min_hour_ret) + " Value: " + str(min_retweet) + ", ID: " + min_ret_tweet_id)
# print("Min Follower At: " + str(min_hour_fol) + " Value: " + str(min_follower) + ", ID: " + min_fol_tweet_id)
