import os
import urllib.request, urllib.error, urllib.parse
import csv


def meta_data(address):
    author_name_txt = address.split("/")[-1]
    if author_name_txt[-3:] != "txt":
        return None
    author = author_name_txt.split("___")[0]
    name_txt = author_name_txt.split("___")[1]
    name = name_txt.replace(".txt", "")
    entries = os.listdir('./Data/Gutindex/')
    for entry in entries:
        f = open('./Data/Gutindex/' + entry, "r")
        text = f.read()
        char_end = 0
        while text.find(name, char_end) != -1:
            # reading whole line with the book name in it
            char_start = text.find(name, char_end)
            char_end = text.find("\n", char_start)
            index_list = [int(s) for s in text[char_start:char_end].split() if s.isdigit()]
            # print(entry, index_list, text[char_start:char_end])
            # checking if index number is available and author name is same
            if index_list != [] and len(set(author.split()).intersection(set(text[char_start:char_end].split()))) != 0:
                url = "http://gutendex.com/books/" + str(index_list[-1]) + "/"
                response = urllib.request.urlopen(url)
                webContent = response.read()

                # author check/ some books are translations of other books
                if str(webContent).find("name") != -1:

                    # subject
                    subject_start_char = str(webContent).find("subjects")
                    subject_end_char = str(webContent).find('],"bookshelves"')
                    subjects = str(webContent)[subject_start_char + 11:subject_end_char]
                    subjects_list = subjects.split('"')
                    while '' in subjects_list:
                        subjects_list.remove('')
                    while ',' in subjects_list:
                        subjects_list.remove(',')

                    # year
                    year_birth_char = str(webContent).find('birth_year')
                    year_death_char = str(webContent).find('death_year')
                    year_birth_str = str(webContent)[year_birth_char + 12:year_birth_char + 16]
                    year_death_str = str(webContent)[year_death_char + 12:year_death_char + 16]
                    if year_birth_str != "null":
                        year_birth = int(year_birth_str)
                    else:
                        year_birth = 0
                    if year_death_str != "null":
                        year_death = int(year_death_str)
                    else:
                        year_death = 0

                    # popularity
                    popularity_start_char = str(webContent).find('download_count')
                    popularity_end_char = str(webContent).find('}', popularity_start_char)
                    popularity_str = str(webContent)[popularity_start_char + 16:popularity_end_char]
                    popularity = int(popularity_str)

                    return name, author, year_birth, year_death, popularity, subjects_list

        f.close()

    for entry in entries:
        f = open('./Data/Gutindex/' + entry, "r")
        # reading whole line with the book name in it
        for line in f.readlines():
            if len(set(author.split()).intersection(set(line.split()))) != 0 and len(
                    set(name.split()).intersection(set(line.split()))) >= 2:
                index_list = [int(s) for s in line.split() if s.isdigit()]
                # print(entry, index_list, line)
                # checking if index number is available and author name is same
                if index_list != []:
                    url = "http://gutendex.com/books/" + str(index_list[-1]) + "/"
                    response = urllib.request.urlopen(url)
                    webContent = response.read()

                    # author check/ some books are translations of other books
                    if str(webContent).find("name") != -1:

                        # subject
                        subject_start_char = str(webContent).find("subjects")
                        subject_end_char = str(webContent).find('],"bookshelves"')
                        subjects = str(webContent)[subject_start_char + 11:subject_end_char]
                        subjects_list = subjects.split('"')
                        while '' in subjects_list:
                            subjects_list.remove('')
                        while ',' in subjects_list:
                            subjects_list.remove(',')

                        # year
                        year_birth_char = str(webContent).find('birth_year')
                        year_death_char = str(webContent).find('death_year')
                        year_birth_str = str(webContent)[year_birth_char + 12:year_birth_char + 16]
                        year_death_str = str(webContent)[year_death_char + 12:year_death_char + 16]
                        if year_birth_str != "null":
                            year_birth = int(year_birth_str)
                        else:
                            year_birth = 0
                        if year_death_str != "null":
                            year_death = int(year_death_str)
                        else:
                            year_death = 0

                        # popularity
                        popularity_start_char = str(webContent).find('download_count')
                        popularity_end_char = str(webContent).find('}', popularity_start_char)
                        popularity_str = str(webContent)[popularity_start_char + 16:popularity_end_char]
                        popularity = int(popularity_str)

                        return name, author, year_birth, year_death, popularity, subjects_list

        f.close()

    return None


if __name__ == '__main__':
    with open('./Data/metadata.csv', mode='w') as csv_file:
        fieldnames = ["name", "author", "year_birth", "year_death", "popularity", "subjects_list"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        addresses = os.listdir("./Data/Gutenberg/txt/")
        for address in addresses:
            book_address = "./Data/Gutenberg/txt/" + address
            if meta_data(book_address) is None:
                print(book_address)
            else:
                name, author, year_birth, year_death, popularity, subjects_list = meta_data(book_address)
                writer.writerow({'name': name, 'author': author, 'year_birth': year_birth, 'year_death': year_death, 'popularity': popularity, 'subjects_list': subjects_list})
