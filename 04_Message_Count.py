import csv
import operator
import os.path

"""
    0)  index_line
    1)  is_retweet                                  *
    2)  is_quote
    3)  original_tweet_date                         *
    4)  original_tweet_time                         *
    5)  original_tweet_user_follower_count          **
    6)  original_tweet_retweet_count                **
    7)  original_tweet_id                           **
    8)  original_tweet_user_id
    9)  retweet_tweet_date                          *
    10) retweet_tweet_time                          *
    11) retweet_tweet_id                            **
    12) retweet_tweet_user_id
    13) original_tweet_epoch                        **
    14) retweet_tweet_epoch                         **
"""
"""
    0)  message_count                               NEW!!!! (Message Number of Source User)
    1)  index_line
    2)  is_retweet                                  *
    3)  is_quote
    4)  original_tweet_date                         *
    5)  original_tweet_time                         *
    6)  original_tweet_user_follower_count          **
    7)  original_tweet_retweet_count                **
    8)  original_tweet_id                           **
    9)  original_tweet_user_id
    10)  retweet_tweet_date                          *
    11) retweet_tweet_time                          *
    12) retweet_tweet_id                            **
    13) retweet_tweet_user_id
    14) original_tweet_epoch                        **
    15) retweet_tweet_epoch                         **
"""


# Input (Sort)
# E:\tweet_process\result_follower-ret\03_retweet_in_fold\aroii\all_retweet_fold_*.cs
# Output (Sort)
# E:\tweet_process\result_follower-ret\03_2_sort_retweet_in_fold\aroii\sort_all_retweet_fold_*.csv


def sort_by_retweet_time(input_path_sort_param, output_path_sort_param):
    data = csv.reader(open(input_path_sort_param, 'r'))
    sort_data = sorted(data, key=operator.itemgetter(14))

    with open(output_path_sort_param, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(sort_data)

    print("Sort By Retweet Time: " + input_path_sort_param + " Successful")
    return


# SELECT TOPIC TO PROCESS (ctr + /)
# topic = "aroii"
# topic = "hormonestheseries"
# topic = "apple"
topic = "thefacethailand"

for loop in range(1, 6):
    input_path_sort = "E:/tweet_process/result_follower-ret/03_1_retweet_in_fold/" + topic + "/all_retweet_fold_" + str(
        loop) + ".csv"
    output_path_sort = "E:/tweet_process/result_follower-ret/03_2_sort_retweet_in_fold/" + topic + "/sort_all_retweet_fold_" + str(
        loop) + ".csv"
    # Sort
    print("Sorting...")
    sort_by_retweet_time(input_path_sort, output_path_sort)
    print("Sorted by Retweet Time Success")

# ===========================================================================================================================================
# Input (Message Count)
# E:\tweet_process\result_follower-ret\03_2_sort_retweet_in_fold\aroii\sort_all_retweet_fold_*.csv
# Temp Process
# E:\tweet_process\result_follower-ret\03_3_temp_message_count\aroii\fold_1\<source_user_id>.csv
# Output (Message Count)
# E:\tweet_process\result_follower-ret\03_4_add_message_count\aroii\mc_and_sort_all_ret_fold_*.csv

for loop in range(1, 6):

    input_path_mc = "E:/tweet_process/result_follower-ret/03_2_sort_retweet_in_fold/" + topic + "/sort_all_retweet_fold_" + str(
        loop) + ".csv"
    output_path_mc = "E:/tweet_process/result_follower-ret/03_4_add_message_count/" + topic + "/mc_and_sort_all_ret_fold_" + str(
        loop) + ".csv"
    input_file = open(input_path_mc, 'r')
    print("Precessing File: " + input_path_mc)

    for line_in in input_file:
        # print(line_in)
        has_this_tweet_id = False
        source_tweet_id = line_in.split(',')[7]
        source_user_tweet_id = line_in.split(',')[8]
        path_temp = "E:/tweet_process/result_follower-ret/03_3_temp_message_count/" + topic + "/fold_" + str(
            loop) + "/" + source_user_tweet_id + ".csv"
        if os.path.isfile(path_temp):  # If Exist File

            read_temp = open(path_temp, 'r')
            num_of_dup_message = 0
            num_of_message = 0
            for line_temp in read_temp:
                temp_source_tweet_id = line_temp.split(',')[8]  # in Temp_File.csv has message_count at [0]
                num_of_message += 1
                if source_tweet_id == temp_source_tweet_id:
                    num_of_dup_message = num_of_message
                    has_this_tweet_id = True  # if True -> not write something in Temp
                    # break  #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1no break
            read_temp.close()

            if has_this_tweet_id == False:  # First Time to see this Retweet (but many time with this source_user)
                write_temp = open(path_temp, 'a')
                write_temp.write(str(num_of_message + 1) + "," + line_in)
                write_temp.close()

                write_output = open(output_path_mc, 'a')
                write_output.write(str(num_of_message + 1) + "," + line_in)
                write_output.close()

            else:  # Many Time to see this Retweet (and many time with this source_user)
                """
                If forget to delete all <user_id>.csv in 03_3_temp_message_count, The Result will be the SAME
                """

                write_output = open(output_path_mc, 'a')
                # write_output.write(str(num_of_dup_message) + "," + line_in)  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11111
                write_output.write(
                    str(num_of_message) + "," + line_in)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11111
                write_output.close()

        else:  # create File <User_ID.csv>  # First Time to see this Retweet (and this source_user)
            write_temp = open(path_temp, 'w')
            write_temp.write("1," + line_in)
            write_temp.close()

            write_output = open(output_path_mc, 'a')
            write_output.write("1," + line_in)
            write_output.close()

    input_file.close()
