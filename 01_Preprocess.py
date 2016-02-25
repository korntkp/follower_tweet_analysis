import glob
import fileinput
import time
from datetime import datetime, timedelta
from email.utils import parsedate_tz
from os.path import basename


def extract_json(source_path, dest_path):
    # Open file
    fo = open(dest_path, "w")
    index_line = 1
    pattern = '%Y-%m-%d %H:%M:%S'

    for line in fileinput.input([source_path], openhook=fileinput.hook_encoded("utf8")):
        is_quote = line.find("quoted_status") != -1
        is_quote = 1 if is_quote else 0
        is_quote = str(is_quote)

        # Get if retweet or not if true value=1 else value=0
        is_retweet = line.find("retweeted_status") != -1
        is_retweet = 1 if is_retweet else 0
        is_retweet = str(is_retweet)

        """
         Types of Tweet
            1) Original Tweet	(no retweeted_status)   ,0,0,
            2) Retweet Tweet    (has retweeted_status)  ,1,0,
            3) Original Quote	(no retweeted_status)   ,0,1,
            4) Retweet Quote    (has retweeted_status)  ,1,1,
        """

        # Original Tweet
        if is_retweet == "0" and is_quote == "0":
            # Extract time
            original_tweet_created_at_index = line.find("created_at")
            original_tweet_datetime = str(to_datetime(line[original_tweet_created_at_index + 13:original_tweet_created_at_index + 43]))

            # Get dayofweek, date, and time
            # dow = str(datetime.weekday())
            original_tweet_date = original_tweet_datetime.split(' ')[0]
            original_tweet_time = original_tweet_datetime.split(' ')[1]

            original_tweet_epoch = str(int(time.mktime(time.strptime(original_tweet_datetime, pattern))))

            # Extract original_tweet_id
            original_tweet_id_index = line.find("id_str")
            original_tweet_text_index = line.find("text")
            original_tweet_id = str(line[original_tweet_id_index + 9:original_tweet_text_index - 3])  # 9)

            # Extract original_tweet_user_id
            original_tweet_user_obj_index = line.find("\"user\":{")
            original_tweet_user_id_index = line.find("id_str", original_tweet_user_obj_index + 8)
            original_tweet_user_name_index = line.find("\",\"name\":", original_tweet_user_obj_index + 8)
            original_tweet_user_id = str(line[original_tweet_user_id_index + 9:original_tweet_user_name_index])

            # Extract original_tweet_user_follower_count
            original_tweet_user_follower_count_index = line.find("\"followers_count\":", original_tweet_user_obj_index + 8)
            original_tweet_user_friend_count_index = line.find(",\"friends_count\":", original_tweet_user_obj_index + 8)
            original_tweet_user_follower_count = str(line[original_tweet_user_follower_count_index + 18:original_tweet_user_friend_count_index])

            # Extract source_tweet_user_retweet_count from retweeted_status
            original_tweet_retweet_count_index = line.find(",\"retweet_count\":", original_tweet_user_obj_index + 8)
            original_tweet_favorite_count_index = line.find(",\"favorite_count\":", original_tweet_retweet_count_index + 17)
            original_tweet_retweet_count = str(line[original_tweet_retweet_count_index + 17:original_tweet_favorite_count_index])

            retweet_tweet_date = "null"
            retweet_tweet_time = "null"
            retweet_tweet_id = "null"
            retweet_tweet_user_id = "null"
            retweet_tweet_epoch = "null"

            #fo.write(str(index_line) + "," + is_retweet + "," + is_quote + "," + original_tweet_date + "," + original_tweet_time + "," + original_tweet_user_follower_count + "," + original_tweet_retweet_count + "," + original_tweet_id + "," + original_tweet_user_id + "," + retweet_tweet_date + "," + retweet_tweet_time + "," + retweet_tweet_id + "," + retweet_tweet_user_id + "," + original_tweet_epoch + "," + retweet_tweet_epoch + "\n")

        # Retweet Tweet
        elif is_retweet == "1" and is_quote == "0":

            # Original in retweeted_status
            original_tweet_retweeted_status_obj_index = line.find(",\"retweeted_status\":{\"")

            # Extract Original tweeet created_at from retweeted_status
            original_tweet_created_at_index = line.find("created_at", original_tweet_retweeted_status_obj_index + 21)
            original_tweet_datetime = str(to_datetime(line[original_tweet_created_at_index + 13:original_tweet_created_at_index + 43]))

            # Get Original dayofweek, date, and time from retweeted_status
            # dow = str(datetime.weekday())
            original_tweet_date = original_tweet_datetime.split(' ')[0]
            original_tweet_time = original_tweet_datetime.split(' ')[1]

            original_tweet_epoch = str(int(time.mktime(time.strptime(original_tweet_datetime, pattern))))

            # Extract original_tweet_id from retweeted_status
            original_tweet_id_index = line.find("id_str", original_tweet_retweeted_status_obj_index + 21)
            original_tweet_text_index = line.find("text", original_tweet_retweeted_status_obj_index + 21)
            original_tweet_id = str(line[original_tweet_id_index + 9:original_tweet_text_index - 3])

            # Original User in retweeted_status in user
            original_tweet_user_obj_index = line.find(",\"user\":{", original_tweet_retweeted_status_obj_index + 21)

            # Extract original_tweet_user_id in retweeted_status
            original_tweet_user_id_index = line.find("id_str", original_tweet_user_obj_index + 9)
            original_tweet_user_name_index = line.find("\",\"name\":", original_tweet_user_obj_index + 9)
            original_tweet_user_id = str(line[original_tweet_user_id_index + 9:original_tweet_user_name_index])


            # Extract original_tweet_user_follower_count in retweeted_status in user
            original_tweet_user_follower_count_index = line.find(",\"followers_count\":", original_tweet_user_obj_index + 9)
            original_tweet_user_friend_count_index = line.find(",\"friends_count\":", original_tweet_user_obj_index + 9)
            original_tweet_user_follower_count = str(line[original_tweet_user_follower_count_index + 19:original_tweet_user_friend_count_index])

            # Extract original_tweet_retweet_count from retweeted_status after user
            original_tweet_retweet_count_index = line.find(",\"retweet_count\":", original_tweet_user_friend_count_index + 17)  # use friend_count_index because want to start after text and username (injection)
            original_tweet_favorite_count_index = line.find(",\"favorite_count\":", original_tweet_user_friend_count_index + 17)  # use friend_count_index because want to start after text and username (injection)
            original_tweet_retweet_count = str(line[original_tweet_retweet_count_index + 17:original_tweet_favorite_count_index])

            # Extract Retweet tweeet created_at
            retweet_tweet_created_at_index = line.find("created_at")
            retweet_tweet_datetime = str(to_datetime(line[retweet_tweet_created_at_index + 13:retweet_tweet_created_at_index + 43]))

            # Get retweet dayofweek, date, and time
            # dow = str(datetime.weekday())
            retweet_tweet_date = retweet_tweet_datetime.split(' ')[0]
            retweet_tweet_time = retweet_tweet_datetime.split(' ')[1]

            retweet_tweet_epoch = str(int(time.mktime(time.strptime(retweet_tweet_datetime, pattern))))

            # Extract retweet_tweet_user_id
            retweet_tweet_id_index = line.find("id_str")
            retweet_tweet_text_index = line.find("text")
            retweet_tweet_id = str(line[retweet_tweet_id_index + 9:retweet_tweet_text_index - 3])

            # Extract original_tweet_user_id
            retweet_tweet_user_obj_index = line.find("\"user\":{")
            retweet_tweet_user_id_index = line.find("id_str", retweet_tweet_user_obj_index + 8)
            retweet_tweet_user_name_index = line.find("\",\"name\":", retweet_tweet_user_obj_index + 8)
            retweet_tweet_user_id = str(line[retweet_tweet_user_id_index + 9:retweet_tweet_user_name_index])

            fo.write(str(index_line) + "," + is_retweet + "," + is_quote + "," + original_tweet_date + "," + original_tweet_time + "," + original_tweet_user_follower_count + "," + original_tweet_retweet_count + "," + original_tweet_id + "," + original_tweet_user_id + "," + retweet_tweet_date + "," + retweet_tweet_time + "," + retweet_tweet_id + "," + retweet_tweet_user_id + "," + original_tweet_epoch + "," + retweet_tweet_epoch + "\n")

        # Original Quote
        elif is_retweet == "0" and is_quote == "1":
            original_tweet_date = "null"
            original_tweet_time = "null"
            original_tweet_user_follower_count = "null"
            original_tweet_retweet_count = "null"
            original_tweet_id = "null"
            original_tweet_user_id = "null"
            retweet_tweet_date = "null"
            retweet_tweet_time = "null"
            retweet_tweet_id = "null"
            retweet_tweet_user_id = "null"
            original_tweet_epoch = "null"
            retweet_tweet_epoch = "null"
            # fo.write(str(index_line) + "," + is_retweet + "," + is_quote + "," + original_tweet_date + "," + original_tweet_time + "," + original_tweet_user_follower_count + "," + original_tweet_retweet_count + "," + original_tweet_id + "," + original_tweet_user_id + "," + retweet_tweet_date + "," + retweet_tweet_time + "," + retweet_tweet_id + "," + retweet_tweet_user_id + "," + original_tweet_epoch + "," + retweet_tweet_epoch + "\n")

        # Retweet Quote
        elif is_retweet == "1" and is_quote == "1":
            original_tweet_date = "null"
            original_tweet_time = "null"
            original_tweet_user_follower_count = "null"
            original_tweet_retweet_count = "null"
            original_tweet_id = "null"
            original_tweet_user_id = "null"
            retweet_tweet_date = "null"
            retweet_tweet_time = "null"
            retweet_tweet_id = "null"
            retweet_tweet_user_id = "null"
            original_tweet_epoch = "null"
            retweet_tweet_epoch = "null"
            # fo.write(str(index_line) + "," + is_retweet + "," + is_quote + "," + original_tweet_date + "," + original_tweet_time + "," + original_tweet_user_follower_count + "," + original_tweet_retweet_count + "," + original_tweet_id + "," + original_tweet_user_id + "," + retweet_tweet_date + "," + retweet_tweet_time + "," + retweet_tweet_id + "," + retweet_tweet_user_id + "," + original_tweet_epoch + "," + retweet_tweet_epoch + "\n")

        """
        fo.write
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
        ------
        Want
            /1) tweet_id,                    (11)
            /2) tweet_created_time,          (9,10)
            /3) source_tweet_id,             (7)
            /4) source_tweet_created_time,   (3,4)
            /5) source_follower_count,       (5)
            /6) source_tweet_retweet_count   (6)
                                                    (not 1,2,8,12 (is_retweet, is_quote, original_tweet_user_id, retweet_tweet_user_id))
        """
        index_line += 1
    # Close file
    fo.close()
    return


"""
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start
"""


# Convert twitter datetime to usable format
def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1]) + timedelta(hours=7)


# ===================================== NEW Way ====================================================
# Path
# E:\tweet_process\real_json\hormonestheseries\week1\*.json
# C:\Senior\apple\week2
# C:\Senior\thefacethailand\week1
# E:\tweet_process\result_follower-ret\01preprocess\hormonestheseries\week1\*.csv
# E:\tweet_process\real_json\aroii\week2\*.json
# E:\tweet_process\result_follower-ret\01preprocess\aroii\week2

# SELECT TOPIC TO PROCESS (ctr + /)
# topic = "aroii"
# topic = "hormonestheseries"
topic = "apple"
# topic = "thefacethailand"
week_list_aroii_apple = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
# week_list_hormones_theface = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
for week in week_list_aroii_apple:
# for week in week_list_hormones_theface:

    file_path = "/"+topic+"/week"+week+"/"

    # source_path = "E:/tweet_process/real_json" + file_path + "*.json"
    source_path = "C:/Senior" + file_path + "*.json"
    print(source_path)

    files_list = glob.glob(source_path)
    # print(files_list)

    for one_file_path in files_list:
        # print(one_file_path)

        filename = basename(one_file_path)
        # print(filename)
        dot_index = filename.find(".")
        only_filename = filename[0:dot_index]
        # print(only_filename)

        # set file_name to output
        destination_path = "E:/tweet_process/result_follower-ret/01preprocess" + file_path + only_filename + ".csv"
        print(destination_path)

        # call extract method
        extract_json(one_file_path, destination_path)
print("Preprocess Success!!")
