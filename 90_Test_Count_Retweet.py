import glob

path_after_preprocess = glob.glob("D:/share_folder_vm/data/*.csv")  # All Hormones Data CSV\
i = 0

for file in path_after_preprocess:
    each_file = open(file, 'r')
    print(each_file)
    for line in each_file:
        i = i + 1
    print(i)
    each_file.close()
print(i)
