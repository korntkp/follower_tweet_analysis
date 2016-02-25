from datetime import datetime
"""
        Input (mc_and_sort_all_ret_fold_*.csv)

0  message_count
1  index_line
2  is_retweet
3  is_quote
4  original_tweet_date
5  original_tweet_time
6  original_tweet_user_follower_count
7  original_tweet_retweet_count
8  original_tweet_id
9  original_tweet_user_id
10  retweet_tweet_date
11 retweet_tweet_time
12 retweet_tweet_id
13 retweet_tweet_user_id
14 original_tweet_epoch
15 retweet_tweet_epoch

        Output (t*.csv)

0   index_hour                              NEW!!!
1   message_count
2   index_line
3   is_retweet
4   is_quote
5   original_tweet_date
6   original_tweet_time
7   original_tweet_user_follower_count
8   original_tweet_retweet_count
9   original_tweet_id
10   original_tweet_user_id
11  retweet_tweet_date
12  retweet_tweet_time
13  retweet_tweet_id
14  retweet_tweet_user_id
15  original_tweet_epoch
16  retweet_tweet_epoch
"""

"""
HormonesTheSeries   Fail Date
2015-11-10	07.07
2015-11-12	No Data
2015-11-19	06.08
2015-12-03	22.09
2015-12-18	10.52
2015-12-22	20.59
2015-12-24	06.07
============================
Aroii   Fail Date
2015-12-03	22.09
2015-12-18	11.10
2015-12-22	21.02
2016-01-11	22.42
2016-01-15	23.24
2016-01-19	15.47
"""

# SELECT TOPIC TO PROCESS (ctr + /)
# topic = "aroii"
# topic = "hormonestheseries"
# topic = "apple"
topic = "thefacethailand"
# start_time = 1447714800  # 2015-11-17,06:00:00  Aroii & Apple                              1447714800
start_time = 1447023600  # 2015-11-09,06:00:00  HormonesTheSeries & TheFaceThailand      1447023600

for loop in range(1, 6):

    input_path_mc = "E:/tweet_process/result_follower-ret/03_4_add_message_count/" + topic + "/mc_and_sort_all_ret_fold_" + str(loop) + ".csv"
    print("Processing File: " + input_path_mc)

    file = open(input_path_mc, 'r')
    for line in file:
        # print(line)
        retweet_tweet_date = line.split(',')[10]    # date
        retweet_tweet_time = line.split(',')[11]    # time
        retweet_tweet_epoch = int(line.split(',')[15])      # unix time
        # print(retweet_tweet_epoch)

        second_from_start = retweet_tweet_epoch - start_time

        float_time_divide = second_from_start / 3600
        int_time_divide = int(float_time_divide) + 1
        # if second_from_start < 7200:
        #     print(second_from_start)
        #     print(int_time_divide)

        output_name = "E:/tweet_process/result_follower-ret/04_each_hour/" + topic + "/fold_" + str(loop) + "/t" + str(int_time_divide) + ".csv"

        fo = open(output_name, "a")
        # print(output_name)
        if (int_time_divide - 19) % 24 == 0:
            print("00:00:00")
        else:
            fo.write(str(int_time_divide) + "," + line)
        fo.close()
        # print(output_name)

        ordinal_time = datetime.fromtimestamp(retweet_tweet_epoch).strftime('%Y-%m-%d %H:%M:%S')
        # print(str(i) + " " + str(retweet_tweet_epoch) + " -> " + ordinal_time + " | " + retweet_tweet_date + " " + retweet_tweet_time)
    file.close()
