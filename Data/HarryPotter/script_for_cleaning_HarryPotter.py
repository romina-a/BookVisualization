import os
IN_FOLDER_PATH = "./Data/HarryPotter/Raw"
OUT_FOLDER_PATH = "./Data/HarryPotter/Cleaned"

counter = 0
for filename in os.listdir(IN_FOLDER_PATH):
    if os.path.splitext(filename)[1] == '.txt':
        in_file = open(os.path.join(IN_FOLDER_PATH, filename))
        out_file = open(os.path.join(OUT_FOLDER_PATH, 'J K Rowling___'+filename), 'w')
        print("reading: ", os.path.join(IN_FOLDER_PATH, filename))
        for line in in_file.readlines():
            if "Page |" not in line and line !='\n':
                out_file.writelines(line+'\n')

