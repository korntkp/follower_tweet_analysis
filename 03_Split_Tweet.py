import fileinput
import glob


# Extract Source User ID from all file in directory
def get_user_id(file_path_param):
    list_user_id = []
    for each_line in fileinput.input([file_path_param]):
        new_line_index = each_line.find("\n")
        user_id_in_line = str(each_line[0:new_line_index])
        list_user_id.append(user_id_in_line)
    fileinput.close()
    return list_user_id

"""
source_path_after_preprocess = glob.glob("D:/share_folder_vm/data/*.csv")  # All Hormones Retweet Data CSV
user_id = get_user_id(source_path_70)  # List
dest_path1_70 = "D:/share_folder_vm/test_sampling_source_user/02_result_tweet/split_tweet_70user.csv"

split_file_old(source_path_after_preprocess, user_id, dest_path1_70)
"""


# def split_file_old(input_path, list_user_id, output_path):
#     file_output_param = open(output_path, "w")
#     for file in input_path:
#         each_file = open(file, 'r')
#         print(each_file)
#         for line in each_file:
#             source_user_id_str = line.split(',')[8]
#             for each_id in list_user_id:
#                 if each_id == source_user_id_str:  # Write into File
#                     file_output_param.write(line)
#         # write file
#         # add index column
#         each_file.close()
#     file_output_param.close()
#     return


"""
source_path_after_preprocess = glob.glob("D:/share_folder_vm/data/*.csv")  # All Hormones Retweet Data CSV
user_id = get_user_id(source_path_70)  # List
dest_path1_70 = "D:/share_folder_vm/test_sampling_source_user/02_result_tweet/split_tweet_70user.csv"

split_file(source_path_after_preprocess, user_id, dest_path1_70)
"""


def split_file(input_path, list_user_id, output_path):
    file_output_append = open(output_path, "a")
    for file in input_path:
        each_file_read = open(file, 'r')
        print(each_file_read)
        for line_read in each_file_read:
            source_user_id_input = line_read.split(',')[8]
            for each_user_id in list_user_id:
                if each_user_id == source_user_id_input:  # Write into File
                    file_output_append.write(line)
        each_file_read.close()
    file_output_append.close()
    return


# Write Each Item from List into File
def write_file(path, list_param):
    fo = open(path, "w")
    for item in list_param:
        fo.write(item + "\n")
    fo.close()
    return


# ====================================================================================================
# SELECT TOPIC TO PROCESS (ctr + /)
# topic = "aroii"  # week2 - week11
# topic = "hormonestheseries"
# topic = "apple"
topic = "thefacethailand"
# week_list_aroii_apple = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
week_list_hormones_theface = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

# Path (Split_User)
# E:\tweet_process\result_follower-ret\02partition_user\hormonestheseries\user_k-fold\user_fold_1.csv
# E:\tweet_process\result_follower-ret\02partition_user\hormonestheseries\user_k-fold\user_fold_2.csv
# E:\tweet_process\result_follower-ret\02partition_user\hormonestheseries\user_k-fold\user_fold_3.csv
# E:\tweet_process\result_follower-ret\02partition_user\hormonestheseries\user_k-fold\user_fold_4.csv
# E:\tweet_process\result_follower-ret\02partition_user\hormonestheseries\user_k-fold\user_fold_5.csv

# Path (Retweet Data)
# E:\tweet_process\result_follower-ret\01preprocess\hormonestheseries\week1\*.csv
# E:\tweet_process\result_follower-ret\01preprocess\aroii\week2\*.csv

for loop in range(1, 6):  # 5 Folds
    path_user_fold = "E:/tweet_process/result_follower-ret/02partition_user/" + topic + "/user_k-fold/user_fold_" + str(loop) + ".csv"
    all_retweet_fold = "E:/tweet_process/result_follower-ret/03_1_retweet_in_fold/" + topic + "/all_retweet_fold_" + str(loop) + ".csv"
    list_user_id_fold = get_user_id(path_user_fold)

    file_output = open(all_retweet_fold, "w")

    # for week in week_list_aroii_apple:
    for week in week_list_hormones_theface:

        file_path = "/"+topic+"/week"+week+"/"

        source_path = "E:/tweet_process/result_follower-ret/01preprocess" + file_path + "*.csv"
        # print(source_path)

        files_list = glob.glob(source_path)
        # print(files_list)

        for one_file_path in files_list:
            print(one_file_path)

            each_file = open(one_file_path, 'r')
            for line in each_file:
                source_user_id_str = line.split(',')[8]
                for each_id in list_user_id_fold:
                    if each_id == source_user_id_str:  # Write into File
                        file_output.write(line)
            each_file.close()
    file_output.close()
    print("================================ " + str(loop*20) + "% =====================================")
    print("Write Split Tweet CSV File Success!!!")
