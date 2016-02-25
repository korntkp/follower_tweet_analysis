import fileinput
import glob
import random


def split_5_fold(list_user_id, topic_name):
    fold_number = 5
    set_user_id_all = set(list_user_id)
    set_user_id_all_length = len(set_user_id_all)

    set_user_id_fold_1 = random.sample(set_user_id_all, int(set_user_id_all_length*20/100))             # Fold 1 -> 20%
    length_of_set_user_id_fold_1 = len(set_user_id_fold_1)

    set_user_id_temp_1 = set(set_user_id_all.difference(set_user_id_fold_1))                                 # Temp_1 -> 80%
    length_of_set_user_id_temp_1 = len(set_user_id_temp_1)

    set_user_id_temp_2 = set(random.sample(set_user_id_temp_1, int(length_of_set_user_id_temp_1*50/100)))        # Temp_2 -> 40%
    length_of_set_user_id_temp_2 = len(set_user_id_temp_2)
    set_user_id_fold_2 = random.sample(set_user_id_temp_2, int(length_of_set_user_id_temp_2*50/100))            # Fold 2 -> 20%
    length_of_set_user_id_fold_2 = len(set_user_id_fold_2)
    set_user_id_fold_3 = set_user_id_temp_2.difference(set_user_id_fold_2)                                      # Fold 3 -> 20%
    length_of_set_user_id_fold_3 = len(set_user_id_fold_3)

    set_user_id_temp_3 = set(set_user_id_temp_1.difference(set_user_id_temp_2))                                  # Temp_3 -> 40%
    length_of_set_user_id_temp_3 = len(set_user_id_temp_3)
    set_user_id_fold_4 = random.sample(set_user_id_temp_3, int(length_of_set_user_id_temp_3*50/100))            # Fold 4 -> 20%
    length_of_set_user_id_fold_4 = len(set_user_id_fold_4)
    set_user_id_fold_5 = set_user_id_temp_3.difference(set_user_id_fold_4)                                      # Fold 5 -> 20%
    length_of_set_user_id_fold_5 = len(set_user_id_fold_5)

    print("Number of Source User with duplicate: " + str(len(list_user_id)))
    print("Number of Source User: " + str(set_user_id_all_length))
    print("Number of Sampling User Fold 1: " + str(length_of_set_user_id_fold_1))
    print("Number of Sampling User Fold 2: " + str(length_of_set_user_id_fold_2))
    print("Number of Sampling User Fold 3: " + str(length_of_set_user_id_fold_3))
    print("Number of Sampling User Fold 4: " + str(length_of_set_user_id_fold_4))
    print("Number of Sampling User Fold 5: " + str(length_of_set_user_id_fold_5))
    print("================================")
    print("Number of Sampling Temp 1: " + str(length_of_set_user_id_temp_1))
    print("Number of Sampling Temp 2: " + str(length_of_set_user_id_temp_2))
    print("Number of Sampling Temp 3: " + str(length_of_set_user_id_temp_3))

    #  write file

    # Path
    # E:\tweet_process\result_follower-ret\02partition_user\aroii\user_k-fold\*.csv
    dest_path_all = "E:/tweet_process/result_follower-ret/02partition_user/" + topic_name + "/user_k-fold/user_all.csv"
    dest_path_fold_1 = "E:/tweet_process/result_follower-ret/02partition_user/" + topic_name + "/user_k-fold/user_fold_1.csv"
    dest_path_fold_2 = "E:/tweet_process/result_follower-ret/02partition_user/" + topic_name + "/user_k-fold/user_fold_2.csv"
    dest_path_fold_3 = "E:/tweet_process/result_follower-ret/02partition_user/" + topic_name + "/user_k-fold/user_fold_3.csv"
    dest_path_fold_4 = "E:/tweet_process/result_follower-ret/02partition_user/" + topic_name + "/user_k-fold/user_fold_4.csv"
    dest_path_fold_5 = "E:/tweet_process/result_follower-ret/02partition_user/" + topic_name + "/user_k-fold/user_fold_5.csv"

    write_file(dest_path_all, set_user_id_all)
    write_file(dest_path_fold_1, set_user_id_fold_1)
    write_file(dest_path_fold_2, set_user_id_fold_2)
    write_file(dest_path_fold_3, set_user_id_fold_3)
    write_file(dest_path_fold_4, set_user_id_fold_4)
    write_file(dest_path_fold_5, set_user_id_fold_5)

    return


def split_user_70_30(list_user_id, topic_name):
    # Path
    # E:\tweet_process\result_follower-ret\02partition_user\aroii\user_70-30\*.csv
    dest_path0_all = "E:/tweet_process/result_follower-ret/02partition_user/" + topic_name + "/user_70-30/user_all.csv"
    dest_path1_70 = "E:/tweet_process/result_follower-ret/02partition_user/" + topic_name + "/user_70-30/user_70.csv"
    dest_path2_30 = "E:/tweet_process/result_follower-ret/02partition_user/" + topic_name + "/user_70-30/user_30.csv"

    set_user_id_all = set(list_user_id)
    set_user_id_all_length = len(set_user_id_all)

    set_user_id_70 = random.sample(set_user_id_all, int(set_user_id_all_length*70/100))
    length_of_set_user_id_70 = len(set_user_id_70)

    set_user_id_30 = set_user_id_all.difference(set_user_id_70)
    length_of_set_user_id_30 = len(set_user_id_30)

    print("Number of Source User with duplicate: " + str(len(list_user_id)))
    print("Number of Source User: " + str(set_user_id_all_length))
    print("Number of Sampling User 70%: " + str(length_of_set_user_id_70))
    print("Number of Sampling User 30%: " + str(length_of_set_user_id_30))

    write_file(dest_path0_all, set_user_id_all)
    write_file(dest_path1_70, set_user_id_70)
    write_file(dest_path2_30, set_user_id_30)

    # print(dest_path0_all)
    # print(dest_path1_70)
    # print(dest_path2_30)

    print("Write UserID 70-30 File Success!!!\n")
    return


def write_file(path, list_user):
    fo = open(path, "w")
    for item in list_user:
        fo.write(item + "\n")
    fo.close()
    return


# ===================================== NEW Way 1 ====================================================

user_id = []
i = 0

# Path
# E:\tweet_process\result_follower-ret\01preprocess\hormonestheseries\week1\*.csv
# E:\tweet_process\result_follower-ret\02partition_user\hormonestheseries\fold*.csv
# E:\tweet_process\result_follower-ret\01preprocess\aroii\week2
# E:\tweet_process\result_follower-ret\02partition_user\aroii\fold.csv

# SELECT TOPIC TO PROCESS (ctr + /)
# topic = "aroii"  # week2 - week11
# topic = "hormonestheseries"
# topic = "apple"
topic = "thefacethailand"
# week_list_aroii_apple = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
week_list_hormones_theface = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
# for week in week_list_aroii_apple:
for week in week_list_hormones_theface:

    file_path = "/"+topic+"/week"+week+"/"

    source_path = "E:/tweet_process/result_follower-ret/01preprocess" + file_path + "*.csv"
    # print(source_path)

    files_list = glob.glob(source_path)
    # print(files_list)

    for one_file_path in files_list:
        # print(one_file_path)

        each_file = open(one_file_path, 'r')
        for line in each_file:
            source_user_id_str = line.split(',')[8]
            user_id.append(source_user_id_str)
        each_file.close()
        # i += 1
        # print(i)

# split_user_70_30(user_id, topic)
print("Topic: " + topic)
split_5_fold(user_id, topic)


print("Write UserID File Success!!!\n")

# # ===================================== NEW Way 2 ====================================================
#
# # topic = "aroii"  # week2 - week11
# topic = "hormonestheseries"
#
# # week_list_aroii = ["2", "3"]
# # week_list_aroii = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
# week_list_hormones = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
#
# # E:\tweet_process\result_time-ret\01preprocess\aroii\week2
# # E:\tweet_process\result_time-ret\02integrate_file\aroii\week2
#
# # Loop through file
# # for week in week_list_aroii:
# for week in week_list_hormones:
#
#     files_list = glob.glob(source_path)
#     # print(files_list)
#
#     name_only_date = ""
#
#     for one_file_path in files_list:
#         dest_path = "E:/tweet_process/result_time-ret/02integrate_file" + file_path
#         filename = basename(one_file_path)
#         # print(filename)
#
#         dot_index = filename.find(".")
#         only_filename = filename[0:dot_index]
#         # print(only_filename)
#
#         check_same_day = only_filename[0:18]
#         # print(check_same_day)
#
#         len_of_name = len(only_filename)
#         len_of_name_list.append(len_of_name)
#         # print(same_day_list)
#         print(one_file_path)
#
#
#
# # ===================================== OLD Way ====================================================
# # Extract Source User ID from all file in directory
# def extract_user_id(all_files):
#     list_user_id = []
#     for file in all_files:
#         each_file = open(file, 'r')
#         for line in each_file:
#             source_user_id_str = line.split(',')[8]
#             list_user_id.append(source_user_id_str)
#         each_file.close()
#     return list_user_id
#
#
# source_path = "D:/share_folder_vm/data/*.csv"  # All Hormones Data
# dest_path0_all = "D:/share_folder_vm/test_sampling_source_user/result/user_all.csv"
# dest_path1_70 = "D:/share_folder_vm/test_sampling_source_user/result/user_70.csv"
# dest_path2_30 = "D:/share_folder_vm/test_sampling_source_user/result/user_30.csv"
# files = glob.glob(source_path)
# user_id = []
#
# # user_id = extract_user_id(files)
#
# set_user_id_all = set(user_id)
# set_user_id_all_length = len(set_user_id_all)
#
# set_user_id_70 = random.sample(set_user_id_all, int(set_user_id_all_length*70/100))
# length_of_set_user_id_70 = len(set_user_id_70)
#
# set_user_id_30 = set_user_id_all.difference(set_user_id_70)
# length_of_set_user_id_30 = len(set_user_id_30)
#
#
# print("Number of Source User with duplicate: " + str(len(user_id)))
# print("Number of Source User: " + str(len(set_user_id_all)))
# print("Number of Sampling User 70%: " + str(length_of_set_user_id_70))
# print("Number of Sampling User 30%: " + str(length_of_set_user_id_30))
#
# # write_file(dest_path0_all, set_user_id_all)
# # write_file(dest_path1_70, set_user_id_70)
# # write_file(dest_path2_30, set_user_id_30)
#
# print("Write UserID File Success!!!\n")
