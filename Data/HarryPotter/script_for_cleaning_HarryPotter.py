import os
IN_FOLDER_PATH = "./Data/HarryPotter/Raw"
OUT_FOLDER_PATH = "./Data/HarryPotter/Cleaned2"

counter = 0
paragraph = []
P = False
for filename in os.listdir(IN_FOLDER_PATH):
    if os.path.splitext(filename)[1] == '.txt':
        in_file = open(os.path.join(IN_FOLDER_PATH, filename))
        out_file = open(os.path.join(OUT_FOLDER_PATH, 'J K Rowling___'+filename), 'w')
        print("reading: ", os.path.join(IN_FOLDER_PATH, filename))
        for line in in_file.readlines():
            if "Page |" not in line and line != '\n':
                paragraph.append(line)
                P = False
                continue
            if "Page |" in line:
                while len(paragraph) > 0 and paragraph[-1] == '\n':
                    paragraph.pop()
                P = True
                continue
            if line == '\n' and not P:
                paragraph.append('\n')
                out_file.writelines(paragraph)
                paragraph = []


