import os.path


# E:\tweet_process\result_follower-ret\04_each_hour\aroii\fold_1
# E:\tweet_process\result_follower-ret\05_pig_script\aroii

start_hour = [0, 300, 600, 900, 1200, 1500]  # end = start + 300
end_hour = 300

# topic = "aroii"
# topic = "hormonestheseries"
# topic = "apple"
topic = "thefacethailand"

for fold in range(1, 6):

    for start_index in range(0, len(start_hour)):

        script_path = "E:/tweet_process/result_follower-ret/05_pig_script/" + topic + "/script_" + topic + "_fold_" + str(fold) + "_" + str(start_hour[start_index]) + "_" + str(start_hour[start_index] + end_hour) + ".pig"
        fo = open(script_path, "w")
        for i in range(start_hour[start_index], start_hour[start_index] + end_hour):
            check_input_path = "E:/tweet_process/result_follower-ret/04_each_hour/" + topic + "/fold_" + str(fold) + "/t" + str(i) + ".csv"
            is_file = os.path.isfile(check_input_path)

            if is_file:
                print(check_input_path)
                code = "csv_file_" + str(i) + " = LOAD '" + topic + "_fold_" + str(fold) + "/t" + str(i) + ".csv' USING PigStorage(',') AS (index_hour_" + str(i) + ":int, message_count_" + str(i) + ":double, index_line_" + str(i) + ":int, is_retweet_" + str(i) + ":int, is_quote_" + str(i) + ":int, original_tweet_date_" + str(i) + ":chararray, original_tweet_time_" + str(i) + ":chararray, original_tweet_user_follower_count_" + str(i) + ":double, original_tweet_retweet_count_" + str(i) + ":double, original_tweet_id_" + str(i) + ":chararray, original_tweet_user_id_" + str(i) + ":chararray, retweet_tweet_date_" + str(i) + ":chararray, retweet_tweet_time_" + str(i) + ":chararray, retweet_tweet_id_" + str(i) + ":chararray, retweet_tweet_user_id_" + str(i) + ":chararray, original_tweet_epoch_" + str(i) + ":int, retweet_tweet_epoch_" + str(i) + ":int);\n" + "grouped_by_original_tweet_id_" + str(i) + " = GROUP csv_file_" + str(i) + " BY original_tweet_id_" + str(i) + ";\n" + "cal_diff_of_each_tweet_" + str(i) + " = FOREACH grouped_by_original_tweet_id_" + str(i) + " {\n" + "sort_end_" + str(i) + " = ORDER csv_file_" + str(i) + " BY retweet_tweet_epoch_" + str(i) + " DESC;\n" + "retweet_at_end_" + str(i) + " = LIMIT sort_end_" + str(i) + " 1;\n" + "sort_start_" + str(i) + " = ORDER csv_file_" + str(i) + " BY retweet_tweet_epoch_" + str(i) + " ASC;\n" + "retweet_at_start_" + str(i) + " = LIMIT sort_start_" + str(i) + " 1;\n" + "start_retweet_" + str(i) + " = SUM(retweet_at_start_" + str(i) + ".original_tweet_retweet_count_" + str(i) + ");\n" + "end_retweet_" + str(i) + " = SUM(retweet_at_end_" + str(i) + ".original_tweet_retweet_count_" + str(i) + ");\n" + "diff_retweet_" + str(i) + " = end_retweet_" + str(i) + "-start_retweet_" + str(i) + ";\n" + "start_follower_" + str(i) + " = SUM(retweet_at_start_" + str(i) + ".original_tweet_user_follower_count_" + str(i) + ");\n" + "end_follower_" + str(i) + " = SUM(retweet_at_end_" + str(i) + ".original_tweet_user_follower_count_" + str(i) + ");\n" + "start_message_count_" + str(i) + " = SUM(retweet_at_start_" + str(i) + ".message_count_" + str(i) + ");\n" + "end_message_count_" + str(i) + " = SUM(retweet_at_end_" + str(i) + ".message_count_" + str(i) + ");\n" + "end_part_" + str(i) + " = end_follower_" + str(i) + " / end_message_count_" + str(i) + ";\n" + "start_part_" + str(i) + " = start_follower_" + str(i) + " / start_message_count_" + str(i) + ";\n" + "diff_follower_" + str(i) + " = end_part_" + str(i) + " - start_part_" + str(i) + ";\n" + "owner_id_" + str(i) + " = retweet_at_start_" + str(i) + ".original_tweet_user_id_" + str(i) + ";\n" + "hour_" + str(i) + " = retweet_at_start_" + str(i) + ".index_hour_" + str(i) + ";\n" + "diff_follower_original_" + str(i) + " = end_follower_" + str(i) + " - start_follower_" + str(i) + ";\n" + "GENERATE group, start_retweet_" + str(i) + ", end_retweet_" + str(i) + ", diff_retweet_" + str(i) + ", end_follower_" + str(i) + ", end_message_count_" + str(i) + ", start_follower_" + str(i) + ", start_message_count_" + str(i) + ", end_part_" + str(i) + ", start_part_" + str(i) + ", diff_follower_" + str(i) + ", FLATTEN(owner_id_" + str(i) + "), FLATTEN(hour_" + str(i) + "), diff_follower_original_" + str(i) + ";\n" + "};\n" + "STORE cal_diff_of_each_tweet_" + str(i) + " INTO 'result_t" + str(i) + "' USING PigStorage(',');\n"
                fo.write(code)
        fo.close()
