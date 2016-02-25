import os.path


all_hours = 24 * 7 * 10  # 1680

# topic = "aroii"                 # 69 Days
# topic = "hormonestheseries"   # 68 Days
# topic = "apple"               # 69 Days
# topic = "thefacethailand"     # 68 Days

topics = ["apple", "aroii", "hormonestheseries", "thefacethailand"]

for each_topic in topics:
    for fold in range(1, 6):
        print("Processing Topic: " + each_topic + ", Fold: " + str(fold))

        output_all_time = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/" + each_topic + "/fold_" + str(fold) + "/all_tweet.csv"

        fo_all_time = open(output_all_time, "w")

        for i in range(1, all_hours):

            input_path = "D:/share_folder_vm/diff_result/" + each_topic + "/fold_" + str(fold) + "/result_t" + str(i) + "/"
            is_exist = os.path.isdir(input_path)
            # print(input_path + ": is exist dir -> " + str(is_exist))

            if is_exist:
                input_file_name = "part-r-00000"
                input_file = input_path + input_file_name
                is_single_result = os.path.isfile(input_file)

                if is_single_result:
                    output_each_time = "E:/tweet_process/result_follower-ret/06_diff_ret_fol_result/" + each_topic + "/fold_" + str(fold) + "/t" + str(i) + ".csv"
                    each_file = open(input_file, "r")
                    fo_each_time = open(output_each_time, "w")
                    for line in each_file:
                        fo_all_time.write(line)
                        fo_each_time.write(line)
                        # print(line)
                    each_file.close()
                    fo_each_time.close()

                else:
                    print(input_file + " is single result -> " + str(is_single_result) + "NO!!!")

        fo_all_time.close()
