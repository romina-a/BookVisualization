import csv

with open('./Data/metadata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    list_temp = []
    past = "author"
    for row in csv_reader:
        current = row[1]
        if past == current:
            past = current
        else:
            past_birth = list_temp[0][2]
            past_death = list_temp[0][3]
            for line in list_temp:
                current_birth = line[2]
                current_death = line[3]
                if current_birth != past_birth or current_death != past_death:
                    print(list_temp[0][1])
                past_birth = current_birth
                past_death = current_death
            past = current
            list_temp.clear()
        # print(f'{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}')
        list_temp.append([row[0], row[1], row[2], row[3], row[4], row[5]])
